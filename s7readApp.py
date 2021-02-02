import time
import s7XinyingLib
import requests
import json
#plc read sampling time [sec]:
ts_plc_update       =    2
#ip upload sampling time [sec]:
ts_ip_update        =    5  
#  s71500 rack number:
rackNo   =    0
#  s71500 slot number:
slotNo   =    1
#  s71500 device number:
deviceNr =    2
# s71500 ip adress:
PLC_IP   =    '169.254.12.77'
# cloud server adress:
mqtthost =    "88.99.24.40"
# cloud server port:
mqttport =    1883
# topics definition
topic1   =    "Simcheng/3002/scy1"
topic2   =    "Simcheng/3002/scy2"
topic3   =    "Simcheng/3002/scy3"
# client name:
clientname = "simchengProducer"
# client user name:
username   = "simcheng"
# client password:
password   = "Simcheng2020"

### IP upload Parameters ###
organId = 2002
devId   = "3001"            # device ID
api_ip_upload = 'user'      # user name
api_password  = 'user'      # password

auth_url = "http://88.99.24.40:8088/api/auth/signin";
optIn_url = "http://88.99.24.40:8088/api/optIn";
  
def step_fun_plc():
    try:
        plc =s7XinyingLib.plcConnect(PLC_IP,rackNo,slotNo)
        DBIdNo,Data = s7XinyingLib.ReadAllDBs(plc,s7XinyingLib.DBTables())
        scy1_Ids,scy1_data =s7XinyingLib.readIDs(s7XinyingLib.DBTables(),Data,1)
        #print(scy1_data)
        s7XinyingLib.on_publish(mqttClient,topic1,s7XinyingLib.Convert2SimchengForm(scy1_Ids, scy1_data) , 1)
    except:
        print("please check the ethernet connection")

     
def step_fun_upload_ip():
    try:
        ipadr = s7XinyingLib.get_ip()
        ngrok_adr = s7XinyingLib.get_ngrok_url()
        s7XinyingLib.ip_upload(auth_url,optIn_url,api_ip_upload,api_password,organId,devId,ipadr,ngrok_adr)
    except:
        print("upload ip or ngrok_address failed")
    #ip_upload(auth_url,optIn_url,api_ip_upload,api_password,organId,devId,ipadr)

if __name__ == "__main__":
    mqttClient = s7XinyingLib.on_mqtt_connect(mqtthost,mqttport,clientname,username,password)
    sched = s7XinyingLib.task_scheduler()
    sched.add_job(step_fun_plc, 'cron', second='*/'+str(ts_plc_update),hour='*',max_instances = int(1e25))
    sched.add_job(step_fun_upload_ip, 'cron', second='*/'+str(ts_ip_update),hour='*',max_instances = int(1e25))
    sched.start()
