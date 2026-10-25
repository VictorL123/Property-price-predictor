# This function finds the highest price in the list of similar properties
def highest_price(similar_properties):
    return similar_properties['currentPrice'].max()
# This function finds the lowest price in the list of similar properties
def lowest_price(similar_properties):
    return similar_properties['currentPrice'].min()

# This function returns the range of estimates for the property
def range_estimates(similar_properties):
    highest = highest_price(similar_properties)
    lowest = lowest_price(similar_properties)
    return highest, lowest