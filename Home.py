# ────────────────────────────────
# Set Up
# ────────────────────────────────

# Libraries
import streamlit as st
import base64

# Page configuration
st.set_page_config(page_title="Weather‑Driven Renewable Energy Insights", layout="wide")





# ────────────────────────────────
# Home-Page-Specific Helper function
# ────────────────────────────────

# The function reads the picture on my computer (locally) by opening it in binary mode, the binary bytes of the PNG picture are re‑encoded with a 64‑character alphabet, and the result is a string of text. 
# This facilitates the display of the image when the web app is run locally.
def _local_img_as_base64(file_path: str) -> str:
    """Return a local image as base64 string (fallbacks gracefully if file missing)."""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Background image '{file_path}' not found. Place it next to app.py.")
        return ""





# ────────────────────────────────
# Styling / Sections
# ────────────────────────────────

BG_IMAGE = "Test_power_pic.png"  # store the file name into BG_IMAGE
bg_base64 = _local_img_as_base64(BG_IMAGE) # convert that picture in base-64 using the helper function created above

# Recall you need to include CSS comments within the following signs:  /* xxx */
st.markdown(
    f"""
    <style>
    /* ───────── Hero banner ───────── */
    .hero {{
        position: relative;
        width: 100%;
        height: 55vh;
        background: url('data:image/png;base64,{bg_base64}') center center / cover no-repeat;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .hero h1 {{ /* white headline on the banner */
        color: #ffffff;
        font-size: 3.2rem;
        text-align: center;
        text-shadow: 1px 1px 6px rgba(0,0,0,0.8);
        margin: 0;
    }}

    /* ───────── Typography ───────── */
    .block-container h3 {{ font-size: 1.80rem; }}
    .block-container p,
    .block-container li {{
        font-size: 1.40rem;
        line-height: 1.70;
    }}
    .block-container ul {{ margin-left: 1.25rem; }}

    /* Remove Streamlit badge entirely */
    footer, footer * {{ display: none !important; }}

    /* ───────── Custom footer ───────── */
    .custom-footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        padding: 0.4rem 0.8rem;
        font-size: 0.9rem;
        /* transparent background so it blends with light & dark themes */
        background: transparent;
        z-index: 9999;
        text-align: center;
        /* text colour adapts to Streamlit theme; falls back to mid-grey */
        color: var(--text-color, #666666);
    }}
    .custom-footer a,
    .custom-footer strong {{
        color: inherit !important;       /* inherit colour in both modes */
        text-decoration: none;
    }}
    .custom-footer a:hover {{ text-decoration: underline; }}
    </style>
    """,
    unsafe_allow_html=True,
)





# ────────────────────────────────
# Hero (applying CSS design to the content through HTML)
# ────────────────────────────────

st.markdown(
    """
    <div class="hero">
        <h1>Weather‑Driven Renewable Energy Insights: Sion, Switzerland</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("\n")  # Add a blank space below the hero for better separation of both sections




# ────────────────────────────────
# Content
# ────────────────────────────────

with st.container(): # create logical box for markdown of content section
    st.markdown("### Project Overview")

    st.markdown(
        """
        This web application explores weather dynamics in Sion, Switzerland, and their impact on the theoretical productivity of solar, hydro, and wind energy sources.

        It is structured in two sections:

        1. **Weather Explorer**  
           Offers an interactive analysis of various weather metrics over a full year of data, starting from March 20, 2024.  
           Users are encouraged to experiment with time ranges, smoothing methods, and variable filters to gain an intuition of seasonal weather behavior.  
           _Note: The year 2024 was particularly humid in Sion, and findings are not meant to represent year‑on‑year norms._

        2. **Renewable Energy Insights**  
           Compares the theoretical generation potential of solar, hydro, and wind power.  
           While Sion’s infrastructure limits large‑scale deployment, the city acts as a practical *weather proxy* for the *canton of Valais*, selected for its varied renewable assets and role in *Switzerland’s Energy Strategy 2050*.  
           The approach presented here can be adapted to other regions and lays the foundation for balancing energy gaps across complementary sources.
        """
    )

# ────────────────────────────────
# Footer (again applying CSS through HTML)
# ────────────────────────────────

st.markdown(
    """
    <div class="custom-footer">
        <strong>Author:</strong> Alexandre Dore<br>
        <a href="https://github.com/Guiso079" target="_blank">GitHub Profile</a>
    </div>
    """,
    unsafe_allow_html=True,
)
