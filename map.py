import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from geopy.geocoders import Nominatim
from io import BytesIO

def display_map(postcode, label):
    #Fetch and display the map for a given postcode.
    geolocator = Nominatim(user_agent="pyqt_map_app")
    location = geolocator.geocode(postcode)  

    # Set the status message
    if location:
        latitude, longitude = location.latitude, location.longitude
        status_message = f"Location: {latitude}, {longitude}"
        
        # Fetch the static map with a pin at the location
        url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&z=14&l=map&size=600,400&pt={longitude},{latitude},pm2rdm"
        response = requests.get(url)

        # Load the map image if the request is successful
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).read())
            label.setPixmap(pixmap)
        else:
            status_message = "Error loading map image."
    else:
        status_message = "Location not found!"
    
    return status_message

def create_window(postcode):
    #Create the PyQt5 application window.
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QMainWindow()
    window.setWindowTitle("Map")
    window.setGeometry(100, 100, 800, 600)
    
    # Central widget for the window
    central_widget = QWidget(window)
    layout = QVBoxLayout(central_widget)

    # Label displaying postcode
    postcode_label = QLabel(f"Displaying map for postcode: {postcode}")
    layout.addWidget(postcode_label)

    # Label for displaying the map
    map_label = QLabel()
    map_label.setFixedSize(600, 400)
    layout.addWidget(map_label)
    
    # Button to close the window
    close_button = QPushButton("Close Map")
    close_button.clicked.connect(window.close)
    layout.addWidget(close_button)

    # Set the central widget
    window.setCentralWidget(central_widget)
    
    # Display the map immediately
    status_message = display_map(postcode, map_label)
    
    # Set the status message
    window.statusBar().showMessage(status_message)

    # Show the window
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    postcode = "SW3 1AJ"  # Example postcode
    create_window(postcode)


