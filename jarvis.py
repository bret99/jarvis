import speech_recognition as sr  
import os
import sys
from selenium import webdriver 
import time
from random import randint 

jarvis_dir = os.getcwd()
hello_vars = {1: jarvis_dir + "/whats_up.mp3", 2: jarvis_dir + "/gday.mp3", 3: jarvis_dir + "/hello_fellow.mp3"}
command_for_hello = "mpg123 -q " + hello_vars[randint(1, 3)]
os.system(command_for_hello)
bye_vars = ["bye", "goodbye", "see you later", "exit"]
calm_vars = ["shut up", "silence", "don't speak"]
r = sr.Recognizer() 
def stay_calm():
    try:
        keep_calm = input("Enter how long system should stay calm (in seconds): ")
        float(keep_calm)
    except ValueError:
        print("Not valid value")
        print("Quiting keeping calm...")
        return
    with sr.Microphone() as source:                                                                       
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)   
        try:
            print("You said ", r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Keeping calm...")
            time.sleep(float(keep_calm))
def speaking():
    with sr.Microphone() as source:                                                                       
        print("Speak:")         
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)   
    try:
        print("You said ", r.recognize_google(audio))
        my_string = r.recognize_google(audio).lower()
        if my_string.startswith("firefox find"):
            fp = webdriver.FirefoxProfile('/home/desktop/.mozilla/firefox/rj3dpw3e.default-release')
            driver = webdriver.Firefox(fp)
            driver.maximize_window()
            driver.get("https://duckduckgo.com")
            search_results = driver.find_element_by_xpath("//input[@id = 'search_form_input_homepage']")
            string_to_find = my_string[13:]
            search_results.send_keys(string_to_find)
            search_results.submit()
        if my_string == "stop firefox" or my_string == "close firefox":
            os.system("bash -c 'killall firefox'")
        if my_string == "top":
            os.system("top")
        if my_string in bye_vars:
            os.system("mpg123 -q " + jarvis_dir + "/bye.mp3")
            sys.exit()
        
        if my_string in calm_vars:
            stay_calm()
    except sr.UnknownValueError:
        what_vars = {1: jarvis_dir + "/whats_wrong.mp3", 2: jarvis_dir + "/what.mp3", 3: jarvis_dir + "/repeat.mp3"}
        command_for_what = "mpg123 -q " + what_vars[randint(1, 3)]
        os.system(command_for_what)
while 1:
    speaking()
