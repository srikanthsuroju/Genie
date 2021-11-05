import datetime
import os
import smtplib
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia

print('initilizing Genie...')
MASTER = "Sunny"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning" + MASTER)
    elif hour>= 12 and hour < 18:
        speak('good afternoon' + MASTER)
    else : 
        speak('good evening' + MASTER)
    
    speak("I am Genie. How may I help you?")

def takeCommand():
    '''
    It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    r.pause_threshold = 1.0
    with sr.Microphone(device_index=2) as source: #'device_index' depends on user system attached devices
        print("listening...")
        audio = r.listen(source)
        print("completed")
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f'User said: {query}\n')
    except Exception as e :
        print(e)
        print('say that again please')
        query = "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login('usermail@gmail.com','userPassword') #type the exact password
    server.sendmail('recievermail@gmail.com', to, content)
    server.close()

def main():
    
    # main program starts here.
    speak('initializing Genie')
    #wishMe()
    while True:
        query = takeCommand().lower()
        #Logic for execution tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query = query.replace('wikipedia', '')
            try:
                results = wikipedia.summary(query, sentences = 2)
                speak(results)
                print(results)
            except wikipedia.DisambiguationError as e:
                print(f"There are more than one article related to {query}. So, please give more specifics")
        elif 'open youtube' in query:
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open('www.youtube.com')
        elif 'open google' in query:
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open('www.google.com')
        elif 'play music' in query:
            songs_dir = 'D:\\songs'
            songs = os.listdir(songs_dir) 
            print(songs)
            os.startfile(os.path.join(songs_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'{MASTER}, the time is {strTime}')

        elif "code" in query:
            codePath = '"C:/Users/Srikanth/AppData/Local/Programs/Microsoft VS Code/Code.exe"' 
            os.startfile(codePath)

        elif "email to" in query:
            try:
                speak('What should I send')
                content = takeCommand()
                to = 'reciever@gmail.com'  # before sending mail user have to unable 'less secure app' in google chrome
                sendEmail(to,content)
                speak('Email has been sent successfully')
            
            except Exception as e:
                print(e)
                speak(f"Sorry {MASTER} I am unable to send this mail")
        
        elif "close" in query:
            print(f"Bye {MASTER}, See you later")
            break


main()
