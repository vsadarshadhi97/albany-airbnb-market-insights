# Albany Airbnb Market Insights AI

An interactive data analytics dashboard for exploring Airbnb listing prices, availability, property types, and review patterns in Albany, New York. Built with Python and Streamlit, this project combines exploratory data analysis, interactive visualizations, and a Gemini-powered AI assistant for natural-language data exploration.

**Live Dashboard:** [Open Albany Airbnb Market Insights AI](https://albany-airbnb-market-insights-axgjfspaavq7ahyw5kemf6.streamlit.app/)

**EDA Notebook:** [View the Exploratory Data Analysis](airbnb_market_insights.ipynb)

---

## Project Overview

This project explores publicly available Airbnb listing data for Albany, New York. The dashboard presents key market indicators and interactive charts to help users investigate nightly prices, availability, property types, neighbourhood patterns, and review information.

The application also includes a Gemini-powered AI assistant that answers natural-language questions using the current dashboard view and its active filters.

## Project Objectives

* Analyze nightly pricing patterns across Airbnb room types.
* Compare listing prices across neighbourhoods and property types.
* Explore listing availability, review scores, and estimated occupancy.
* Present key findings through an interactive analytics dashboard.
* Integrate an AI assistant to make the dataset easier to explore with natural-language questions.
* Demonstrate practical skills in data cleaning, exploratory analysis, visualization, and deployment.

## Dashboard Features

* **Interactive filters:** Filter listings by room type and nightly price range.
* **Key performance indicators:** View summary metrics for the currently selected listings.
* **Nightly price analysis:** Explore price distributions and compare median prices by room type.
* **Neighbourhood analysis:** Compare listing prices across neighbourhoods.
* **Availability analysis:** Examine listing availability over different time periods.
* **Review analysis:** Explore review counts and review score patterns.
* **Property type analysis:** Review the distribution of property types in the dataset.
* **Geographic visualization:** Explore the locations of listings on a map.
* **AI-powered Q&A:** Ask questions about the data in natural language and receive answers based on the current dashboard view.

## Exploratory Data Analysis (EDA)

The EDA notebook documents the data preparation and exploratory analysis performed before building the dashboard. It includes data cleaning, inspection of important variables, descriptive statistics, and visual exploration of the Albany Airbnb listings.

**[Open the EDA Notebook on GitHub](airbnb_market_insights.ipynb)**

## Dataset

The project uses publicly available Airbnb listing data for Albany, New York, from [Inside Airbnb](https://insideairbnb.com/).

The prepared dashboard dataset contains **490 listings and 17 selected fields**. The original data was cleaned and transformed for use in the dashboard. Some listings have missing nightly prices, so price-based summaries use only records with a known price.

### Selected Dataset Fields

| Field                       | Description                                   |
| --------------------------- | --------------------------------------------- |
| `id`                        | Listing identifier                            |
| `neighbourhood_cleansed`    | Neighbourhood associated with the listing     |
| `latitude`, `longitude`     | Geographic coordinates of the listing         |
| `property_type`             | Property category                             |
| `room_type`                 | Airbnb room category                          |
| `accommodates`              | Maximum guest capacity                        |
| `bedrooms`                  | Number of bedrooms                            |
| `beds`                      | Number of beds                                |
| `nightly_price`             | Listed nightly price                          |
| `availability_30`           | Number of available days in the next 30 days  |
| `availability_90`           | Number of available days in the next 90 days  |
| `availability_365`          | Number of available days in the next 365 days |
| `number_of_reviews`         | Total number of reviews                       |
| `review_scores_rating`      | Listing review score                          |
| `estimated_occupancy_l365d` | Estimated occupancy over the last 365 days    |
| `estimated_revenue_l365d`   | Estimated revenue over the last 365 days      |

**Source:** [Inside Airbnb](https://insideairbnb.com/)

## Key Findings

The following statistics are based on the prepared dataset used in the dashboard:

* **490** total listings in the prepared dataset.
* **458** listings with a known nightly price.
* **$145.67** overall median nightly price among listings with available prices.
* **$71.82** median nightly price for private rooms.
* **$166.00** median nightly price for entire homes/apartments.

These figures are descriptive summaries of the dataset. They are not predictions of future prices or guarantees of booking revenue. Results shown in the dashboard may differ when filters are applied.

## Tools and Technologies

| Tool / Technology         | Purpose                             |
| ------------------------- | ----------------------------------- |
| Python                    | Data preparation and analysis       |
| Pandas                    | Data cleaning and transformation    |
| Plotly                    | Interactive data visualizations     |
| Streamlit                 | Dashboard development and web app   |
| Google Gemini API         | AI-powered natural-language Q&A     |
| Jupyter Notebook          | Exploratory data analysis           |
| GitHub                    | Version control and project hosting |
| Streamlit Community Cloud | Application deployment              |

## Repository Structure

```text
albany-airbnb-market-insights/
│
├── app.py
├── albany_airbnb_dashboard.csv
├── airbnb_market_insights.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/vsadarshahi97/albany-airbnb-market-insights.git
cd albany-airbnb-market-insights
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows, activate it with:

```bash
.venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

The AI assistant requires a Gemini API key. Create a folder named `.streamlit` in the project directory and create a file named `secrets.toml` inside it.

Add your key in this format:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key.

**Security note:** Keep your API key private. Do not commit `secrets.toml` to GitHub or share the key publicly. The repository's `.gitignore` excludes the local secrets file.

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal to use the dashboard.

## AI Assistant

The dashboard integrates the Google Gemini API to support natural-language questions about the listing data. The assistant is designed to use the current dashboard view, including active filters, when preparing its responses.

AI-generated answers can occasionally be incomplete or inaccurate. Check important figures against the dashboard and underlying dataset before relying on them.

## Limitations

* The analysis is limited to the available Albany listing dataset and may not include every Airbnb listing in the area.
* Some records have missing nightly prices, reducing the number of listings included in price-based calculations.
* Occupancy and revenue fields are estimates from the source dataset and should not be treated as verified financial results.
* Listing prices and availability can change over time. This dashboard is not a live booking or pricing feed.
* AI-generated responses may contain errors and should be verified against the data.
* The findings describe the dataset and should not be interpreted as causal conclusions about the wider short-term rental market.

## Future Improvements

* Add date-based comparisons to explore changes in listing prices and availability over time.
* Extend the analysis to additional cities to enable market comparisons.
* Add more filters for guest capacity, bedroom count, and property type.
* Expand the AI assistant with guided analytical questions and clearer explanations of its data scope.
* Support automated data refreshes when updated source data becomes available.
* Add downloadable reports and additional market indicators.

## Author

**Adarsh VS**

GitHub: [vsadarshahi97](https://github.com/vsadarshahi97)

---

*This project was developed as a data analytics portfolio project demonstrating data preparation, exploratory analysis, interactive visualization, AI integration, and web application deployment.*
