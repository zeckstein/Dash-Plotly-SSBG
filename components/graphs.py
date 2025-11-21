"""
Reusable graph components
"""

import plotly.graph_objects as go
import plotly.express as px
from dash import dcc


def create_time_series_line_chart(
    df,
    x_col="year",
    y_col="value",
    color_col="service_category",
    title="Time Series",
    x_title="Year",
    y_title="Value",
):
    """
    Create a time series line chart

    Parameters:
    -----------
    df : pd.DataFrame
        Data with columns for x, y, and color
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    color_col : str
        Column name for line colors
    title : str
        Chart title
    x_title : str
        X-axis title
    y_title : str
        Y-axis title
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: x_title, y_col: y_title, color_col: "Service Category"},
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01),
        xaxis=dict(
            tickmode="array",
            tickvals=[int(x) for x in sorted(df[x_col].unique()) if str(x).isdigit()],
            tickformat="d",
        ),
    )
    return dcc.Graph(figure=fig, className="mb-4")


def create_bar_chart(
    df,
    x_col,
    y_col,
    title="Bar Chart",
    x_title="Category",
    y_title="Value",
    orientation="v",
    color_col=None,
):
    """
    Create a bar chart

    Parameters:
    -----------
    df : pd.DataFrame
        Data
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    title : str
        Chart title
    x_title : str
        X-axis title
    y_title : str
        Y-axis title
    orientation : str
        'v' for vertical, 'h' for horizontal
    color_col : str, optional
        Column name for color mapping
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: x_title, y_col: y_title},
        orientation=orientation,
        color=color_col if color_col else None,
    )
    fig.update_layout(
        template="plotly_white",
        showlegend=bool(color_col),
        yaxis={"categoryorder": "total ascending"},
    )
    return dcc.Graph(figure=fig, className="mb-4")


def create_pie_chart(df, names_col, values_col, title="Pie Chart", hovertemplate=None):
    """
    Create a pie chart

    Parameters:
    -----------
    df : pd.DataFrame
        Data
    names_col : str
        Column name for pie slice labels
    values_col : str
        Column name for pie slice values
    title : str
        Chart title
    """
    # Create custom legend labels with percentages
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
    )
    fig.update_layout(template="plotly_white")
    if hovertemplate:
        fig.update_traces(hovertemplate=hovertemplate)
    return dcc.Graph(figure=fig, className="mb-4")
