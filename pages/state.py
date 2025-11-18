"""
State-specific report page for SSBG dashboard
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback, dash_table
from urllib.parse import unquote
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import (
    load_data,
    get_state_totals,
    get_state_time_series,
    get_state_service_breakdown,
    get_state_full_data,
    get_unique_values,
)
from components.graphs import (
    create_pie_chart,
    create_time_series_line_chart,
    create_bar_chart,
)

# Load data once
df = load_data()
unique_vals = get_unique_values(df)
min_year = min(unique_vals["years"])
max_year = max(unique_vals["years"])


def layout(state_name="Alabama"):
    """Create the state page layout"""
    return dbc.Container(
        [
            # Header with back button
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Button(
                            "← Back to National Overview",
                            href="/",
                            color="secondary",
                            className="mb-3",
                        ),
                        html.H1(id="state-page-title", className="mb-4 fw-bold"),
                    ],
                    width=12,
                )
            ),
            # Filters
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Year", className="form-label fw-bold"),
                                    dcc.Dropdown(
                                        id="state-year-dropdown",
                                        options=[
                                            {"label": str(year), "value": year}
                                            for year in range(min_year, max_year + 1)
                                        ],
                                        value=max_year,
                                        placeholder="Select year...",
                                        className="mb-2",
                                    ),
                                ]
                            ),
                            className="shadow-sm",
                        ),
                        width=12,
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label(
                                        "Service Categories",
                                        className="form-label fw-bold",
                                    ),
                                    dcc.Dropdown(
                                        id="state-service-category-dropdown",
                                        options=[
                                            {"label": cat, "value": cat}
                                            for cat in unique_vals["service_categories"]
                                        ],
                                        value=[],  # All selected by default
                                        multi=True,
                                        placeholder="All service categories selected by default...",
                                        className="mb-2",
                                    ),
                                ]
                            ),
                            className="shadow-sm",
                        ),
                        width=12,
                        md=6,
                        className="mb-3",
                    ),
                ],
                className="mb-4",
            ),
            # Summary Cards
            dbc.Row(
                [
                    dbc.Col(
                        id="state-total-expenditures-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="state-total-recipients-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="state-service-categories-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="state-avg-expenditure-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                ],
                className="mb-4",
            ),
            # Service Category Breakdown
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="state-service-bar"),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(id="state-service-recipient-pie"),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                ]
            ),
            # Time Series Graphs
            # TODO: add line for national average
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="state-expenditures-time-series"),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(id="state-recipients-time-series"),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                ]
            ),
            # Data Table
            dbc.Row(
                dbc.Col(
                    [
                        html.H3("Full Data Table", className="mb-3"),
                        html.Div(id="state-data-table"),
                    ],
                    width=12,
                    className="mb-4",
                )
            ),
            # Data Export
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Export Data", className="card-title"),
                                html.P("Download the filtered data as CSV"),
                                dbc.Button(
                                    "Download CSV",
                                    id="state-download-btn",
                                    color="primary",
                                    className="mt-2",
                                ),
                                dcc.Download(id="state-download-csv"),
                            ]
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    md=6,
                    className="mb-4",
                )
            ),
        ],
        fluid=True,
        className="py-4",
        id="state-page-container",
    )


# Store state name in dcc.Store
# Callbacks
@callback(
    [
        Output("state-total-expenditures-card", "children"),
        Output("state-total-recipients-card", "children"),
        Output("state-service-categories-card", "children"),
        Output("state-avg-expenditure-card", "children"),
    ],
    [
        Input("state-year-dropdown", "value"),
        Input("state-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_summary_cards(year, service_categories, pathname):
    """Update state summary cards"""
    if pathname and pathname.startswith("/state/"):
        from urllib.parse import unquote

        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"  # Default

    totals = get_state_totals(df, state_name, year, service_categories)
    all_time_totals = get_state_totals(df, state_name, None, None)

    # Calculate average expenditure per recipient
    avg_expenditure = (
        totals["expenditures"] / totals["recipients"] if totals["recipients"] > 0 else 0
    )

    # Get number of service categories
    filtered_df = df[df["state_name"] == state_name].copy()
    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]
    num_categories = len(filtered_df["service_category"].unique())

    expenditures_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Expenditures", className="card-title"),
                html.H2(f"${totals['expenditures']:,.0f}", className="fw-bold"),
                html.P(
                    f"All-time: ${all_time_totals['expenditures']:,.0f}",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    recipients_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total Recipients", className="card-title"),
                html.H2(f"{totals['recipients']:,.0f}", className="fw-bold"),
                html.P(
                    f"All-time: {all_time_totals['recipients']:,.0f}",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    categories_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Service Categories", className="card-title"),
                html.H2(f"{num_categories}", className="fw-bold"),
                html.P("Active categories", className="text-muted mb-0"),
            ]
        ),
        className="shadow-sm h-100",
    )

    avg_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Avg per Recipient", className="card-title"),
                html.H2(f"${avg_expenditure:,.0f}", className="fw-bold"),
                html.P("Expenditure per recipient", className="text-muted mb-0"),
            ]
        ),
        className="shadow-sm h-100",
    )

    return expenditures_card, recipients_card, categories_card, avg_card


@callback(
    Output("state-page-title", "children"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)
def update_state_title(pathname):
    """Update state page title"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
        return f"SSBG Report: {state_name}"
    return "SSBG Report: Alabama"


@callback(
    Output("state-service-bar", "children"),
    [Input("state-year-dropdown", "value"), Input("url", "pathname")],
)
def update_state_service_bar(year, pathname):
    """Update service category bar chart"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    breakdown = get_state_service_breakdown(df, state_name, year)

    return create_bar_chart(
        breakdown,
        x_col="expenditures",
        y_col="service_category",
        orientation="h",
        title=(
            f"Service Categories by Expenditures ({year}) - {state_name}"
            if year
            else f"Service Categories by Expenditures - {state_name}"
        ),
    )


@callback(
    Output("state-service-recipient-pie", "children"),
    [Input("state-year-dropdown", "value"), Input("url", "pathname")],
)
def update_state_service_recipient_pie(year, pathname):
    """Update service category pie chart"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    # service category breakdown by recipients
    breakdown = get_state_service_breakdown(df, state_name, year)

    fig = px.pie(
        breakdown,
        names="service_category",
        values="recipients",
        title=(
            f"Service Category Breakdown by Recipients ({year}) - {state_name}"
            if year
            else f"Service Category Breakdown by Recipients - {state_name}"
        ),
    )
    fig.update_layout(template="plotly_white", height=400)
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Recipients: %{value:,}<br>Percent: %{percent}"
    )

    return create_pie_chart(
        breakdown,
        names_col="service_category",
        values_col="recipients",
        title=(
            f"Service Category Breakdown by Recipients ({year}) - {state_name}"
            if year
            else f"Service Category Breakdown by Recipients - {state_name}"
        ),
        hovertemplate="<b>%{label}</b><br>Recipients: %{value:,}<br>Percent: %{percent}",
    )


# TODO Make sure line graphs start at zero for y-axis
# TODO Examine all card subtitles for clarity, consistency, accuracy
# TODO Consider new cards or graphs to add or swap


@callback(
    Output("state-expenditures-time-series", "children"),
    [
        Input("state-year-dropdown", "value"),
        Input("state-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_expenditures_time_series(year, service_categories, pathname):
    """Update state expenditures time series graph"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    ts_data = get_state_time_series(df, state_name, "expenditures", service_categories)

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title=f"SSBG Expenditures Over Time - {state_name}",
        labels={"year": "Year", "value": "Expenditures ($)"},
    )
    fig.update_layout(template="plotly_white", hovermode="x unified", height=400)

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("state-recipients-time-series", "children"),
    [
        Input("state-year-dropdown", "value"),
        Input("state-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_recipients_time_series(year, service_categories, pathname):
    """Update state recipients time series graph"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    ts_data = get_state_time_series(df, state_name, "recipients", service_categories)

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title=f"SSBG Recipients Over Time - {state_name}",
        labels={"year": "Year", "value": "Recipients"},
    )
    fig.update_layout(template="plotly_white", hovermode="x unified", height=400)

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("state-data-table", "children"),
    [
        Input("state-year-dropdown", "value"),
        Input("state-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_data_table(year, service_categories, pathname):
    """Update state data table"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    table_data = get_state_full_data(df, state_name, year, service_categories)

    # Format the table
    table = dash_table.DataTable(
        data=table_data.to_dict("records"),
        columns=[
            {
                "name": col,
                "id": col,
                "type": "numeric" if table_data[col].dtype == "int64" else "text",
            }
            for col in table_data.columns
        ],
        page_size=30,
        sort_action="native",
        style_cell={
            "textAlign": "left",
            "padding": "10px",
            "fontFamily": "Arial, sans-serif",
        },
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_data={"whiteSpace": "normal", "height": "auto"},
        style_table={"overflowX": "auto"},
    )

    return table


@callback(
    Output("state-download-csv", "data"),
    Input("state-download-btn", "n_clicks"),
    [
        State("state-year-dropdown", "value"),
        State("state-service-category-dropdown", "value"),
        State("url", "pathname"),
    ],
    prevent_initial_call=True,
)
def download_state_csv(n_clicks, year, service_categories, pathname):
    """Download filtered state data as CSV"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    table_data = get_state_full_data(df, state_name, year, service_categories)
    # TODO add year to filename and in national download also
    filename = f"ssbg_{state_name.replace(' ', '_')}_data.csv"

    return dcc.send_data_frame(table_data.to_csv, filename, index=False)
