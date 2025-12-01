"""
Data loading and processing utilities for SSBG dashboard
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Union, Tuple, Any
from utils.constants import (
    COL_YEAR,
    COL_STATE,
    COL_SERVICE_CATEGORY,
    COL_TOTAL_SSBG_EXPENDITURES,
    COL_SSBG_EXPENDITURES,
    COL_TANF_TRANSFER,
    COL_TOTAL_RECIPIENTS,
    COL_CHILDREN,
    COL_ADULTS,
    COL_TOTAL_EXPENDITURES,
)

# Path to the data file
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "ssbg_data_cleaned.pkl"
)


def load_data() -> pd.DataFrame:
    """Load the SSBG data from pickle file"""
    return pd.read_pickle(DATA_PATH)


def get_national_totals(
    df: pd.DataFrame, year: Optional[int] = None, service_categories: Optional[List[str]] = None
) -> Dict[str, Union[int, float]]:
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
    dict with 'expenditures' and 'recipients' totals
    """
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    total_ssbg = int(filtered_df[COL_TOTAL_SSBG_EXPENDITURES].sum())
    total_exp = int(filtered_df[COL_TOTAL_EXPENDITURES].sum())
    
    return {
        "total_ssbg_expenditures": total_ssbg,
        "ssbg_expenditures": int(filtered_df[COL_SSBG_EXPENDITURES].sum()),
        "tanf_transfer_funds": int(filtered_df[COL_TANF_TRANSFER].sum()),
        "total_recipients": int(filtered_df[COL_TOTAL_RECIPIENTS].sum()),
        "children": int(filtered_df[COL_CHILDREN].sum()),
        "total_adults": int(filtered_df[COL_ADULTS].sum()),
        "total_expenditures": total_exp,
        "percent_total_ssbg_expenditures_of_total_expenditures": int(
            (total_ssbg / total_exp) * 100
        ) if total_exp > 0 else 0,
        "average_total_ssbg_expenditures": int(
            filtered_df.groupby(COL_YEAR)[COL_TOTAL_SSBG_EXPENDITURES].sum().mean()
        ),
        "average_total_recipients": int(
            filtered_df.groupby(COL_YEAR)[COL_TOTAL_RECIPIENTS].sum().mean()
        ),
        "average_ssbg_expenditures": int(
            filtered_df.groupby(COL_YEAR)[COL_SSBG_EXPENDITURES].sum().mean()
        ),
        "average_tanf_expenditures": int(
            filtered_df.groupby(COL_YEAR)[COL_TANF_TRANSFER].sum().mean()
        ),
        "average_child_recipients": int(
            filtered_df.groupby(COL_YEAR)[COL_CHILDREN].sum().mean()
        ),
        "average_adult_recipients": int(
            filtered_df.groupby(COL_YEAR)[COL_ADULTS].sum().mean()
        ),
    }


def get_state_totals(
    df: pd.DataFrame, state_name: str, year: Optional[int] = None, service_categories: Optional[List[str]] = None
) -> Dict[str, Union[int, float]]:
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
    dict with 'expenditures' and 'recipients' totals
    """
    filtered_df = df[df[COL_STATE] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    return {
        "num_service_categories": filtered_df[
            filtered_df[COL_TOTAL_SSBG_EXPENDITURES] > 0
        ][COL_SERVICE_CATEGORY].nunique(),
        "total_ssbg_expenditures": int(filtered_df[COL_TOTAL_SSBG_EXPENDITURES].sum()),
        "ssbg_expenditures": int(filtered_df[COL_SSBG_EXPENDITURES].sum()),
        "tanf_transfer_funds": int(filtered_df[COL_TANF_TRANSFER].sum()),
        "total_recipients": int(filtered_df[COL_TOTAL_RECIPIENTS].sum()),
        "children": int(filtered_df[COL_CHILDREN].sum()),
        "total_adults": int(filtered_df[COL_ADULTS].sum()),
        "total_expenditures": int(filtered_df[COL_TOTAL_EXPENDITURES].sum()),
        "average_total_ssbg_expenditures": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_TOTAL_SSBG_EXPENDITURES].sum().mean()
        ),
        "average_total_recipients": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_TOTAL_RECIPIENTS].sum().mean()
        ),
        "average_ssbg_expenditures": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_SSBG_EXPENDITURES].sum().mean()
        ),
        "average_tanf_expenditures": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_TANF_TRANSFER].sum().mean()
        ),
        "average_child_recipients": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_CHILDREN].sum().mean()
        ),
        "average_adult_recipients": int(
            filtered_df.groupby(COL_YEAR, observed=True)[COL_ADULTS].sum().mean()
        ),
    }


def get_time_series_data(
    df: pd.DataFrame,
    value_col: str = COL_TOTAL_SSBG_EXPENDITURES,
    service_categories: Optional[List[str]] = None,
    time_range: Optional[Tuple[int, int]] = None,
) -> pd.DataFrame:
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
    time_range : tuple, optional
        (min_year, max_year) to filter by

    Returns:
    --------
    pd.DataFrame with columns: year, service_category, value
    """
    filtered_df = df.copy()
    filtered_df[COL_YEAR] = filtered_df[COL_YEAR].astype(int)

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    if time_range:
        # print(f"Filtering data for years between {time_range[0]} and {time_range[1]}")
        min_year, max_year = time_range
        filtered_df = filtered_df[
            (filtered_df[COL_YEAR].astype(int) >= min_year)
            & (filtered_df[COL_YEAR].astype(int) <= max_year)
        ]

    # Group by year
    grouped = filtered_df.groupby(COL_YEAR)[value_col].sum().reset_index()
    grouped[COL_YEAR] = grouped[COL_YEAR].astype(int)
    grouped = grouped.sort_values(COL_YEAR)

    # Rename value column for consistency
    grouped = grouped.rename(columns={value_col: "value"})

    return grouped


def get_state_time_series(
    df: pd.DataFrame,
    state_name: str,
    value_col: str = COL_TOTAL_SSBG_EXPENDITURES,
    service_categories: Optional[List[str]] = None,
    time_range: Optional[Tuple[int, int]] = None,
) -> pd.DataFrame:
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
    filtered_df = df[df[COL_STATE] == state_name].copy()

    filtered_df[COL_YEAR] = filtered_df[COL_YEAR].astype(int)

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    if time_range:
        # print(f"Filtering data for years between {time_range[0]} and {time_range[1]}")
        min_year, max_year = time_range
        filtered_df = filtered_df[
            (filtered_df[COL_YEAR].astype(int) >= min_year)
            & (filtered_df[COL_YEAR].astype(int) <= max_year)
        ]

    # Group by year
    grouped = filtered_df.groupby(COL_YEAR, observed=True)[value_col].sum().reset_index()
    grouped[COL_YEAR] = grouped[COL_YEAR].astype(int)
    grouped = grouped.sort_values(COL_YEAR)

    # Rename value column for consistency
    grouped = grouped.rename(columns={value_col: "value"})

    return grouped


def get_map_data(
    df: pd.DataFrame,
    metric: str = "recipients",
    year: Optional[int] = None,
    service_categories: Optional[List[str]] = None,
) -> pd.DataFrame:
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

    filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    # Group by state
    grouped = (
        filtered_df.groupby(COL_STATE, observed=True)
        .agg(
            {
                COL_TOTAL_SSBG_EXPENDITURES: "sum",
                COL_TOTAL_RECIPIENTS: "sum",
                COL_SSBG_EXPENDITURES: "sum",
                COL_TANF_TRANSFER: "sum",
                COL_CHILDREN: "sum",
                COL_ADULTS: "sum",
            }
        )
        .reset_index()
    )

    if metric == "expenditures":
        grouped["value"] = grouped[COL_TOTAL_SSBG_EXPENDITURES]
    else:
        grouped["value"] = grouped[COL_TOTAL_RECIPIENTS]

    return grouped


def get_state_service_breakdown(
    df: pd.DataFrame, state_name: str, year: Optional[int] = None
) -> pd.DataFrame:
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
    filtered_df = df[df[COL_STATE] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    grouped = (
        filtered_df.groupby(COL_SERVICE_CATEGORY, observed=True)
        .agg({COL_TOTAL_SSBG_EXPENDITURES: "sum", COL_TOTAL_RECIPIENTS: "sum"})
        .reset_index()
    )

    grouped.columns = [COL_SERVICE_CATEGORY, "expenditures", "recipients"]

    # drop service categories with zero expenditures
    grouped = grouped[grouped["expenditures"] > 0]

    return grouped.sort_values("expenditures", ascending=False)


def get_state_full_data(
    df: pd.DataFrame, state_name: str, year: Optional[int] = None, service_categories: Optional[List[str]] = None
) -> pd.DataFrame:
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
    filtered_df = df[df[COL_STATE] == state_name].copy()

    if year:
        filtered_df = filtered_df[filtered_df[COL_YEAR].astype(int) == year]

    if service_categories:
        filtered_df = filtered_df[
            filtered_df[COL_SERVICE_CATEGORY].isin(service_categories)
        ]

    return filtered_df


def get_unique_values(df: pd.DataFrame) -> Dict[str, List[Any]]:
    """
    Get unique values for filters

    Returns:
    --------
    dict with 'years', 'states', 'service_categories',

    """
    return {
        "years": sorted([int(y) for y in df[COL_YEAR].unique()]),
        "states": sorted(df[COL_STATE].unique().tolist()),
        "service_categories": sorted(df[COL_SERVICE_CATEGORY].unique().tolist()),
    }
