# aws_deepracer
 Reinforcement Learning using [AWS Cloud Services DeepRacer](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

<img src="images/run_cropped_compressed.gif" width=800 />

## Fast Model
AWSDeepRacer2020-fastest3L-wheels-left-tuned-wp-5hours

### Agent and Model Configuration
Parameters chosen following indications on [AWS DeepRace Workshop Lab200](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-reInvent/Lab_200_AIM207) except max. speed = 4 m/s 

### Training job description
3-layer CNN, front-facing camera, fastest speed. Trained on The 2019 DeepRacer Championship Cup for around 5 hours.

### Reward Function
See faster3CNN.py file

## Results
- Rank: 48
- Best average: 00:00:16.110

<img src="images/Capture.jpg" width=400 />

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
See slow3CNN.py file

### Hyper-parameters
Learning rate = 0.0008 
Batch size = 32 
Epochs = 5 
Entropy = 0.02
