# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207)

### Model Name
AWSDeepRacer2020-waypoints-allwheels-steering-speed

### Training job description
Rewards being close to waypoints, having all wheels on track, and going fast plus max reward on straight lines (no steering). 
3-layer CNN, front-facing camera. Trained on Cumulo carrera track.

### Reward Function
```python
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
    #also read steering 
    steering = abs(params['steering_angle']) # We don't care whether it is left or right steering
    STEERING_THRESHOLD = 20.0
    #update to also read wheels on track and speed
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    SPEED_THRESHOLD = 1.0 

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
    
    DIRECTION_THRESHOLD = 10.0
    
    if direction_diff > DIRECTION_THRESHOLD: # Penalize if the difference is too large
        reward *= 0.5 # reward = reward *0.5
        if not all_wheels_on_track: # Penalize more if the car is going off track
            reward *= 0.5
            
    elif direction_diff < DIRECTION_THRESHOLD: # Reward if close to waypoints
        reward *= 2.0 
        if all_wheels_on_track == True: # Reward more if all wheels are in the track
            reward *= 2.0
            if steering < STEERING_THRESHOLD: #Max Reward when not steering (straight lines)
                reward *= 2.0
    
    elif speed > SPEED_THRESHOLD: # High reward if the car stays on track and goes fast
        reward *= 2.0
    else: # Penalize if the car goes too slow
        reward *= 0.5
        
    return reward
```

## Hyper-parameter tuning

Changed learning rate to 0.0007 to save training time.