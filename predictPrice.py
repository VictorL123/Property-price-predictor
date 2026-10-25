# Imports
import pickle 
import pandas as pd

# Function to format data for prediction
def validate_inputs(user_details):
    # Check if property type has been selected
    if user_details[0] == "Select":
        return "type"
    # Check if postcode is valid
    if postcode_checker(user_details[1]) == False:
        return "postcode"
    # Check if address has been entered
    if user_details[2] == "":
        return "address"
    # Check if tenure has been selected
    if user_details[3] == "Select":
        return "tenure"
    #Check if area is a number
    try:
        area = int(user_details[6])
        if area <= 0:
            return "area"
    except ValueError:
        return "area_type"
    #If all inputs are valid
    else:
        return "valid"
    
# Function to get the headers of the dataset
def get_headers():
    df = pd.read_csv('sampled_data_dummies.csv')
    headings = df.columns.values.tolist()
    return headings
    
# Function to check if the postcode is in the dataset
def postcode_checker(postcode):
    headings = get_headers()
    for heading in headings:
        if heading == "postcode_" + postcode:
            return True
    return False
    

# Function to return a predicted price
def predict_price(user_details):
    # Open the machine learning model
    with open('model.pkl', 'rb') as file: 
        # Call load method to deserialze 
        model = pickle.load(file)
        
    # Format the data
    new_property = format_data(user_details)
    
    # Predict the price
    predicted_price = model.predict(pd.DataFrame(new_property, index=[0]))
    predicted_price = round(predicted_price[0], 2)
    
    return predicted_price

# Function to format the data for prediction
def format_data(user_details):
    # Get headings of dataset
    headings = get_headers()
    
    # Create a dictionary with all headings and default values
    new_property = {category: "0" for category in headings}
    del new_property['currentPrice']
    del new_property['fullAddress']
    
    # Get the outcode from the postcode
    outcode = user_details[1].split(" ")[0]
    
    # Update the dictionary with the user's inputs
    new_property.update(
        {
            "propertyType_" + user_details[0]: "1",
            "postcode_" + user_details[1]: "1",
            "tenure_" + user_details[3]: "1",
            "bedrooms": user_details[4],
            "bathrooms": user_details[5],
            "floorAreaSqM": user_details[6],
            "outcode_" + outcode: "1"
            
        }
    )
    
    return new_property
    

    
    
    


  
    