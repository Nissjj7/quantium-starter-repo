import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv("pink_morsel_sales.csv")

# Clean + convert types
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].str.lower()
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f7f7f7",
        "padding": "30px"
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            id="header",
            style={
                "textAlign": "center",
                "color": "#e75480",
                "marginBottom": "10px"
            }
        ),

        html.P(
            "Explore how Pink Morsel sales changed over time and across regions. "
            "The price increase on January 15, 2021 is marked on the chart.",
            style={
                "textAlign": "center",
                "fontSize": "16px",
                "color": "#555"
            }
        ),

        html.Div(
            style={
                "width": "60%",
                "margin": "20px auto",
                "padding": "15px",
                "backgroundColor": "white",
                "borderRadius": "8px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
            },
            children=[
                html.Label(
                    "Select Region:",
                    style={"fontWeight": "bold"}
                ),

                dcc.RadioItems(
                    id="region-picker",   # ✅ REQUIRED BY TESTS
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"marginTop": "10px"}
                ),
            ],
        ),

        dcc.Graph(
            id="sales-graph"   # ✅ REQUIRED BY TESTS
        )
    ]
)

# Callback to update chart
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-picker", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
        title_suffix = "All Regions"
    else:
        filtered_df = df[df["Region"] == selected_region]
        title_suffix = selected_region.capitalize()

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title=f"Pink Morsel Sales Over Time — {title_suffix}",
        labels={
            "Date": "Date",
            "Sales": "Total Sales ($)"
        }
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
        yaxis_tickprefix="$",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


# Run server
if __name__ == "__main__":
    app.run(debug=True)
