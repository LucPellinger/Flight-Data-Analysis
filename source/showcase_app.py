import streamlit as st
from flightclass.flight import FlightData
import streamlit.components.v1 as components
import os
import pandas as pd
from openai import RateLimitError, AuthenticationError
import base64
from pathlib import Path


def get_base64_asset(relative_path: str) -> str:
    """Read an image from the package and return base64-encoded string."""
    abs_path = Path(__file__).parent / "assets" / relative_path
    with open(abs_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load both images
colorful_bg = get_base64_asset("background_colorful.png")
plain_bg = get_base64_asset("background_softgrey.png")

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Initialize class only once
@st.cache_resource
def get_flight_data():
    if "flight_data" not in st.session_state:
        with st.spinner("Loading flight data... This may take a few moments."):
            st.session_state.flight_data = FlightData()
    return st.session_state.flight_data


st.set_page_config(page_title="Flight Data Explorer", layout="wide")

# header text
st.markdown(
    "<h1 style='padding-top: 1rem; margin-top: 1rem;'>✈️ Flight Data Explorer</h1>",
    unsafe_allow_html=True
)

# Toggle between background modes
st.expander("🖼️ Background Options", expanded=False)
with st.expander("Background Options", expanded=False):
    st.markdown(
        """
        <style>
            .stExpanderHeader {
                font-size: 1.2rem;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Toggle for colorful background
    use_colorful = st.toggle("🎨 Use colorful background", value=True)

    # Choose background based on toggle
    selected_bg = colorful_bg if use_colorful else plain_bg 

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{selected_bg}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        header {{
            background-color: transparent !important;
            background-size: cover !important;
            box-shadow: none !important; /* optional: remove drop shadow */
            background-position: center !important;
            background-repeat: no-repeat !important;
        }}

        .block-container {{
            background-color: rgba(255, 255, 255, 0.80);
            padding: 2rem;
            border-radius: 10px;
        }}

        .block-container {{
            padding-top: 1rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Define tabs
tabs = st.tabs([
    "🔑 API Setup",
    "Overview", 
    "Airports Map", 
    "Airport Flights", 
    "Top Airplane Models", 
    "Flight Distance Analysis", 
    "Country Flights & CO₂", 
    "🔒 Aircraft Explorer", 
    "🔒 Airport Explorer"
])

# API Setup Tab
with tabs[0]:
    st.header("🔐 Enter Your OpenAI API Key")
    st.markdown("""
    This app uses OpenAI to retrieve information about aircraft and airports.  
    Please enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below to use 🔒 features.
    """)
    api_key_input = st.text_input("OpenAI API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        os.environ["OPENAI_API_KEY"] = api_key_input  # Temporary for this session
        st.success("API key saved for this session.")
    elif not st.session_state.api_key:
        st.warning("You must enter an API key to use certain features.")

# Overview Tab
with tabs[1]:
    st.header("📊 Dataset Overview")
    flight_data = get_flight_data()
    st.subheader("Airlines")
    st.dataframe(flight_data.airlines_df.head())
    st.subheader("Airplanes")
    st.dataframe(flight_data.airplanes_df.head())
    st.subheader("Airports")
    st.dataframe(flight_data.airports_df.head())
    st.subheader("Routes")
    st.dataframe(flight_data.routes_df.head())

# Airports Map Tab
with tabs[2]:
    st.header("🗺️ Airports in a Country")
    flight_data = get_flight_data()
    country = st.selectbox("Select a country", flight_data.airports_df["Country"].unique(), key="airport_map")
    try:
        m = flight_data.plot_airports(country)
        components.html(m._repr_html_(), height=600)
    except ValueError as e:
        st.error(str(e))

# Airport Flights Tab
with tabs[3]:
    st.header("🛫 Flights from an Airport")
    flight_data = get_flight_data()
    code = st.selectbox("Choose IATA Airport Code", flight_data.airports_df["IATA"].dropna().unique(), key="airport_flights")
    internal = st.checkbox("Only internal flights?", value=False)
    map_ = flight_data.plot_airport_flights(code, internal=internal)
    if map_:
        components.html(map_._repr_html_(), height=600)

# Top Models Tab
with tabs[4]:
    st.header("🛩️ Top Airplane Models")
    flight_data = get_flight_data()

    # Layout: left column for controls, right column for the plot
    col1, col2 = st.columns([1, 3])  # Adjust the width ratio as needed
    with col1:    
        top_n = st.slider("Number of top models", 5, 20, 10)
        st.markdown("Optionally filter by country")
        countries = st.multiselect("Select countries", flight_data.airports_df["Country"].unique(), default=["Canada", "United States", "Germany", "Portugal"])
    with col2:
        try:
            fig = flight_data.plot_top_models(countries=countries if countries else None, top_n=top_n)
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
        except ValueError as e:
            st.error(str(e))

# Distance Analysis Tab
with tabs[5]:
    st.header("📏 Distribution of Flight Distances")
    flight_data = get_flight_data()
    fig = flight_data.distance_analysis()
    fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig)

# Country Flights & CO2 Tab
with tabs[6]:
    st.header("🌍 Country Flight Map & CO₂ Emissions")
    flight_data = get_flight_data()
    country = st.selectbox("Select a country", flight_data.airports_df["Country"].unique(), key="co2_map")
    internal = st.checkbox("Only internal flights?", value=False, key="co2_internal")
    threshold = st.slider("Short-haul threshold (km)", 100, 2000, 1000)
    m = flight_data.plot_country_flights(country, threshold=threshold, internal=internal)
    components.html(m.get_root().render(), height=600, scrolling=True)

# Aircraft Explorer Tab
with tabs[7]:
    st.header("🛫 Aircraft Explorer")
    if not st.session_state.get("api_key"):
        st.warning("Please enter your OpenAI API key in the API Setup tab first.")
    else:
        try:
            flight_data = get_flight_data()
            aircrafts = flight_data.aircrafts()
            selected_aircraft = st.selectbox("Choose an aircraft", aircrafts)
            st.markdown("Fetching info from ChatOpenAI...")
            flight_data.aircraft_info(selected_aircraft)
        except RateLimitError:
            st.error("❌ You've hit your OpenAI rate limit or quota. Please check your usage.")
        except AuthenticationError:
            st.error("❌ Authentication error. Please check your OpenAI API key.")


# Airport Explorer Tab
with tabs[8]:
    st.header("🏙️ Airport Explorer")
    if not st.session_state.get("api_key"):
        st.warning("Please enter your OpenAI API key in the API Setup tab first.")
    else:
        try:
            flight_data = get_flight_data()
            airports = flight_data.airports()
            selected_aircraft = st.selectbox("Choose an airport", airports)
            st.markdown("Fetching info from ChatOpenAI...")
            flight_data.airport_info(selected_aircraft)
        except RateLimitError:
            st.error("❌ You've hit your OpenAI rate limit or quota. Please check your usage.")
        except AuthenticationError:
            st.error("❌ Authentication error. Please check your OpenAI API key.")
