# [SSBG Dashboard](https://dash-plotly-ssbg.onrender.com)

A Dash Plotly web app for visualizing Social Services Block Grant (SSBG) data from states.  
The application is currently hosted on render.com [SSBG Data Dashboard](https://dash-plotly-ssbg.onrender.com).

## Features

- **National Overview Page**
  - Summary cards with total expenditures and recipients
  - Interactive choropleth map of US states
  - Time series graphs for expenditures and recipients by service category
  - Filter controls for year range and service categories
  - Toggle between expenditures and recipients view on map
  - Data export functionality (CSV download)
  - Links to SSBG annual reports and resources

- **State Report Pages**
  - State-specific summary cards
  - Time series graphs for state expenditures and recipients
  - Service category breakdown (pie and bar charts)
  - Full data table with sorting
  - Data export functionality (CSV download)
  - Navigation back to national overview

## Installation

1. Install dependencies using `uv`:
```bash
# Install project dependencies
uv sync
```

2. Ensure your data file is located at `data/ssbg_data_cleaned.pkl`

## Running the Application

### Development
```bash
# Using uv (recommended)
uv run app.py
```

The application will be available at `http://localhost:8050`

### Production (with Gunicorn)
```bash
gunicorn app:server
```

## Deployment Thoughts

### Render.com

1. Connect your GitHub repository
  - In Render, click New → Web Service → Connect to GitHub and select this repository and branch.
2. Set the build command
  - Preferred (uv): `uv sync`
3. Set the start command
  - `gunicorn app:server`
4. Deploy
  - Create the service and click "Deploy Web Service” in Render. Subsequent pushes to the connected branch will trigger new builds.

### Plotly Cloud Free Tier
1. Create a new app on Plotly Cloud
2. Drag and Drop your Dash app code to upload
3. Configure by setting the python version
4. After building, set to public visibility

## Project Structure

```
Dash-Plotly-SSBG/
├── app.py                 # Main application entry point
├── pyproject.toml         # Project configuration and dependencies (uv)
├── uv.lock                # Locked dependency versions
├── Procfile              # Gunicorn configuration for deployment
├── runtime.txt           # Python version specification
├── utils/
│   └── data_loader.py    # Data loading and processing utilities
├── components/
│   ├── cards.py          # Reusable card components
│   ├── filters.py        # Filter control components
│   ├── graphs.py         # Graph components
│   └── map.py            # Choropleth map component
├── pages/
│   ├── national.py       # National overview page
│   └── state.py          # State report pages
└── assets/
    └── custom.css        # Custom CSS styling
```

## Data Format
The application expects a pandas DataFrame stored as a pickle file in data/ that looks like this currently:

```<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21240 entries, 0 to 21239
Data columns (total 15 columns):
 #   Column                           Non-Null Count  Dtype   
---  ------                           --------------  -----   
 0   year                             21240 non-null  category
 1   state_name                       21240 non-null  category
 2   line_num                         21240 non-null  category
 3   service_category                 21240 non-null  category
 4   ssbg_expenditures                21240 non-null  int64   
 5   tanf_transfer_funds              21240 non-null  int64   
 6   total_ssbg_expenditures          21240 non-null  int64   
 7   other_fed_state_and_local_funds  21240 non-null  int64   
 8   total_expenditures               21240 non-null  int64   
 9   children                         21240 non-null  int64   
 10  adults_59_and_younger            21240 non-null  int64   
 11  adults_60_and_older              21240 non-null  int64   
 12  adults_unknown                   21240 non-null  int64   
 13  total_adults                     21240 non-null  int64   
 14  total_recipients                 21240 non-null  int64   
dtypes: category(4), int64(11)
memory usage: 1.9 MB
```
