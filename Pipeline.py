
import redis,json
from FalconEye_Methods import FileandLogManager as FLM

Queues = [          # These are the Queues that will be used kind of like API endpoint (More will be added in the future commits)
    "UI->BACKEND",
    "BACKEND->UI",
    "Logger->UI"
]

class Pipleine_Manager():
    def __init__(self): # This creates the redis server instances with the settings any brpop method will be waiting forever for tasks.
        self.redis_client = redis.Redis(host='localhost',port=6379,socket_keepalive=True,
        decode_responses=True, socket_timeout = 0, socket_connect_timeout = 0
        )
    
    def flush_queues(self): # This is used to create queue data from previous scanning session
        for item in Queues:
            self.redis_client.delete(item)
        FLM.addLogUI("Queues has been flushed")
        FLM.addLogF("Queues has been flushed")
    
    def Set_State(self,given_state): # This is used to set variables to be accessed easier and faster on demand
        self.redis_client.set("State",f"{given_state}")
        FLM.addLogUI("state has been set")
        FLM.addLogF("State has been set")

    def Set_Tool_Object(self,Tool_Name,object): # This method is used to store the tool json for easier access on demand
        self.redis_client.set(f"{Tool_Name}",json.dumps(object))
        FLM.addLogUI(f"{Tool_Name} object stored.")
        FLM.addLogF(f"{Tool_Name} object stored")
    
    def Get_Tool_Object(self,Tool_Name): # This is used to load the stored tool json
        return self.redis_client.get(f"{Tool_Name}")

    def Send_Log_To_UI(self,message):
        self.redis_client.lpush("Logger->UI",message)
        return True

    def Load_Tool_Template(Name):
        with open("Tool_Output_Formats.jsonl","r") as f:
            pass

    def Verfiy_Connection(self): # As the name suggests this is used to verfiy the instance of redis server.
        return self.redis_client.ping()
    
    # There are still methods to add here, i just haven't thought of them yet
