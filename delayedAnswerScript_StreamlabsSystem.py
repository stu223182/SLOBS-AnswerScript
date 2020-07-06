import time
import json
import os
import codecs


#Required script information for the streamlabs chatbot.
ScriptName = "delayedAnswerScript"
Website = "https://www.twitch.tv/tanker22"
Description = "Bot posts a random text and after some time the corresponding answer"
Creator = "Tanker22"
Version = "0.2"

#-----------------------------
#Global variables
settings = {}

Command = ""
timerBool = False
timer = 0



#   [Required] Initialize Data (Only called when script is loaded.)


def Init():
    global settings
    work_dir = os.path.dirname(__file__)
    global Command

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except Exception, e:
        log(str(e))
        Command = "!answer"
        settings = {
            "command": "!answer",
            "userCooldown": 30,
            "timeToAnswer": 30
        }


    Command = settings["command"]
    return

#[Required] Execute Data / Process messages. Called whenever there is incoming data in chat.
def Execute(data):
    global timerBool, timer


    if data.GetParam(0) == Command and not Parent.IsOnUserCooldown(ScriptName, Command, data.User):
        log("Command typed in and will be executed")
        send_message(chooseMessage())
        timerBool = True
        Parent.AddUserCooldown(ScriptName, Command, data.User, settings["userCooldown"])

        #Set timer to given time in seconds.
        timer = time.time() + settings["timeToAnswer"]
        log("Command executed and now leaving Execute")
        return
    elif data.GetParam(0) == settings["answer" +str(answerNumber)] and timerBool:
        log("User gave the right answer")
        send_message("Wir haben einen Gewinner!")
        send_message("!gold add " + data.User + " " + str(settings["reward"]))
        timerBool = False
        return

    return

#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
def Tick():
    global timerBool, timer

    if timerBool and time.time() > timer:
        timer = 0
        timerBool = False
        send_message(messageAnswer())
    return


def chooseMessage():
    log("Entering chooseMessage method")
    global answerNumber
    answerNumber = Parent.GetRandom(1, 4)
    log("Exiting chooseMessage method")
    return settings["string" + str(answerNumber)]

def messageAnswer():
    log("Choosing and returning the answer to String" + str(answerNumber))
    return settings["answer" + str(answerNumber)]

# Sending the message to the chat
def send_message(message):
    log("Entered send_message")
    Parent.SendStreamMessage(message)
    log("Exiting send_message")
    return

# Writes the given message to the loggingsystem of the SLOBS-Chatbot
def log(message):
    Parent.Log(Command, message)
    return