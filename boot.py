import network
import esp
import gc

#Make sure that ESP debugging is off
esp.osdebug(None)

#Garbage collect
gc.collect()

#Define WiFi credencials
ssid = 'WiFi SSID HERE'
password = 'WiFi PASSWORD HERE'

#Connect to WiFi with given SSID and password
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connected to WiFi')