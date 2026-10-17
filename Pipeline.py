# This file only contains code for redis (more methods will be added)

import redis,json

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
        return "Queues has been flushed" # These return statements are temporary i will add a logger object that sends data to the frontend to display these messages
    
    def Set_State(self,gvien_state):
        self.redis_client.set("State",f"{given_state}")
        return "state has been set" # Same for these

    def Set_Tool_Object(self,Tool_Name,object):
        self.redis_client.set(f"{Tool_Name}",json.dumps(object))
        return f"{Tool_Name} object stored."
    
    def Get_Tool_Object(self,Tool_Name):
        return self.redis_client.get(f"{Tool_Name}")
    
    
    def Verfiy_Connection(self):
        return self.redis_client.ping()
    
    # There are still methods to add here, i just haven't thought of them yet
