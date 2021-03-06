#gateway.py
# hostname must be set to lex-nci-gateway
# autostart should also be turned on in /etc/rc.local with the following code before the exit 0:
# sleep 10
#sudo python gateway.py &
#from inject import posit
#sudo apt-get install mosquitto mosquitto-clients
import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import socket
import sys
import os
import time
import datetime
import subprocess
import paho.mqtt.publish as publish
from gpiozero import LED
from time import sleep


#=======================
# variables
gateway = "yes"
ip1 = None
blacklist = [None]
ID = []


#=============================
# find local ip address
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


#==================================
#subcribe to own broker
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#", 1)

def on_message_garage(client, userdata, msg):
    print("recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    caller = topic_parts[1]
    pay = msg.payload.decode('UTF-8')
    payload_parts = pay.split('-')
    message = payload_parts[0]
    photo_id = payload_parts[1]
    print (caller)
    posit(message,caller,photo_id)
    
def on_message_startup(client, userdata, msg):
    print("recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    if msg.payload == "request":
        time.sleep(3)
        publish.single("gateway/yes", str(localip), hostname=localip, qos=0)
        print ("published")

def on_message_power(client, userdata, msg):
    print("recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    data = subprocess.Popen(["/var/www/rfoutlet/codesend", msg.payload, "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
    print ("switched" )   
    
def on_message_garagedoor(client, userdata, msg):
    print("recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #top = msg.topic.decode('UTF-8')
    msg.payload = msg.payload.decode("utf-8")
    #topic_parts = top.split('/')
    if msg.payload == 'door1':
        door1 = LED(21) #pin 38 see pinout
        sleep(1)
        door1.on()
        sleep(1)
        door1.off()
        print('Door 1 button pressed')
    elif msg.payload == 'door2':
        door2 = LED(20) #pin 40 see pinout
        sleep(1)
        door2.on()
        sleep(1)
        door2.off()
        print('Door 2 button pressed')
    else:
        print ('door not recongnized')
    
    
    
def on_message_keepalive(client, userdata, msg):
    top=msg.payload
    #dont do anything

#============================================
#Handler for all sensor messages: forward all messages to the cloud server
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    top = msg.topic.decode('UTF-8')
    topic_parts = top.split('/')
    #print("keepalive: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            # lex/customer_id/gateway_id/thing_id/datatype/ timestamp data

#boot
localip = find_ip()
print (localip)
print ("booted")

#connect to own broker; loop forevery
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add("lex/#", on_message_garage)
client.message_callback_add("gateway/#", on_message_startup)
client.message_callback_add("switches/#", on_message_power)
client.message_callback_add("garagedoor/#", on_message_garagedoor)
client.on_message = on_message
client.subscribe("#", 0)
client.connect(localip, 1883, 60)
client.loop_forever()

print ("error loop overrun")
