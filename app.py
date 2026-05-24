from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_FILE = Path(__file__).parent / "data" / "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = "2021-01-15"
REGION_OPTIONS = [
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
    {"label": "All", "value": "all"},
]

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="hero",
            children=[
                html.Div("Soul Foods Analytics", className="hero-badge"),
                html.H1("Pink Morsel Sales Visualiser"),
                html.P(
                    "Explore daily Pink Morsel revenue by region. "
                    f"Look for the step change around {PRICE_INCREASE_DATE}, "
                    "when the price increased from $3.00 to $5.00."
                ),
            ],
        ),
        html.Div(
            className="panel",
            children=[
                html.P("Filter by region", className="panel-title"),
                dcc.RadioItems(
                    id="region-filter",
                    options=REGION_OPTIONS,
                    value="all",
                    inline=True,
                    className="region-radio",
                    inputStyle={"marginRight": "6px"},
                    labelStyle={"marginRight": "0"},
                ),
            ],
        ),
        html.Div(
            className="panel chart-panel",
            children=[dcc.Graph(id="sales-chart")],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    filtered = df if selected_region == "all" else df[df["Region"] == selected_region]
    chart_data = (
        filtered.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    region_label = selected_region.title() if selected_region != "all" else "All Regions"
    figure = px.line(
        chart_data,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales — {region_label}",
        markers=True,
        color_discrete_sequence=["#e84a8a"],
    )
    figure.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans, sans-serif", "color": "#2b1f24"},
        title={"font": {"size": 20, "color": "#2b1f24"}},
        margin={"l": 40, "r": 24, "t": 56, "b": 40},
    )
    figure.update_xaxes(showgrid=True, gridcolor="rgba(232, 74, 138, 0.12)")
    figure.update_yaxes(showgrid=True, gridcolor="rgba(232, 74, 138, 0.12)")
    return figure


if __name__ == "__main__":
    app.run(debug=True)
