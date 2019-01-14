from __future__ import print_function
from appJar import gui
import speech_recognition as sr
import spacy
import datetime
import dateparser
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def upcomingEvents(service): 
    global app
    now = datetime.datetime.utcnow().isoformat()+'Z'
    events_result = service.events().list(calendarId='primary',timeMin=now,maxResults=10,singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # app.addLabel((start+event['summary']))    
    return events



def auth():
	# scope is for to take permission from user
	# diff scopes gives diff permissions as per given url
	# ex: 'https://www.googleapis.com/auth/calendar/readonly' can allow only reading
	# and 'https://www.googleapis.com/auth/calendar' can allow reading as well as writting 

	SCOPES = 'https://www.googleapis.com/auth/calendar'

	# token file will store access rights user has given and this file will generate automatically
	store = file.Storage('token.json')
	creds = store.get()

	# download credentials.json file from https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample
	# credentials.json file inables the googleAPI
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))
	return service


def createEvent(summary_of_event,start_time,end_time,service=auth()):
    global app
    EVENT = {
        'summary': summary_of_event,					
        'start': {'dateTime': start_time}, 
        'end': {'dateTime': end_time}
    }

    e = service.events().insert(calendarId='primary',sendNotifications=True,body=EVENT).execute()
    app.addFlashLabel("m","{} reminder created".format(summary_of_event))



def analyse(text):
    # service=auth()
    word_list=[]

    nlp=spacy.load('en_core_web_sm')
    query = text     
    for word in query.split(' '):
        wk=word
        word = word.replace("th","")
        word = word.replace("rd","")
        word = word.replace("st","")
        word = word.replace("nd","")
    try:
        temp = int(word)
        if len(word==1):
            word = "0"+word
        query = query.replace(wk,word)
    except:
        pass
    doc=nlp(query)
    adjs=[]
    for token in doc:
        if token.pos_=="ADJ":
            adjs.append(token.text)
    for token in doc:
        word_list.append(token.text)

    if "Reminder" in word_list or "Remind" in word_list or "remind" in word_list or "reminder" in word_list:


        ################################################################################
        def verb(x):
            verb_list=[]
            for token in x:
                if token.pos_=='VERB':
                    verb_list.append(token.text)
            return verb_list
        ################################################################################
        def noun(x):
            noun_list=[]
            for token in x:
                if token.pos_=='NOUN':
                    noun_list.append(token.text)
            return noun_list
        ################################################################################
        def date(x):
            date_list=[]
            for token in x.ents:
                if token.label_=='DATE':
                    date_list.append(token.text)
            return date_list
        ################################################################################
        def time(x):
            time_list=[]
            for token in x.ents:
                if token.label_=='TIME':
                    time_list.append(token.text)
            return time_list
        ################################################################################
        Noun=noun(doc)
        Verb=verb(doc)
        ################################################################################
        for i in Noun:
            if 'p.m.' in Noun:
                Noun.remove('p.m.')
            if 'a.m.' in Noun:
                Noun.remove('a.m.')
            if 'reminder' in Noun:
                Noun.remove('reminder')
            if 'Reminder' in Noun:
                Noun.remove('Reminder')
        ################################################################################
            
        time_set=dateparser.parse(time(doc)[0],settings={'TIMEZONE': 'GMT+5:30'})

        hour,mins,secs=time_set.hour,time_set.minute,time_set.second
        new_hour,new_mins,new_secs=str(hour),str(mins),str(secs)
        end_mins=str(mins+5)                
        if not date(doc):
            default_date=datetime.datetime.now()
            day,month,year=default_date.day,default_date.month,default_date.year
        else:
            date_set=dateparser.parse(date(doc)[0])
            day,month,year=date_set.day,date_set.month,date_set.year

        # print(day,month,year)
        new_day,new_month,new_year=str(day),str(month),str(year)
        '''
        Displaying task
        '''

        start_time_1=new_year+"-"+new_month+"-"+new_day+"T"+new_hour+":"+new_mins+":"+new_secs +"+05:30"
        end_time_1=new_year+"-"+new_month+"-"+new_day+"T"+new_hour+":"+end_mins+":"+new_secs+"+05:30" 
        task=(Verb[1]+' '+Noun[0])
        createEvent(task,start_time_1,end_time_1)
################################################################################
    else:
        print('I won\'t Remind you anything')

def checkStop():
    global app
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")

def press_history(win):
    app.showSubWindow(win)

def press_info(win):
    app.showSubWindow(win)

def recog(audio,r):
    try:    
        text=r.recognize_google(audio)
        print(text)        
        analyse(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
   

def press_record():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    recog(audio,r)
    # es.text=text_spoken

def up_event(app,events):
    i=0
    color=['pink','yellow','blue','orange','purple','red','white','grey','brown','green']
    for e in events:
        app.addLabel(i,e['start'].get('dateTime', e['start'].get('date'))+" "+e['summary'])
        i+=1

def input_text():
    global app
    text_typed=app.getEntry("Enter Text ")
    if(len(str(text_typed)) != 0):
        print(str(text_typed))
        analyse(str(text_typed))
    else:
        app.setEntry("Enter Text ","Please enter text here and then press the button")
try:
    with gui("RemindMe","fullscreen",bg="orange",font={"size":22}) as app:
    # app.gui("RemindMe","840x640",bg="orange",font={"size":22})
    # app.addButtons(["Info"],[press_info],0,2)
    # app.addLabel("title","Welcome!",1,1)
    # app.addButtons(["Upcoming Events"],[press_history],2,0)
    # app.addButtons(["Record"],[press_record],2,1)
    # app.addButtons(["Past Events"],[press_history],2,2)
    #this is for upcoming window
    #this is for info window
    #the app starts
        app.addButtons(["Info"],[press_info],0,2)
        app.addLabel("title","Welcome to RemindMe!",0,1)
        app.setLabelEntryBg("white")
        app.addLabelEntry("Enter Text ",1,1)
        app.addButtons(["Enter"],[input_text],1,2)
        app.setFocus("Enter Text ")
        app.addButtons(["Upcoming Events"],[press_history],2,0)
        app.addButtons(["Record"],[press_record],2,2)
        app.setStopFunction(checkStop)

        #this is for info window
        app.startSubWindow("Info",modal=True)
        app.addLabel("sT1","This is the RemindMe! app developed by Team 5")
        app.addLabel("sT2","To set a reminder: ")
        app.addLabel("sT3","1. Press the Record button to record reminder using voice input")
        app.addLabel("sT4","2. Enter text in the below given text field")
        app.addLabel("sT5","To see your upcoming events click on the Upcoming Events button")
        app.addLabel("sT6","To see your past events click on the Past Events button")
        app.stopSubWindow()
        
               #this is for the upcoming events window
        app.startSubWindow("Upcoming Events",modal=True)
        service=auth()
        events=upcomingEvents(service)
        up_event(app,events)
        app.stopSubWindow()


        app.go()
except:
    print("App stopped!")
