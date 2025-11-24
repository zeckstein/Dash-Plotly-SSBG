"""
Reusable card components for the dashboard
"""
import dash_bootstrap_components as dbc
from dash import html

def create_summary_card(title, value, subtitle=None, footer=None, color="primary"):
    """
    Create a summary card component
    
    Parameters:
    -----------
    title : str
        Card title
    value : str or number
        Main value to display
    subtitle : str, optional
        Subtitle text (displayed below title)
    footer : str, optional
        Footer text (displayed below value, often for averages or percentages)
    color : str
        Bootstrap color theme or custom color class
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(title, className="card-title text-center"),
                html.H6(subtitle, className="card-subtitle mb-2 text-muted text-center") if subtitle else None,
                html.H2(
                    value,
                    className="fw-bold text-center"
                ),
                html.P(
                    footer,
                    className="text-muted mb-0 text-center"
                ) if footer else None,
            ]
        ),
        className="shadow-sm h-100",
        # color=color, # We are using custom CSS for colors mostly, or default white cards with colored text
        # outline=True
    )
