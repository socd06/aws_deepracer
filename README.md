# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207)

### Reward Function
```python
def reward_function(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car in the right direction but also using the steering angle to make the car go faster on straight lines
    '''
    import math
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    #also read steering 
    steering = abs(params['steering_angle']) # We don't care whether it is left or right steering
    STEERING_THRESHOLD = 20.0
    
    # Initialize the reward depending on steering
    if steering > STEERING_THRESHOLD: #penalize if steering
        reward *= 0.8
    else:
        reward = 1.0 #reward if not steering

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

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    return reward
```
