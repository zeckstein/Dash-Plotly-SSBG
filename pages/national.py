"""
National overview page for SSBG dashboard
# TODO update cards and subtitles
# TODO add cards for ssbgexp and tanf and then children and adults served (with pie for children v adults (split into adult age categories))
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback, dash_table
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import (
    load_data,
    get_national_totals,
    get_time_series_data,
    get_map_data,
    get_unique_values,
)
from components.filters import (
    create_year_dropdown,
    create_service_category_dropdown,
    create_metric_toggle,
)
from components.map import create_choropleth_map

# Load data once
df = load_data()
unique_vals = get_unique_values(df)
min_year = min(unique_vals["years"])
max_year = max(unique_vals["years"])


def layout():
    """Create the national page layout"""
    return dbc.Container(
        [
            # Header
            dbc.Row(
                dbc.Col(
                    [
                        html.H1(
                            "SSBG National Overview",
                            className="text-center mb-4 fw-bold",
                        ),
                        html.P(
                            "Social Services Block Grant Data Dashboard",
                            className="text-center text-muted mb-4",
                        ),
                    ],
                    width=12,
                )
            ),
            # Filters Year and Service Category
            dbc.Row(
                [
                    dbc.Col(
                        create_year_dropdown(min_year, max_year, "national"),
                        width=12,
                        md=4,
                    ),
                    dbc.Col(
                        create_service_category_dropdown(
                            unique_vals["service_categories"], "national"
                        ),
                        width=8,
                        md=8,
                    ),
                ],
                className="mb-4",
            ),
            # Summary Cards
            # Summary Cards Row (Total SSBG Expenditures & Total Recipients)
            dbc.Row(
                [
                    dbc.Col(
                        id="national-total-ssbg-expenditures-card",
                        width=12,
                        md=6,
                        className="mb-3 align-items-center justify-content-center",
                    ),
                    dbc.Col(
                        id="national-total-recipients-card",
                        width=12,
                        md=6,
                        className="mb-3",
                    ),
                ],
                className="mb-4",
            ),
            # Subtotals Row (SSBG Expenditures, TANF Transfer Funds, Children, Adults)
            dbc.Row(
                [
                    dbc.Col(
                        id="national-ssbg-expenditures-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="national-tanf-transfer-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="national-children-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="national-adults-card",
                        width=12,
                        md=3,
                        className="mb-3",
                    ),
                ],
                className="mb-4",
            ),
            # Metric Toggle Row
            dbc.Row(
                [
                    dbc.Col(
                        create_metric_toggle("national"),
                        width=12,
                        md=4,
                        className="d-flex flex-column justify-content-end",
                    ),
                ]
            ),
            # Chloropleth Map (Main Feature)
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "Click on a state to view detailed state report",
                            className="text-center text-muted mb-3",
                        ),
                        html.Div(
                            id="national-choropleth-map", style={"cursor": "pointer"}
                        ),
                    ],
                    width=12,
                ),
                className="mb-4",
            ),
            # Time Series Graphs
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="national-expenditures-time-series"),
                        width=12,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(id="national-recipients-time-series"),
                        width=12,
                        className="mb-4",
                    ),
                ]
            ),
            # Top Service Categories
            dbc.Row(
                dbc.Col(
                    html.Div(id="national-top-services"), width=12, className="mb-4"
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
                                    id="national-download-btn",
                                    color="primary",
                                    className="mt-2",
                                ),
                                dcc.Download(id="national-download-csv"),
                            ]
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    md=6,
                    className="mb-4",
                )
            ),
            # Resources Section
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Additional Resources", className="card-title"),
                                html.P(
                                    "Links to SSBG annual reports and additional information:"
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            html.A(
                                                "ACF SSBG Annual Reports",
                                                href="https://www.acf.hhs.gov/ocs/resource/ssbg-annual-reports",
                                                target="_blank",
                                            )
                                        ),
                                        html.Li(
                                            html.A(
                                                "SSBG Program Information",
                                                href="https://www.acf.hhs.gov/ocs/programs/ssbg",
                                                target="_blank",
                                            )
                                        ),
                                    ]
                                ),
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
    )


# Callbacks
@callback(
    [
        Output("national-total-ssbg-expenditures-card", "children"),
        Output("national-total-recipients-card", "children"),
        Output("national-ssbg-expenditures-card", "children"),
        Output("national-tanf-transfer-card", "children"),
        Output("national-children-card", "children"),
        Output("national-adults-card", "children"),
    ],
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
    ],
)
def update_summary_cards(year, service_categories):
    """Update summary cards"""
    totals = get_national_totals(df, year, service_categories)
    all_time_totals = get_national_totals(df, None, None)
    unique_vals = get_unique_values(df)

    total_ssbg_expenditures_card = dbc.Card(
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
                    f"Average since {min_year}: ${all_time_totals['average_total_ssbg_expenditures']:,.0f}",
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

    ssbg_expenditures_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"SSBG Expenditures FY{str(year)[-2:]}", className="card-title"
                ),
                html.H2(f"${totals['ssbg_expenditures']:,.0f}", className="fw-bold"),
            ]
        ),
        className="shadow-sm h-100",
    )

    tanf_transfer_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"TANF Transfer Funds FY{str(year)[-2:]}", className="card-title"
                ),
                html.H2(f"${totals['tanf_transfer_funds']:,.0f}", className="fw-bold"),
            ]
        ),
        className="shadow-sm h-100",
    )

    children_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(f"Children Served FY{str(year)[-2:]}", className="card-title"),
                html.H2(f"{totals['children']:,.0f}", className="fw-bold"),
            ]
        ),
        className="shadow-sm h-100",
    )

    adults_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(f"Adults Served FY{str(year)[-2:]}", className="card-title"),
                html.H2(f"{totals['total_adults']:,.0f}", className="fw-bold"),
            ]
        ),
        className="shadow-sm h-100",
    )

    return (
        total_ssbg_expenditures_card,
        recipients_card,
        ssbg_expenditures_card,
        tanf_transfer_card,
        children_card,
        adults_card,
    )


@callback(
    Output("national-choropleth-map", "children"),
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
        Input("national-metric-toggle", "value"),
    ],
)
def update_map(year, service_categories, metric):
    """Update chloropleth map"""
    map_data = get_map_data(df, metric, year, service_categories)
    return create_choropleth_map(map_data, metric, f"SSBG {metric.title()} by State")


@callback(
    Output("national-expenditures-time-series", "children"),
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
    ],
)
def update_expenditures_time_series(year, service_categories):
    """Update total_ssbg_expenditures time series graph"""
    ts_data = get_time_series_data(df, "total_ssbg_expenditures", service_categories)

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        color="service_category",
        title="SSBG Expenditures Over Time by Service Category",
        labels={
            "year": "Year",
            "value": "Expenditures ($)",
            "service_category": "Service Category",
        },
    )
    fig.update_layout(template="plotly_white", hovermode="x unified", height=400)

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("national-recipients-time-series", "children"),
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
    ],
)
def update_recipients_time_series(year, service_categories):
    """Update recipients time series graph"""
    ts_data = get_time_series_data(df, "total_recipients", service_categories)

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        color="service_category",
        title="SSBG Recipients Over Time by Service Category",
        labels={
            "year": "Year",
            "value": "Recipients",
            "service_category": "Service Category",
        },
    )
    fig.update_layout(template="plotly_white", hovermode="x unified", height=400)

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("national-top-services", "children"),
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
    ],
)
def update_top_services(year, service_categories):
    """Update top service categories chart"""
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    # Use selected year
    latest_data = (
        filtered_df[filtered_df["year"].astype(int) == year] if year else filtered_df
    )

    service_totals = (
        latest_data.groupby("service_category")["total_ssbg_expenditures"]
        .sum()
        .reset_index()
    )
    service_totals = service_totals.sort_values(
        "total_ssbg_expenditures", ascending=False
    ).head(10)

    fig = px.bar(
        service_totals,
        x="total_ssbg_expenditures",
        y="service_category",
        orientation="h",
        title=(
            f"Top Service Categories by Expenditures ({year})"
            if year
            else "Top Service Categories by Expenditures"
        ),
        labels={
            "total_ssbg_expenditures": "Expenditures ($)",
            "service_category": "Service Category",
        },
    )
    fig.update_layout(
        template="plotly_white", height=400, yaxis={"categoryorder": "total ascending"}
    )

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("national-download-csv", "data"),
    Input("national-download-btn", "n_clicks"),
    [
        State("national-year-dropdown", "value"),
        State("national-service-category-dropdown", "value"),
    ],
    prevent_initial_call=True,
)
def download_csv(n_clicks, year, service_categories):
    """Download filtered data as CSV"""
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    return dcc.send_data_frame(
        filtered_df.to_csv, "ssbg_national_data.csv", index=False
    )
