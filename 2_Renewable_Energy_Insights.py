# ────────────────────────────────
# Set up
# ────────────────────────────────

# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

# Import constants and helper functions from the app utilities file
from app_utils import (
    load_data,
    build_renewable_cols,
    filter_by_period,
    RENEW_MAP,
    SMOOTH_SUFFIX,
    TIME_RANGES, MONTHS, SEASONS,
)

# Page configuration
st.set_page_config(page_title="Renewable Potential", layout="wide")
st.title("Renewable Energy Potential in Sion, Switzerland")

# Load our data
weather_df = load_data()

# Contextual information to better understand the following analysis.
st.markdown("---")
st.subheader("Renewable Energy Insights – Variable Definitions")
st.markdown("""
- **Solar Power Potential:** Shortwave radiation (W/m²) is used as a proxy for solar energy. This variable reflects the global horizontal irradiance (GHI), which is a key determinant of photovoltaic output, especially for rooftop solar panels installed at a fixed horizontal angle.

- **Wind Power Potential:** We approximate wind energy potential using the cube of wind speed at 10 meters above ground. This follows the standard wind power formula: power = 1/2*(rhoAV^3), where rho is air density, A the area sweapt by the air turbine, and V^3 is the cubed wind velocity.

- **Hyro Power Potential:** Measuring true hydropower potential would require detailed models of snowmelt, runoff, and water storage, which are beyond the scope of this project. Instead, we focus on run-of-river hydropower, which is more directly influenced by recent precipitation. Given that snow in Sion is expected to melt within 24 hours, and that runoff takes time to reach river systems, we use the sum of meaningful precipitation (≥1mm) in the preceding 24 hours as a proxy. While a simplification, it reflects short-term water availability that could influence electricity generation in run-of-river plants.


> **Note 1:** Since raw proxies – like cubed wind speed – don’t translate directly to absolute power potential without unavailable, energy specific factors, only normalised values are presentend. Thus, all series are min-max scaled to [0, 1] for comparison of relative temporal patterns.

> **Note 2:** Variables are available in three temporal resolutions (smoothing levels):

>   - *Hourly:* raw values

>   - *Weekly:* 168-hour moving average

>   - *Monthly:* 30-day moving average
""")










# ────────────────────────────────
# Sidebar Controls
# ────────────────────────────────
st.sidebar.header("Renewable Energy Potential Analysis Settings")

# 1) Time-range + period label + filtering
duration = st.sidebar.selectbox("Time range:", TIME_RANGES, key="ren_duration")
month = season = None
if duration == "One Month":
    month = st.sidebar.selectbox("Choose month:", MONTHS,
                                 format_func=lambda m: calendar.month_name[m],
                                 key="ren_month")
    period_label = calendar.month_name[month]
elif duration == "One Season":
    season = st.sidebar.selectbox("Choose season:", SEASONS, key="ren_season")
    period_label = season
else:
    period_label = "Full Year"

df_period = filter_by_period(weather_df, duration, month, season)

# 2) Smoothing selector
smooth = st.sidebar.selectbox(
    "Smoothing level:", list(SMOOTH_SUFFIX.keys()), key="ren_smooth"
)

# Build columns for all three potentials (which will always all be shown in the correlation matrix and in the time series plot)
cols = build_renewable_cols(list(RENEW_MAP.keys()), smooth)





# ────────────────────────────────
# Correlation Matrix
# ────────────────────────────────
st.markdown("---")
st.subheader(f"{smooth} Correlation of Renewable Potentials ({period_label})")

corr_df = df_period[cols].corr()
fig_corr = px.imshow(
    corr_df,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    origin="lower",
)
fig_corr.update_layout(margin=dict(t=30, b=0, l=0, r=0))
st.plotly_chart(fig_corr, use_container_width=True)





# ────────────────────────────────
# Time Series Plot
# ────────────────────────────────
st.markdown("---")
st.subheader(f"{smooth} Normalised Renewable Potentials ({period_label})")

# 1) Build the column names for the three renewable energy potentials
cols = [
    RENEW_MAP[friendly] + SMOOTH_SUFFIX[smooth]
    for friendly in RENEW_MAP
]

# 2) Take just those columns for the selected period and min-max normalise to facilitate comparison in evolution of potentials
df_ts = df_period[cols].copy()
for col in cols:
    df_ts[col] = (df_ts[col] - df_ts[col].min()) / (df_ts[col].max() - df_ts[col].min())

# 3) Melt into long form for Plotly
df_plot = (
    df_ts
    .rename_axis("time")
    .reset_index()
    .melt(id_vars="time", value_vars=cols, var_name="col", value_name="val")
)

# 4) Map each full column name back to its friendly label (rather the extensive but complicated varibale name)
label_map = {
    RENEW_MAP[friendly] + SMOOTH_SUFFIX[smooth]: friendly
    for friendly in RENEW_MAP
}
df_plot["Variable"] = df_plot["col"].map(label_map)

# 5) Render the time series line chart
fig_ts = px.line(
    df_plot,
    x="time",
    y="val",
    color="Variable",
    labels={"time": "Time", "val": "Normalised"},
)
fig_ts.update_layout(legend=dict(y=0.5, x=1.02))
st.plotly_chart(fig_ts, use_container_width=True)




# ────────────────────────────────
# Seasonal Share of Total Annual Renewable Potential
# ────────────────────────────────
st.markdown("---")
st.subheader("Seasonal Share of Total Annual Renewable Potential")

# 1) Build the three hourly column names
hourly_cols = [RENEW_MAP[k] + SMOOTH_SUFFIX[smooth] for k in RENEW_MAP]

# 2) Sum them over each season (re‐ordering to Winter→Spring→Summer→Autumn)
seasonal_sum = (
    weather_df[hourly_cols]
    .groupby(weather_df["season"])
    .sum()
    .reindex(SEASONS)
)

# 3) Convert to share of the full‐year total for each source
seasonal_share = seasonal_sum.div(seasonal_sum.sum(), axis=1)

# Create a constant to go from the "raw" variable name to their user-friendly versions, used a figure legend (basically opposite as build_renewable_cols)
friendlier_vars_map = {
    RENEW_MAP[k] + SMOOTH_SUFFIX[smooth]: k
    for k in RENEW_MAP
}
seasonal_share = seasonal_share.rename(columns=friendlier_vars_map)

# 4) Plot grouped bar chart
fig_season = px.bar(
    seasonal_share,
    x=seasonal_share.index,
    y=list(friendlier_vars_map.values()),
    labels={"value":"Share of Annual Potential","season":"Season"},
    barmode="group",
)
fig_season.update_layout(
    yaxis_tickformat=".0%",
    xaxis_title="Season",
    legend_title_text="Source",
)
st.plotly_chart(fig_season, use_container_width=True)


