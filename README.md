# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207)

### Model Name
AWSDeepRacer2020-fastest3L-tuned-hp

### Training job description
3-layer CNN, front-facing camera, fastest speed. Trained for first time on The 2019 DeepRacer Championship Cup for an hour.

### Reward Function
```python
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
    steering = abs(params['steering_angle'])
    #Read progress
    progress = params['progress']
    
    
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
    # Reward will be increased exponentially capping at 10000 and decreased at every penalty
    reward = 1 #very little but not 0, cero means crashed
    
    #Initialize thresholds
    DIRECTION_THRESHOLD = 10.0
    #STEERING_THRESHOLD will depend on the agent's action space
    STEERING_THRESHOLD = 15
    #SPEED_THRESHOLD will depend on the agent's action space
    SPEED_THRESHOLD = 2.67 
    
    # Reward if close to waypoints, minimal steering and going fast
    if direction_diff < DIRECTION_THRESHOLD:
        reward *= 1e+1
    if steering < STEERING_THRESHOLD:
        reward *= 1e+1
    if speed > SPEED_THRESHOLD:
        reward *= 1e+1
    #Incentivize finishing laps but cap at 10000
    if progress == 100: 
        reward *= 1e+1
    
    # Penalize every time it goes away from waypoints, steers too much or goes slow
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 1e-1
    if steering > STEERING_THRESHOLD:
        reward *= 1e-1
    if speed < SPEED_THRESHOLD:
        reward *= 1e-1
    
    return reward
```

## Hyper-parameters

Learning rate = 0.001
batch size = 64 
epochs = 10  
entropy = 0.05
Discount factor = 0.999
Loss Type = Mean square error (already spent about 3 hours training, convergence should not be an issue)
Episodes = 30