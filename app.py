"""
Main Dash application for SSBG Dashboard
"""
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from pages import national, state
from utils.data_loader import load_data, get_unique_values
from urllib.parse import unquote

# Load data once at startup
df = load_data()
unique_vals = get_unique_values(df)

# Initialize Dash app with Bootstrap theme and custom CSS
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Custom CSS will be automatically loaded from assets/custom.css

# App layout with URL routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='state-name-store', data=None),
    html.Div(id='page-content')
])

# Callback to render the appropriate page based on URL
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Display the appropriate page based on URL"""
    if pathname is None or pathname == '/' or pathname == '':
        return national.layout()
    elif pathname.startswith('/state/'):
        # Extract state name from URL
        state_name = unquote(pathname.replace('/state/', ''))
        return state.layout(state_name)
    else:
        return national.layout()

# Callback to handle map clicks and navigate to state pages
@callback(
    Output('url', 'pathname'),
    Input('choropleth-map', 'clickData'),
    prevent_initial_call=True
)
def navigate_to_state(click_data):
    """Navigate to state page when state is clicked on map"""
    if click_data and 'points' in click_data and len(click_data['points']) > 0:
        # Get state abbreviation from click
        state_abbrev = click_data['points'][0]['location']
        
        # Map abbreviation back to state name
        from components.map import STATE_ABBREV
        reverse_map = {v: k for k, v in STATE_ABBREV.items()}
        state_name = reverse_map.get(state_abbrev)
        
        if state_name:
            # URL encode state name
            from urllib.parse import quote
            encoded_name = quote(state_name)
            return f'/state/{encoded_name}'
    
    return dash.no_update

# Callback to update state name store from URL
@callback(
    Output('state-name-store', 'data'),
    Input('url', 'pathname')
)
def update_state_name_from_url(pathname):
    """Extract state name from URL and store it"""
    if pathname and pathname.startswith('/state/'):
        state_name = unquote(pathname.replace('/state/', ''))
        return state_name
    return None

# Expose server for gunicorn
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

