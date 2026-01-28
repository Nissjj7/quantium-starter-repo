import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("pink_morsel_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Create line chart
fig = px.line(
    df,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    markers=True
)

fig.update_traces(line=dict(width=3))

# Price increase marker
fig.add_shape(
    type="line",
    x0="2021-01-15",
    x1="2021-01-15",
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="red", dash="dash")
)

fig.add_annotation(
    x="2021-01-15",
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase<br>15 Jan 2021",
    showarrow=False,
    yanchor="bottom",
    font=dict(color="red")
)

fig.update_layout(
    template="plotly_white",
    yaxis_title="Total Sales ($)",
    xaxis_title="Date",
    yaxis_tickprefix="$"
)

# Dash app
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center"}
        ),
        html.P(
            "This chart shows total daily sales of Pink Morsels across all regions. "
            "The red dashed line marks the price increase on January 15, 2021.",
            style={"textAlign": "center"}
        ),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
