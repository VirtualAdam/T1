import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("gateway/yes/", hostname="192.168.1.8")
publish.single("gateway/", "request", hostname="192.168.1.8", qos=0)
print("%s %s" % (msg.topic, msg.payload))
publish.single("gateway/", "request", hostname="192.168.1.8", qos=0)
