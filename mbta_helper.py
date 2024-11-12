#Used ChatGPT Help


import os



from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


import requests
# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return {}






def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
     # Build the full API URL for Mapbox Geocoding
    url = f"{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}"
    print(url)
    
    # Send GET request to Mapbox API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        if features:
            # Get the coordinates (longitude, latitude) from the first feature
            coordinates = features[0].get('geometry', {}).get('coordinates', [])
            if len(coordinates) == 2:
                longitude, latitude = coordinates
                return str(latitude), str(longitude)
        else:
            print(f"Error: No features found for place '{place_name}'")
            return None
    else:
        print(f"Error: Unable to fetch data from Mapbox. Status code: {response.status_code}")
        return None



def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?filter[latitude]={latitude}&filter[longitude]={longitude}&api_key={MBTA_API_KEY}"

    # Send GET request to MBTA API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        stops = data.get('data', [])
        
        if stops:
            # Assuming the stops are ordered by proximity, use the first one
            nearest_stop = stops[0]
            station_name = nearest_stop.get('attributes', {}).get('name', "Unknown")
            wheelchair_accessible = nearest_stop.get('attributes', {}).get('wheelchair_boarding', False)
            return station_name, wheelchair_accessible
        else:
            print(f"Error: No stops found near coordinates ({latitude}, {longitude})")
            return None
    else:
        print(f"Error: Unable to fetch data from MBTA. Status code: {response.status_code}")
        return None



def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
      # Step 1: Get latitude and longitude for the place
    lat_lng = get_lat_lng(place_name)
    
    if lat_lng:
        latitude, longitude = lat_lng
        
        # Step 2: Get the nearest station using the latitude and longitude
        return get_nearest_station(latitude, longitude)
    else:
        print("Error: Unable to get latitude and longitude for the place.")
        return None


def main():
    """
    You should test all the above functions here
    """
     # Test case 1: Geocoding a place name
    place_name = " Prudential Center, Boston"
    print(f"Testing get_lat_lng for place: '{place_name}'")
    lat_lng = get_lat_lng(place_name)
    if lat_lng:
        print(f"Latitude and Longitude for '{place_name}': {lat_lng}")
    else:
        print("Failed to get latitude and longitude.")
    
    # # Test case 2: Find nearest station for given latitude and longitude
    if lat_lng:
        latitude, longitude = lat_lng
        print(f"\nTesting get_nearest_station with coordinates: Latitude: {latitude}, Longitude: {longitude}")
        station_info = get_nearest_station(latitude, longitude)
        if station_info:
            station_name, wheelchair_accessible = station_info
            print(f"Nearest Station: {station_name}")
            print(f"Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}")
        else:
            print("Failed to get nearest station.")
    
    # # Test case 3: Find nearest station by place name using the find_stop_near function
    print(f"\nTesting find_stop_near for place: '{place_name}'")
    station_info = find_stop_near(place_name)
    if station_info:
        station_name, wheelchair_accessible = station_info
        print(f"Nearest Station: {station_name}")
        print(f"Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}")
    else:
        print("Failed to find nearest station.")


if __name__ == "__main__":
    main()
