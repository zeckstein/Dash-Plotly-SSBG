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
from utils.constants import (
    COL_YEAR,
    COL_SERVICE_CATEGORY,
    COL_TOTAL_SSBG_EXPENDITURES,
    COL_TOTAL_RECIPIENTS,
    COL_SSBG_EXPENDITURES,
    COL_TANF_TRANSFER,
    COL_CHILDREN,
    COL_ADULTS,
    COL_TOTAL_EXPENDITURES,
    DISPLAY_NAMES,
)
from components.filters import (
    create_year_dropdown,
    create_service_category_dropdown,
)
from components.map import create_choropleth_map
from components.cards import create_summary_card

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
                            "Social Services Block Grant Dashboard",
                            className="mb-4 fw-bold",
                        ),
                        html.P(
                            "The Social Services Block Grant (SSBG) is a federal program that provides states and territories with flexible funding to support essential social services for children, adults, and families. Administered by the Office of Community Services (OCS), SSBG empowers local agencies to design programs that meet their communities’ unique needs—from child protection and foster care to employment assistance and pregnancy and parenting services.\n This interactive dashboard offers a transparent view into how SSBG funds are used across the country.",
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
    
    year_suffix = f"FY{str(year)[-2:]}" if year else f"FY{str(min_year)[-2:]}-FY{str(max_year)[-2:]}"

    total_ssbg_expenditures_card = create_summary_card(
        title=f"Total SSBG Expenditures {year_suffix}",
        value=f"${totals['total_ssbg_expenditures']:,.0f}",
        footer=f"Average since {min_year}: ${all_time_totals['average_total_ssbg_expenditures']:,.0f}"
    )

    recipients_card = create_summary_card(
        title=f"Total Recipients {year_suffix}",
        value=f"{totals['total_recipients']:,.0f}",
        footer=f"Average since {min_year}: {all_time_totals['average_total_recipients']:,.0f}"
    )

    avg_per_person_card = create_summary_card(
        title=f"Average $ per Recipient {year_suffix}",
        value=f"${(totals['total_ssbg_expenditures']/totals['total_recipients']):,.0f}" if totals['total_recipients'] > 0 else "$0",
        footer=f"Average since {min_year}: ${all_time_totals['total_ssbg_expenditures']/all_time_totals['total_recipients']:,.0f}" if all_time_totals['total_recipients'] > 0 else "$0"
    )

    ssbg_expenditures_card = create_summary_card(
        title=f"SSBG Expenditures {year_suffix}",
        value=f"${totals['ssbg_expenditures']:,.0f}",
        footer=f"{(totals['ssbg_expenditures']/totals['total_ssbg_expenditures'])*100:.0f}% of the Total SSBG Expenditures" if totals['total_ssbg_expenditures'] > 0 else "0%"
    )

    tanf_transfer_card = create_summary_card(
        title=f"TANF Transfer Funds {year_suffix}",
        value=f"${totals['tanf_transfer_funds']:,.0f}",
        footer=f"{(totals['tanf_transfer_funds']/totals['total_ssbg_expenditures'])*100:.0f}% of the Total SSBG Expenditures" if totals['total_ssbg_expenditures'] > 0 else "0%"
    )

    children_card = create_summary_card(
        title=f"Children Served {year_suffix}",
        value=f"{totals['children']:,.0f}",
        footer=f"{(totals['children']/totals['total_recipients'])*100:.0f}% of the Total Recipients" if totals['total_recipients'] > 0 else "0%"
    )

    adults_card = create_summary_card(
        title=f"Adults Served {year_suffix}",
        value=f"{totals['total_adults']:,.0f}",
        footer=f"{(totals['total_adults']/totals['total_recipients'])*100:.0f}% of the Total Recipients" if totals['total_recipients'] > 0 else "0%"
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
        df, COL_TOTAL_SSBG_EXPENDITURES, service_categories, time_range
    )

    fig = px.line(
        ts_data,
        x=COL_YEAR,
        y="value",
        title="SSBG Expenditures Over Time by Service Category",
        labels={
            COL_YEAR: "Year",
            "value": "Expenditures ($)",
        },
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=400,
        xaxis=dict(
            tickmode="array",
            tickvals=[int(x) for x in sorted(df[COL_YEAR].unique()) if str(x).isdigit()],
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
        df, COL_TOTAL_RECIPIENTS, service_categories, time_range
    )

    fig = px.line(
        ts_data,
        x=COL_YEAR,
        y="value",
        title="SSBG Recipients Over Time",
        labels={
            COL_YEAR: "Year",
            "value": "Recipients",
        },
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=400,
        xaxis=dict(
            tickmode="array",
            tickvals=[int(x) for x in sorted(df[COL_YEAR].unique()) if str(x).isdigit()],
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
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    # Use selected year
    latest_data = (
        filtered_df[filtered_df[COL_YEAR].astype(int) == year] if year else filtered_df
    )

    service_totals = (
        latest_data.groupby(COL_SERVICE_CATEGORY)[COL_TOTAL_SSBG_EXPENDITURES]
        .sum()
        .reset_index()
    )
    service_totals = service_totals.sort_values(
        COL_TOTAL_SSBG_EXPENDITURES, ascending=False
    ).head(10)

    fig = px.bar(
        service_totals,
        x=COL_TOTAL_SSBG_EXPENDITURES,
        y=COL_SERVICE_CATEGORY,
        orientation="h",
        title=(
            f"Top 10 Service Categories by Total SSBG Expenditures FY{str(year)[-2:]}"
            if year
            else "Top 10 Service Categories by Total SSBG Expenditures"
        ),
        labels={
            COL_TOTAL_SSBG_EXPENDITURES: "Expenditures ($)",
            COL_SERVICE_CATEGORY: "Service Category",
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
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    # Use selected year
    latest_data = (
        filtered_df[filtered_df[COL_YEAR].astype(int) == year] if year else filtered_df
    )

    service_totals = (
        latest_data.groupby(COL_SERVICE_CATEGORY)[COL_TOTAL_RECIPIENTS].sum().reset_index()
    )
    service_totals = service_totals.sort_values(
        COL_TOTAL_RECIPIENTS, ascending=False
    ).head(10)

    fig = px.bar(
        service_totals,
        x=COL_TOTAL_RECIPIENTS,
        y=COL_SERVICE_CATEGORY,
        orientation="h",
        title=(
            f"Top 10 Service Categories by Total Recipients FY{str(year)[-2:]}"
            if year
            else "Top 10 Service Categories by Total Recipients"
        ),
        labels={
            COL_TOTAL_RECIPIENTS: "Recipients",
            COL_SERVICE_CATEGORY: "Service Category",
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
    table_data = table_data[table_data[COL_YEAR] == year] if year else table_data
    table_data = (
        table_data[table_data[COL_SERVICE_CATEGORY].isin(service_categories)]
        if service_categories
        else table_data
    )

    # make columns more readable with $ and ,
    monetary_columns = [
        COL_SSBG_EXPENDITURES,
        COL_TANF_TRANSFER,
        COL_TOTAL_SSBG_EXPENDITURES,
        "other_fed_state_and_local_funds",
        COL_TOTAL_EXPENDITURES,
    ]
    recipient_columns = [
        COL_CHILDREN,
        "adults_59_and_younger",
        "adults_60_and_older",
        "adults_unknown",
        COL_ADULTS,
        COL_TOTAL_RECIPIENTS,
    ]
    for col in monetary_columns:
        table_data[col] = table_data[col].apply(lambda x: f"${x:,}")
    for col in recipient_columns:
        table_data[col] = table_data[col].apply(lambda x: f"{x:,}")

    # rename columns for better readability
    table_data = table_data.rename(columns=DISPLAY_NAMES)

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
