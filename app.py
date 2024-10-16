import streamlit as st
from streamlit_searchbox import st_searchbox
import proteovis as pv

import seaborn as sns
import pandas as pd  # Import pandas for DataFrame manipulation
import tempfile
import os

def get_next_state(flag,flgButton):

  if flag not in st.session_state:
      st.session_state[flag] = False


  # ボタンが押された場合、セッションデータを更新
  if flgButton == True and st.session_state[flag] == False:
      st.session_state[flag] = True
  elif flgButton == True and st.session_state[flag] == True:
      st.session_state[flag] = True


st.set_page_config(page_title="ProteoVis", layout="wide")

st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=select] span{
            max-width: 600px;
            font-size: 1rem;
            background-color: #4a9687 !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Proteovis Visualization App")

# File uploaders with unique keys
uploaded_zip = st.file_uploader("Upload Unicorn .zip file", type="zip", key="zip_uploader")
uploaded_image = st.file_uploader("Upload CBB image", type=["jpg", "png"], key="image_uploader")

if "use_color_palette" not in st.session_state:
  st.session_state.use_color_palette = None


if uploaded_zip:
     
      if "data" not in st.session_state:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_zip.read())
            zip_path = tmp_zip.name
            st.session_state.data = pv.pycorn.load_uni_zip(zip_path)

      if "df" not in st.session_state:
        st.session_state.df = pv.pycorn.utils.get_series_from_data(st.session_state.data, ["UV 1_280", "UV 2_254", "Cond", "pH", "Conc B", "Run Log", 'Fractions'])

      fig = pv.graph.unicorn_ploty_graph(st.session_state.df)
      st.plotly_chart(fig,key="chromatogram",theme=None)
      

      if "frac_df" not in st.session_state:
        st.session_state.frac_df = pv.pycorn.utils.get_fraction_rectangle(st.session_state.df)

      pool_fractions = st.multiselect(
          "Select fractions to pool:",
          st.session_state.frac_df["Fraction_Start"].values,
          key="pool_frac"
      )
          

      pool_name = st.text_input("Enter a name for the pooled fraction:")

      pooling_bottun = st.button("pooling")

      if pooling_bottun and pool_name and pool_fractions:
        st.session_state.frac_df = pv.pycorn.utils.pooling_fraction(st.session_state.frac_df,pool_fractions, name=pool_name)
      

      st.write("Initial frac_df:")  # Debug print
      st.write(st.session_state.frac_df)

      

      selected_fractions = st.multiselect(
          "Visualize Select fractions:",
          st.session_state.frac_df["Fraction_Start"].values,
          key="vis_frac"
      )

      show_fig2_button = st.button("Show fraction")  # Button to toggle
      get_next_state("fraction_finish",show_fig2_button)

      if not st.session_state["fraction_finish"]:
        get_next_state("fraction_finish",get_next_state)
        st.stop()


      palette = sns.color_palette("rainbow", len(st.session_state.frac_df))
      fig2, st.session_state.use_color_palette = pv.graph.annotate_fraction(fig, st.session_state.frac_df, palette=palette, annotations=selected_fractions)
      st.plotly_chart(fig2,key="frac_chromatogram",theme=None)




######################################
#CBB

def fractions_search(searchterm: str):
  search_list = ["marker","input"]
  if "frac_df" not in st.session_state:
    pass
  else:
    search_list += st.session_state.frac_df["Fraction_Start"].values.tolist()
  
  return [s for s in search_list if searchterm in s]


if uploaded_image:
     
      if "image" not in st.session_state:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_image.read())
            zip_path = tmp_zip.name
            st.session_state.page = pv.pypage.PageImage(zip_path,lane_width=44)


      with st.form("annotate_page"):
        annotate_col1,annotate_col2 = st.columns(2)

        with annotate_col1: 
          fig3 = st.session_state.page.check_image()
          st.plotly_chart(fig3,key="check_image")
        
        with annotate_col2:
          st.session_state.label = {i:"" for i in range(len(st.session_state.page.lanes))}
          for i,lane in  enumerate(st.session_state.page.lanes):
            #st.session_state.label[i] = st_searchbox(fractions_search,edit_after_submit="option",placeholder=st.session_state.label[i],key=f"lane{i}")
            st.session_state.label[i] = st.text_input(f"lane {i} annotate",placeholder=st.session_state.label[i],key=f"lane{i}")

        annotate_button = st.form_submit_button("annotate image")  # Button to toggle
      
      get_next_state("annotate_page_finish",annotate_button)
      


        
      st.session_state.page.annotate_lanes(list(st.session_state.label.values()))
      fig4 = st.session_state.page.annotated_imshow(st.session_state.use_color_palette,rectangle=True)  
      st.plotly_chart(fig4,key="annotate_image")
      
    
      labels = [v for km,v in st.session_state.label.items() if v != ""]
      marker_lane = st.selectbox(label="Marker lane is ",options=labels)
        
    
      with st.form("annotate_marker"):
          marker_col1,marker_col2 = st.columns(2)
          with marker_col1:
            marker_image = st.session_state.page.get_lane(name=marker_lane,start=0)        
            st.session_state.marker = pv.pypage.Marker(marker_image)
            fig5 = st.session_state.marker.check()
            st.plotly_chart(fig5,key="check_marker")
          
          with marker_col1:
            st.session_state.marker_label = {i:"" for i in range(len(st.session_state.marker.peak_index))}
            for i,peak in  enumerate(st.session_state.marker.peak_index):
              st.session_state.marker_label[i] = st.text_input("Enter a name for number peak",placeholder=st.session_state.marker_label[i],key=f"peak{i}")

          annotate_marker_button = st.form_submit_button("annotate marker")  # Button to toggle
      
      get_next_state("annotate_marker_finish",annotate_marker_button)
      if not st.session_state["annotate_marker_finish"]:
        get_next_state("annotate_marker_finish",get_next_state)
        st.stop()


      st.session_state.marker.annotate(st.session_state.marker_label.values())
      fig6 = pv.pypage.write_marker(fig4,st.session_state.marker)
      st.plotly_chart(fig6,key="marker_image")


      



      
