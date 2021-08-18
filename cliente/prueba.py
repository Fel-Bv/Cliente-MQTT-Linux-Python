# Tutorial: https://www.youtube.com/watch?v=hEFSaysEIhs

import sys
import paho.mqtt.client

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='mqtt', qos=2)

def on_message(client, userdata, message):
	print('------------------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	print('qos: %d' % message.qos)

def main():
	client = paho.mqtt.client.Client(client_id='subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='192.168.100.5', port=8080)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)