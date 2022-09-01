#!/usr/bin/env python3

import RPi.GPIO as GPIO
import ds18b20
import segment
import time
import paho.mqtt.client as mqtt # distance-pub.pyから追加

#### distance-pub.pyからマージ （ここから）####

###### Edit variables to your environment #######
broker_address = "test.mosquitto.org"     #MQTT broker_address :192.168.0.31
Topic = "pipertest_makotofukuyama"

Trigger = 16
Echo = 18

# # initialize GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(Trigger, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(Echo ,GPIO.IN)

print("creating new instance")
client = mqtt.Client("pub5") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

#### distance-pub.pyからマージ （ここまで）####


def setup():
	segment.TM1638_init()

def destory():
	GPIO.cleanup()

def loop():
	tmp = 0.0
	while True:
		tmp = ds18b20.ds18b20Read()
		df = "%0.2f" %tmp	 # 小数点以下2桁
		client.publish(Topic, df) #MQTTへpublish
		segment.numberDisplay_dec(tmp)
		time.sleep(60)

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destory()
