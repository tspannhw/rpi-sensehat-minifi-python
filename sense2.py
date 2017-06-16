from sense_hat import SenseHat
import json
import sys, socket
import os
import psutil
import subprocess
import time
import datetime
from time import sleep
from time import gmtime, strftime

# get data 
#current_milli_time = lambda: int(round(time.time() * 1000))

# yyyy-mm-dd hh:mm:ss
currenttime= strftime("%Y-%m-%d %H:%M:%S",gmtime())
host = os.uname()[1]
rasp = ('armv' in os.uname()[4])

cpu = psutil.cpu_percent(interval=1)
if rasp:
    f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
    l = f.readline()
    ctemp = 1.0 * float(l)/1000
usage = psutil.disk_usage("/")
mem = psutil.virtual_memory()
 
diskrootfree =  "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
mempercent = mem.percent

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

#p = subprocess.Popen(['/opt/vc/bin/vcgencmd','measure_temp'], stdout=subprocess.PIPE,
#    stderr=subprocess.PIPE)
#out, err = p.communicate()

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

ipaddress = IP_address()
sense = SenseHat() 
sense.clear()
temp = sense.get_temperature()
temp = round(temp, 2)
humidity = sense.get_humidity()
humidity = round(humidity, 1)
pressure = sense.get_pressure()
pressure = round(pressure, 1)
orientation = sense.get_orientation()
pitch = orientation['pitch']
roll = orientation['roll']
yaw = orientation['yaw']
acceleration = sense.get_accelerometer_raw()
x = acceleration['x']
y = acceleration['y']
z = acceleration['z']
#cputemp = out
x=round(x, 0)
y=round(y, 0)
z=round(z, 0)
pitch=round(pitch,0)
roll=round(roll,0)
yaw=round(yaw,0)
row =  { 'ts': currenttime, 'host': host, 'memory': mempercent, 'diskfree': diskrootfree, 'cputemp': round(ctemp,2), 'ipaddress': ipaddress, 'temp': temp, 'tempf': round(((temp * 1.8) + 12),2), 'humidity': humidity, 'pressure': pressure, 'pitch': pitch, 'roll': roll, 'yaw': yaw, 'x': x, 'y': y, 'z': z } 
json_string = json.dumps(row)
print(json_string)

