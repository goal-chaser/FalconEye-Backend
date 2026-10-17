
import redis,json
from FalconEye_Methods import FileandLogManager as FLM

Queues = [
    "UI->BACKEND",
    "BACKEND->UI",
    "Logger->UI"
]

class Pipleine_Manager():
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost',port=6379,socket_keepalive=True,
        decode_responses=True, socket_timeout = 0, socket_connect_timeout = 0
        )
    
    def flush_queues(self):
        for item in Queues:
            self.redis_client.delete(item)
        FLM.addLogUI("Queues has been flushed")
        FLM.addLogF("Queues has been flushed")
    
    def Set_State(self,given_state):
        self.redis_client.set("State",f"{given_state}")
        FLM.addLogUI("state has been set")
        FLM.addLogF("State has been set")

    def Set_Tool_Object(self,Tool_Name,object):
        self.redis_client.set(f"{Tool_Name}",json.dumps(object))
        FLM.addLogUI(f"{Tool_Name} object stored.")
        FLM.addLogF(f"{Tool_Name} object stored")
    
    def Get_Tool_Object(self,Tool_Name):
        return self.redis_client.get(f"{Tool_Name}")

    def Send_Log_To_UI(self,message):
        self.redis_client.lpush("Logger->UI",message)
        return True
    
    def Verfiy_Connection(self):
        return self.redis_client.ping()
    
    # There are still methods to add here, i just haven't thought of them yet
