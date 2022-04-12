from gpsdclient import GPSDClient
import sys

client = GPSDClient(host="127.0.0.1")

for result in client.dict_stream(convert_datetime=True):
    if result["class"] == "TPV":
        print("Latitude: %s" % result.get("lat", "n/a"))
        print("Longitude: %s" % result.get("lon", "n/a"))

sys.exit(0)
