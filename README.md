# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

<img src="images/run_cropped_compressed.gif" width=720 />

## Fast Model
AWSDeepRacer2020-fastest3L-wheels-left-tuned-wp-5hours

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207) except max. speed = 4 m/s 

### Training job description
3-layer CNN, front-facing camera, fastest speed. Trained on The 2019 DeepRacer Championship Cup for around 4 hours.

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
```

## Results

<img src="images/capture.gif" width=360 />

### Hyper-parameters
Learning rate = 0.001
batch size = 32 
epochs = 5 
entropy = 0.001 
Discount factor = 0.999
Loss Type = Huber
Episodes = 20

## Original (AKA Slow) Model
Agent and Model Configuration
Parameters chosen following indications on AWS DeepRace Workshop Lab200

### Model Name
AWSDeepRacer2020-waypoints-allwheels-speed

### Training job description
Trained on 2019 DeepRacer Championship cup for an hour and a half. Tuned hyperparameters for higher learning rate (0.00075), smaller batch size (32) and epochs to 5.

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
```

### Hyper-parameters
Learning rate = 0.0008 
Batch size = 32 
Epochs = 5 
Entropy = 0.02
