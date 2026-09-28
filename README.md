# Albany Airbnb Market Insights AI

An interactive analytics dashboard for exploring Airbnb listing prices, availability, property types, and review patterns in Albany, New York. Built with Python and Streamlit, the project combines data analysis and visualization with a Gemini-powered AI assistant to help users explore the market through natural-language questions.

**Live Dashboard:** [Open Albany Airbnb Market Insights AI](https://albany-airbnb-market-insights-axgjfspaavq7ahyw5kemf6.streamlit.app/)

---

## Project Overview

This project analyzes publicly available Airbnb listing data for Albany, New York. It presents key market indicators in an interactive dashboard, allowing users to filter listings and investigate pricing and other listing characteristics.

A built-in AI assistant uses the current dashboard view to answer questions about the filtered data, making the analysis easier to explore without writing queries or code.

## Objectives

* Explore nightly pricing patterns across Airbnb room types.
* Compare listing prices by neighbourhood and property type.
* Examine availability, review scores, and estimated occupancy.
* Present key findings through interactive charts and metrics.
* Enable natural-language exploration of the current filtered dataset using Gemini.

## Dashboard Features

* **Interactive filters:** Filter listings by room type and nightly price range.
* **Key metrics:** View summary indicators such as listing counts and nightly price statistics.
* **Price analysis:** Explore nightly price distributions and compare median prices across room types.
* **Neighbourhood insights:** Compare listing prices across neighbourhoods.
* **Availability and reviews:** Examine availability, review scores, and relationships between listing characteristics.
* **Property type analysis:** Explore the mix of property types in the dataset.
* **Listing map:** View geographic patterns for the listings.
* **AI-powered Q&A:** Ask questions in natural language and receive responses based on the active dashboard view.

## Dataset

The project uses publicly available listing data from **Inside Airbnb** for Albany, New York.

The dashboard is powered by a prepared dataset containing **490 listings and 17 selected fields**. The original data was cleaned and transformed for analysis. Some records have missing nightly prices, so price-based summaries use listings with available price data.

### Selected fields

| Field                                                    | Description                                |
| -------------------------------------------------------- | ------------------------------------------ |
| `neighbourhood_cleansed`                                 | Neighbourhood associated with the listing  |
| `latitude`, `longitude`                                  | Listing coordinates                        |
| `property_type`                                          | Type of property                           |
| `room_type`                                              | Airbnb room category                       |
| `accommodates`                                           | Maximum guest capacity                     |
| `bedrooms`, `beds`                                       | Bedroom and bed counts                     |
| `nightly_price`                                          | Listed nightly price                       |
| `availability_30`, `availability_90`, `availability_365` | Availability over the specified periods    |
| `number_of_reviews`                                      | Total number of reviews                    |
| `review_scores_rating`                                   | Listing review score                       |
| `estimated_occupancy_l365d`                              | Estimated occupancy over the last 365 days |
| `estimated_revenue_l365d`                                | Estimated revenue over the last 365 days   |

**Data source:** [Inside Airbnb](https://insideairbnb.com/)

## Key Findings

The following figures are based on the prepared dataset used in the dashboard:

* **490** total listings in the prepared dataset.
* **458** listings have a known nightly price.
* **$145.67** overall median nightly price among listings with available prices.
* **$71.82** median nightly price for private rooms.
* **$166.00** median nightly price for entire homes/apartments.

These are descriptive statistics from the dataset, not predictions of future prices or guarantees of actual booking revenue. Results may change when filters are applied.

## Tools and Technologies

* **Python** — data preparation and analysis
* **Pandas** — data cleaning and transformation
* **Plotly** — interactive visualizations
* **Streamlit** — dashboard and web app
* **Google Gemini API** — natural-language AI assistant
* **Jupyter Notebook** — exploratory analysis and development
* **GitHub** — source control and project hosting
* **Streamlit Community Cloud** — deployment

## Project Structure

```text
albany-airbnb-market-insights/
│
├── app.py
├── albany_airbnb_dashboard.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/vsadarshahi97/albany-airbnb-market-insights.git
cd albany-airbnb-market-insights
```

### 2. Install dependencies

It is recommended to use a virtual environment.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a folder named `.streamlit` in the project directory, then create a file named `secrets.toml` inside it.

Add your API key in this format:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own key. **Never commit this file or share your API key publicly.**

### 4. Start the dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local address in the terminal. Open that address in your browser to use the dashboard.

## AI Assistant

The dashboard includes a Gemini-powered assistant for asking questions about the data. Responses are intended to reflect the current filtered view of the dashboard.

The assistant is a convenience for exploring the dataset. Verify important figures against the dashboard or source data, and do not treat AI-generated explanations as a substitute for checking the underlying calculations.

## Limitations

* The analysis covers the available Albany listing dataset and may not represent every Airbnb listing in the market.
* Some listings have missing nightly prices, which affects the number of records included in price calculations.
* Occupancy and revenue fields are estimates from the source dataset and should not be interpreted as verified financial results.
* Listing prices and availability can change over time; this dashboard is not a live booking or pricing feed.
* AI responses can occasionally be incomplete or inaccurate, so key findings should be checked against the data.

## Future Improvements

* Add date-based comparisons to examine how listing prices and availability change over time.
* Expand the analysis with additional cities and compare markets.
* Add more detailed filters for guest capacity, bedrooms, and property type.
* Improve the AI assistant with more guided analytical questions and clearer explanations of its data scope.
* Add automated data refreshes when updated source data becomes available.
* Introduce additional market indicators and downloadable filtered reports.

## Author

**Adarsh VS**

GitHub: [vsadarshahi97](https://github.com/vsadarshahi97)

---

*This project was developed as a data analytics portfolio project to demonstrate data preparation, exploratory analysis, interactive visualization, and the integration of an AI assistant into a web dashboard.*
