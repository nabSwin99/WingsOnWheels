import osmnx as ox
import networkx as nx
import folium
from geopy.geocoders import Nominatim
from folium.plugins import BeautifyIcon




def generate_route_map():
    # Configure osmnx settings
    ox.settings.log_console = True
    ox.settings.use_cache = True
    # Initialize Nominatim Geolocator with a user-agent name
    locator = Nominatim(user_agent="myapp")

    # Define addresses for start and end locations
    start_location = "593 Glenferrie Rd, Hawthorn VIC 3122"
    end_location = "John St, Hawthorn VIC 3122"

    # Geocode addresses to get latitude and longitude
    start_point = locator.geocode(start_location).point
    end_point = locator.geocode(end_location).point

    # Extract latitude and longitude from geopy Point
    start_latlng = (start_point.latitude, start_point.longitude)
    end_latlng = (end_point.latitude, end_point.longitude)

    # Specify the location and mode for creating the graph
    place = 'melbourne, victoria, australia'
    mode = 'drive'  # Options: 'drive', 'bike', 'walk', 'drone'
    optimizer = 'length'  # Options: 'length', 'time'

    if mode != 'drone':
            # Generate a graph from OpenStreetMap data
            graph = ox.graph_from_place(place, network_type=mode)

            # Find the nearest nodes to the start and end points
            orig_node = ox.distance.nearest_nodes(graph, start_latlng[1], start_latlng[0])
            dest_node = ox.distance.nearest_nodes(graph, end_latlng[1], end_latlng[0])

            # Compute the shortest path
            shortest_route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer)
    
            # Create a map to display the route
            route_map = ox.plot_route_folium(graph, shortest_route, tiles='openstreetmap')

    else:
         # Create a map centered around the start location
         route_map = folium.Map(location=start_latlng, zoom_start=15, tiles='openstreetmap')
         # Draw a line between start and end locations
         folium.PolyLine([start_latlng, end_latlng], color="blue", weight=5, opacity=0.7).add_to(route_map)


    # Add markers for the start and end locations
    icon_start = BeautifyIcon(icon='plane', background_color='green', icon_shape='circle')
    icon_end = BeautifyIcon(icon='flag-checkered', background_color='red', icon_shape='circle')
    start_marker = folium.Marker(location=start_latlng, popup=start_location, icon=icon_start)
    end_marker = folium.Marker(location=end_latlng, popup=end_location, icon=icon_end)
    start_marker.add_to(route_map)
    end_marker.add_to(route_map)
    return route_map

            

def save_map(route_map, filename='route_map.html'):
    route_map.save(filename)
    return filename