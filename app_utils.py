# This is a small collectoin of app utilities to speed up the development and improve the clarity of my web app code across pages.

# Load libraries
import pandas as pd
import calendar
import streamlit as st





# 1) Defining constants - these will be re-used multiple times and are centralised here (Don't repeat yourself / DRY principle)

# Map friendlier variable names to var's actual names in the data frame (basically UI). Use in weather overview. 
VARS_MAP = {
    "Temperature":      "temperature_2m",
    "Humidity":         "relative_humidity_2m",
    "Rain":             "rain",
    "Snowfall":         "snowfall",
    "Precipitation":    "precipitation",
    "Cloud Cover":      "cloudcover",
    "Solar Radiation":  "shortwave_radiation",
    "Wind Speed":       "windspeed_10m",
}
# The below will be used to apend the desired smoothing-level to variable's "base" name. Used in weather overview.
SMOOTH_SUFFIX = {
    "Hourly":    "",
    "Weekly MA": "_weekly_avg",
    "Monthly MA":"_month_avg",
}
# The following will be used to set up time-range filters in the sidebar. Use in both web app pages.
TIME_RANGES = ["One Month", "One Season", "Full Year"]
MONTHS      = list(range(1, 13))
SEASONS     = ["Winter", "Spring", "Summer", "Autumn"]

# Build constants for renewables, following similar pattern as above. Used in renewable energy potential file. 
RENEW_MAP = {
    "Solar Potential": "solar_potential",
    "Wind Potential":  "wind_potential",
    "Hydro Potential": "hydro_potential",
}





# 2) Create helper functions to make code in later sections more concise

# Enable users to select the specific time period they want to get data for, given their previously selected time range (if haven't selected full year). 
def filter_by_period(df, duration, month=None, season=None):
    if duration == "One Month":
        return df[df.index.month == month]
    elif duration == "One Season":
        return df[df["season"] == season]
    else:
        return df.copy()

# Append the correct suffix to variables' base name, as per the smoothing-level selected by the user. For weather overview file. 
def build_smoothed_var_names(selected_vars, smooth):
    return [VARS_MAP[v] + SMOOTH_SUFFIX[smooth] for v in selected_vars]

# Equivalent function to build_smoothed_var_names, but for the renewable potential variables instead of broader weather ones. 
def build_renewable_cols(selected_vars, smooth):
    return [RENEW_MAP[v] + SMOOTH_SUFFIX[smooth] for v in selected_vars] 

# Map variables' full name (including suffix) to more a user-friendly name, making chart labels more readable.
def make_label_map(selected_vars, smooth):
    return {
        VARS_MAP[v] + SMOOTH_SUFFIX[smooth]: v
        for v in selected_vars
    }

# Load the Data (essentially, you apply the fn. which reads the parquet file, transforms it into a pd data frame, and then caches the result so don't need to re-read the parquet file every time I run the script)
@st.cache_data
def load_data():
    df = pd.read_parquet("sion_weather_enriched.parquet")
    df.index = pd.to_datetime(df.index) # convert time stamp index into datetime object to enable future time-based slicing in figures
    return df
weather_df = load_data()

