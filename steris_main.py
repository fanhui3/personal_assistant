from neuralintents.main import GenericAssistant as GA
from modules.text_speech_convert import Steris
from modules.helper_modes import Assistant

def hello():
    "Hello World!!!"

mapping = {"greeting": hello,
           "personal_assistant_mode": Assistant.general_help,
           "therapist_mode": Assistant.therapist,
           "career_coach_mode": Assistant.career_coach}
           
steris = GA(intents="intents.json", model_name="steris", intent_methods=mapping)
steris.load_model("./neuralintents/general_therapy_and_career_coach")

while True:
    #TODO add wake up sound and voice prompt

    #turning on
    Steris.dictation("Yes?")

    # collect input #TODO add voice recogniser
    message = input("Message: ")

    #terminate the program with a command
    if "stop" in message:
         Steris.dictation("Standing by")
         break
    
    #diver to the module if it understands
    steris.request(message)

    #TODO add measures in case steris do not understand your intent
