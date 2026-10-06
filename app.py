import streamlit as st
import pandas as pd
import pydeck as pdk
from pydantic import BaseModel, Field
from typing import List

# --- Pydantic Schema for Structured Itinerary Stops ---
class TravelStop(BaseModel):
    name: str = Field(description="Name of the place, restaurant, or activity")
    category: str = Field(description="Category: e.g., Scenic Stop, Family Attraction, Restaurant")
    latitude: float = Field(description="Latitude coordinate")
    longitude: float = Field(description="Longitude coordinate")
    rating: float = Field(description="User review rating out of 5.0")
    description: str = Field(description="Brief highlight of why this stop is recommended")

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="AI Travel Itinerary & Route Optimizer",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Agentic Travel Logistics & Route Optimizer")
st.markdown("Plan your road trip or vacation with dynamic duration adjustments, top-rated local restaurant and family activity backups, and interactive geospatial mapping.")

# --- Sidebar Configuration ---
st.sidebar.header("Trip Parameters")
origin = st.sidebar.text_input("Starting Location", "San Jose, CA")
destination = st.sidebar.text_input("Destination", "Los Angeles, CA")
trip_duration_days = st.sidebar.slider("Trip Duration (Days)", min_value=1, max_value=7, value=3)
interests = st.sidebar.multiselect(
    "Preferred Activities",
    ["Family Attractions", "Top-Rated Restaurants", "Scenic Viewpoints", "Outdoor Parks"],
    default=["Family Attractions", "Top-Rated Restaurants", "Scenic Viewpoints"]
)

api_key = st.sidebar.text_input("Mapbox / LLM API Key (Optional)", type="password")

if st.button("Generate Optimized Itinerary & Map", type="primary"):
    with st.spinner("Agentic workflow crawling travel databases, optimizing geographic routes, and scoring locations..."):
        
        # Simulated Route Stops and Recommendations (San Jose to Los Angeles corridor)
        mock_stops = [
            TravelStop(
                name="Monterey Bay Aquarium",
                category="Family Attraction",
                latitude=36.6183,
                longitude=-121.9012,
                rating=4.8,
                description="World-renowned aquarium featuring interactive marine exhibits for families."
            ),
            TravelStop(
                name="Phil's Fish Market",
                category="Restaurant",
                latitude=36.8005,
                longitude=-121.7871,
                rating=4.6,
                description="Legendary coastal seafood restaurant famous for cioppino and patio dining."
            ),
            TravelStop(
                name="Bixby Creek Bridge (Big Sur)",
                category="Scenic Stop",
                latitude=36.3714,
                longitude=-121.9018,
                rating=4.9,
                description="Iconic coastal bridge offering breathtaking Pacific Ocean photo opportunities."
            ),
            TravelStop(
                name="Hearst Castle",
                category="Family Attraction",
                latitude=35.6852,
                longitude=-121.1663,
                rating=4.7,
                description="Historic mountainside estate with magnificent art collections and tours."
            ),
            TravelStop(
                name="Splash Cafe (Pismo Beach)",
                category="Restaurant",
                latitude=35.1428,
                longitude=-120.6431,
                rating=4.5,
                description="Famous beachside spot celebrated for award-winning clam chowder in sourdough bowls."
            )
        ]
        
        df_stops = pd.DataFrame([stop.dict() for stop in mock_stops])
        
        # Filter based on user duration scaling
        max_items = min(len(df_stops), trip_duration_days * 2)
        active_df = df_stops.head(max_items)
        
        st.success(f"Generated optimized itinerary for {trip_duration_days} day(s) along the {origin} to {destination} corridor!")
        
        # --- Interactive PyDeck Map Visualization ---
        st.subheader("📍 Interactive Route Map & Recommended Stops")
        
        # Center map dynamically around midpoint
        mid_lat = active_df["latitude"].mean()
        mid_lon = active_df["longitude"].mean()
        
        view_state = pdk.ViewState(
            latitude=mid_lat,
            longitude=mid_lon,
            zoom=6.5,
            pitch=30
        )
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=active_df,
            get_position="[longitude, latitude]",
            get_color="[255, 75, 75, 200]",
            get_radius=15000,
            pickable=True,
            auto_highlight=True
        )
        
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}\nCategory: {category}\nRating: {rating} ⭐\n{description}"}
        )
        
        st.pydeck_chart(r)
        
        # --- Itinerary Breakdown Table & Details ---
        st.subheader("📋 Recommended Stops & High-Rating Backups")
        st.dataframe(active_df[["name", "category", "rating", "description"]], use_container_width=True)
        
        st.markdown("### 🗓️ Day-by-Day Dynamic Schedule")
        for i, row in active_df.iterrows():
            day_num = (i % trip_duration_days) + 1
            with st.expander(f"Day {day_num}: {row['name']} ({row['category']}) - {row['rating']} ⭐"):
                st.markdown(f"**Description:** {row['description']}")
                st.markdown(f"**Coordinates:** Latitude {row['latitude']}, Longitude {row['longitude']}")
                st.info("💡 **Travel Tip:** Reserve tickets or table slots in advance during peak travel seasons.")
else:
    st.info("Configure your trip parameters in the sidebar and click **Generate Optimized Itinerary & Map** to begin.")
