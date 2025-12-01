"""
National overview page for SSBG dashboard
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
                            "Social Services Block Grant National Overview",
                            className="text-center mb-4 fw-bold",
                        ),
                        html.P(
                            "The Social Services Block Grant (SSBG) is a federal program that provides states and territories with flexible funding to support essential social services for children, adults, and families. Administered by the Office of Community Services (OCS), SSBG empowers local agencies to design programs that meet their communities’ unique needs—from child protection and foster care to employment assistance and pregnancy and parenting services.\n This interactive dashboard offers a transparent view into how SSBG funds are used across the country: ",
                            className="mb-4",
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    "National Overview: Explore aggregated data on service categories, funding allocations, and populations served."
                                ),
                                html.Li(
                                    "State-Level Insights: Click on any state in the map to view detailed data on expenditures, service delivery, and annual trends."
                                ),
                            ],
                            className="mb-4",
                        ),
                        html.P(
                            "The filtered and unfiltered datasets are available for download. For additional information about the SSBG program, please visit the program information site, read the SSBG Annual Report, or explore related resources. To contact the creator of this dashboard, please see the footer at the bottom of the page.",
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
                                html.Li(
                                    html.A(
                                        "Uniform Definition of Services",
                                        href="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-96/appendix-Appendix%20A%20to%20Part%2096",
                                        target="_blank",
                                    )
                                ),
                            ],
                            className="mb-4",
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
                        width=3,
                    ),
                    dbc.Col(
                        create_service_category_dropdown(
                            unique_vals["service_categories"], "national"
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Download SSBG Dataset FY10-FY22",
                                        className="card-title",
                                    ),
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
                        width=3,
                        className="mb-4",
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
                        width=8,
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="national-avg-per-person-card",
                        width=8,
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        id="national-total-recipients-card",
                        width=8,
                        md=4,
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
            # Top Service Categories
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="national-top-services"), width=6, className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(id="national-top-services-recipients"),
                        width=6,
                        className="mb-4",
                    ),
                ]
            ),
            # Choropleth Map (Main Feature) with Metric Toggle
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H4(
                                                "State-Level Insights",
                                                className="card-title",
                                            ),
                                            width=12,
                                            md=8,
                                        ),
                                        dbc.Col(
                                            dbc.RadioItems(
                                                id="national-metric-toggle",
                                                className="btn-group",
                                                inputClassName="btn-check",
                                                labelClassName="btn btn-outline-primary",
                                                labelCheckedClassName="active",
                                                options=[
                                                    {
                                                        "label": "Recipients",
                                                        "value": "recipients",
                                                    },
                                                    {
                                                        "label": "Expenditures",
                                                        "value": "expenditures",
                                                    },
                                                ],
                                                value="recipients",
                                            ),
                                            width=12,
                                            md=4,
                                            className="d-flex justify-content-md-end",
                                        ),
                                    ],
                                    className="mb-3 align-items-center",
                                ),
                                html.P(
                                    "Click on a state to view detailed state report",
                                    className="text-muted mb-3",
                                ),
                                html.Div(
                                    id="national-choropleth-map",
                                    style={"cursor": "pointer"},
                                ),
                            ]
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                ),
                className="mb-4",
            ),
            # Time Series Graphs
            # slider
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
                                        id="national-time-series-range-slider",
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
                        create_service_category_dropdown(
                            unique_vals["service_categories"], "time-series-national"
                        ),
                        width=6,
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="national-expenditures-time-series"),
                        width=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(id="national-recipients-time-series"),
                        width=6,
                        className="mb-4",
                    ),
                ]
            ),
            # Full Data Table
            dbc.Row(
                dbc.Col(
                    [
                        html.H3("Full Data Table", className="mb-3"),
                        html.Div(id="national-data-table"),
                    ],
                    width=12,
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
        Output("national-avg-per-person-card", "children"),
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
    all_time_totals = get_national_totals(df, None, service_categories)
    unique_vals = get_unique_values(df)

    total_ssbg_expenditures_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Total SSBG Expenditures {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"${totals['total_ssbg_expenditures']:,.0f}",
                    className="fw-bold text-center",
                ),
                html.P(
                    f"Average since {min_year}: ${all_time_totals['average_total_ssbg_expenditures']:,.0f}",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    recipients_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Total Recipients {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"{totals['total_recipients']:,.0f}",
                    className="fw-bold text-center",
                ),
                html.P(
                    f"Average since {min_year}: {all_time_totals['average_total_recipients']:,.0f}",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    avg_per_person_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Average $ per Recipient {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"${(totals['total_ssbg_expenditures']/totals['total_recipients']):,.0f}",
                    className="fw-bold text-center",
                ),
                html.P(
                    f"Average since {min_year}: ${all_time_totals['total_ssbg_expenditures']/all_time_totals['total_recipients']:,.0f}",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    ssbg_expenditures_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"SSBG Expenditures {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"${totals['ssbg_expenditures']:,.0f}",
                    className="fw-bold text-center",
                ),
                html.P(
                    f"{(totals['ssbg_expenditures']/totals['total_ssbg_expenditures'])*100:.0f}% of the Total SSBG Expenditures",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    tanf_transfer_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"TANF Transfer Funds {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"${totals['tanf_transfer_funds']:,.0f}",
                    className="fw-bold text-center",
                ),
                html.P(
                    f"{(totals['tanf_transfer_funds']/totals['total_ssbg_expenditures'])*100:.0f}% of the Total SSBG Expenditures",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    children_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Children Served {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(f"{totals['children']:,.0f}", className="fw-bold text-center"),
                html.P(
                    f"{(totals['children']/totals['total_recipients'])*100:.0f}% of the Total Recipients",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    adults_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    f"Adults Served {'FY'+ str(year)[-2:] if year else f'FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}' }",
                    className="card-title text-center",
                ),
                html.H2(
                    f"{totals['total_adults']:,.0f}", className="fw-bold text-center"
                ),
                html.P(
                    f"{(totals['total_adults']/totals['total_recipients'])*100:.0f}% of the Total Recipients",
                    className="text-muted mb-0 text-center",
                ),
            ]
        ),
        className="shadow-sm h-100",
    )

    return (
        total_ssbg_expenditures_card,
        recipients_card,
        avg_per_person_card,
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
    """Update choropleth map"""
    map_data = get_map_data(df, metric, year, service_categories)
    return create_choropleth_map(
        map_data,
        metric,
        f"SSBG {metric.title()} by State {'FY'+str(year)[-2:] if year else ''}",
    )


@callback(
    Output("national-expenditures-time-series", "children"),
    [
        Input("national-time-series-range-slider", "value"),
        Input("time-series-national-service-category-dropdown", "value"),
    ],
)
def update_expenditures_time_series(time_range, service_categories):
    """Update total_ssbg_expenditures time series graph"""
    ts_data = get_time_series_data(
        df, "total_ssbg_expenditures", service_categories, time_range
    )

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title="SSBG Expenditures Over Time by Service Category",
        labels={
            "year": "Year",
            "value": "Expenditures ($)",
        },
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
    Output("national-recipients-time-series", "children"),
    [
        Input("national-time-series-range-slider", "value"),
        Input("time-series-national-service-category-dropdown", "value"),
    ],
)
def update_recipients_time_series(time_range, service_categories):
    """Update recipients time series graph"""
    ts_data = get_time_series_data(
        df, "total_recipients", service_categories, time_range
    )

    fig = px.line(
        ts_data,
        x="year",
        y="value",
        title="SSBG Recipients Over Time",
        labels={
            "year": "Year",
            "value": "Recipients",
        },
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
    Output("national-top-services", "children"),
    [
        Input("national-year-dropdown", "value"),
    ],
)
def update_top_services(year):
    """Update top service categories chart"""
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

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
            f"Top 10 Service Categories by Total SSBG Expenditures FY{str(year)[-2:]}"
            if year
            else "Top 10 Service Categories by Total SSBG Expenditures"
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
    Output("national-top-services-recipients", "children"),
    [
        Input("national-year-dropdown", "value"),
    ],
)
def update_top_services_recipients(year):
    """Update top service categories chart"""
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    # Use selected year
    latest_data = (
        filtered_df[filtered_df["year"].astype(int) == year] if year else filtered_df
    )

    service_totals = (
        latest_data.groupby("service_category")["total_recipients"].sum().reset_index()
    )
    service_totals = service_totals.sort_values(
        "total_recipients", ascending=False
    ).head(10)

    fig = px.bar(
        service_totals,
        x="total_recipients",
        y="service_category",
        orientation="h",
        title=(
            f"Top 10 Service Categories by Total Recipients FY{str(year)[-2:]}"
            if year
            else "Top 10 Service Categories by Total Recipients"
        ),
        labels={
            "total_recipients": "Recipients",
            "service_category": "Service Category",
        },
    )
    fig.update_layout(
        template="plotly_white", height=400, yaxis={"categoryorder": "total ascending"}
    )

    return dcc.Graph(figure=fig, className="mb-4")


@callback(
    Output("national-data-table", "children"),
    [
        Input("national-year-dropdown", "value"),
        Input("national-service-category-dropdown", "value"),
    ],
)
def update_national_data_table(year, service_categories):
    """Update national data table"""

    table_data = df.copy()
    table_data = table_data[table_data["year"] == year] if year else table_data
    table_data = (
        table_data[table_data["service_category"].isin(service_categories)]
        if service_categories
        else table_data
    )

    # make columns more readable with $ and ,
    monetary_columns = [
        "ssbg_expenditures",
        "tanf_transfer_funds",
        "total_ssbg_expenditures",
        "other_fed_state_and_local_funds",
        "total_expenditures",
    ]
    recipient_columns = [
        "children",
        "adults_59_and_younger",
        "adults_60_and_older",
        "adults_unknown",
        "total_adults",
        "total_recipients",
    ]
    for col in monetary_columns:
        table_data[col] = table_data[col].apply(lambda x: f"${x:,}")
    for col in recipient_columns:
        table_data[col] = table_data[col].apply(lambda x: f"{x:,}")

    # rename columns for better readability
    column_renames = {
        "year": "Year",
        "state_name": "State",
        "line_num": "Form Line",
        "service_category": "Service Category",
        "ssbg_expenditures": "SSBG Expenditures",
        "tanf_transfer_funds": "TANF Transfer Funds",
        "total_ssbg_expenditures": "Total SSBG Expenditures",
        "other_fed_state_and_local_funds": "All Other Federal/State/Local Funds",
        "total_expenditures": "Total Expenditures",
        "children": "Children Served",
        "adults_59_and_younger": "Adults 59 and Younger Served",
        "adults_60_and_older": "Adults 60 and Older Served",
        "adults_unknown": "Adults Unknown Age Served",
        "total_adults": "Total Adults Served",
        "total_recipients": "Total Recipients Served",
    }
    table_data = table_data.rename(columns=column_renames)

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
    Output("national-download-csv", "data"),
    Input("national-download-btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    """Download filtered data as CSV"""
    df_copy = df.copy()

    return dcc.send_data_frame(df_copy.to_csv, "ssbg_national_data.csv", index=False)
