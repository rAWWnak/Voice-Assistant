import webbrowser
import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import openai
from config import apikey
listener = aa.Recognizer()
machine = pyttsx3.init()
voice = machine.getProperty('voices')
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for request: {prompt} \n ****************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    #print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
chatStr = ""
def chat(instruction):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Rounak: {instruction}\n Sephora: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    talk(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
def talk(text):
    machine.setProperty('voice', voice[1].id)
    machine.say(text)
    machine.runAndWait()
def input_instruction():
    global instruction
    with aa.Microphone() as origin:
        listener.pause_threshold = 1.0
        speech = listener.listen(origin)
        try:
            print("Recognizing...")
            instruction = listener.recognize_google(speech, language="en-in")
            print(f"user said: {instruction}")
            instruction = instruction.lower()
            return instruction

        except Exception as e:
            return "Some error occured. Sorry from Sephora!"
if __name__ == '__main__':
    talk("Hello!!  I am Sephora AI")
    print("Hello!! I am Sephora AI")
    while True:
        print("Listening...")
        instruction = input_instruction()
        sites = [["youtube", "https://www.youtube.com/"], ["wikipedia", "https://www.wikipedia.org/"], ["google", "https://www.google.co.in/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in instruction.lower():
                talk(f"Opening {site[0]} sir...")
                webbrowser.open(site[0])

        if "time".lower() in instruction:
            curtime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {curtime}")
            talk(f"Sir the time is {curtime}")

        elif 'how are you'.lower() in instruction:
            print('I am fine, Sir.  How about you?')
            talk('I am fine, Sir. How about you?')

        elif "date".lower() in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            print(" Sir, today's date is: " + date)
            talk("Sir, today's date is" + date)

        elif "play".lower() in instruction:
            song = instruction.replace('Sephora play', "")
            talk("Playing " + song)
            print("Playing" + song)
            pywhatkit.playonyt(song)

        elif "using wikipedia search".lower() in instruction:
            find = instruction.split("using wikipedia search")
            finder = find[1]
            talk("Information displayed:")
            print(wikipedia.page(finder,1).content)

        elif  "open google chrome".lower() in instruction:
            chromepath = "C:\Program Files\Google\Chrome\Application>chrome.exe"
            os.system(f'" {chromepath}"')

        elif "using artificial intelligence".lower() in instruction:
            ai(prompt=instruction)

        elif "Sephora Quit".lower() in instruction:
            exit()

        elif "reset chat".lower() in instruction:
            chatStr = ""

        elif 'search'.lower() in instruction:
            word = instruction.split('about')
            wordy = word[1]
            pywhatkit.search(wordy)

        else:
            print("Chatting...")
            chat(instruction)