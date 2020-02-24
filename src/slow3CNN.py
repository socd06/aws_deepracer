def reward_function(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car in the right direction
    '''
    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    #update to also read wheels on track and speed
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    SPEED_THRESHOLD = 1.0 
    HIGH_SPEED_THRESHOLD = 4.0

    # Initialize the reward
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    
    DIRECTION_THRESHOLD = 15.0
    CLOSE_DIRECTION_THRESHOLD = 5.0
    
    # Reward if close to waypoints
    if direction_diff < CLOSE_DIRECTION_THRESHOLD: #Reward more if closer to the center
        reward *= 4.0
    elif direction_diff < DIRECTION_THRESHOLD: #Still reward if close to waypoints
        reward *= 2.0 
    
    # Higher reward if the car goes faster
    elif speed > HIGH_SPEED_THRESHOLD: 
        reward *= 4.0
    elif speed > SPEED_THRESHOLD: # Still reward if car goes fast
        reward *= 2.0
    
    # Penalize if going away from waypoints, going off track or going slow 
    elif direction_diff > DIRECTION_THRESHOLD or speed < SPEED_THRESHOLD or all_wheels_on_track == False:  
        reward *= 0.01
    
    return reward