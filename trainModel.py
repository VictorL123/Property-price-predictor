# Here I have imported libraries, which can then be used

import pandas as pd
import numpy as np
import math as math
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


#This function cleans the data
def clean_data(df):
    df = df.dropna()
    return df


#This function preprocesses the data using one hot encoding
def preprocess_data(df):
    df = pd.get_dummies(df, columns=['postcode','outcode','tenure','propertyType'])
    return df

def split_data(df):
    #Split the data into dependent and independent variables
    y = df['currentPrice']
    x = df.drop(['currentPrice', 'fullAddress'], axis=1)

    #Split the data into training and testing data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test

# Function to train and evaluate models
def train_and_evaluate_models(df):
    # Split the data into dependent and independent variables
    y = df['currentPrice']
    x = df.drop(['currentPrice', 'fullAddress'], axis=1)

    # Split the data into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # Train and evaluate Linear Regression model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_lr_train_pred = lr.predict(X_train)
    y_lr_test_pred = lr.predict(X_test)
    
    # Calculate the test staistics
    lr_train_mse = mean_squared_error(y_train, y_lr_train_pred)
    lr_train_r2 = r2_score(y_train, y_lr_train_pred)
    lr_test_mse = mean_squared_error(y_test, y_lr_test_pred)
    lr_test_r2 = r2_score(y_test, y_lr_test_pred)
    lr_results = pd.DataFrame(['Linear regression', lr_train_mse, lr_train_r2, lr_test_mse, lr_test_r2]).transpose()
    lr_results.columns = ['Method', 'Training MSE', 'Training R2', 'Test MSE', 'Test R2']

    # Train and evaluate Random Forest model
    rf = RandomForestRegressor(random_state=100)
    rf.fit(X_train, y_train)
    y_rf_train_pred = rf.predict(X_train)
    y_rf_test_pred = rf.predict(X_test)
    
    # Calculate the test statistics
    rf_train_mse = mean_squared_error(y_train, y_rf_train_pred)
    rf_train_r2 = r2_score(y_train, y_rf_train_pred)
    rf_test_mse = mean_squared_error(y_test, y_rf_test_pred)
    rf_test_r2 = r2_score(y_test, y_rf_test_pred)
    rf_results = pd.DataFrame(['Random forest', rf_train_mse, rf_train_r2, rf_test_mse, rf_test_r2]).transpose()
    rf_results.columns = ['Method', 'Training MSE', 'Training R2', 'Test MSE', 'Test R2']

    # Save the better model
    if rf_test_r2 > lr_test_r2:
        with open('model.pkl', 'wb') as f:
            pickle.dump(rf, f)
    else:
        with open('model.pkl', 'wb') as f:
            pickle.dump(lr, f)


# Main function to execute the workflow
def main():
    df = pd.read_csv('london_house_price_data.csv')
    
    # Clean and sample the data
    df = clean_data(df)
    df = df.sample(frac=0.01)
    
    # Prepare the data for model training
    df.to_csv('sampled_data.csv', index=False)
    df_dummies = preprocess_data(df)
    df_dummies.to_csv('sampled_data_dummies.csv', index=False)
    
    # Train the model
    train_and_evaluate_models(df_dummies)

