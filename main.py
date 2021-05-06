
from time import sleep_ms
from machine import Pin
import dht
import urequests
import json
import gc

#Define DHT11 connected to pin 14 as dhtpin
dhtpin = dht.DHT11(Pin(14))
avg=0
  
def main():

    #Define the Heroku server url where to send temp. data
    url = "https://tempsensorserver.herokuapp.com/postdata"
    headers = {'content-type': 'application/json'}
    counter = 0
    values = []
    secondsCounter = 0
    
    while True:
        counter += 1

        #Measure temperature with DHT11
        measure = dhtpin.measure()
        temperature = dhtpin.temperature()
        message = "Temperature: " + str(int(temperature))
        #Save the measured temp. to values[]
        if(len(values) <= 60):
            values.insert(0, int(temperature))
        else:
            values.remove(values[59])
            values.insert(0, int(temperature))

        sleep_ms(2000)

        #Count average when 30 values have been measured
        if(counter == 60):
            #Round avg
            avg = round(sum(values) / len(values), 0)
            counter = 0
        sleep_ms(1000)
        secondsCounter += 1
        print("Counted seconds: " + str(secondsCounter) + " " + message)

        if (secondsCounter % 60 == 0):

            #Run garbage cleaner
            gc.collect()
            
            data = {"value": avg}
            jsonObj = json.dumps(data)

            #Send the average to Heroku server as JSON by POST request
            resp = urequests.post(url, data=jsonObj, headers=headers)
            print("Average sent to server with following value: " + str(avg))
            resp.close()

            secondsCounter = 0
            
main()