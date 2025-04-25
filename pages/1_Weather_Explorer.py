# ────────────────────────────────
# Set Up
# ────────────────────────────────

# Load libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

# Import constants and helper functions from the app utilities folder
from app_utils import (
    load_data,
    filter_by_period,
    build_smoothed_var_names,
    make_label_map,
    VARS_MAP,
    SMOOTH_SUFFIX,
    TIME_RANGES,
    MONTHS,
    SEASONS,
)

# Browser tab title + page title (on page itself)
st.set_page_config(page_title= "Sion Weather Analysis", layout="wide")
st.title("Weather Variable Trends for Sion, Switzerland")

# Load our data
weather_df = load_data()

# Contextual information to better understand the following analysis.
st.markdown("---")
st.subheader("Weather Explorer – Variable Definitions")
st.markdown("""
- **Air Temperature (°C):** Air temperature measured 2 m above ground.

- **Relative Humidity (%):** Ratio of water vapor in the air  to how much water vapour the air could potentially contain at a given temperature, measured 2 m above ground.

- **Hourly Rainfall (mm):** Total liquid precipitation over the previous 60 minutes.

- **Hourly Snowfall (cm):** Total snow depth accumulated in the past hour.  
  *(To convert to water equivalent in mm, divide by 7.)*

- **Hourly Precipitation (mm):** Combined rain + snow water equivalent in the previous hour.

- **Cloud Cover (%):** Percentage of sky obscured by clouds (0 = clear, 100 = overcast).

- **Shortwave Irraadience (W/m²):** Average short-wave solar radiation on a horizontal surface over the past hour. Equal to Global Horizontal Irradiation.

- **10 m Wind Speed (m/s):** Airflow velocity measured 10 m above ground (standard meteorological height).

> **Note on Normalisation:** When “normalise” options are turned on, min-max scaling (0 to 1) is applied to compare variables with different units without altering their overall distribution shape.

> **Note on Smoothing Levels:** Each variable is available in three temporal resolutions:

>   - *Hourly:* raw values

>   - *Weekly:* 168-hour moving average

>   - *Monthly:* 30-day moving average

""")










# ────────────────────────────────
# Summary Statistics Table
# ────────────────────────────────

st.markdown("---")
st.sidebar.header("Summary Table Settings")



# 1) Time-range selector, filtering and period labels for dynamic header
stats_duration = st.sidebar.selectbox(
    "Summary stats time range:", TIME_RANGES,
    key="stats_duration"
)
month = season = None
if stats_duration == "One Month":
    month = st.sidebar.selectbox(
        "Choose month:", MONTHS,
        format_func=lambda m: calendar.month_name[m],
        key="stats_month"
    )
    stats_period = calendar.month_name[month]

elif stats_duration == "One Season":
    season = st.sidebar.selectbox(
        "Choose season:", SEASONS,
        key="stats_season"
    )
    stats_period = season

else:
    stats_period = "Full Year"

df_stats = filter_by_period(weather_df, stats_duration, month, season)



# 2) Smoothing selector
stats_smooth = st.sidebar.selectbox(
    "Smoothing level:", list(SMOOTH_SUFFIX.keys()),
    key="stats_smooth"
)



# 3) Append the relevant suffixes based on selected smoothing
summary_cols = build_smoothed_var_names(list(VARS_MAP.keys()),stats_smooth)



# 4) Compute statistics
summary_stats = df_stats[summary_cols].agg(["min", "max", "mean", "median", "std"]).T
summary_stats.columns = ["Min", "Max", "Mean", "Median", "Standard Deviation"]



# 5) Replace each row index (table's row names) with its more user-friendly version (e.g. Temperature instead of temperature_2m)
summary_stats.index = list(VARS_MAP.keys())



# 6) Display
st.subheader(f"{stats_smooth} Summary Statistics ({stats_period})")
st.dataframe(summary_stats.style.format("{:.2f}"))










# ────────────────────────────────
# Correlation Matrix 
# ────────────────────────────────

st.markdown("---")
st.sidebar.markdown("---")  
st.sidebar.header("Correlation Settings")



# 1) Time-range selector and filtering options based on time range
# selectbox to choose the desired time range
corr_duration = st.sidebar.selectbox(
    "Time range:", TIME_RANGES, key="corr_duration"
)
month = season = None
if corr_duration == "One Month":
    month = st.sidebar.selectbox(
        "Choose month:", MONTHS,
        format_func=lambda m: calendar.month_name[m],
        key="corr_month"
    )
    corr_period = calendar.month_name[month]

elif corr_duration == "One Season":
    season = st.sidebar.selectbox(
        "Choose season:", SEASONS,
        key="corr_season"
    )
    corr_period = season

else:
    corr_period = "Full Year"

# Apply the same filtering helper as in Time Series Analysis section
df_corr = filter_by_period(weather_df, corr_duration, month, season)



# 2) Correlation smoothing selector
corr_smooth = st.sidebar.selectbox(
    "Correlation smoothing:", list(SMOOTH_SUFFIX.keys()), key="corr_smooth"
)



# 3) Append the right suffix to each "raw" column name based on selected smoothing level
cols_corr = build_smoothed_var_names(list(VARS_MAP.keys()), corr_smooth)



# 4) Compute correlation matrix
corr_df = df_corr[cols_corr].corr()



# 5) Display with dynamic header
st.subheader(f"{corr_smooth} Correlation Matrix ({corr_period})")
fig_corr = px.imshow(
    corr_df,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r",
    origin="lower",
)
fig_corr.update_layout(margin=dict(t=30, b=0, l=0, r=0))
st.plotly_chart(fig_corr, use_container_width=True)











# ────────────────────────────────
# Time Series Analysis
# ────────────────────────────────

# Sidebar controls
st.markdown("---")  
st.sidebar.markdown("---")  
st.sidebar.header("Time Series Settings")



# 1) Select which variables to plot

# Button to select the variables in the side bar, with temperature and humidity as the two default vars to be plotted.
sel_vars = st.sidebar.multiselect(
    "Time Series Variables:", list(VARS_MAP.keys()), default=["Temperature", "Humidity"], key="ts_vars"
)



# 2) Time‐range selector + filtering
duration = st.sidebar.selectbox(
    "Time range:", TIME_RANGES, key="ts_duration"
)

month = season = None
if duration == "One Month":
    month = st.sidebar.selectbox(
        "Choose month:", MONTHS,
        format_func=lambda m: calendar.month_name[m],
        key="ts_month"
    )
    time_series_period = calendar.month_name[month] # this will be used to make a dynamic section header 

elif duration == "One Season":
    season = st.sidebar.selectbox(
        "Choose season:",SEASONS,
        key="ts_season"
    )
    time_series_period = season

else:
    time_series_period = "Full Year"

# Slice the df based on the time period that was just selected by the app user (specific month or season)
df_ts = filter_by_period(weather_df, duration, month, season) 
# In the “Full Year” case, the month and season remain None, so you automatically get an unfiltered copy of the full dataset without needing a separate condition for “Full Year.”. 
# aka no need for: else:
    # df_ts = weather_df.copy()



# 3) Buttons to let the web app user select the data's smoothing level, as well as which variables they want to plot
smooth = st.sidebar.selectbox("Time Series Smoothing:", list(SMOOTH_SUFFIX.keys()),key="ts_smooth")

# Depending on the smoothing choice, append the right suffix to each "raw" column name
cols = build_smoothed_var_names(sel_vars, smooth)


# 4) Prepare data for plotting
df_plot = (
    df_ts[cols] # keep only the user-selected variables, at the right smoothing level (to avoid modifying the initial variables, which I might need later on)
    .rename_axis("time") # Assign DatetimeIndex a column name so reset_index doesn't create an index column
    .reset_index() # convert index to df column, as need time to be a column to use melt and reshape the df
    .melt(id_vars="time", value_vars=cols, var_name="col", value_name="val") # transform from wide to long format, as required by plotly.
)
# Map back to friendlier variable names so that chart labels don't have complicated names but the simplified variables names
df_plot["Variable"] = df_plot["col"].map(make_label_map(sel_vars, smooth))



# 5) Optional min-max normalisation for better comparison of variables along time series : a value of 0.6 means that it is 60% of the range between the var's min and max values
# Min-max is good because it keeps that shape of the original time-series intact, so good to identify when a variable peaks etc. We're not interested in z-score standardisation because we're not that interested in how far values deviate from their mean and anomaly detection. 
if st.sidebar.radio("Normalise?", ["No", "Yes"]) == "Yes":
    df_plot["val"] = (
        df_plot
        .groupby("Variable")["val"] # We want each variable to be normalised against itself, not all others.
        .transform(lambda x: (x - x.min()) / (x.max() - x.min())) # min-max normalisation formula
    )
    y_label = "Normalised"
else:
    y_label = "Value"



# 6) Section header and line chart plotting
st.subheader(f"{smooth}{' Normalised' if y_label=='Normalised' else ''} Weather Trends ({time_series_period})")

# Plotting
fig = px.line(
    df_plot,
    x="time",
    y="val",
    color="Variable",
    labels={"time": "Time", "val": y_label},
)
fig.update_layout(legend=dict(y=0.5, x=1.02))
st.plotly_chart(fig, use_container_width=True)










# ────────────────────────────────
# Weather Variable Distribution Plot
# ────────────────────────────────
st.sidebar.markdown("---")  
st.sidebar.header("Histogram Settings")



# 1) Selecting the variable to plot on the histogram (so the user knows straight up what it is they are filtering afterwards)
hist_var = st.sidebar.selectbox(
    "Histogram variable:",
    list(VARS_MAP.keys()),
    index=list(VARS_MAP.keys()).index("Temperature"), # Make temperature the default variable to plot
    key="hist_var"
)



# 2) Histogram time‑range selector, filtering of the data frame by time periods, and period labelling for dynamic section header
hist_duration = st.sidebar.selectbox(
    "Histogram time range:", TIME_RANGES,
    key="hist_duration"
)

month = season = None
if hist_duration == "One Month":
    month = st.sidebar.selectbox(
        "Choose month:", MONTHS,
        format_func=lambda m: calendar.month_name[m],
        key="hist_month"
    )
    hist_period = calendar.month_name[month]

elif hist_duration == "One Season":
    season = st.sidebar.selectbox(
        "Choose season:", SEASONS,
        key="hist_season"
    )
    hist_period = season

else:
    hist_period = "Full Year"

# Apply the same filtering helper as before
df_hist = filter_by_period(weather_df, hist_duration, month, season)



# 3) Histogram smoothing-level selector
hist_smooth = st.sidebar.selectbox(
    "Histogram smoothing:", list(SMOOTH_SUFFIX.keys()),
    key="hist_smooth"
)



# 4) Append the appropriate suffix (if any) to build the column names corresponding to the smoothing option selected by the wep app user. 
hist_col = build_smoothed_var_names([hist_var], hist_smooth)[0] # select first (and only) element from the list created by fn.



# 5) Filter the histogram by another variable, if requested 

# Toggle on/off
filter_on = st.sidebar.checkbox(
    "Filter histogram by another variable?",
    key="hist_filter_on"
)
if filter_on:
    # Choose what variable we are filtering by
    filt_var = st.sidebar.selectbox(
        "Optional filter variable:",
        [v for v in VARS_MAP if v != hist_var],
        key="hist_filter_var"
    )
    # Its smoothig level 
    filt_smooth = st.sidebar.selectbox(
        "Filter smoothing:",
        list(SMOOTH_SUFFIX.keys()),
        key="hist_filter_smooth"
    )
    # Build the variable's raw column name (adding suffix) and find its data range
    filt_col = VARS_MAP[filt_var] + SMOOTH_SUFFIX[filt_smooth]
    raw_min, raw_max = float(df_hist[filt_col].min()), float(df_hist[filt_col].max())
    sel_min, sel_max = st.sidebar.slider( # Let the user pick a range *in the variable's units* to filter on 
        f"{filt_var} range ({filt_smooth}):",
        min_value=raw_min,
        max_value=raw_max,
        value=(raw_min, raw_max), # make full span of the filter variable the default position for slider 
        step=(raw_max - raw_min) / 100, # increments of the slider filter
        key="hist_filter_range"
    )
    # Apply the filter
    df_hist = df_hist[(df_hist[filt_col] >= sel_min) & (df_hist[filt_col] <= sel_max)]



# 6) Plot the histogram and create dashboard section (NB: vars cannot be normalised as not relevant when plotting single var)
st.markdown("---") # add a seperator between this section and the previous one
st.subheader(f"{hist_smooth} Distribution of {hist_var} ({hist_period})") # dynamic dashboard title

# Adapt bin count to filtered size
n = len(df_hist)
nbins = max(5, min(50, n // 10))

fig_hist = px.histogram(
    df_hist,
    x=hist_col,
    nbins=nbins,
    title= None # Not including any plot title directly for now, as I find the subsection title informative enough
)
fig_hist.update_layout(
    xaxis_title=hist_var,
    yaxis_title="Frequency",
    bargap=0.1
)
st.plotly_chart(fig_hist, use_container_width=True)












