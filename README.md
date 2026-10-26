# Property Price Predictor

Machine learning project that predicts property prices from scraped listing
data, with an interactive interface including a map view.

## Documentation
Full write-up of the data collection, modelling and results:
[Project documentation (PDF)](docs/Documentation.pdf)

## What it does
- Scrapes and cleans over 10,000 property listings from postcode area
- Trains Random Forest and Linear Regression models to predict price from
  features, e.g. location, size, bedrooms, property type
- Compares the two models on held-out data
- Provides an interactive UI with a map for exploring listings and
  predictions

## How it works
1. **Data collection:** listings scraped with BeautifulSoup and stored with
   pandas
2. **Cleaning:** removed duplicates, handled missing values, converted
   prices to numbers
3. **Modelling:** scikit-learn Random Forest and Linear Regression
4. **Interface:** generate prediction, and find similar properties, displaying on a map

## Data
10,000+ listings scraped with BeautifulSoup and cleaned with pandas.
Features: location, floor area, bedrooms, bathrooms, property type.
The scraped data is not included in this repository.

## Results
Evaluated on a 20% held-out test set.

| Model | Test R² | Test RMSE |
|---|---|---|
| Linear Regression | 0.937 | ≈ £82,300 |
| Random Forest | 0.961 | ≈ £64,850 |

The Random Forest outperformed Linear Regression, suggesting non-linear
relationships between the features and price.

## Tech
Python, pandas, NumPy, BeautifulSoup, scikit-learn, PyQt5, Geopy
