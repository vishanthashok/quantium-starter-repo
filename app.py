from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_FILE = Path(__file__).parent / "data" / "pink_morsel_sales.csv"
PRICE_INCREASE_DATE = "2021-01-15"

df = pd.read_csv(DATA_FILE)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "24px"},
    children=[
        html.H1("Soul Foods Pink Morsel Sales Visualiser"),
        html.P(
            "Daily Pink Morsel sales revenue across regions. "
            f"The price increased on {PRICE_INCREASE_DATE}."
        ),
        html.Label("Region"),
        dcc.Dropdown(
            id="region-filter",
            options=[{"label": "All regions", "value": "all"}]
            + [{"label": region.title(), "value": region} for region in sorted(df["Region"].unique())],
            value="all",
            clearable=False,
            style={"width": "240px", "marginBottom": "24px"},
        ),
        dcc.Graph(id="sales-chart"),
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

    figure = px.line(
        chart_data,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
        markers=True,
    )
    figure.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode="x unified",
    )
    return figure


if __name__ == "__main__":
    app.run(debug=True)
