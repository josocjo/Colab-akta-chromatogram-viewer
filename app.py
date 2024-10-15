import streamlit as st
import proteovis as pv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd  # Import pandas for DataFrame manipulation
import tempfile
import os


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


if uploaded_zip:
     
      if "data" not in st.session_state:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_zip.read())
            zip_path = tmp_zip.name
            st.session_state.data = pv.pycorn.load_uni_zip(zip_path)

      if "df" not in st.session_state:
        st.session_state.df = pv.pycorn.utils.get_series_from_data(st.session_state.data, ["UV 1_280", "UV 2_254", "Cond", "pH", "Conc B", "Run Log", 'Fractions'])

      fig = pv.graph.unicorn_ploty_graph(st.session_state.df)
      st.plotly_chart(fig)
      

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

      show_fig2_bottun = st.button("Show/Hide fig2")  # Button to toggle


      if show_fig2_bottun:
        palette = sns.color_palette("rainbow", len(st.session_state.frac_df))
        fig2, st.session_state.use_color_palette = pv.graph.annotate_fraction(fig, st.session_state.frac_df, palette=palette, annotations=selected_fractions)
        st.plotly_chart(fig2)




######################################
#CBB

if uploaded_image:
     
      if "image" not in st.session_state:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
            tmp_zip.write(uploaded_image.read())
            zip_path = tmp_zip.name
            st.session_state.page = pv.pypage.PageImage(zip_path)
      
      fig3 = st.session_state.page.check_image()
      st.plotly_chart(fig3)

      if "annotate_page" not in st.session_state:
        st.session_state.annotate_page = st.text_input(
          "Enter a name for the pooled fraction:",
          default=",".join(selected_fractions))

      annotate_bottun = st.button("annotate image")  # Button to toggle
      if annotate_bottun:
        st.session_state.page.annotate_lanes(cbb_list)
        fig4 = st.session_state.page.annotated_imshow(st.session_state.use_color_palette,rectangle=True)  
        st.plotly_chart(fig4)

      



      
