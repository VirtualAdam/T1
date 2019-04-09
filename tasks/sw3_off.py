#import subprocess
import paho.mqtt.publish as publish

outlet1_on = '1332531'
outlet1_off = '1332540'
outlet2_on = '1332675'
outlet2_off = '1332684'
outlet3_on = '1332995'
outlet3_off = '1333004'
outlet4_on = '1334531'
outlet4_off = '1334540'
outlet5_on = '1340675'
outlet5_off = '1340684'
gateway = '192.168.1.7'

publish.single("switches", outlet3_off, hostname=gateway, qos=0)
#data = subprocess.Popen(["/var/www/rfoutlet/codesend", outlet3_on, "-p", "3"], stdout=subprocess.PIPE).communicate()[0]
