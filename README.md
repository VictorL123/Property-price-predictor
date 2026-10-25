# Property Price Predictor

Machine learning project that predicts property prices from scraped listing
data, with an interactive interface including a map view.

## Documentation
Full write-up of the data collection, modelling and results:
[Project documentation (PDF)](docs/Project Documentation.pdf)

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

## Tech
Python, pandas, NumPy, BeautifulSoup, scikit-learn, PyQt5, Geopy
