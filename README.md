# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207)

### Model Name
AWSDeepRacer2020-advanced-reward-hyperparameters

### Training job description
3-layer CNN, front-facing camera. Trained on Cumulo carrera, re:Invent 2018, AWS Summit Raceway and 2019 Championship Cup tracks.

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
    #update to also read wheels on track and speed
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    #Read progress
    progress = params['progress']
    
    #Set thresholds
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
        reward = 1e-3
    
    if progress == 100: #Incentivize finishing laps
        reward += 10000
    
    return reward
```

## Hyper-parameters

Learning rate = 0.001
batch size = 32 
epochs = 5
entropy = 0.05
Discount factor = 0.999
Loss Type = Mean square error (already spent about 3 hours training, convergence should not be an issue)
Episodes = 30