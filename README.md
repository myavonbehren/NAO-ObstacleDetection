# NAO Obstacle Detection

https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/dcb8c350-e9fa-4f8a-bf88-762ac5b85345

## Introduction

During the Fall Quarter of my third year, I continued to work with Aldebaran Robotics’ NAO humanoid robot to develop a module dedicated to detecting obstacles and implementing avoidance strategies. Achieving this goal enhances the robot’s functionality and holds significant potential for diverse real-world applications.

I began my research by exploring the various sensors equipped on the NAO robot and identifying those I could utilize. I quickly realized that NAO’s ultrasonic sensors offered the most promising means of obstacle avoidance. According to Softbank Robotics documentation, the NAO robot has two ultrasonic sensors that can identify obstacles within a specified range of 0.25m to 0.80m in its environment.

In addition to the ultrasonic sensors, I considered the tactile sensors a potential solution, mainly when the ultrasonic sensors might be limited by distance. Lastly, I considered incorporating NAO’s camera into the project to enhance capabilities such as detecting specific objects.

## Method

I started the process by experimenting with the ultrasonic sensors to assess their accuracy. Employing an infinite loop, I placed various objects in NAO’s path at different distances. Given that the sensor outputs measurements in meters, I converted them to feet for improved readability. While the ultrasonic sensors demonstrated overall accuracy, there were occasional erratic readings significantly deviating from the actual distance of the object. Additionally, obtaining precise measurements proved challenging due to the sensors’ broad scope, detecting both front-facing and nearby objects, thereby presenting limitations in the controlled environment.

<p align="center">
  <img width="460" height="300" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/6bda6fbe-3cd9-4085-8906-79c5eebb1bb1">
</p>

```python
    memory_service = session.service("ALMemory")
    sonar_service = session.service("ALSonar")


    sonar_service.subscribe("myApplication")
    
    try:
        while True:
      
            left = memory_service.getData("Device/SubDeviceList/US/Left/Sensor/Value")

            right = memory_service.getData("Device/SubDeviceList/US/Right/Sensor/Value")

            print("Left Sonar Value: ", left*3.28)
            print("Right Sonar Value: ", right*3.28)
            time.sleep(3)
    except KeyboardInterrupt:
        pass
              
    sonar_service.unsubscribe("myApplication")
```

For the most accurate results, the final program iteratively reads the sensor values and calculates the average of these values. Thus reducing the likelihood of erratic readings and improving the overall reliability of the results.

```python
        left_sum = 0
        right_sum = 0

        for _ in range(5):
            left_sum += round(self.memory.getData("Device/SubDeviceList/US/Left/Sensor/Value") * 3.28, 2)
            right_sum += round(self.memory.getData("Device/SubDeviceList/US/Right/Sensor/Value") * 3.28, 2)
            time.sleep(0.04)

        left_avg = round(left_sum/5, 2)
        right_avg = round(right_sum/5, 2)
```
Next, I experimented with the tactical sensors. The NAO robot has various tactile sensors, including three head capacitive sensors, a chest button, three hand capacitive sensors for each hand, and two bumpers at each foot's tip. I employed the [sensors_touch.py](http://doc.aldebaran.com/2-1/_downloads/sensors_touch.py) script from Aldebaran’s documentation. If any of its tactile sensors were touched, this program triggered NAO to vocalize the specific sensor that detected the touch. This program deepened my understanding of tactile sensors and provided insight into how events work and how the robot could respond to them.

<p align="center">
  <img width="460" height="300" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/dbf6367c-77d2-42fe-b1d6-8a6ade543fb9">
</p>

While I attempted to integrate these tactile sensors into my final program, I faced some challenges that made it difficult to implement everything successfully in time. The main challenge was getting the sensors to respond correctly when the robot moved. There were instances where the sensors were touched but did not react, and this was particularly noticeable when the robot was in motion. As a result, I could not incorporate these sensors into my final program, considering that motion was a crucial component of my project.

Lastly, I explored NAO’s two cameras located in the forehead. Utilizing NAO’s cameras allowed the robot to identify distinct objects, a pivotal capability for navigating through potentially hazardous elements during obstacle avoidance. My exploration concentrated on image processing to program NAO to initiate a response upon detecting a particular colored object.

<p align="center">
  <img width="460" height="300" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/6055c1ae-d123-450d-a6b8-d9c9cc8d5052">
</p>

The Image_Detection folder has a set of modules that use NAO’s top camera to capture an image facing forward. Following this, it turns its head right, capturing another image, replicating this process by turning its head left and obtaining a third image. Then, these three images are processed using OpenCV. Using OpenCV, the program creates a mask identifying the blue object, and if the count of blue pixels surpasses a predefined threshold, NAO then executes a programmed response.
<p align="center">
  <img width="850" height="283" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/163d1782-28c2-4126-89cc-f821483dc77c">
</p>
<p align="center">
  <img width="850" height="283" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/e4e4409c-ed90-4b9e-a328-a3617ad61b94">
</p>
<p align="center">
  <img width="850" height="283" src="https://github.com/myavonbehren/NAO-ObstacleDetection/assets/105401477/1b4632ee-363b-42b2-a912-d36f049423f9">
</p>

Below is a short description of what each module does:
- detect_blue.py
  - Processes an image and masks out any blue from the picture

- move_head.py
  - Moves the robot’s head left, right, and to the center

- take_picture.py
  - Takes a picture using one of NAO’s cameras and saves it as a PNG image.

- color_reaction.py
  - Combines the above modules so NAO can react to detect a blue object.


I successfully executed this process; nevertheless, I opted not to incorporate it into my final program due to concerns about the time it would take for the robot to respond. Given the sequential nature of the camera usage—requiring multiple head turns, image processing, and subsequent reaction time—I anticipated potential delays. 


## Main Program
Upon thorough experimentation with various sensors, I determined that the sonar sensors proved the most effective. I successfully programmed NAO to navigate and avoid obstacles.

Three key functions drive the functionality. First, the `check()` function evaluates sonar values and returns True if the robot detects an obstacle closer or equal to the minimum safe distance of 1.82 feet. The second function, `handle_obstacles()`, utilizes the check function to obtain sonar values and takes appropriate actions based on obstacle detection. It assesses both left and right sonar values, determining the presence of obstacles in the robot's path. The robot proceeds forward if no obstacles are identified, announcing, "Nothing in my way." If obstacles are detected, the robot halts, vocalizing, "Oh uh, something is in my way," and turns 15 degrees clockwise. The third and concluding function is `run()`, which wakes up the robot, moves it to a stand position, and continuously runs `handle_obstacles()` at 3-second intervals.

In the `main` function, the program establishes a connection with the robot and initiates the `run()` function, orchestrating the seamless execution of obstacle avoidance.

## Conclusion
Successfully implementing obstacle avoidance marked a significant achievement, yet there are areas that remain for improvement. The current approach involves the robot consistently turning 15 degrees clockwise until it perceives no obstacles. To improve this behavior, I suggest revising the algorithm to guide the robot in turning right when an obstacle is on its left and vice versa. Although I attempted this modification, I encountered challenges in its execution.

Moreover, instances of the robot falsely detecting obstacles, although improved with the averaging of sensor values, still require further optimization. I think exploring the potential integration of the camera may offer a valuable solution.

Overall, this project allowed me to understand the trial-and-error of problem-solving, where learning from mistakes was crucial. Despite encountering challenges, like the camera and tactile sensors not being as useful as anticipated, I embraced the process and gained valuable experience in robotics.





