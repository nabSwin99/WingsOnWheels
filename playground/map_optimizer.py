import osmnx as ox
import networkx as nx
import folium
from geopy.geocoders import Nominatim
from folium.plugins import BeautifyIcon
from django.shortcuts import render
from django.http import HttpResponse
import json


def generate_route_map(request1):
    # Configure osmnx settings
    ox.settings.log_console = True
    ox.settings.use_cache = True
    # Initialize Nominatim Geolocator with a user-agent name
    locator = Nominatim(user_agent="myapp")

    # Define addresses for start and end locations
    start_location = "593 Glenferrie Rd, Hawthorn VIC 3122"
    end_location = request1.user.customer.address
    if request1.user.is_authenticated:
        # User is logged in
        # Access user attributes
        address = request1.user.customer.address
        end_location = address
    else:
        # User is not logged in
        return render(request1, 'login.html')
    
    # Geocode addresses to get latitude and longitude
    start_point = locator.geocode(start_location).point
    end_point = locator.geocode(end_location).point
    print("hello")
    print(end_point)

    # Extract latitude and longitude from geopy Point
    start_latlng = (start_point.latitude, start_point.longitude)
    end_latlng = (end_point.latitude, end_point.longitude)

    # Specify the location and mode for creating the graph
    place = 'melbourne, victoria, australia'
    mode = 'drone'  # Options: 'drive', 'bike', 'walk', 'drone'
    optimizer = 'length'  # Options: 'length', 'time'

    if mode != 'drone':
            # Generate a graph from OpenStreetMap data
            graph = ox.graph_from_place(place, network_type=mode)

            # Find the nearest nodes to the start and end points
            orig_node = ox.distance.nearest_nodes(graph, start_latlng[1], start_latlng[0])
            dest_node = ox.distance.nearest_nodes(graph, end_latlng[1], end_latlng[0])

            # Compute the shortest path
            shortest_route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer)
            route_points = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_route]

    
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
    route_map.save('route_map.html')
    return route_map

            

from geopy.geocoders import Nominatim

def create_map_html(request2, filename, start_location, end_location, order, cart_details):
    locator = Nominatim(user_agent="myapp")
    customer_name = request2.user.first_name
    order_id = order.id

    cart_details = cart_details
 



    start_point = locator.geocode(start_location)
    end_point = locator.geocode(end_location)

    # Check if geocoding failed
    if not start_point or not end_point:
        return "Geocoding failed. Check the addresses provided."

    # Extract latitude and longitude from the geocoded points
    start_point_coords = [start_point.latitude, start_point.longitude]
    end_point_coords = [end_point.latitude, end_point.longitude]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delivery Tracking Map</title>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f4f4;
        }}
        .container-fluid {{
            padding-right: 0;
            padding-left: 0;
            margin-right: auto;
            margin-left: auto;
        }}
        #map {{
            height: 60vh; /* Reduced height */
            width: 94%; /* Full width */
            margin-left: 3%;
        
        }}

        #cartContainer {{
            background-color: white;
            padding: 20px;
            margin: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 90%;
            margin-left: auto;
            margin-right: auto;
        }}
        #cartTable {{
            width: 100%;
            border-collapse: collapse;
        }}
        #cartTable th, #cartTable td {{
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        #cartTable th {{
            background-color: #4CAF50;
            color: white;
        }}
        #totalPrice {{
            text-align: right;
            font-weight: bold;
        }}
        #info {{
            text-align: center;
            font-size: larger; /* Increase the font size for better readability */
            margin-top: 20px;
            padding: 10px;
            background-color: #fff; /* Optional: white background for contrast */
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Soft shadow for depth */
            max-width: 400px; /* Restrict the width for better layout */
            margin: 20px auto; /* Center align the block */
        }}

        #info p {{
            margin: 10px 0; /* Add some vertical spacing between the lines */
            color: #333; /* Darker text for better readability */
            font-weight: bold; /* Optional: bold font for emphasis */
        }}
    </style>


    </head>
    <div class="container">
        <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
        <div class="col-md-3 mb-2 mb-md-0">
            Meals on Wings
        </div>

        <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <h5> Your order with ID:{order_id} is on the way...</h5>
        </ul>

        <div class="col-md-3 text-end">

        Hello, {customer_name}
    
        </div>
        </header>
    </div>
    <body>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <div class="container-fluid">
        <div id="map"></div>
        <div id="info">
            <p>Distance Left: <span id="distance-left">Calculating...</span></p>
            <p>Time Left: <span id="time-left">Calculating...</span></p>
        </div>
    </div>
        <script>
            var map = L.map('map').setView([-37.814, 144.96332], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: 'Map data &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }}).addTo(map);

            var droneIcon = L.icon({{
                iconUrl: 'https://cdn-icons-png.flaticon.com/512/8169/8169618.png',
                iconSize: [50, 50],
                iconAnchor: [25, 25]
            }});

            var startIcon = L.icon({{
                iconUrl: '/static/images/store.png',
                iconSize: [50, 50],
                iconAnchor: [25, 50]
            }});

            var endIcon = L.icon({{
                iconUrl: '/static/images/destination_marker.png',
                iconSize: [50, 50],
                iconAnchor: [25, 50]
            }});

            var startCoords = {start_point_coords};
            var endCoords = {end_point_coords};

            function interpolatePoints(start, end, numberOfPoints) {{
                var points = [start];
                for (var i = 1; i < numberOfPoints; i++) {{
                    var fraction = i / numberOfPoints;
                    var lat = start[0] + fraction * (end[0] - start[0]);
                    var lng = start[1] + fraction * (end[1] - start[1]);
                    points.push([lat, lng]);
                }}
                points.push(end);
                return points;
            }}

            var routePoints = interpolatePoints(startCoords, endCoords, 10);
            var polyline = L.polyline(routePoints, {{color: 'blue'}}).addTo(map);
            map.fitBounds(polyline.getBounds());

            L.marker(startCoords, {{icon: startIcon}}).addTo(map).bindPopup("Start Point");
            L.marker(endCoords, {{icon: endIcon}}).addTo(map).bindPopup("End Point");

            var movingMarker = L.marker(routePoints[0], {{icon: droneIcon}}).addTo(map);
            var counter = 0;
            function moveMarker() {{
                if (counter < routePoints.length) {{
                    movingMarker.setLatLng(new L.LatLng(routePoints[counter][0], routePoints[counter][1]));
                    map.panTo(new L.LatLng(routePoints[counter][0], routePoints[counter][1]));
                    var remainingDistance = 0;
                    for (var j = counter; j < routePoints.length - 1; j++) {{
                        remainingDistance += map.distance(routePoints[j], routePoints[j + 1]);
                    }}

                    document.getElementById('distance-left').textContent = remainingDistance.toFixed(2) + ' meters';
                    var speed = 50; // meters per minute
                    var timeLeft = remainingDistance / speed; // minutes
                    document.getElementById('time-left').textContent = timeLeft.toFixed(2) + ' minutes';

                    counter++;
                    setTimeout(moveMarker, 2000);
                }} else {{
                    var modal = new bootstrap.Modal(document.getElementById('deliveryCompleteModal'));
                    modal.show();
                }}
            }}

            function redirectToNext() {{
                window.location.href = 'order_delivered'; // Triggering the order_delivered view to change order status.
            }}



        moveMarker(); //Executing the drone simulation.
        </script>

<div id="cartContainer">
    <h1>Your Cart</h1>
    <table id="cartTable">
        <thead>
            <tr>
                <th>Item</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <!-- JavaScript will dynamically insert rows here -->
        </tbody>
        <tfoot>
            <tr>
                <td colspan="3" style="text-align: right;">Total Price:</td>
                <td id="totalPrice"></td>
            </tr>
        </tfoot>
    </table>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {{
    // Assuming cart_details is already defined in your script as a global variable
    var cartItems = {cart_details};  // Directly use the variable if it's included as a script in your page

    // Check the structure of cartItems to ensure it's loaded correctly
    console.log(cartItems);

    if (cartItems && Array.isArray(cartItems.items)) {{
        var tableBody = document.getElementById('cartTable').getElementsByTagName('tbody')[0];
        var totalPrice = 0;  // Initialize total price

        cartItems.items.forEach(function(item) {{
            var row = tableBody.insertRow();
            row.insertCell(0).innerHTML = item.name;
            row.insertCell(1).innerHTML = '$' + parseFloat(item.price).toFixed(2);
            row.insertCell(2).innerHTML = item.quantity;
            row.insertCell(3).innerHTML = '$' + parseFloat(item.total).toFixed(2);
            totalPrice += parseFloat(item.total);  // Calculate total price from item totals
        }});

        document.getElementById('totalPrice').innerHTML = '$' + totalPrice.toFixed(2);
    }} else {{
        console.error('Items is not an array or cartItems is undefined');
    }}
}});
</script>

    <!-- Delivery Complete Modal -->
    <div class="modal fade" id="deliveryCompleteModal" tabindex="-1" aria-labelledby="deliveryCompleteModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="deliveryCompleteModalLabel">Delivery Complete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" onclick="redirectToNext()"></button>

        </div>
        <div class="modal-body">
            Your order has been delivered successfully!
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" onclick="redirectToNext()">OK</button>
        </div>
        </div>
    </div>
    </div>





    </body>
    </html>

    """
    # Write HTML to file
    with open(filename, 'w') as file:
         file.write(html_content)
    return f"Map has been saved as {filename}"