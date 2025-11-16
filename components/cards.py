"""
Reusable card components for the dashboard
"""
import dash_bootstrap_components as dbc

def create_summary_card(title, value, subtitle=None, color="primary"):
    """
    Create a summary card component
    
    Parameters:
    -----------
    title : str
        Card title
    value : str or number
        Main value to display
    subtitle : str, optional
        Subtitle text
    color : str
        Bootstrap color theme
    """
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.CardTitle(title, className="card-title"),
                dbc.CardSubtitle(
                    subtitle,
                    className="mb-2 text-muted"
                ) if subtitle else None,
                dbc.CardText(
                    value,
                    className="display-4 fw-bold"
                ),
            ]
        ),
        className="mb-3 shadow-sm",
        color=color,
        outline=True
    )

