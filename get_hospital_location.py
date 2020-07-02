from googleplaces import GooglePlaces, types, lang

API_KEY = "ENTER YOUR API KEY"
google_places = GooglePlaces(API_KEY)

query_result = google_places.nearby_search(
    lat_lng={'lat': 30, 'lng': -8039728},
    radius=5000, types=[types.TYPE_HOSPITAL])


if query_result.has_attributions:
    print(query_result.html_attributions)

# Iterate over the search results
for place in query_result.places:
    print(place.name)
    print("Latitude", place.geo_location['lat'])
    print("Longitude", place.geo_location['lng'])
    print()