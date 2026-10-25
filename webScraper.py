#Imports
import requests #Used to connect to the website to scrape data from
from bs4 import BeautifulSoup #This is a web scraping library
import pandas as pd #This is a dataset analysis library

# Rightmove area codes for London boroughs
# A dictionary that stores all the boroughs of London and their corresponding regional codes

boroughs = {
    "City of London":"5E61224",
    "City of Westminster":"5E61233",
    "Kensington and Chelsea":"5E61229",
    "Hammersmith and Fulham":"5E61407",
    "Wandsworth":"5E93977",
    "Lambeth":"5E93971",
    "Southwark":"5E61518",
    "Tower Hamlets":"5E61417",
    "Hackney":"5E93953",
    "Islington":"5E93965",
    "Camden":"5E93941",
    "Brent":"5E93935",
    "Ealing":"5E93947",
    "Hounslow":"5E93962",
    "Richmond upon Thames":"5E61415",
    "Kingston upon Thames":"5E93968",
    "Merton":"5E61414",
    "Sutton": "5E93974",
    "Croydon": "5E93944",
    "Bromley": "5E93938",
    "Lewisham": "5E61413",
    "Greenwich": "5E61226",
    "Bexley": "5E93932",
    "Havering": "5E61228",
    "Barking and Dagenham": "5E61400",
    "Redbridge": "5E61537",
    "Newham": "5E61231",
    "Waltham Forest": "5E61232",
    "Haringey": "5E61227",
    "Enfield": "5E93950",
    "Barnet": "5E93929",
    "Harrow": "5E93956",
    "Hillingdon": "5E93959"

}

#Setting up the preliminary lists to store all the data of the properties
all_properties_address = [] 
all_properties_price = [] 
all_properties_links = [] 
all_properties_type = []
all_properties_bedrooms = []
all_properties_bathrooms = []
all_properties_size = []

#This function will be used to locate and extract all the data from the webpage
def data_retrieval_development(properties_html):

  #This loop will go through each individual properties' html found in the full list
  for property_no in range(len(properties_html)):
    current_property = properties_html[property_no]


    #Obtaining the link to the webpage of the specific property

    #This finds and extracts the class where the link is held
    property_info = current_property.find("a", class_="propertyCard-link")

    #Concatenate the individual link to form a proper weblink
    link = "https://www.rightmove.co.uk" + property_info.attrs["href"]

    #Append this link to our list
    all_properties_links.append(link)


    #Obtaining the address of a specific property
    address = (
        property_info.find("address", class_="propertyCard-address")
        .get_text() #This will extract the text from the html
        .strip() #This ensures only the desired text is saved
    )
    all_properties_address.append(address)

    #Obtaining the price of a specific property
    price = (
        current_property.find("div", class_="propertyCard-priceValue")
        .get_text() #Extract the price
        .strip() #Ensure it is only the price
    )
    price = price[1:]
    all_properties_price.append(price)

# Set up a function and loop to iterate through all the boroughs
def property_scraping(max_search):
  for borough in list(boroughs.values()):

    # This will initialise the index to match the index on the rightmove website
    index = 0

    # This is to show what the program is currently trying to scrape
    current_key = [key for key,value in boroughs.items() if value == borough][0]
    print(current_key)

    # Each borough will show a maximum of 42 pages hence this loops through all
    for pages in range(41):

      #This is needed to match the header of the browser when scraping
      user_headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
      }

      #The links on the website are slightly different on the first page compared to others
      if index == 0:
        rightmove_link = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
      elif index != 0:
        rightmove_link = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

      #The requests with the specific link and headers are sent to the website
      request = request.get(rightmove_link, headers=user_headers)
      request.html.render()

      #This receives all the html of the web page using the BeautifulSoup library
      page_html = BeautifulSoup(request.html.html, "html.parser")

      #Having identified the class data is found in, this returns all relevant html
      properties_html = page_html.find_all("div", class_="l-searchResult is-list")

      #Find total number of listings displayed
      total_no_listings = (
          page_html.find("span", {"class": "searchHeader-resultCount"})
          .get_text()
      )
      #Obtain just the integer value so can be used later
      total_no_listings = int(total_no_listings.replace(",", ""))

      #Call the function to extract the data from the html
      data_retrieval_development(properties_html)

      # For development purposes to show I am actually scraping
      print(f"{pages + 1} pages scraped")
      print(f"You have {total_no_listings - index} listings left")

      # Jump to the next page of properties on website
      index = index + 24

      #To stop the program when there are no more listings
      if index >= total_no_listings or index >= max_search:
        break



#Function to extract the more detailed information from each specific property
def detailed_info_scrape():
  #Iterate through all the properties found in the list of links
  property_no = 0
  while property_no < len(all_properties_links):

    property_link = all_properties_links[property_no]

    user_headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    request = requests.get(property_link, headers=user_headers)
    request.raise_for_status()

    #This receives the html of the property web page using the BeautifulSoup library
    property_html = BeautifulSoup(request.text, "html.parser")
    properties_html = property_html.find_all("p", class_="_1hV1kqpVceE9m-QrX_hWDN")


    #This validates that all information is present otherwise I discard
    if len(properties_html)!= 5:
      all_properties_links.pop(property_no)
      all_properties_price.pop(property_no)
      all_properties_address.pop(property_no)

    #This will extract the information and append to the relevant list
    else:
      all_properties_type.append(properties_html[0].get_text().strip())
      all_properties_bedrooms.append(properties_html[1].get_text().strip())
      all_properties_bathrooms.append(properties_html[2].get_text().strip())
      size = properties_html[3].get_text().strip()
      # Validate if the size is present or not
      if size == "Ask agent":
        all_properties_size.append(-1)
      else:
        all_properties_size.append(int(size[:-6]))
      property_no+=1

#Function to create a dataset from the lists
def dataset_creation():
  data = {
      "Address": all_properties_address,
      "Type": all_properties_type,
      "Bedrooms": all_properties_bedrooms,
      "Bathrooms": all_properties_bathrooms,
      "Size": all_properties_size,
      "Price": all_properties_price
  }

  # Write the data to a csv file
  df = pd.DataFrame.from_dict(data)
  df.to_csv(r"london_house_price_data.csv", encoding="utf-8", header="true", index = False)

#Main function from which all other functions are called
def webScraper():
  property_scraping(1000)
  detailed_info_scrape()
  dataset_creation()

