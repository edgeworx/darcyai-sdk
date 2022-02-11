# Setting up your Raspberry Pi for Darcy AI development

Raspberry Pi boards are excellent for building and running Darcy AI applications. This guide will show you how to get your RPi ready for Darcy AI development so you can run and debug your applications.

## Hardware you will need

- Raspberry Pi board (Pi 4 with 2GB+ of RAM recommended)
- Video camera attached to the camera port
- Google Coral edge TPU (USB version attached to USB 3.0 port)
- Micro SD card with at least 16GB capacity (32GB+ recommended)
- Power supply
    - 5 Volts with at least 3 Amps output for RPi4 (standard Raspberry Pi 4 power supply)
    - 5 Volts with at least 2.5 Amps output for RPi3 (most power supplies will qualify)

## Pick your Raspberry Pi operating system and flash your SD card

You can choose either a 32-bit or 64-bit Raspberry Pi OS. The instructions in this guide are the same for either operating system version, but note that using the newly released 64-bit version may result in some unforeseen issues because it is new and not all software packages in the ecosystem have been updated yet.

Follow the official Raspberry Pi Foundation instructions for getting your operating system and flashing it onto your Micro SD card. We recommend installing the Raspberry Pi OS with Desktop option because many helpful software packages will already be installed for you.

The Raspberry Pi SD card imager can be found here:
[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

The Raspberry Pi OS versions can be downloaded here if you want to flash your SD card without the RPi Imager software:
[https://www.raspberrypi.com/software/operating-systems/](https://www.raspberrypi.com/software/operating-systems/)

## Connect your Raspberry Pi to your network and the Internet



## Set up a callback and add the Output Stream to the Pipeline

Before we add the LiveFeed Output Stream to the Pipeline, we need to set up a callback function that we are going to use to process the data before displaying the video. Follow the comments to learn about the steps that are taken. This is the most complex portion of the whole application and it is where all of the business logic is taking place. After the callback function definition, there is a line for adding the LiveFeed Output Stream to the Pipeline. That command needs to have the callback function already defined before it can execute successfully.
```
#Create a callback function for handling the Live Feed output stream data before it gets presented
def live_feed_callback(pom, input_data):
    #Start wth the annotated video frame available from the People Perceptor
    frame = pom.peeps.annotatedFrame().copy()

    #Add some text telling how many people are in the scene
    label = "{} peeps".format(pom.peeps.peopleCount())
    color = (0, 255, 0)
    cv2.putText(frame, str(label), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)

    #If we have anyone, demonstrate looking up that person in the POM by getting their face size
    #And then put it on the frame as some text
    #NOTE: this will just take the face size from the last person in the array
    if pom.peeps.peopleCount() > 0:
        for person_id in pom.peeps.people():
            face_size = pom.peeps.faceSize(person_id)
            face_height = face_size[1]
            label2 = "{} face height".format(face_height)
            color = (0, 255, 255)
            cv2.putText(frame, str(label2), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)

    #Pass the finished frame out of this callback so the Live Feed output stream can display it
    return frame
    
#Add the Live Feed output stream to the Pipeline and use the callback from above as the handler
pipeline.add_output_stream("output", live_feed_callback, live_feed)
```

## Define an event callback and an input callback and instantiate the People Perceptor

Just like the LiveFeed Output Stream, the People Perceptor must have the callbacks already defined before it can work with those callbacks. The input callback simply takes the Input Stream data and sends it onward to the People Perceptor. The “New Person” event callback simply prints the unique person identifier string to the console output when a new person has been detected by Darcy.
```
#Create a callback function for handling the input that is about to pass to the People Perceptor
def people_input_callback(input_data, pom, config):
    #Just take the frame from the incoming Input Stream and send it onward - no need to modify the frame
    frame = input_data.data.copy()
    return frame
    
#Create a callback function for handling the "New Person" event from the People Perceptor
#Just print the person ID to the console
def new_person_callback(person_id):
    print("New person: {}".format(person_id))
    
#Instantiate a People Perceptor
people_ai = PeoplePerceptor()

#Subscribe to the "New Person" event from the People Perceptor and use our callback from above as the handler
people_ai.on("new_person_entered_scene", new_person_callback)
```

## Add the People Perceptor to the Pipeline

```
#Add the People Perceptor instance to the Pipeline and use the input callback from above as the input preparation handler
pipeline.add_perceptor("peeps", people_ai, input_callback=people_input_callback)
```

## Change some configuration items in the People Perceptor

```
#Update the configuration of the People Perceptor to show the pose landmark dots on the annotated video frame
pipeline.set_perceptor_config("peeps", "show_pose_landmark_dots", True)
pipeline.set_perceptor_config("peeps", "pose_landmark_dot_size", 2)
pipeline.set_perceptor_config("peeps", "pose_landmark_dot_color", "0,255,0")
```

## Start the Pipeline

```
#Start the Pipeline
pipeline.run()
```

## Check your completed code

Your finished Python file should look similar to this. If it doesn’t, take a minute to figure out what is missing or incorrect. Next we will build an application container from this code.
```
import cv2
import os
import pathlib

from darcyai_coral.people_perceptor import PeoplePerceptor
from darcyai_engine.input.camera_stream import CameraStream
from darcyai_engine.output.live_feed_stream import LiveFeedStream
from darcyai_engine.pipeline import Pipeline

#Instantiate an Camera Stream input stream object
camera = CameraStream(video_device="/dev/video0", fps=20)

#Instantiate the Pipeline object and pass it the Camera Stream object as its input stream source
pipeline = Pipeline(input_stream=camera)

#Create a Live Feed output stream object and specify some URL parameters
live_feed = LiveFeedStream(path="/", port=3456, host="0.0.0.0")

#Create a callback function for handling the Live Feed output stream data before it gets presented
def live_feed_callback(pom, input_data):
    #Start wth the annotated video frame available from the People Perceptor
    frame = pom.peeps.annotatedFrame().copy()

    #Add some text telling how many people are in the scene
    label = "{} peeps".format(pom.peeps.peopleCount())
    color = (0, 255, 0)
    cv2.putText(frame, str(label), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)

    #If we have anyone, demonstrate looking up that person in the POM by getting their face size
    #And then put it on the frame as some text
    #NOTE: this will just take the face size from the last person in the array
    if pom.peeps.peopleCount() > 0:
        for person_id in pom.peeps.people():
            face_size = pom.peeps.faceSize(person_id)
            face_height = face_size[1]
            label2 = "{} face height".format(face_height)
            color = (0, 255, 255)
            cv2.putText(frame, str(label2), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)

    #Pass the finished frame out of this callback so the Live Feed output stream can display it
    return frame

#Add the Live Feed output stream to the Pipeline and use the callback from above as the handler
pipeline.add_output_stream("output", live_feed_callback, live_feed)

#Create a callback function for handling the input that is about to pass to the People Perceptor
def people_input_callback(input_data, pom, config):
    #Just take the frame from the incoming Input Stream and send it onward - no need to modify the frame
    frame = input_data.data.copy()
    return frame
    
#Create a callback function for handling the "New Person" event from the People Perceptor
#Just print the person ID to the console
def new_person_callback(person_id):
    print("New person: {}".format(person_id))
    
#Instantiate a People Perceptor
people_ai = PeoplePerceptor()

#Subscribe to the "New Person" event from the People Perceptor and use our callback from above as the handler
people_ai.on("new_person_entered_scene", new_person_callback)

#Add the People Perceptor instance to the Pipeline and use the input callback from above as the input preparation handler
pipeline.add_perceptor("peeps", people_ai, input_callback=people_input_callback)

#Update the configuration of the People Perceptor to show the pose landmark dots on the annotated video frame
pipeline.set_perceptor_config("peeps", "show_pose_landmark_dots", True)
pipeline.set_perceptor_config("peeps", "pose_landmark_dot_size", 2)
pipeline.set_perceptor_config("peeps", "pose_landmark_dot_color", "0,255,0")

#Start the Pipeline
pipeline.run()
```

## Save your Python file to your Raspberry Pi

If you are using VS Code remote development, then your file should automatically save on the device when you save in VS Code. If you are manually adding your file to your Raspberry Pi, copy the file to the device now.

## Add a Dockerfile to the same directory as your Python file

You will build a Docker container to run your Darcy AI application. You only need your Python file and a Dockerfile to build the container. Make sure you create this Dockerfile in the same directory as your Python file and change the name from YOURFILE.py to the actual name of your file.
```
FROM edgeworx/darcy-ai-coral-armv7l:dev

RUN python3 -m pip install --upgrade darcyai-engine
RUN python3 -m pip install --upgrade darcyai-coral

COPY YOURFILE.py /src/my_app.py

ENTRYPOINT ["/bin/bash", "-c", "cd /src/ && python3 -u ./my_app.py"]
```

## Build your Docker container

Use the following command to build your Docker container. It may take 10 or 15 minutes if you are building for the first time and you do not have a very fast internet connection. This is because the underlying container base images will need to be downloaded. After the first build, this process should only take a minute or two.
```
sudo docker build -t darcydev/my-people-ai-app:1.0.0 .
```

## Run your application

Use this Docker command to run your application container right away. You can also use this Docker container with the [Edgeworx Cloud](https://cloud.edgeworx.io) to deploy and manage the application.
```
sudo docker run -d --privileged -p 3456:3456 -p 8080:8080 -v /dev:/dev darcydev/my-people-ai-app:1.0.0
```

## View your real-time Darcy AI application video output

Once your application container is running, you can view the live video feed by visiting the following URL in any browser. Replace `YOUR.DEVICE.IP.ADDRESS` with the actual IP address of your Raspberry Pi.
```
https://YOUR.DEVICE.IP.ADDRESS:3456/
```