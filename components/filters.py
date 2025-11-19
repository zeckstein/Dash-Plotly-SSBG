"""
Filter control components
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_year_dropdown(min_year, max_year, id_prefix="national"):
    """
    Create a single year dropdown selector

    Parameters:
    -----------
    min_year : int
        Minimum year
    max_year : int
        Maximum year
    id_prefix : str
        Prefix for component IDs
    """
    years = list(range(min_year, max_year + 1))
    return dbc.Card(
        dbc.CardBody(
            [
                html.Label("Year", className="form-label fw-bold"),
                dcc.Dropdown(
                    id=f"{id_prefix}-year-dropdown",
                    options=[{"label": str(year), "value": year} for year in years],
                    value=max_year,  # Default to latest year
                    placeholder="Select year...",
                    className="mb-2",
                ),
            ]
        ),
        className="mb-3 shadow-sm",
    )


def create_service_category_dropdown(service_categories, id_prefix="national"):
    """
    Create a multi-select dropdown for service categories

    Parameters:
    -----------
    service_categories : list
        List of service category names
    id_prefix : str
        Prefix for component IDs
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.Label("Service Categories", className="form-label fw-bold"),
                dcc.Dropdown(
                    id=f"{id_prefix}-service-category-dropdown",
                    options=[
                        {"label": cat, "value": cat} for cat in service_categories
                    ],
                    value=[],  # All selected by default
                    multi=True,
                    placeholder="All service categories selected by default...",
                    className="mb-2",
                ),
            ]
        ),
        className="mb-3 shadow-sm",
    )


def create_metric_toggle(id_prefix="national"):
    """
    Create a toggle button for expenditures/recipients

    Parameters:
    -----------
    id_prefix : str
        Prefix for component IDs
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.Label("View Metric", className="form-label fw-bold"),
                dcc.RadioItems(
                    id=f"{id_prefix}-metric-toggle",
                    options=[
                        {"label": "Recipients", "value": "recipients"},
                        {"label": "Expenditures", "value": "expenditures"},
                    ],
                    value="recipients",  # Default to recipients
                    inline=True,
                    className="mb-2",
                ),
            ]
        ),
        className="mb-3 shadow-sm",
    )
