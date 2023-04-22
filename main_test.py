# import conf
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from boltiot import Bolt
import json
import time
from twilio.rest import Client
import serial

from pyfirmata import Arduino, util
import time

intermediate_value = 55
max_value = 80

arduino = serial.Serial('COM3', 9600)

# board = Arduino('COM3')

arduino.write(b'a0') # Send 'a' to request analog input
analog_input = arduino.readline().decode().strip()

print('Analog input:', analog_input)


# temp  = arduino.get_pin('a:0:o')
time.sleep(2.0)



# print("Temperature is: " + str(temperature) + "°C")




# Configure Twilio API settings
account_sid = 'ACc10811a3687ebbc48648729841790510'
auth_token = 'd206dd7aed59ba8996cfd02cef8ed82f'
twilio_number = '+15074874092'
recipient_number = '+91 7506157604'
client = Client(account_sid, auth_token)

# Configure email settings
key = 'b39fc551fa543076f27c48bcfaed0b45-b36d2969-cadd52a1'
sandbox = 'sandbox4f2dd10cf5d3445c81a1f2f28f530684.mailgun.org'
recipient = 'naqeeb@eng.rizvi.edu.in'


def twillo_message(message):
    try:
        print("Making request to Twilio to send a SMS")
        response = client.messages.create(from_='+15074874092',
							body =message,
							to ='+91 7506157604')
        print("Response received from Twilio is: " + str(response))
        print("Status of SMS at Twilio is :" + str(response.status))
    except Exception as e:
        print("Below are the details")
        print(e)


def mailgun_message(head, message_1):
    try:
        print("Making request to Mailgun to send an email")
        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
        response = requests.post(request_url, auth=('api', key), data={
            'from': 'hello@example.com',
            'to': recipient,
            'subject': head,
            'text': message_1
        })
        print("Response received from Mailgun is: " + response.text)
        print('Status: {0}'.format(response.status_code))
        print('Body:   {0}'.format(response.text))
    except Exception as e:
        print("Below are the details")
        print(e)

# ser = serial.Serial('COM3', 9600, timeout=1)
# time.sleep(2)

while True:
    print("Reading Water-Level Value")
    # Read digital pin 10
    arduino.write(b'10')  # Send a command to Arduino to read pin 10
    # time.sleep(2)
    Water_level = arduino.readline().decode().strip()  # Read the value sent by Arduino
    # time.sleep(1)
    
    # Print value
    # print("Water level:", value)
    # response = mybolt.analogRead('A0')
    # data_1 = json.loads(response_1)
    # data = json.loads(response)
    # Water_level = data_1['value'].rstrip()
    print("Water Level value is: " + str(Water_level) + "%")
    # sensor_value = int(data['value'])
    # temp = (100*sensor_value)/1024
    # temp_value = round(temp, 2)
    value = (0.5-int(analog_input))*100
    temp_value= int(value)
    print("Temperature is: " + str(temp_value) + "°C")
    try:

        if int(Water_level) >= intermediate_value:
            message = "Orange Alert!. Water level is increased by " + str(Water_level) + "% at your place. Please be Safe. The current   Temperature is " + str(temp_value) + "°C."
            head = "Orange Alert"
            message_1 = "Water level is increased by " + str(Water_level) + "% at your place. Please be Safe. The current Temperature is " + str(temp_value) + "°C."
            twillo_message(message)
            mailgun_message(head, message_1)

        if int(Water_level) >= max_value:
            message = "Red Alert!. Water level is increased by " + str(Water_level) + "% at your place. Please Don't move out of the house. The Current Temperature is " + str(temp_value) + "°C"
            head = "Red Alert!"
            message_1 = "Water level is increased by " + str(Water_level) + "% at your place. Please Don't move out of the house. The Current Temperature is " + str(temp_value) + "°C."
            twillo_message(message)
            mailgun_message(head, message_1)

    except Exception as e:
        print("Error occured: Below are the details")
        print(e)
    time.sleep(15)
