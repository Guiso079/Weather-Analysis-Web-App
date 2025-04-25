## This web application explores weather dynamics in Sion, Switzerland, and their impact on the theoretical productivity of solar, hydro, and wind energy sources.

The web application is available at: https://weather-analysis-web-app-alexandredore.streamlit.app/

It is structured in two sections:

**Weather Explorer:**
Offers an interactive analysis of various weather metrics over a full year of data, starting from March 20, 2024.
Users are encouraged to experiment with time ranges, smoothing methods, and variable filters to gain an intuition of seasonal weather behavior.
Note: The year 2024 was particularly humid in Sion, and findings are not meant to represent year‑on‑year norms.

**Renewable Energy Insights:**
Compares the theoretical generation potential of solar, hydro, and wind power.
While Sion’s infrastructure limits large‑scale deployment, the city acts as a practical weather proxy for the canton of Valais, selected for its varied renewable assets and role in Switzerland’s Energy Strategy 2050.
The approach presented here can be adapted to other regions and lays the foundation for balancing energy gaps across complementary sources.

**Information on Repo Documents:**
- Data_Sourcing_Notebook: notebook used to source the data from https://open-meteo.com/en/docs/historical-weather-api, and perform data cleaning, checks, and enhancement. The resulting file is saved as sion_weather_enriched.parquet.
- App_utils: contains app utilities to speed up the development, detect dirty data, and improve the clarity of my web app code across pages.
- Home.py: code to design and set up the home page of the web app.
- 1_Weather_Explorer: code to design and set up the weather explorer page of the web app.
- 2_Renewable_Energy_Insights: code to design and set up the Renewable Energy Insights page of the web app.
