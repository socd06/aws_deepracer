def reward_function(params):
    ###################################################################
    '''
    Customized reward function using waypoints and heading to make the car in the right direction and incentivizing going fast and finishing laps
    '''
    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    is_left_of_center = params['is_left_of_center']
    
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
    
    # Initialize the reward
    reward = 1e-3 #very little but not 0, cero means crashed
    
    #Initialize thresholds
    #SPEED_THRESHOLD will depend on the agent's action space
    SPEED_THRESHOLD = 2.67 
    DIRECTION_THRESHOLD = 30 #Originally 10
    
    if speed > SPEED_THRESHOLD:
        reward += 20
    
    if direction_diff < DIRECTION_THRESHOLD:
        reward += 30
        
    if is_left_of_center == True:
        reward += 30
        
    if all_wheels_on_track == True:
        reward += 20
    
    #Incentivize finishing laps
    if progress == 100: 
        reward += 1000
    elif progress == 25 or progress == 50 or progress == 75:
        reward += progress
    #Max reward is 100 + 10000 if completed full lap
    return reward