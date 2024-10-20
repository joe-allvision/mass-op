#!/usr/bin/env python3

import math
from pymavlink import mavutil

# Class for formatting the mission items
class mission_item:
    def __init__(self, seq, x, y, z):
        self.seq = seq
        self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        self.current = 0
        self.autocontinue = 1
        self.param1 = 0.0  # Hold time
        self.param2 = 0.0
        self.param3 = 0.0
        self.param4 = math.nan
        self.x = x  # Latitude
        self.y = y  # Longitude
        self.z = z  # Altitude
        self.mission_type = 0

# Function to acknowledge MAVLink messages
def ack(the_connection, message_type):
    print(f":: Waiting for {message_type} ::")
    message = the_connection.recv_match(type=message_type, blocking=True)
    print(f":: {message_type} Received :: {message}")

# Function to upload the mission to the drone
def upload_mission(the_connection, mission_items):
    print(":: Sending Mission Out ::")
    the_connection.mav.mission_clear_all_send(the_connection.target_system, the_connection.target_component, 0)
    ack(the_connection, "MISSION_REQUEST")
    for waypoint in mission_items:
        print(":: Creating a waypoint ::")
        the_connection.mav.mission_item_send(the_connection.target_system, the_connection.target_component,
                                             waypoint.seq, waypoint.frame, waypoint.command, waypoint.current,
                                             waypoint.autocontinue, waypoint.param1, waypoint.param2,
                                             waypoint.param3, waypoint.param4, waypoint.x, waypoint.y, waypoint.z,
                                             waypoint.mission_type)


# Function to arm the drone
def arm_the_connection(the_connection):
    print(":: Arming ::")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    ack(the_connection, "COMMAND_ACK")

# Function to initiate takeoff
def takeoff(the_connection):
    print(":: Takeoff Initiated ::")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, math.nan, 0, 0, 10)
    ack(the_connection, "COMMAND_ACK")


# Function to set return to launch
def set_return(the_connection):
    print(":: Set Return to Launch ::")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)

# Function to start the mission
def start_mission(the_connection):
    print(":: Mission Start!")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)
    ack(the_connection, "COMMAND_ACK")

# Main function to start the program
if __name__ == "__main__":
    print(":: Program Started ::")
    the_connection = mavutil.mavlink_connection('udp:localhost:14550')

    while the_connection.target_system == 0:
        print(":: Checking heartbeat ::")
        the_connection.wait_heartbeat()
        print(f":: Heartbeat from system {the_connection.target_system} {the_connection.target_component} ::")

    mission_waypoints = [
        mission_item(0, 40.6992, -74.0545, 50),
        mission_item(1, 40.6992, -74.0345, 50),
        mission_item(2, 40.6892, -74.0345, 50),
        mission_item(3, 40.6792, -74.0345, 50),
        mission_item(4, 40.6792, -74.0545, 50),
        mission_item(5, 40.6892, -74.0545, 50)
    ]

    upload_mission(the_connection, mission_waypoints)
    arm_the_connection(the_connection)
    takeoff(the_connection)
    start_mission(the_connection)

    for waypoint in mission_waypoints:
        print(":: Mission Item Reached :: " + str(the_connection.recv_match(type='MISSION_ITEM_REACHED', blocking=True)))

    set_return(the_connection)
    
# #!/usr/bin/env python3

# import time
# from pymavlink import mavutil

# # Initialize the connection to QGroundControl
# def init_connection():
#     # Creates a UDP connection on a port which QGroundControl listens to
#     return mavutil.mavlink_connection('udpout:localhost:14550', source_system=255)

# # Send a heartbeat to QGroundControl
# def send_heartbeat(the_connection):
#     while True:
#         the_connection.mav.heartbeat_send(
#             mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
#             mavutil.mavlink.MAV_AUTOPILOT_INVALID,  # No autopilot
#             0, 0, 0, 0
#         )
#         print("Heartbeat sent to QGroundControl")
#         time.sleep(1)  # Send heartbeat every 1 second

# # Define waypoints and send them as a mission to QGroundControl
# def send_waypoints(the_connection):
#     waypoints = [
#         [40.6992, -74.0545, 50],
#         [40.6992, -74.0345, 50],
#         [40.6892, -74.0345, 50],
#         [40.6792, -74.0345, 50],
#         [40.6792, -74.0545, 50],
#         [40.6892, -74.0545, 50]
#     ]
    
#     # Home and landing location close to the waypoints
#     home_location = [40.6892, -74.0445, 50]  # This location is approximately in the center of the waypoint loop

#     # Clear any existing mission
#     the_connection.mav.mission_clear_all_send(the_connection.target_system)

#     # Send home location as the first waypoint
#     the_connection.mav.mission_item_send(
#         the_connection.target_system,
#         the_connection.target_component,
#         0,  # sequence number
#         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
#         mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
#         2,  # current
#         1,  # autocontinue
#         0, 0, 0, 0,  # params
#         home_location[0], home_location[1], home_location[2]
#     )
#     print(f"Home Location set at: Latitude {home_location[0]}, Longitude {home_location[1]}, Altitude {home_location[2]}")

#     # Send waypoints as mission items
#     for i, waypoint in enumerate(waypoints, start=1):
#         lat, lon, alt = waypoint
#         the_connection.mav.mission_item_send(
#             the_connection.target_system,
#             the_connection.target_component,
#             i,
#             mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
#             mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
#             0, 1,  # current, autocontinue
#             0, 0, 0, 0,  # params
#             lat, lon, alt
#         )
#         print(f"Waypoint {i} sent: Latitude {lat}, Longitude {lon}, Altitude {alt}")
#         time.sleep(0.5)  # Delay to ensure waypoints are not sent too quickly

# if __name__ == "__main__":
#     print(":: Program Started ::")
#     connection = init_connection()
#     # Consider running heartbeat in a separate thread if you want non-blocking behavior
#     send_heartbeat(connection)  # Can be in a thread
#     send_waypoints(connection)

# # #!/usr/bin/env python3

# # import math
# # from pymavlink import mavutil

# # # Class for formatting the mission items
# # class mission_item:
# #     def __init__(self, seq, x, y, z):
# #         self.seq = seq
# #         self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT  # Use Global Latitude and Longitude for position data
# #         self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT  # Move to the waypoint
# #         self.current = 0
# #         self.autocontinue = 1
# #         self.param1 = 0.0  # Hold time
# #         self.param2 = 0.0
# #         self.param3 = 0.0
# #         self.param4 = math.nan
# #         self.x = x  # Latitude
# #         self.y = y  # Longitude
# #         self.z = z  # Altitude
# #         self.mission_type = 0  # The MAV_MISSION_TYPE value for MAV_MISSION_TYPE_MISSION

# # # Arm the Drone
# # def arm_the_connection(the_connection):
# #     print(":: Arming ::")
# #     the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
# #                                          mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
# #     ack(the_connection, "COMMAND_ACK")

# # # Takeoff the Drone
# # def takeoff(the_connection):
# #     print(":: Takeoff Initiated ::")
# #     the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
# #                                          mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, math.nan, 0, 0, 10)
# #     ack(the_connection, "COMMAND_ACK")

# # # Upload the mission to the drone
# # def upload_mission(the_connection, mission_items):
# #     print(":: Sending Mission Out ::")
# #     the_connection.mav.mission_clear_all_send(the_connection.target_system, the_connection.target_component, 0)
# #     ack(the_connection, "MISSION_REQUEST")
# #     for waypoint in mission_items:
# #         print(":: Creating a waypoint ::")
# #         the_connection.mav.mission_item_send(the_connection.target_system, the_connection.target_component,
# #                                              waypoint.seq, waypoint.frame, waypoint.command, waypoint.current,
# #                                              waypoint.autocontinue, waypoint.param1, waypoint.param2,
# #                                              waypoint.param3, waypoint.param4, waypoint.x, waypoint.y, waypoint.z,
# #                                              waypoint.mission_type)

# # # Acknowledge MAVLink messages
# # def ack(the_connection, message_type):
# #     print(f":: Waiting for {message_type} ::")
# #     message = the_connection.recv_match(type=message_type, blocking=True)
# #     print(f":: {message_type} Received :: {message}")

# # # Set Return to Launch
# # def set_return(the_connection):
# #     print(":: Set Return to Launch ::")
# #     the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
# #                                          mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)

# # # Start the mission
# # def start_mission(the_connection):
# #     print(":: Mission Start!")
# #     the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
# #                                          mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)
# #     ack(the_connection, "COMMAND_ACK")

# # # Main function to start the program
# # if __name__ == "__main__":
# #     print(":: Program Started ::")
# #     the_connection = mavutil.mavlink_connection('udp:localhost:14540')

# #     while the_connection.target_system == 0:
# #         print(":: Checking heartbeat ::")
# #         the_connection.wait_heartbeat()
# #         print(f":: Heartbeat from system {the_connection.target_system} {the_connection.target_component} ::")

# #     mission_waypoints = [
# #         mission_item(0, 42.44319622718235, -83.9996183573619, 10),  # Above takeoff point
# #         mission_item(1, 42.4432743767685, -83.99614352948624, 10),   # Above Destination Point
# #         mission_item(2, 42.4432743767685, -83.99614352948624, 5)     # Destination Point
# #     ]

# #     upload_mission(the_connection, mission_waypoints)
# #     arm_the_connection(the_connection)
# #     takeoff(the_connection)
# #     start_mission(the_connection)

# #     for waypoint in mission_waypoints:
# #         print(":: Mission Item Reached :: " + str(the_connection.recv_match(type='MISSION_ITEM_REACHED', blocking=True)))

# #     set_return(the_connection)