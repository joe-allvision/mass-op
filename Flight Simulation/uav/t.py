# Helper functions to simulate data retrieval
def get_telemetry_data(data_type):
    # Simulated telemetry data
    telemetry_data = {
    "GPS": {"latitude": 37.7749, "longitude": -122.4194},
    "altitude": 1200, # in meters
    "battery": 85, # in percentage
    "flight_mode": "AUTO",
    "speed": 45,
    # in m/s
    "heading": 90
    # in degrees
    }
    return telemetry_data.get(data_type, "Data type not available")

print(get_telemetry_data("GPS")) # {'latitude': 37.7749, 'longitude': -122.4194}