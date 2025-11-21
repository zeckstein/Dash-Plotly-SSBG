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
                                    html.Label("State", className="form-label fw-bold"),
                                    dcc.Dropdown(
                                        id="state-selector-dropdown",
                                        options=[
                                            {"label": state, "value": state}
                                            for state in unique_vals["states"]
                                        ],
                                        value=state_name,
                                        placeholder="Select a state...",
                                        className="mb-2",
                                        clearable=False,
                                    ),
                                ]
                            ),
                            className="shadow-sm",
                        ),
                        width=3,
                        className="mb-3",
                    ),
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
                                        clearable=False,
                                    ),
                                ]
                            ),
                            className="shadow-sm",
                        ),
                        width=3,
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
                        id="state-total-ssbg-expenditures-card",
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
            # Service Category Breakdown (cards for consistent styling)
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Expenditures by Service Category",
                                        className="card-title mb-3",
                                    ),
                                    html.Div(id="state-service-bar"),
                                ]
                            ),
                            className="shadow-sm h-100",
                        ),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Recipients by Service Category",
                                        className="card-title mb-3",
                                    ),
                                    html.Div(id="state-service-recipient-pie"),
                                ]
                            ),
                            className="shadow-sm h-100",
                        ),
                        width=12,
                        md=6,
                        className="mb-4",
                    ),
                ]
            ),
            dbc.Row(html.H2("Trends Over Time", className="mb-4 fw-bold")),
            # Time range slider (carded and aligned with other controls)
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label(
                                        "Fiscal Year Range",
                                        className="form-label fw-bold mb-2",
                                    ),
                                    dcc.RangeSlider(
                                        id="state-time-series-range-slider",
                                        min=min_year,
                                        max=max_year,
                                        value=[min_year, max_year],
                                        marks={
                                            year: str(year)
                                            for year in range(min_year, max_year + 1)
                                        },
                                        step=1,
                                    ),
                                    html.Small(
                                        "Adjust the range to filter the time series charts.",
                                        className="text-muted d-block mt-2",
                                    ),
                                ]
                            ),
                            className="shadow-sm",
                        ),
                        width=6,
                        className="mb-4",
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
                                        id="state-time-series-service-category-dropdown",
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
                    ),
                ]
            ),
            # Time Series Graphs
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
            # Data Export
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Export Data", className="card-title"),
                                html.P("Download the full data FY10-FY22 as a CSV"),
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
                    width=4,
                    className="mb-4",
                )
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
        ],
        fluid=True,
        className="py-4",
        id="state-page-container",
    )


# Store state name in dcc.Store
# Callbacks
@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("state-selector-dropdown", "value"),
    prevent_initial_call=True,
)
def update_url_from_state_dropdown(selected_state):
    """Update URL when state is selected from dropdown"""
    if selected_state:
        return f"/state/{selected_state}"
    return "/state/Alabama"


@callback(
    [
        Output("state-total-ssbg-expenditures-card", "children"),
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
    all_time_totals = get_state_totals(
        df, state_name, None, service_categories=service_categories
    )

    # Calculate average expenditure per recipient
    avg_expenditure = (
        totals["total_ssbg_expenditures"] / totals["total_recipients"]
        if totals["total_recipients"] > 0
        else 0
    )

    # Get number of service categories
    filtered_df = df[df["state_name"] == state_name].copy()
    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    total_SSBG_expenditures_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Total SSBG Expenditures FY{str(year)[-2:]}",
                    className="card-title",
                ),
                html.H2(
                    f"${totals['total_ssbg_expenditures']:,.0f}", className="fw-bold"
                ),
                html.P(
                    f"Average since {min_year}: {all_time_totals['average_total_ssbg_expenditures']:,.0f}",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    recipients_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(f"Total Recipients FY{str(year)[-2:]}", className="card-title"),
                html.H2(f"{totals['total_recipients']:,.0f}", className="fw-bold"),
                html.P(
                    f"Average since {min_year}: {all_time_totals['average_total_recipients']:,.0f}",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    categories_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Service Categories Funded FY{str(year)[-2:]}",
                    className="card-title",
                ),
                html.H2(f"{totals['num_service_categories']}", className="fw-bold"),
                html.P(
                    "service categories funded in whole or in part.",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    avg_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Average per Recipient FY{str(year)[-2:]}", className="card-title"
                ),
                html.H2(f"${avg_expenditure:,.0f}", className="fw-bold"),
                html.P(
                    f"Average since {min_year}: ${all_time_totals['average_total_ssbg_expenditures'] / all_time_totals['average_total_recipients'] if all_time_totals['average_total_recipients'] > 0 else 0:,.0f}",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    return total_SSBG_expenditures_card, recipients_card, categories_card, avg_card


@callback(
    Output("state-page-title", "children"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)
def update_state_title(pathname):
    """Update state page title"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
        return f"SSBG Recipient Report: {state_name}"
    return "SSBG Recipient Report: Alabama"


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
            f"Expenditures by Service Category FY{str(year)[-2:]} - {state_name}"
            if year
            else f"Expenditures by Service Category - {state_name}"
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

    return create_pie_chart(
        breakdown,
        names_col="service_category",
        values_col="recipients",
        title=(
            f"Recipients by Service Category FY{str(year)[-2:]} - {state_name}"
            if year
            else f"Recipients by Service Category - {state_name}"
        ),
        hovertemplate="<b>%{label}</b><br>Recipients: %{value:,}<br>Percent: %{percent}",
    )


@callback(
    Output("state-expenditures-time-series", "children"),
    [
        Input("state-time-series-range-slider", "value"),
        Input("state-time-series-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_expenditures_time_series(time_range, service_categories, pathname):
    """Update state expenditures time series graph"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    ts_data = get_state_time_series(
        df,
        state_name,
        value_col="total_ssbg_expenditures",
        service_categories=service_categories,
        time_range=time_range,
    )

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title=f"SSBG Expenditures Over Time - {state_name}",
        labels={"year": "Year", "value": "Expenditures ($)"},
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=400,
        xaxis=dict(
            tickmode="array",
            tickvals=[int(x) for x in sorted(df["year"].unique()) if str(x).isdigit()],
            tickformat="d",
        ),
    )
    fig.update_yaxes(range=[0, None])

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("state-recipients-time-series", "children"),
    [
        Input("state-time-series-range-slider", "value"),
        Input("state-time-series-service-category-dropdown", "value"),
        Input("url", "pathname"),
    ],
)
def update_state_recipients_time_series(time_range, service_categories, pathname):
    """Update state recipients time series graph"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    ts_data = get_state_time_series(
        df,
        state_name,
        value_col="total_recipients",
        service_categories=service_categories,
        time_range=time_range,
    )

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title=f"SSBG Recipients Over Time - {state_name}",
        labels={"year": "Year", "value": "Recipients"},
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=400,
        xaxis=dict(
            tickmode="array",
            tickvals=[int(x) for x in sorted(df["year"].unique()) if str(x).isdigit()],
            tickformat="d",
        ),
    )
    fig.update_yaxes(range=[0, None])

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
        State("url", "pathname"),
    ],
    prevent_initial_call=True,
)
def download_state_csv(n_clicks, pathname):
    """Download filtered state data as CSV"""
    if pathname and pathname.startswith("/state/"):
        state_name = unquote(pathname.replace("/state/", ""))
    else:
        state_name = "Alabama"

    table_data = get_state_full_data(df, state_name, None, None)

    filename = f"ssbg_{state_name.replace(' ', '_')}_data_FY10-FY22.csv"

    return dcc.send_data_frame(table_data.to_csv, filename, index=False)
