# This File is going to contain all the code related to managing tools and the main execution loop and workflow conditions
# Other file should be added named Workflow_methods which contains code for logger object for now


import json, Pipleine_Manager

comms = Pipeline_Manager()


class ToolManager:
    def __init__(self,Tools_Configuration):
        self.Tools_Configuration = Tools_Configuration
    
    def Declare_Tool(self):
        tool_conf = self.Tools_Configuration
        for tool in tool_conf:
            comms.Set_Tool_Command(tool["Name"],tool["Command"])
        return "All the commands have been loaded" # Will be replaced by logger



