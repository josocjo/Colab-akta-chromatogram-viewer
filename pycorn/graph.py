import plotly.graph_objects as go


def ploty_graph(df,html=True,name="",show=True):
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
          domain=[0.05, 0.85]
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
      template="plotly_white")

  # Update layout properties
  fig.update_layout(
      title_text="Chromatogram",
      width=1200,
      height=600
  )

  if html:
    fig.write_html(f"{name}_chromatogram.html")
  
  if show:
    fig.show()