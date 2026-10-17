import json,subprocess,datetime,os,asyncio
from FalconEye import comms

path_to_program_files = None

class Tool_Manager:
    def __init__(self,Tool_Configuration):
        self.Tool_conf = Tool_Configuration

    def Create_Object(self,type):
        if type["type"] == "Init":
            for tool in self.Tool_conf:
                tool["Instance_Type"] = "Master"
                comms.Set_Tool_Object(f"{tool["Name"]}",json.dumps(tool))
            return "Tool object created"

    def Destroy_Object(self,name):
        comms.Set_Tool_Object(f"{name}",None)
        return f"{name} has been destroyed and can't be used anymore in the workflow"

    def Verify_Command():
        pass
    @staticmethod
    def Start_New_Session(Session_Name):
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check == 1:
            subprocess.run(["tmux","new-session","-d","-s",Session_Name])
            FileandLogManager.addLogUI("A new Terminal Session has been created!")
            FileandLogManager.addLogF("A new Terminal Session has been created!")
            return 1
        else:
            FileandLogManager.addLogUI("The session already exists abording the start!!")
            FileandLogManager.addLogF("The session already exists abording the start!!")
            return 0
    @staticmethod
    async def Run_Command_On_Session(Session_Name,Command):
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check == 0:
            subprocess.run(["tmux","send_keys","-t",Session_Name,Command + f" && touch {path_to_program_files}/{Session_Name}.txt","Enter"])
            while not await os.path.exists(f"{path_to_program_files}/{Session_Name}.txt"):
                await asyncio.sleep(10)
            FileandLogManager.addLogUI(f"{Session_Name} has been completed")
            FileandLogManager.addLogF(f"{Session_Name} has been completed")
            return 1
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exist!! Creating a new Session")
            FileandLogManager.addLogF(f"{Session_Name} does not exits!! Creating a new session")

            Tool_Manager.Start_New_Session(Session_Name)
            Tool_Manager.Run_Command_On_Session(Session_Name,Command)
            return 1
    @staticmethod
    def Emergency_Interrupt_Session(Session_Name):
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check == 0:
            subprocess.run(["tmux","send-keys","-t",Session_Name,"C-c"])
            FileandLogManager.addLogUI(f"{Session_Name} has been terminated!!!")
            FileandLogManager.addLogF(f"{Session_Name} has been terminated!!!")
            return 1
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            return 1
    @staticmethod
    def Display_Terminal_Session(Session_Name):
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check == 0:
            subprocess.run(["tmux","attach-session","-t",Session_Name])
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
    @staticmethod
    def Hide_Terminal_Session(Session_Name):
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check == 0:
            subprocess.run(["tmux","detach-client","-s",Session_Name])
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
        

class FileandLogManager:
    @staticmethod
    def addLogF(message,PATH):
        with open(f"{PATH}","w") as f:
            f.write(f"[{datetime.now().strftime("%H:%M:%S")}]" + ": " + f"{message}\n")

    @staticmethod
    def addLogUI(message):
        comms.Send_Log_To_UI(message)
        