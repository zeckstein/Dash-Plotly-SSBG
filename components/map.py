"""
Chloropleth map component for US states and territories
"""

import plotly.graph_objects as go
from dash import dcc
import pandas as pd

# State abbreviations mapping (including territories)
STATE_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "Puerto Rico": "PR",
    "Guam": "GU",
    "U.S. Virgin Islands": "VI",
    "American Samoa": "AS",
    "Northern Mariana Islands": "MP",
}


def create_choropleth_map(df, metric="recipients", title="SSBG Data by State"):
    """
    Create a chloropleth map of US states and territories

    Parameters:
    -----------
    df : pd.DataFrame
        Data with columns: state_name, value, total_ssbg_expenditures, total_recipients
    metric : str
        'expenditures' or 'recipients' (determines which value to show)
    title : str
        Map title
    """
    # Create a copy and add state abbreviations
    map_df = df.copy()
    map_df["state_abbrev"] = map_df["state_name"].map(STATE_ABBREV)

    # Filter out states without abbreviations (if any)
    map_df = map_df[map_df["state_abbrev"].notna()]

    # SSBG color scale: from light blue (secondary) to dark blue (primary)
    ssbg_colorscale = [
        [0, "rgb(255, 255, 255)"],  # white
        [0.5, "rgb(70, 137, 187)"],  # Medium blue
        [1, "rgb(38, 74, 100)"],  # Primary dark blue
    ]

    fig = go.Figure(
        data=go.Choropleth(
            locations=map_df["state_abbrev"],
            z=map_df["value"],
            locationmode="USA-states",
            colorscale=ssbg_colorscale,
            text=map_df.apply(
                lambda row: f"<b>{row['state_name']}</b><br>"
                + f"Expenditures: ${row['total_ssbg_expenditures']:,.0f}<br>"
                + f"Recipients: {row['total_recipients']:,.0f}",
                axis=1,
            ),
            hovertemplate="%{text}<extra></extra>",
            marker_line_color="black",
            marker_line_width=1,
            colorbar_title=metric.title(),
            colorbar=dict(
                title=dict(font=dict(size=14, color="rgb(51, 106, 144)")),
                tickfont=dict(size=12, color="rgb(51, 106, 144)"),
            ),
        )
    )

    fig.update_layout(
        title_text=title,
        title_x=0.5,
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return dcc.Graph(
        figure=fig,
        id="choropleth-map",
        className="mb-4",
        config={"displayModeBar": False},
        clickData=None,
    )
