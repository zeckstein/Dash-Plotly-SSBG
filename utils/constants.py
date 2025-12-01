"""
Constants for the SSBG Dashboard
"""

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

# Reverse mapping
STATE_NAME = {v: k for k, v in STATE_ABBREV.items()}

# Column Names
COL_YEAR = "year"
COL_STATE = "state_name"
COL_LINE_NUM = "line_num"
COL_SERVICE_CATEGORY = "service_category"
COL_TOTAL_SSBG_EXPENDITURES = "total_ssbg_expenditures"
COL_SSBG_EXPENDITURES = "ssbg_expenditures"
COL_TANF_TRANSFER = "tanf_transfer_funds"
COL_TOTAL_RECIPIENTS = "total_recipients"
COL_CHILDREN = "children"
COL_ADULTS = "total_adults"
COL_TOTAL_EXPENDITURES = "total_expenditures"
COL_OTHER_FED_STATE_LOCAL = "other_fed_state_and_local_funds"
COL_ADULTS_59_AND_YOUNGER = "adults_59_and_younger"
COL_ADULTS_60_AND_OLDER = "adults_60_and_older"
COL_ADULTS_UNKNOWN = "adults_unknown"

# Display Names
DISPLAY_NAMES = {
    COL_YEAR: "Year",
    COL_STATE: "State",
    COL_LINE_NUM: "Line Number",
    COL_SERVICE_CATEGORY: "Service Category",
    COL_SSBG_EXPENDITURES: "SSBG Expenditures",
    COL_TANF_TRANSFER: "TANF Transfer Funds",
    COL_TOTAL_SSBG_EXPENDITURES: "Total SSBG Expenditures",
    COL_OTHER_FED_STATE_LOCAL: "All Other Federal/State/Local Funds",
    COL_TOTAL_EXPENDITURES: "Total Expenditures",
    COL_CHILDREN: "Children Served",
    COL_ADULTS_59_AND_YOUNGER: "Adults 59 and Younger Served",
    COL_ADULTS_60_AND_OLDER: "Adults 60 and Older Served",
    COL_ADULTS_UNKNOWN: "Adults Unknown Age Served",
    COL_ADULTS: "Total Adults Served",
    COL_TOTAL_RECIPIENTS: "Total Recipients Served",
}

# Colors (matching CSS)
COLOR_PRIMARY = "rgb(51, 106, 144)"
COLOR_SECONDARY = "rgb(90, 169, 230)"
COLOR_TERTIARY = "rgb(212, 136, 41)"
