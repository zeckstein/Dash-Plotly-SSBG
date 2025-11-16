# SSBG Dashboard

A Dash Plotly web application for visualizing Social Services Block Grant (SSBG) data from states and territories.

## Features

- **National Overview Page**
  - Summary cards with total expenditures and recipients
  - Interactive chloropleth map of US states and territories
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

1. Connect GitHub repository
2. Set build command: `uv sync` (or `pip install -r requirements.txt` if using pip)
3. Set start command: `gunicorn app:server`
4. Deploy!


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
│   └── map.py            # Chloropleth map component
├── pages/
│   ├── national.py       # National overview page
│   └── state.py          # State report pages
└── assets/
    └── custom.css        # Custom CSS styling
```

## Data Format

The application expects a pandas DataFrame stored as a pickle file with the following columns:
- `year`: Year of the data
- `state_name`: Name of the state or territory
- `service_category`: Service category name
- `total_ssbg_expenditures`: Total SSBG expenditures amount
- `total_recipients`: Total number of recipients
- and more... see SSBG data repo for run down # TODO add data dict for download
