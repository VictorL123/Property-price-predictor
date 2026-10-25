import pandas as pd

# Function to remove duplicates from the dataset
def remove_duplicates(dataset):
    dataset = dataset.drop_duplicates(subset=['fullAddress'])
    return dataset

# Function to get all unique postcodes from the dataset
def get_postcodes():
    df = pd.read_csv('london_house_price_data.csv')
    df = df.dropna()
    postcodes = df['postcode'].unique()
    return postcodes

# Function to extract the outcode from a postcode
def get_outcode(postcode):
    return postcode.split(" ")[0]

# Function to extract the sector from a postcode
def get_sector(postcode):
    return postcode.split(" ")[0] + " " + postcode.split(" ")[1][0]

# Function to sort the dataset by postcode using merge sort
def merge_sort(dataset, factor):
    if len(dataset) > 1:
        mid = len(dataset) // 2
        left_half = dataset[:mid]
        right_half = dataset[mid:]

        # Recursive call on each half
        merge_sort(left_half, factor)
        merge_sort(right_half, factor)

        i = j = k = 0

        # Copy data to temp arrays left_half[] and right_half[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i][factor] < right_half[j][factor]:
                dataset[k] = left_half[i]
                i += 1
            else:
                dataset[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            dataset[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            dataset[k] = right_half[j]
            j += 1
            k += 1
    # Return the sorted dataset
    return dataset

# Function to find postcode with the same sector
def binary_search(dataset, postcode):
    left = 0
    right = len(dataset) - 1
    # Binary search
    while left <= right:
        mid = left + (right - left) // 2
        # Check if postcode is in sector by using starts with
        if dataset[mid][1].startswith(postcode):
            return mid
        elif dataset[mid][1] < postcode:
            left = mid + 1
        else:
            right = mid - 1
    return False
    
# Function to find all properties with the same sector after binary search
def find_contiguous(dataset, postcode, start):
    left = start
    right = start
    while left >= 0 and dataset[left][1].startswith(postcode):
        left -= 1
    while right < len(dataset) and dataset[right][1].startswith(postcode):
        right += 1
    # Return the dataset with the sliced values
    return dataset[left + 1:right]

# Main function to find all properties with the same sector
def similar_dataset(postcode):
    # Read the dataset, removing duplicates and Nan values
    df = pd.read_csv('london_house_price_data.csv')
    df = df.dropna()
    df = remove_duplicates(df)
    
    # Convert dataframe to list and sort by postcode
    df_list = df.values.tolist()
    df_list = merge_sort(df_list, 1)
    
    # Use sector to find similarly located properties
    sector = get_sector(postcode)
    start_value = binary_search(df_list, sector)
    if start_value is False:
        return False
    df = find_contiguous(df_list, sector, start_value)
    
    # Convert list back to dataframe
    df = pd.DataFrame(df, columns=['fullAddress', 'postcode', 'outcode', 'bathrooms', 'bedrooms', 'floorAreaSqM', 'tenure', 'propertyType', 'currentPrice'])
    return df

# Function to find properties with matching type
def matching_type(type, dataset):
    mod_dataset = dataset[dataset['propertyType'] == type]
    if not mod_dataset.empty:    
        return mod_dataset 
    return dataset

# Function to find properties with matching tenure
def matching_tenure(tenure, dataset):
    mod_dataset = dataset[dataset['tenure'] == tenure]    
    if not mod_dataset.empty:
        return mod_dataset
    return dataset

# Function to find properties with matching bedrooms 
def matching_bedrooms(bedrooms, dataset):
    mod_dataset = dataset[dataset['bedrooms'] == bedrooms]
    if dataset.shape[0] > 3:
        return mod_dataset 
    # if no exact match, find properties with similar number of bedrooms
    return dataset[abs(dataset['bedrooms'] - bedrooms) <= 1]

# Function to find properties with matching bathrooms
def matching_bathrooms(bathrooms, dataset):
    mod_dataset = dataset[dataset['bathrooms'] == bathrooms]
    if dataset.shape[0] > 3:
        return mod_dataset 
    # if no exact match, find properties with similar number of bathrooms
    return dataset[abs(dataset['bathrooms'] - bathrooms) <= 1]

# Function to find properties with similar size
def similar_size(size, dataset):
    mod_dataset = dataset[(dataset['floorAreaSqM'] >= int(size) - 20) & (dataset['floorAreaSqM'] <= int(size) + 20)]
    if not mod_dataset.empty:
        return mod_dataset 
    return dataset

# Function to find similar properties based on user details
def find_similar(user_details):
    dataset = similar_dataset(user_details[1])
    if dataset is False:
        return False
    # Find matching properties based on user details
    else:
        dataset = matching_type(user_details[0], dataset)
        dataset = matching_tenure(user_details[3], dataset)
        dataset = matching_bedrooms(user_details[4], dataset)
        dataset = matching_bathrooms(user_details[5], dataset)
        dataset = similar_size(user_details[6], dataset)
        
        # Check if empty
        if dataset.empty:
            return False
        
    return dataset


