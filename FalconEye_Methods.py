import json,subprocess
from FalconEye import comms

class Tool_Creater:
    def Create_Object(self,type):
        if type["type"] == "Init":
            for tool in self.Tool_conf:
                tool["Instance_Type"] = "Master"
                comms.Set_Tool_Object(f"{tool[Name]}",json.dumps(tool))
            return "Tool object created"

    def Destroy_Object(self,name):
        comms.Set_Tool_Object(f"{name}",None)
        return f"{name} has been destroyed and can't be used anymore in the workflow"

    def __init__(self,Tool_Configuration):
        self.Tool_conf = Tool_configuration


class ToolManager:
    @staticmethod
    def Verify_Command():
        pass
    @staticmethod
    def run(Tool_Name):
        pass
        