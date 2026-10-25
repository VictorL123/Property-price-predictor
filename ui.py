# Imports
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import importlib.util
import threading

# Global list to store confirmed details
confirmed_details_list = []

# Import the predict_price function from phase 4 file
spec = importlib.util.spec_from_file_location("predictPrice", "predictPrice.py")
predictPrice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(predictPrice)

# Import the similar properties function from phase 5 file
spec2 = importlib.util.spec_from_file_location("similarProperties", "similarProperties.py")
similarProperties = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(similarProperties)

# Import the range estimates function from phase 6 file
spec3 = importlib.util.spec_from_file_location("rangeEstimates", "rangeEstimates.py")
rangeEstimates = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(rangeEstimates)

# Import the map function from map.py
spec4 = importlib.util.spec_from_file_location("map", "map.py")
map = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(map)

# Import the web scraper function from webScraper.py
spec5 = importlib.util.spec_from_file_location("webScraper", "webScraper.py")
webScraper = importlib.util.module_from_spec(spec5)
spec5.loader.exec_module(webScraper)

# Import the model trainer function from trainModel.py
spec6 = importlib.util.spec_from_file_location("trainModel", "trainModel.py")
trainModel = importlib.util.module_from_spec(spec6)
spec6.loader.exec_module(trainModel)

# Function to get options for property types, postcodes, and tenures from the CSV file
def get_options():
    df = pd.read_csv('sampled_data.csv')
    df = df.dropna()
    
    # Get unique values for propertyType, postcode, and tenure
    property_types = df['propertyType'].unique()
    tenures = df['tenure'].unique()
    
    # Convert the numpy arrays to lists
    property_types = property_types.tolist()
    tenures = tenures.tolist()
    return property_types, tenures

# Function to create the main window
def create_main_window():
    root = tk.Tk()
    root.title("House Details Form")
    root.state("zoomed")  # Maximize the window
    root.configure(bg="#f0f0f0")  # Light grey background
    root.bind("<Configure>", lambda event: adjust_font_size(root))
    return root

# Function to adjust font size dynamically
def adjust_font_size(root):
    width = root.winfo_width()
    height = root.winfo_height()
    new_size = max(10, int(min(width, height) / 50))
    global font_style
    font_style = ("Helvetica", new_size)
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, ttk.Combobox, tk.Entry)):
            widget.config(font=font_style)

# Function to create the widgets in the main window
def create_widgets(root, property_types, tenures):
    # Property Type
    tk.Label(root, text="Property Type:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
    property_type_var = tk.StringVar(value="Select")
    property_type_menu = ttk.Combobox(root, textvariable=property_type_var, values=property_types, width=30)
    property_type_menu.grid(row=0, column=1, pady=5, padx=5)

    # Postcode
    tk.Label(root, text="Postcode:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
    postcode_var = tk.StringVar()
    postcode_menu = tk.Entry(root, textvariable=postcode_var, width=30)
    postcode_menu.grid(row=1, column=1, pady=5, padx=5)

    # Address
    tk.Label(root, text="Address:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
    address_var = tk.StringVar()
    address_entry = tk.Entry(root, textvariable=address_var, width=30)
    address_entry.grid(row=2, column=1, pady=5, padx=5)

    # Tenure
    tk.Label(root, text="Tenure:").grid(row=3, column=0, pady=5, padx=5, sticky="w")
    tenure_var = tk.StringVar(value="Select")
    tenure_menu = ttk.Combobox(root, textvariable=tenure_var, values=tenures)
    tenure_menu.grid(row=3, column=1, pady=5, padx=5)

    # Number of Bedrooms
    tk.Label(root, text="Number of Bedrooms:").grid(row=4, column=0, pady=5, padx=5, sticky="w")
    bedrooms_var = tk.IntVar(value=1)
    bedrooms_menu = ttk.Combobox(root, textvariable=bedrooms_var, values=list(range(1, 11)))
    bedrooms_menu.grid(row=4, column=1, pady=5, padx=5)

    # Number of Bathrooms
    tk.Label(root, text="Number of Bathrooms:").grid(row=5, column=0, pady=5, padx=5, sticky="w")
    bathrooms_var = tk.IntVar(value=1)
    bathrooms_menu = ttk.Combobox(root, textvariable=bathrooms_var, values=list(range(1, 11)))
    bathrooms_menu.grid(row=5, column=1, pady=5, padx=5)

    # Area
    tk.Label(root, text="Area (sq meters):").grid(row=6, column=0, pady=5, padx=5, sticky="w")
    area_var = tk.StringVar()
    area_entry = tk.Entry(root, textvariable=area_var)
    area_entry.grid(row=6, column=1, pady=5, padx=5)

    # Submit Button
    submit_button = tk.Button(root, text="Submit for prediction", command=lambda: submit_details(root, property_type_var, postcode_var, address_var, tenure_var, bedrooms_var, bathrooms_var, area_var))
    submit_button.grid(row=7, column=0, columnspan=2, pady=20)
    
    # Button to retrain the model
    retrain_button = tk.Button(root, text="Retrain Model", command=lambda: reset_model(root))
    retrain_button.grid(row=8, column=0, columnspan=2, pady=20)
    
# Function to retrain the model
def reset_model(root):
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()
        
    # Refresh the GUI so everything is deleted
    root.update()
    
    # Show loading screen on the main window
    loading_label = tk.Label(root, text="Retraining model, please wait...", font=("Helvetica", 16))
    loading_label.pack(pady=20, padx=20)
    root.update_idletasks()
    
    # Run the prediction in a separate thread
    threading.Thread(target=lambda: retrain_model(root)).start()
            
# Function to retrain the model
def retrain_model(root):
    # Call the web scraper function
    webScraper.webScraper()
    trainModel.main()
    
    # Message to show the model has been retrained
    messagebox.showinfo("Model Retrained", "Model has been retrained!")
    
    # Reseting the prediction
    reset(root)        
            
# Function to handle the submission of details
def submit_details(root, property_type_var, postcode_var, address_var, tenure_var, bedrooms_var, bathrooms_var, area_var):
    # Get the entered details
    property_type = property_type_var.get()
    postcode = postcode_var.get()
    address = address_var.get()
    tenure = tenure_var.get()
    bedrooms = bedrooms_var.get()
    bathrooms = bathrooms_var.get()
    area = area_var.get()
    
    # Show the entered details in a custom pop-up window
    details_window = tk.Toplevel(root)
    details_window.title("House Details")
    details_window.geometry("300x200")
    
    # Display the entered details
    details = (
        f"Property Type: {property_type}\n"
        f"Postcode: {postcode}\n"
        f"Address: {address}\n"
        f"Tenure: {tenure}\n"
        f"Bedrooms: {bedrooms}\n"
        f"Bathrooms: {bathrooms}\n"
        f"Area: {area} sq m"
    )
    
    tk.Label(details_window, text=details).pack(pady=10)
    
    def edit_details():
        details_window.destroy()
    
    def confirm_details():
        user_details = [property_type, postcode, address, tenure, bedrooms, bathrooms, area]
        # Validate the inputs
        validation = predictPrice.validate_inputs(user_details)
        if validation == "valid":
            confirmed_details_list.append(user_details)
            messagebox.showinfo("Confirmation", "Details confirmed!")
            details_window.destroy()
            
            # Clear the main window
            for widget in root.winfo_children():
                widget.destroy()
                
            # Refresh the GUI so everything is deleted
            root.update()
            
            # Show loading screen on the main window
            loading_label = tk.Label(root, text="Calculating value, please wait...", font=("Helvetica", 16))
            loading_label.pack(pady=20, padx=20)
            root.update_idletasks()
            
            # Run the prediction in a separate thread
            threading.Thread(target=lambda: run_prediction(root, user_details, loading_label)).start()
            
        # If details are not valid, return to original submission form
        elif validation == "address":
            messagebox.showerror("Error", "Please enter your address!")
            details_window.destroy()
        elif validation == "area":
            messagebox.showerror("Error", "Please enter the area!")
            details_window.destroy()
        elif validation == "postcode":
            messagebox.showerror("Error", "Postcode not found! \n(Warning: Model only trained on certain postcodes)")
            details_window.destroy()
        elif validation == "tenure":
            messagebox.showerror("Error", "Please select a tenure!")
            details_window.destroy()
        elif validation == "type":
            messagebox.showerror("Error", "Please select a property type!")
            details_window.destroy()
        elif validation == "area_type":
            messagebox.showerror("Error", "Please enter a number for area!")
            details_window.destroy()
    
    tk.Button(details_window, text="Edit", command=edit_details).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(details_window, text="Confirm", command=confirm_details).pack(side=tk.RIGHT, padx=10, pady=10)

# Function to run the prediction in a separate thread
def run_prediction(root, user_details, loading_label):
    # Get the predicted price
    prediction = get_predicted_price(user_details)
    
    # Destroy loading screen
    loading_label.destroy()
    
    # Display the predicted price
    display_prediction(root, prediction, user_details)

# Function to get the predicted price from nea_phase_4.py
def get_predicted_price(user_details):
    return predictPrice.predict_price(user_details)

# Function to display the predicted price
def display_prediction(root, predicted_price, user_details):
    # Display the details about the users property
    tk.Label(root, text="Property Details:",).grid(row=0, column=0, pady=5, padx=5, sticky="nw")
    details = (
        f"Address: {user_details[2]}\n"
        f"Postcode: {user_details[1]}\n"
        f"Property Type: {user_details[0]}\n"
        f"Tenure: {user_details[3]}\n"
        f"Bedrooms: {user_details[4]}\n"
        f"Bathrooms: {user_details[5]}\n"
        f"Area: {user_details[6]} sq m"
    )
    
    tk.Label(root, text=details, anchor="w", justify="left").grid(row=0, column=1, pady=5, padx=5, sticky="w")

    
    # Display the predicted price
    tk.Label(root, text="Predicted Price:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
    tk.Label(root, text=f"£{predicted_price}").grid(row=1, column=1, pady=5, padx=5, sticky="w")
    
    # Button to find similar properties
    similar_button = tk.Button(root, text="Find Similar Properties", command=lambda: find_similar_properties(root))
    similar_button.grid(row=1, column=2, columnspan=2, pady=20)
    
    # Button to predict another property
    another_button = tk.Button(root, text="Predict Another Property", command=lambda: reset(root))
    another_button.grid(row=2, column=0, columnspan=2, pady=20)
    
    # Button to display the map
    map_button = tk.Button(root, text="Display Map", command=lambda: map.create_window(user_details[1]))
    map_button.grid(row=2, column=2, columnspan=2, pady=20)
    
def reset(root):
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()
        
    # Clear the confirmed details list
    confirmed_details_list.clear()
        
    # Refresh the GUI so everything is deleted
    root.update()
    
    # Get the property types and tenures
    property_types, tenures = get_options()
    
    # Create the widgets again
    create_widgets(root, property_types, tenures)    
    
# Function to find similar properties
def find_similar_properties(root):
    # Get the user details
    user_details = confirmed_details_list[0]
    
    # Run the similar properties search in a separate thread
    threading.Thread(target=lambda: run_similar_properties_search(root, user_details)).start()

# Function to run the similar properties search in a separate thread
def run_similar_properties_search(root, user_details):
    # Find similar properties
    similar_properties = similarProperties.find_similar(user_details)
    
    # Display the similar properties
    display_similar_properties(root, similar_properties)

# Function to display the similar properties
def display_similar_properties(root, similar_properties):
    if similar_properties is False:
        messagebox.showinfo("No Similar Properties", "No similar properties found!")
    else:
        # Display the similar properties
        similar_properties_window = tk.Toplevel(root)
        similar_properties_window.title("Similar Properties")
        similar_properties_window.geometry("500x400")
        
        # Create a treeview to display the similar properties
        tree = ttk.Treeview(similar_properties_window)
        tree["columns"] = ("Address", "Postcode", "Type", "Tenure", "Bedrooms", "Bathrooms", "Area", "Price")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Address", anchor=tk.W, width=300)
        tree.column("Postcode", anchor=tk.W, width=100)
        tree.column("Type", anchor=tk.W, width=200)       
        tree.column("Tenure", anchor=tk.W, width=100)
        tree.column("Bedrooms", anchor=tk.W, width=75)
        tree.column("Bathrooms", anchor=tk.W, width=75)
        tree.column("Area", anchor=tk.W, width=50)
        tree.column("Price", anchor=tk.W, width=100)
        
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Address", text="Address", anchor=tk.W)
        tree.heading("Postcode", text="Postcode", anchor=tk.W)
        tree.heading("Type", text="Type", anchor=tk.W)
        tree.heading("Tenure", text="Tenure", anchor=tk.W)
        tree.heading("Bedrooms", text="Bedrooms", anchor=tk.W)
        tree.heading("Bathrooms", text="Bathrooms", anchor=tk.W)
        tree.heading("Area", text="Area", anchor=tk.W)
        tree.heading("Price", text="Price", anchor=tk.W)
        
        for index, row in similar_properties.iterrows():
            tree.insert("", tk.END, values=(row['fullAddress'], row['postcode'], row['propertyType'],  row['tenure'], row['bedrooms'], row['bathrooms'], row['floorAreaSqM'], row['currentPrice']))
        
        tree.pack(pady=20, padx=20)
        
        # Display the range of estimates
        highest, lowest = rangeEstimates.range_estimates(similar_properties)
        highest_label = tk.Label(similar_properties_window, text=f"Highest Price: £{highest}")
        highest_label.pack(pady=10)
        lowest_label = tk.Label(similar_properties_window, text=f"Lowest Price: £{lowest}")
        lowest_label.pack(pady=10)
        
        # Button to close the window
        close_button = tk.Button(similar_properties_window, text="Close", command=similar_properties_window.destroy)   
        close_button.pack(pady=20)

# Main function to execute the workflow
def main():
    root = create_main_window()
    property_types, tenures = get_options()
    create_widgets(root, property_types, tenures)
    root.mainloop()

if __name__ == "__main__":
    main()
    
