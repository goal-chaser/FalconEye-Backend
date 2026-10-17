import json,subprocess,datetime,os,asyncio
from FalconEye import comms

path_to_program_files = None


# The following class is used to organize all the Methods that are related to Scanning tools organized in one place.

class Tool_Manager:
    def __init__(self,Tool_Configuration):
        self.Tool_conf = Tool_Configuration # This tool configuration is the json that is returned from frontend with the data (It's structure is mentioned in Tool_Output_Format json file in tools section)


    def Create_Object(self,type): # This Method is used to edit that tool configuration and save it in a redis variable for easier and faster access
        if type["type"] == "Init":
            for tool in self.Tool_conf:
                tool["Instance_Type"] = "Master"
                comms.Set_Tool_Object(f"{tool["Name"]}",tool)
            return "Tool object created"

    def Destroy_Object(self,name): # This Method is called when all the work that needs to be done by the tool is finished in the workflow. It is set to None
        comms.Set_Tool_Object(f"{name}",None)
        return f"{name} has been destroyed and can't be used anymore in the workflow"

    def Verify_Command(): # This method is used to verify the commands to stop the execution when extreme values of specific performace switches are found to keep the web traffic in check
        pass
    @staticmethod
    def Start_New_Session(Session_Name): # This Start new session method is used to create a new tmux session which is like creating a new linux terminal session
        check = subprocess.run(["tmux","has-session","-t",Session_Name]) # This tmux is purely used to type out the command given by us in the linux terminal and this does not return any output information that is provided by the scanner
        if check.returncode == 1: # The above command is used to see if a session with the specified name is running 1 for not existing and 0 for exisiting
            subprocess.run(["tmux","new-session","-d","-s",Session_Name])
            FileandLogManager.addLogUI("A new Terminal Session has been created!")
            FileandLogManager.addLogF("A new Terminal Session has been created!")
            return 1
        else:
            FileandLogManager.addLogUI("The session already exists abording the start!!")
            FileandLogManager.addLogF("The session already exists abording the start!!")
            return 0
    @staticmethod
    async def Run_Command_On_Session(Session_Name,Command): # This method is used to run the actual command in the linux terminal
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check.returncode == 0:
            subprocess.run(["tmux","send-keys","-t",Session_Name,Command + f" && touch {path_to_program_files}/{Session_Name}.txt","Enter"])
#           while not await os.path.exists(f"{path_to_program_files}/{Session_Name}.txt"):  These two comments need chaining
 #               await asyncio.sleep(10) This is not the right way to do this.
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
    def Emergency_Interrupt_Session(Session_Name): # This is used to stop any scanner execution in the current running session
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check.returncode == 0:
            subprocess.run(["tmux","send-keys","-t",Session_Name,"C-c"])
            FileandLogManager.addLogUI(f"{Session_Name} has been terminated!!!")
            FileandLogManager.addLogF(f"{Session_Name} has been terminated!!!")
            return 1
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            return 1
    @staticmethod
    def Display_Terminal_Session(Session_Name): # This method is used to open up the terminal in GUI to see what's going on.
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check.returncode == 0:
            subprocess.run(["tmux","attach-session","-t",Session_Name])
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
    @staticmethod
    def Hide_Terminal_Session(Session_Name):# This is used to background the process
        check = subprocess.run(["tmux","has-session","-t",Session_Name])
        if check.returncode == 0:
            subprocess.run(["tmux","detach-client","-s",Session_Name])
        else:
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")
            FileandLogManager.addLogUI(f"{Session_Name} does not exists!!")

    @staticmethod
    def Filter_Subdomains(Result1,Result2):
        Common = Result1 & Result2
        Unique = Result1 ^ Result2
        return Common,Unique

        

class FileandLogManager:
    @staticmethod
    def addLogF(message,path): # This is used to log the data in a log file specific to the BB Program. For potential Future references.
        with open(f"{path}","w") as f:
            f.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")}]" + ": " + f"{message}\n")

    @staticmethod
    def addLogUI(message): # This is used to send the debug data to UI to be displayed in the UI.
        comms.Send_Log_To_UI(message)
        