import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Albany Airbnb Market Insights",
    page_icon="🏠",
    layout="wide"
)


# --------------------------------------------------
# Load data and validate it
# --------------------------------------------------
st.title("🏠 Albany Airbnb Market Insights")
st.write(
    "Explore Airbnb listing prices, room types, neighbourhoods, "
    "availability, and reviews in Albany, New York."
)

DATA_FILE = "albany_airbnb_dashboard.csv"

REQUIRED_COLUMNS = [
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "nightly_price",
    "availability_30",
    "availability_90",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
]

try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    st.error(
        f"Could not find {DATA_FILE}. Make sure it is in the same folder "
        "as app.py."
    )
    st.stop()

missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

# Convert expected numeric fields safely
NUMERIC_COLUMNS = [
    "latitude",
    "longitude",
    "accommodates",
    "nightly_price",
    "availability_30",
    "availability_90",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
]

for col in NUMERIC_COLUMNS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Show a small validation summary
with st.expander("Dataset validation details"):
    st.write(f"**Rows loaded:** {len(df):,}")
    st.write(f"**Columns loaded:** {len(df.columns):,}")

    null_counts = df[REQUIRED_COLUMNS].isna().sum()
    null_counts = null_counts[null_counts > 0]

    if null_counts.empty:
        st.success("No missing values found in the required fields.")
    else:
        st.write("Missing values in required fields:")
        st.dataframe(
            null_counts.rename("Missing values").to_frame(),
            use_container_width=True
        )

    invalid_coords = (
        df["latitude"].isna()
        | df["longitude"].isna()
        | ~df["latitude"].between(-90, 90)
        | ~df["longitude"].between(-180, 180)
    )
    st.write(f"**Listings with invalid or missing coordinates:** {invalid_coords.sum():,}")


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("Dashboard filters")

room_types = ["All"] + sorted(
    df["room_type"].dropna().astype(str).unique().tolist()
)
selected_room = st.sidebar.selectbox("Room type", room_types)

filtered_df = df.copy()

if selected_room != "All":
    filtered_df = filtered_df[filtered_df["room_type"] == selected_room]

# Price range filter uses listings with known prices
priced_values = filtered_df["nightly_price"].dropna()

if not priced_values.empty:
    min_price = float(priced_values.min())
    max_price = float(priced_values.max())

    if min_price < max_price:
        selected_price_range = st.sidebar.slider(
            "Nightly price range (USD)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=1.0
        )

        filtered_df = filtered_df[
            filtered_df["nightly_price"].between(
                selected_price_range[0],
                selected_price_range[1]
            )
        ]
    else:
        selected_price_range = (min_price, max_price)
        st.sidebar.caption(f"Available price: ${min_price:,.2f}")
else:
    selected_price_range = None
    st.sidebar.info("No priced listings available for this room type.")

priced = filtered_df["nightly_price"].dropna()


# --------------------------------------------------
# Key metrics
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Listings shown", f"{len(filtered_df):,}")
col2.metric(
    "Median nightly price",
    f"${priced.median():,.2f}" if not priced.empty else "N/A"
)
col3.metric(
    "Average nightly price",
    f"${priced.mean():,.2f}" if not priced.empty else "N/A"
)
col4.metric(
    "Room types shown",
    filtered_df["room_type"].nunique()
)


# --------------------------------------------------
# Nightly price distribution
# --------------------------------------------------
st.subheader("1. Nightly Price Distribution")

if not priced.empty:
    fig = px.histogram(
        filtered_df.dropna(subset=["nightly_price"]),
        x="nightly_price",
        nbins=30,
        title="Nightly prices in the filtered listings",
        labels={"nightly_price": "Price per night (USD)"},
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No listings with a known price match these filters.")


# --------------------------------------------------
# Median price by room type
# --------------------------------------------------
st.subheader("2. Median Nightly Price by Room Type")

room_price = (
    df.dropna(subset=["nightly_price"])
    .groupby("room_type", as_index=False)["nightly_price"]
    .median()
    .sort_values("nightly_price", ascending=False)
)

if not room_price.empty:
    fig = px.bar(
        room_price,
        x="room_type",
        y="nightly_price",
        title="Median nightly price across all room types",
        labels={
            "room_type": "Room type",
            "nightly_price": "Median price per night (USD)"
        },
        text_auto=".2f",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Neighbourhood comparison
# --------------------------------------------------
st.subheader("3. Neighbourhood-Level Price Comparison")

neighbourhood_price = (
    filtered_df.dropna(subset=["nightly_price", "neighbourhood_cleansed"])
    .groupby("neighbourhood_cleansed", as_index=False)
    .agg(
        listing_count=("nightly_price", "count"),
        median_price=("nightly_price", "median")
    )
    .sort_values("median_price", ascending=False)
)

if not neighbourhood_price.empty:
    fig = px.bar(
        neighbourhood_price.head(15),
        x="neighbourhood_cleansed",
        y="median_price",
        hover_data=["listing_count"],
        title="Top 15 neighbourhoods by median nightly price",
        labels={
            "neighbourhood_cleansed": "Neighbourhood",
            "median_price": "Median nightly price (USD)",
            "listing_count": "Listings with prices"
        },
        text_auto=".2f",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "This chart shows up to 15 neighbourhoods in the current filtered view. "
        "Neighbourhoods with few listings may have less stable medians."
    )
else:
    st.info("No neighbourhood price data available for these filters.")


# --------------------------------------------------
# Listing map
# --------------------------------------------------
st.subheader("4. Listing Map")

map_df = filtered_df.dropna(subset=["latitude", "longitude"]).copy()
map_df = map_df[
    map_df["latitude"].between(-90, 90)
    & map_df["longitude"].between(-180, 180)
]

if not map_df.empty:
    map_df = map_df.rename(
        columns={
            "latitude": "lat",
            "longitude": "lon"
        }
    )
    st.map(map_df[["lat", "lon"]], use_container_width=True)
    st.caption(
        "Map points show the locations recorded in the dataset. "
        "The map is limited to listings that have valid coordinates."
    )
else:
    st.info("No valid coordinates are available for the selected listings.")


# --------------------------------------------------
# Availability charts
# --------------------------------------------------
st.subheader("5. Listing Availability")

availability_cols = [
    "availability_30",
    "availability_90",
    "availability_365"
]

availability_labels = {
    "availability_30": "Available days in next 30 days",
    "availability_90": "Available days in next 90 days",
    "availability_365": "Available days in next 365 days"
}

availability_long = (
    filtered_df[availability_cols]
    .rename(columns=availability_labels)
    .melt(
        var_name="Period",
        value_name="Available days"
    )
    .dropna(subset=["Available days"])
)

if not availability_long.empty:
    fig = px.box(
        availability_long,
        x="Period",
        y="Available days",
        title="Distribution of available days by time window",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No availability information is available for these filters.")


# --------------------------------------------------
# Reviews charts
# --------------------------------------------------
st.subheader("6. Reviews and Ratings")

review_col1, review_col2 = st.columns(2)

with review_col1:
    reviews_df = filtered_df.dropna(subset=["number_of_reviews"])

    if not reviews_df.empty:
        fig = px.histogram(
            reviews_df,
            x="number_of_reviews",
            nbins=30,
            title="Number of reviews per listing",
            labels={"number_of_reviews": "Number of reviews"},
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No review-count data available.")

with review_col2:
    rating_df = filtered_df.dropna(
        subset=["review_scores_rating", "number_of_reviews"]
    )

    if not rating_df.empty:
        fig = px.scatter(
            rating_df,
            x="number_of_reviews",
            y="review_scores_rating",
            hover_data=["room_type", "neighbourhood_cleansed"],
            title="Review count vs. rating",
            labels={
                "number_of_reviews": "Number of reviews",
                "review_scores_rating": "Review rating"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No paired review-count and rating data available.")


# --------------------------------------------------
# Property-type chart
# --------------------------------------------------
st.subheader("7. Property Types")

property_counts = (
    filtered_df["property_type"]
    .fillna("Not specified")
    .value_counts()
    .head(15)
    .rename_axis("property_type")
    .reset_index(name="listing_count")
)

if not property_counts.empty:
    fig = px.bar(
        property_counts,
        x="listing_count",
        y="property_type",
        orientation="h",
        title="Most common property types in the filtered listings",
        labels={
            "property_type": "Property type",
            "listing_count": "Number of listings"
        },
        template="plotly_white"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Dataset preview
# --------------------------------------------------
st.subheader("8. Filtered Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)


# --------------------------------------------------
# AI assistant
# --------------------------------------------------
st.divider()
st.header("🤖 Ask the Albany Airbnb AI Assistant")
st.write(
    "Ask a question about the currently filtered listings. "
    "The assistant uses calculated summaries from this view."
)

question = st.text_input(
    "Your question",
    placeholder="Example: Which neighbourhood has the highest median price in this view?"
)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Please enter a question first.")
    elif filtered_df.empty:
        st.warning("No listings match the selected filters.")
    else:
        with st.spinner("Analyzing the filtered dataset..."):
            try:
                priced_view = filtered_df.dropna(subset=["nightly_price"])

                if not priced_view.empty:
                    room_summary = (
                        priced_view.groupby("room_type")["nightly_price"]
                        .agg(["count", "median", "mean"])
                        .round(2)
                        .to_string()
                    )

                    neighbourhood_summary = (
                        priced_view.dropna(
                            subset=["neighbourhood_cleansed"]
                        )
                        .groupby("neighbourhood_cleansed")["nightly_price"]
                        .agg(["count", "median", "mean"])
                        .sort_values("count", ascending=False)
                        .head(15)
                        .round(2)
                        .to_string()
                    )

                    overall_median = round(
                        float(priced_view["nightly_price"].median()), 2
                    )
                    overall_mean = round(
                        float(priced_view["nightly_price"].mean()), 2
                    )
                else:
                    room_summary = "No priced listings in this view."
                    neighbourhood_summary = "No priced listings in this view."
                    overall_median = "Not available"
                    overall_mean = "Not available"

                property_summary = (
                    filtered_df["property_type"]
                    .fillna("Not specified")
                    .value_counts()
                    .head(15)
                    .to_string()
                )

                availability_summary = (
                    filtered_df[availability_cols]
                    .mean()
                    .round(2)
                    .to_string()
                )

                review_summary = (
                    filtered_df[
                        ["number_of_reviews", "review_scores_rating"]
                    ]
                    .describe()
                    .round(2)
                    .to_string()
                )

                context = f"""
                Dataset: Albany Airbnb listings, New York.

                Active room-type filter: {selected_room}
                Active nightly-price filter: {selected_price_range}

                Listings in current view: {len(filtered_df)}
                Listings with known nightly prices: {len(priced_view)}
                Median nightly price in current view: {overall_median} USD
                Average nightly price in current view: {overall_mean} USD

                Price summary by room type:
                {room_summary}

                Neighbourhood price summary (up to 15 neighbourhoods):
                {neighbourhood_summary}

                Property-type counts (top 15):
                {property_summary}

                Mean availability values:
                {availability_summary}

                Review statistics:
                {review_summary}
                """

                client = genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )

                prompt = f"""
                You are a data analytics assistant for an Albany Airbnb dashboard.

                Answer the user's question using only the provided summary.
                The summary reflects the current room-type and price filters.
                Do not invent figures or details.
                If the summary does not contain the requested information,
                say that it is not available in this summary.
                Explain the answer in clear, beginner-friendly language.
                All prices are in USD per night.

                DATA SUMMARY:
                {context}

                USER QUESTION:
                {question}
                """

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.subheader("AI answer")
                st.write(response.text)

            except Exception as e:
                st.error(
                    "The AI assistant could not complete the request. "
                    "Check your internet connection and Gemini API setup."
                )
                st.caption(f"Technical details: {e}")