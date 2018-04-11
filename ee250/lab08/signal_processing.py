import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime
import time

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 3
ranger1_dist = []
ranger2_dist = []


def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    

    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()
    
    MAX_AVERAGE_LIST_LENGTH = 3
    ranger1_average = []
    ranger2_average = []
    
    side_Max = 70 #this helps us determine which sensor the person is closest to
    buf = 5 #we found that this gave us more accurate results (see its use below)
    
    time.sleep(0.5) # this fixes a bug we were experiencing with the ranger distance
                    # lists not being populated

    #format the payload of the HTTP message as a JSON object:

    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }


    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        

        if (len(ranger1_dist) >= 3): #if 3 integers are in the list
            

            ranger1_average.append((ranger1_dist[0] + ranger1_dist[1] + ranger1_dist[2]) / 3)
            ranger1_average = ranger1_average[-MAX_AVERAGE_LIST_LENGTH:]
        
            ranger2_average.append((ranger2_dist[0] + ranger2_dist[1] + ranger2_dist[2]) / 3)
            ranger2_average = ranger2_average[-MAX_AVERAGE_LIST_LENGTH:]

        
            if ((ranger1_average[-1] > 125) and (ranger2_average[-1] > 125)):
                print("No object ") 
                
                payload = {
                    'time': str(datetime.now()),
                    'event': "No object "
                }      
                
            else:
            
                if ((ranger1_average[-1] < side_Max) and ((ranger1_average[-2] - buf) <= ranger1_dist[-1]) and ((ranger1_average[-2] + buf) >= ranger1_dist[-1])):
                    print("Still - Left")

                    payload = {
                        'time': str(datetime.now()),
                        'event': "Still - Left "
                    }
                
                elif ((ranger2_average[-1] < side_Max) and ((ranger2_average[-2] - buf) <= ranger2_dist[-1]) and ((ranger2_average[-2] + buf) >= ranger2_dist[-1])):
                    print("Still - Right ")

                    payload = {
                        'time': str(datetime.now()),
                        'event': "Still - Right "
                    }

                elif ((ranger1_average[-1] < ranger1_average[-2]) or (ranger2_average[-1] > ranger2_average[-2])):
                    print("Moving Left ")
                
                    payload = {
                        'time': str(datetime.now()),
                        'event': "Moving Left "
                    }

                elif ((ranger2_average[-1] < ranger2_average[-2]) or (ranger1_average[-1] > ranger1_average[-2])):
                    print("Moving Right ")

                    payload = {
                        'time': str(datetime.now()),
                        'event': "Moving Right "
                    }


                else:
                    print("Still - Middle ")

                    payload = {
                        'time': str(datetime.now()),
                        'event': "Still - Middle "
                    }


            #Sends an HTTP post message and blocks until a response is given

            response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr,
                                 data = json.dumps(payload))
            #Print the JSON object from the HTTP response
            print(response.json())

            
            #this makes it so that the distance values are not too high

            if (ranger1_dist[-1] > 125):
                ranger1_dist[-1] = 125
            if (ranger2_dist[-1] > 125):
                ranger2_dist[-1] = 125
               
        
        else: #if 3 integers are not in the list yet, append more
            ranger1_average.append(ranger1_dist[0])
            ranger2_average.append(ranger2_dist[0])

        time.sleep(0.2)
        