from geopy.geocoders import OpenCage
from geopy.distance import geodesic


DICTS = {
    3: 0,
    5: 500,
    10: 700,
}

class DistanceCheack:
    price = 0.0
    distance = 0.0
    api_key = '79cce39ecda14a94948e79ef92a8ce7f'
    loc1 = "Златоуст ул. Румянцева 95"

    def __init__(self, loc2):
        self.loc2 = loc2

    def get_distance(self):
        geolocator = OpenCage(self.api_key)
        loc1 = geolocator.geocode(self.loc1)
        loc2 = geolocator.geocode(self.loc2)
        if loc1 is not None and loc2 is not None:
            distance = geodesic((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).km
            return distance
        else:
            print("One or both locations not found.")

    def get_price(self, distance):
        distance = self.get_distance()
        for key, value in DICTS.items():
            if distance <= key:
                self.price = value
                break

def start(adres: str):
    d = DistanceCheack(adres)
    distance = d.get_distance()
    d.get_price(distance)
    return d.price


start("Златоуст ул. Аносова 275")



# print(f"Distance between the locations: {distance:.2f} km")

# Check if both locations were found
