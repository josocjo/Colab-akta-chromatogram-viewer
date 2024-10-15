import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
from copy import copy
from pypage import pypage


def unicorn_ploty_graph(df):
  uv_color = "#1f77b4"
  ph_color = "#2ca772"
  cond_color = "#f29d5f"
  concb_color = "#b5b5b5"

  fig = go.Figure()

  fig.add_trace(go.Scatter(
      x=df["mL"],
      y=df["UV 1_280"],
      yaxis="y",
      line=dict(
              color=uv_color
          ),
      fill = "tozeroy",
      name="UV 280nm (mAU)"
  ))

  fig.add_trace(go.Scatter(
      x=df["mL"],
      y=df["Cond"],
      yaxis="y2",
      line=dict(
              color=cond_color
          ),
      name="Conductivity (mS/cm)",
  ))

  fig.add_trace(go.Scatter(
      x=df["mL"],
      y=df["pH"],
      yaxis="y3",
      line=dict(
              color=ph_color
          ),
      name="pH"
  ))

  fig.add_trace(go.Scatter(
      x=df["mL"],
      y=df["Conc B"],
      yaxis="y4",
      name="B Concentration (%)",
      line=dict(
              color=concb_color
          ),
  ))



  # Create axis objects
  fig.update_layout(
      xaxis=dict(
          domain=[0.05, 0.85],
          title="mL",
      ),
      yaxis=dict(
          title="UV 280nm (mAU)",
          titlefont=dict(
              color=uv_color
          ),
          tickfont=dict(
              color=uv_color
          )
      ),
      yaxis2=dict(
          title="Cond (mS/cm)",
          titlefont=dict(
              color=cond_color
          ),
          tickfont=dict(
              color=cond_color
          ),
          anchor="x",
          side="right",
          overlaying="y"),

      yaxis3=dict(
          title="pH",
          titlefont=dict(
              color=ph_color
          ),
          tickfont=dict(
              color=ph_color
          ),
          anchor="free",
          side="right",
          range=(2,12),
          overlaying="y", autoshift=True),
      
      yaxis4=dict(
          title="B Concentration (%)",
          titlefont=dict(
              color=concb_color,
          ),
          tickfont=dict(
              color=concb_color
          ),
          anchor="free",
          side="right",
          overlaying="y", autoshift=True),

  )
  fig.update_layout(
      template="plotly_white",
      plot_bgcolor='rgba(0,0,0,0)',
      font=dict(
        size=24,
      ),
      title=dict(text='Chromatogram',
                 font=dict(size=24),
                  x=0.2,
                  xanchor='center'
                ),
      width=1280,
      height=720,
      legend=dict(
          yanchor="bottom",
          y=1,
          xanchor="right",
          x=0.8,
          font=dict(size=12),
      ))
  
  return fig



def annotate_fraction(fig,frac_df,rectangle=True,text=True,palette=None,annotations=None):

  fig =copy(fig)
  
  if not palette:
    palette = sns.color_palette("Blues", len(frac_df))
  
  use_color_palette = {}

  for i,(index, row) in enumerate(frac_df.iterrows()):
    if annotations:
      if not row["Fraction_Start"] in annotations:
        continue

    color = f"rgb({int(palette[i][0]*255)},{int(palette[i][1]*255)},{int(palette[i][2]*255)})"
    use_color_palette[row["Fraction_Start"]] = palette[i]

    if rectangle:
      
      fig.add_shape(type="rect",
                    x0=row["Start_mL"], y0=0, x1=row["End_mL"], y1=row["Max_UV"],
                    line=dict(color=color,width=2),
                    )

    if text:
      fig.add_annotation(
                        go.layout.Annotation(x=(row["Start_mL"]+row["End_mL"])/2,
                        y=0,
                        xref="x",
                        yref="y",
                        text=row["Fraction_Start"],
                        align='center',
                        showarrow=False,
                        yanchor='top',
                        textangle=90,
                        font=dict(
                        size=14
                        ),
                        bgcolor=color,

                        opacity=0.8))
      fig.update_shapes(dict(xref='x', yref='y'))
  return fig,use_color_palette



def annotate_page(image, lanes, lane_width=30,rectangle=True,text=True,palette_dict=None,annotations=None):

  fig = px.imshow(image)
  height, width = image.shape[:2]
  fig.update_layout(
      template="plotly_white",
      title=dict(text='CBB stain',
                 font=dict(size=24),
                  x=0.5,
                  y=0.95,
                  xanchor='center',
                  #yanchor="bottom"
                ),
      width=width,
      height=height
  )  

  fig.update_layout(
    # プロットの背景を透明に
    plot_bgcolor='rgba(0,0,0,0)',
    # 図全体の背景を透明に（必要に応じて）
    paper_bgcolor='rgba(0,0,0,0)',
    # x軸の線を消す
    xaxis=dict(
        showline=False,
        showgrid=False,
        zeroline=False,
    ),
    # y軸の線を消す
    yaxis=dict(
        showline=False,
        showgrid=False,
        zeroline=False,
    )
  )
  if not palette_dict:
      palette = sns.color_palette("Set1", len(lanes))
      annotations = list(range(len(lanes)))
      palette_dict = {a:p for a,p in zip(annotations,palette)}

  if not annotations:
      annotations = list(range(len(lanes)))

  i=0
  for label,lane in zip(annotations,lanes):
    if not label in palette_dict.keys():
        continue

    color = f"rgb({int(palette_dict[label][0]*255)},{int(palette_dict[label][1]*255)},{int(palette_dict[label][2]*255)})"

    if rectangle:
      lane_coord = pypage.get_lane(image,lane,lane_width=50)
      
      fig.add_shape(type="rect",
                    x0=lane_coord.x0, y0=lane_coord.y0, x1=lane_coord.x1, y1=lane_coord.y1,
                    line=dict(color=color,width=2),
                    )

    if text:
      fig.add_annotation(
                        go.layout.Annotation(
                            x=lane, y=100,
                            xref="x",
                            yref="y",
                            text=f"{label}",
                            align='center',
                            showarrow=False,
                            yanchor='bottom',
                            textangle=90,
                            font=dict(
                            size=18,
                            ),
                            bgcolor=color,
                            opacity=0.8))
  fig.update_shapes(dict(xref='x', yref='y'))
  fig.update_layout(coloraxis_showscale=False)
  fig.update_xaxes(showticklabels=False)
  fig.update_yaxes(showticklabels=False)

  return fig