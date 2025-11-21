"""
Data loading and processing utilities for SSBG dashboard
"""

import pandas as pd
import os

# Path to the data file
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "ssbg_data_cleaned.pkl"
)


def load_data():
    """Load the SSBG data from pickle file"""
    return pd.read_pickle(DATA_PATH)


def get_national_totals(df, year=None, service_categories=None):
    """
    Get national totals for expenditures and recipients

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    year : int, optional
        Year to filter by
    service_categories : list, optional
        List of service categories to filter by

    Returns:
    --------
    dict with 'expenditures' and 'recipients' totals:
    'total_expenditures' = total SSBG expenditures + 'Other Fed State and Local funds'
    'total_ssbg_expenditures' = ssbg_expenditures + 'tanf_transfer_funds'
    'percent_total_ssbg_expenditures_of_total_expenditures',
    'average_total_ssbg_expenditures',
    'average_total_recipients',
    'average_ssbg_expenditures',
    'average_tanf_expenditures',
    'average_child_recipients',
    'average_adult_recipients',
    """
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    return {
        "total_ssbg_expenditures": int(filtered_df["total_ssbg_expenditures"].sum()),
        "ssbg_expenditures": int(filtered_df["ssbg_expenditures"].sum()),
        "tanf_transfer_funds": int(filtered_df["tanf_transfer_funds"].sum()),
        "total_recipients": int(filtered_df["total_recipients"].sum()),
        "children": int(filtered_df["children"].sum()),
        "total_adults": int(filtered_df["total_adults"].sum()),
        "total_expenditures": int(filtered_df["total_expenditures"].sum()),
        "percent_total_ssbg_expenditures_of_total_expenditures": int(
            (
                filtered_df["total_ssbg_expenditures"].sum()
                / filtered_df["total_expenditures"].sum()
            )
            * 100
        ),
        "average_total_ssbg_expenditures": int(
            filtered_df.groupby("year")["total_ssbg_expenditures"].sum().mean()
        ),
        "average_total_recipients": int(
            filtered_df.groupby("year")["total_recipients"].sum().mean()
        ),
        "average_ssbg_expenditures": int(
            filtered_df.groupby("year")["ssbg_expenditures"].sum().mean()
        ),
        "average_tanf_expenditures": int(
            filtered_df.groupby("year")["tanf_transfer_funds"].sum().mean()
        ),
        "average_child_recipients": int(
            filtered_df.groupby("year")["children"].sum().mean()
        ),
        "average_adult_recipients": int(
            filtered_df.groupby("year")["total_adults"].sum().mean()
        ),
    }


def get_state_totals(df, state_name, year=None, service_categories=None):
    """
    Get totals for a specific state.
    TODO: add Massachusetts Commission for the Blind data to Massachusetts totals for each year.
    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    state_name : str
        Name of the state
    year : int, optional
        Year to filter by
    service_categories : list, optional
        List of service categories to filter by

    Returns:
    --------
    dict with 'expenditures' and 'recipients' totals:
    'expenditures' = total SSBG expenditures
    'recipients' = total recipients
    'total_expenditures' = total SSBG expenditures + 'Other Fed State and Local funds'
    'total_ssbg_expenditures' = ssbg_expenditures + 'tanf_transfer_funds'
    'percent_total_ssbg_expenditures_of_total_expenditures',
    'average_total_ssbg_expenditures',
    'average_total_recipients',
    'average_ssbg_expenditures',
    'average_tanf_expenditures',
    'average_child_recipients',
    'average_adult_recipients',
    """
    filtered_df = df[df["state_name"] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    return {
        "num_service_categories": filtered_df[
            filtered_df["total_ssbg_expenditures"] > 0
        ]["service_category"].nunique(),
        "total_ssbg_expenditures": int(filtered_df["total_ssbg_expenditures"].sum()),
        "ssbg_expenditures": int(filtered_df["ssbg_expenditures"].sum()),
        "tanf_transfer_funds": int(filtered_df["tanf_transfer_funds"].sum()),
        "total_recipients": int(filtered_df["total_recipients"].sum()),
        "children": int(filtered_df["children"].sum()),
        "total_adults": int(filtered_df["total_adults"].sum()),
        "total_expenditures": int(filtered_df["total_expenditures"].sum()),
        "average_total_ssbg_expenditures": int(
            filtered_df.groupby("year")["total_ssbg_expenditures"].sum().mean()
        ),
        "average_total_recipients": int(
            filtered_df.groupby("year")["total_recipients"].sum().mean()
        ),
        "average_ssbg_expenditures": int(
            filtered_df.groupby("year")["ssbg_expenditures"].sum().mean()
        ),
        "average_tanf_expenditures": int(
            filtered_df.groupby("year")["tanf_transfer_funds"].sum().mean()
        ),
        "average_child_recipients": int(
            filtered_df.groupby("year")["children"].sum().mean()
        ),
        "average_adult_recipients": int(
            filtered_df.groupby("year")["total_adults"].sum().mean()
        ),
    }


def get_time_series_data(
    df, value_col="total_ssbg_expenditures", service_categories=None, time_range=None
):
    """
    Get time series data for expenditures or recipients by service category

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    value_col : str
        Column to aggregate (ex.'total_ssbg_expenditures' or 'total_recipients')
    service_categories : list, optional
        List of service categories to filter by

    Returns:
    --------
    pd.DataFrame with columns: year, service_category, value
    """
    filtered_df = df.copy()
    filtered_df["year"] = filtered_df["year"].astype(int)

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    if time_range:
        print(f"Filtering data for years between {time_range[0]} and {time_range[1]}")
        min_year, max_year = time_range
        filtered_df = filtered_df[
            (filtered_df["year"].astype(int) >= min_year)
            & (filtered_df["year"].astype(int) <= max_year)
        ]

    # Group by year
    grouped = filtered_df.groupby("year")[value_col].sum().reset_index()
    grouped["year"] = grouped["year"].astype(int)
    grouped = grouped.sort_values("year")

    # Rename value column for consistency
    grouped = grouped.rename(columns={value_col: "value"})

    return grouped


def get_state_time_series(
    df,
    state_name,
    value_col="total_ssbg_expenditures",
    service_categories=None,
    time_range=None,
):
    """
    Get time series data for a specific state

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    state_name : str
        Name of the state
    value_col : str
        Column to aggregate (ex.'total_ssbg_expenditures' or 'total_recipients')
    service_categories : list, optional
        List of service categories to filter by
    time_range : list or tuple, optional
        (min_year, max_year) to filter by

    Returns:
    --------
    pd.DataFrame with columns: year, value
    """
    filtered_df = df[df["state_name"] == state_name].copy()

    filtered_df["year"] = filtered_df["year"].astype(int)

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    if time_range:
        print(f"Filtering data for years between {time_range[0]} and {time_range[1]}")
        min_year, max_year = time_range
        filtered_df = filtered_df[
            (filtered_df["year"].astype(int) >= min_year)
            & (filtered_df["year"].astype(int) <= max_year)
        ]

    # Group by year
    grouped = filtered_df.groupby("year")[value_col].sum().reset_index()
    grouped["year"] = grouped["year"].astype(int)
    grouped = grouped.sort_values("year")

    # Rename value column for consistency
    grouped = grouped.rename(columns={value_col: "value"})

    return grouped


def get_map_data(df, metric="recipients", year=None, service_categories=None):
    """
    Get data for chloropleth map - state-level totals

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    metric : str
        'expenditures' or 'recipients'
    year : int
        Year to filter by
    service_categories : list, optional
        List of service categories to filter by

    Returns:
    --------
    pd.DataFrame with columns: state_name, value, total_ssbg_expenditures, ssbg_expenditures, tanf_transfer_funds,
    total_recipients, children, total_adults
    """
    filtered_df = df.copy()

    filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    # Group by state
    grouped = (
        filtered_df.groupby("state_name")
        .agg(
            {
                "total_ssbg_expenditures": "sum",
                "total_recipients": "sum",
                "ssbg_expenditures": "sum",
                "tanf_transfer_funds": "sum",
                "children": "sum",
                "total_adults": "sum",
            }
        )
        .reset_index()
    )

    if metric == "expenditures":
        grouped["value"] = grouped["total_ssbg_expenditures"]
    else:
        grouped["value"] = grouped["total_recipients"]

    return grouped


def get_state_service_breakdown(df, state_name, year=None):
    """
    Get service category breakdown for a state

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    state_name : str
        Name of the state
    year : int, optional
        Year to filter by

    Returns:
    --------
    pd.DataFrame with columns: service_category, expenditures, recipients
    """
    filtered_df = df[df["state_name"] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    grouped = (
        filtered_df.groupby("service_category")
        .agg({"total_ssbg_expenditures": "sum", "total_recipients": "sum"})
        .reset_index()
    )

    grouped.columns = ["service_category", "expenditures", "recipients"]

    # drop service categories with zero expenditures
    grouped = grouped[grouped["expenditures"] > 0]

    return grouped.sort_values("expenditures", ascending=False)


def get_state_full_data(df, state_name, year=None, service_categories=None):
    """
    Get full filtered dataset for a state (for data table)

    Parameters:
    -----------
    df : pd.DataFrame
        The SSBG dataframe
    state_name : str
        Name of the state
    year : int, optional
        Year to filter by
    service_categories : list, optional
        List of service categories to filter by

    Returns:
    --------
    pd.DataFrame with filtered data
    """
    filtered_df = df[df["state_name"] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df["year"].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df["service_category"].isin(service_categories)
        ]

    return filtered_df


def get_unique_values(df):
    """
    Get unique values for filters

    Returns:
    --------
    dict with 'years', 'states', 'service_categories',

    """
    return {
        "years": sorted([int(y) for y in df["year"].unique()]),
        "states": sorted(df["state_name"].unique().tolist()),
        "service_categories": sorted(df["service_category"].unique().tolist()),
    }
