import time
from pymavlink import mavutil 

def connect_to_vehicle():
    # Connect to the vehicle
    connection_string = 'udp:127.0.0.1:14591'
    vehicle = mavutil.mavlink_connection(connection_string)
    vehicle.wait_heartbeat()
    print('Connected to vehicle!')

    return vehicle

def calibrate_accel_gyro(vehicle):
    # Calibrate gyroscope using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, 0, 1, 0, 0, 0, 0, 0, 0)
    print('Send gyroscope calibration...')
    time.sleep(5)  # Wait for calibration to complete

    # Calibrate accelerometer using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, 0, 0, 0, 0, 0, 4, 0, 0)
    print('Send simple accelerometer calibration...')

    # Calibrate accelerometer using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION, 0, 0, 1, 0, 0, 0, 0, 0)
    print('Send magnetometer calibration...')
    time.sleep(5)  # Wait for calibration to complete


def arm_vehicle(vehicle):
    AP_GUIDED_MODE_FLAG = 4
    # Change vehicle mode to GUIDED using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, AP_GUIDED_MODE_FLAG, 0, 0, 0, 0, 0)
    print('Changing vehicle mode to GUIDED...')
    time.sleep(1)  # Wait for mode change to complete

    # Arm the vehicle
    print('Arming the vehicle...')
    # Arm the vehicle using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    # Wait for arming command response
    while True:
        msg = vehicle.recv_match(type='COMMAND_ACK', blocking=False)
        if msg.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM and msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print('Vehicle armed!')
            break
        else:
            vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        time.sleep(0.5)  

def set_home(vehicle):
    # Wait until good GPS lock is obtained
    while True:
        msg = vehicle.recv_match(type='GPS_RAW_INT', blocking=True)
        if msg.fix_type >= 3:  # Check if fix type is 3 or higher (good GPS lock)
            print('Good GPS lock obtained!')
            break
        time.sleep(1)
    # Get current latitude, longitude, and altitude using MAVLink message
    msg = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    current_lat = msg.lat / 1e7
    current_lon = msg.lon / 1e7
    current_alt = msg.alt / 1000.0  # Convert from millimeters to meters

    # Set home position using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 0, 0, 0, current_lat, current_lon, current_alt)

    print(f'Set home position to: Lat={current_lat}, Lon={current_lon}, Alt={current_alt} m')

def takeoff(vehicle, target_altitude):

    # Send takeoff command using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, target_altitude)
    print('Sending takeoff command...')

    while True:
        # Get current altitude using MAVLink message
        msg = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        current_altitude = msg.relative_alt / 1000.0  # Convert from millimeters to meters
        print(f'Current altitude: {current_altitude} m')
        if current_altitude >= target_altitude * 0.98:
            print('Reached target altitude')
            break
        time.sleep(0.001)

def return_to_launch(vehicle):
    # Send return to launch command using MAVLink command long
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)
    print('Sending return to launch command...')

    # check local frame position in North and east and check if it is close to home position
    while True:
        msg = vehicle.recv_match(type='LOCAL_POSITION_NED', blocking=True)
        current_north = msg.x
        current_east = msg.y
        if abs(current_north) < 0.5 and abs(current_east) < 0.5:
            print('Reached home position')
            break
        time.sleep(0.001)

def navigate_to_NEDposition(vehicle, north, east, down):
    # Send position using SET_POSITION_TARGET_LOCAL_NED command
    vehicle.mav.set_position_target_local_ned_send(
        0,  # time_boot_ms
        vehicle.target_system,  # target_system
        vehicle.target_component,  # target_component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111111000,  # type_mask (only positions enabled)
        north,  # x
        east,  # y
        down,  # z
        0, 0, 0,  # vx, vy, vz
        0, 0, 0,  # afx, afy, afz
        0, 0)  # yaw, yaw_rate
    print(f'Sending navigation command to position: North={north} m, East={east} m, Down={down} m')

    while True:
        # Get current position using MAVLink message
        msg = vehicle.recv_match(type='LOCAL_POSITION_NED', blocking=True)
        current_north = msg.x
        current_east = msg.y
        current_down = msg.z
        print(f'Current position: North={current_north:.3f} m, East={current_east:.3f} m, Down={current_down:.3f} m')
        if abs(current_north - north) < 0.1 and abs(current_east - east) < 0.1 and abs(current_down - down) < 0.1:
            print('Reached target position')
            break
        time.sleep(0.001)

def navigate_to_LLAposition(vehicle, latitude, longitude, altitude):
    # Send position using SET_POSITION_TARGET_GLOBAL_INT command
    vehicle.mav.set_position_target_global_int_send(
        0,  # time_boot_ms
        vehicle.target_system,  # target_system
        vehicle.target_component,  # target_component
        mavutil.mavlink.MAV_FRAME_GLOBAL_INT,  # frame
        0b0000111111100000,  # type_mask (only positions enabled)
        int(latitude * 1e7),  # lat_int
        int(longitude * 1e7),  # lon_int
        altitude,  # alt
        15, 15, 0,  # vx, vy, vz
        0, 0, 0,  # afx, afy, afz
        0, 0)  # yaw, yaw_rate
    print(f'Sending navigation command to position: Lat={latitude:.3f}, Lon={longitude:.3f}, Alt={altitude:.3f} m')

    while True:
        # Get current position using MAVLink message
        msg = vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        current_lat = msg.lat / 1e7
        current_lon = msg.lon / 1e7
        current_alt = msg.alt / 1000.0  # Convert from millimeters to meters
        print(f'Current position: Lat={current_lat}, Lon={current_lon}, Alt={current_alt} m')
        if abs(current_lat - latitude) < 0.0001 and abs(current_lon - longitude) < 0.0001 and abs(current_alt - altitude) < 0.1:
            print('Reached target position')
            break
        time.sleep(0.001)

def land(vehicle):
        # Send land command using MAVLink command long
        #vehicle.mav.command_long_send(
        #    vehicle.target_system, vehicle.target_component,
        #    mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)
        #print('Sending land command...')
        # Or can send command long to change mode to LAND
        vehicle.mav.command_long_send(
            vehicle.target_system, vehicle.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 9, 0, 0, 0, 0, 0)
        print('Changing vehicle mode to LAND...')
        time.sleep(1)  # Wait for mode change to complete

def fly(waypoints):
    vehicle = connect_to_vehicle()

    # Set the home LLA of the vehicle
    set_home(vehicle)

    # Calibrate the Accel and Gyro
    calibrate_accel_gyro(vehicle)

    # Arm the vehicle
    arm_vehicle(vehicle)

    # Takeoff to 20 meters
    takeoff(vehicle, 20)

    # Navigate to a position in local NED frame
    # navigate_to_NEDposition(vehicle, 10, 60, -50)
    # time.sleep(1)

    # waypoints = [
    #     [40.778314, -73.305668, 50],
    #     [40.777814, -73.304668, 50],
    #     [40.777594, -73.305668, 50],
    #     [40.777814, -73.306468, 50],
    #     [40.778042, -73.305940, 50],
    # ]

    for lat, lon, alt in waypoints:
        navigate_to_LLAposition(vehicle, lat, lon, alt)

    # Navigate to position in global LLA frame
    # navigate_to_LLAposition(vehicle, 40.777372, -73.3205297, 100)
    time.sleep(1)

    # Return to launch position
    return_to_launch(vehicle)

    # Land the vehicle
    land(vehicle)

# if __name__ == '__main__':
#     main()