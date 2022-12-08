"""
This program is a survey (questionnaire) containing questions from: 
'Analysis and prediction of professional sports consumer 
behavior using artificial neural network'
Kyung Hee University
2011.08

Programmer: Joshua Willman
Date: 2019.11.17
"""
from tkinter import (Tk, Label, Button, Radiobutton, Frame, Menu,
    messagebox, StringVar, Listbox, BROWSE, END, Toplevel, Entry)
from tkinter import ttk
from tkinter import messagebox
import pathlib
import time
import csv
import os.path
import tkinter as tk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import date
import warnings
warnings.filterwarnings("ignore")




# create empty lists used for each set of questions
user_inputs_list = []
lifestyle_list = []
mcq_ans_list = []
bone_ans_list = []
general_answers_list = []

def dialogBox(title, message):
    """
    Basic function to create and display general dialog boxes.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 800, 500
    positionRight = int(dialog.winfo_screenwidth()/2 - dialogWidth/2)
    positionDown = int(dialog.winfo_screenheight()/2 - dialogHeight/2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.configure(bg="#baffc9")
    
    style_ = ttk.Style()
    style_.configure("BW.TLabel", background="white")

    ttk.Label(dialog, text=message, font=('Calibri', 18), style_="BW.TLabel", relief="ridge").pack(side="top", pady=50)

    enter_button = ttk.Button(dialog, text="Quit", command=quit)
    enter_button.pack(ipady=5, pady=20)

    dialog.mainloop()


def nextSurveyDialog(title, message, cmd):
    return None

def disable_event():
    pass

def finishedDialog(title, message):
    """
    Display the finished dialog box when user reaches the end of the survey.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 325, 150
    positionRight = int(dialog.winfo_screenwidth()/2 - dialogWidth/2)
    positionDown = int(dialog.winfo_screenheight()/2 - dialogHeight/2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Quit", command=quit)
    ok_button.pack(ipady=3, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", disable_event) # prevent user from clicking ALT + F4 to close
    dialog.mainloop()

def writeToFile(filename, answer_list):
        headers = []  
        file_exists = os.path.isfile(filename)

        with open(filename, 'a') as csvfile:
            for i in range(1, len(answer_list) + 1):
                headers.append("Q{}".format(i))
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            
            if not file_exists:
                writer.writerow(headers) # file doesn't exist yet, write a header

            writer.writerow(answer_list)

class otherPopUpDialog(object):
    def __init__(self, master, text):
        top=self.top=Toplevel(master)
        self.text = text
        top.wm_title("Other Answers")
        top.grab_set()
        dialogWidth, dialogHeight = 200, 150
        positionRight = int(top.winfo_screenwidth()/2 - dialogWidth/2)
        positionDown = int(top.winfo_screenheight()/2 - dialogHeight/2)
        top.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
        self.label = Label(top, text=self.text)
        self.label.pack(ipady=5)
        self.enter = Entry(top)
        self.enter.pack(ipady=5)
        self.ok_button = Button(top, text="Ok", command=self.cleanup) 
        self.ok_button.pack(ipady=5)

    def cleanup(self):
        self.value = self.enter.get()
        self.top.destroy()

class Survey(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # call closing protocol to create dialog box to ask 
        # if user if they want to quit or not.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        Tk.wm_title(self, "Survey")

        # get position of window with respect to screen
        windowWidth, windowHeight = 800, 500
        positionRight = int(Tk.winfo_screenwidth(self)/2 - windowWidth/2)
        positionDown = int(Tk.winfo_screenheight(self)/2 - windowHeight/2)
        Tk.geometry(self, newGeometry="{}x{}+{}+{}".format(
            windowWidth, windowHeight, positionRight, positionDown))
        Tk.maxsize(self, windowWidth, windowHeight)

        # Create container Frame to hold all other classes, 
        # which are the different parts of the survey.
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        Tk.config(self, menu=menubar)

        # create empty dictionary for the different frames (the different classes)
        self.frames = {}

        for fr in (StartPage, yesnoclass, mcqclass,
            num_mcqclass, gender_class,
            bone_class, sleep_class, workout_class, boneacc_class, 
            input_class):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def show_frame(self, cont):
        """
        Used to display a frame.
        """
        frame = self.frames[cont]
        frame.tkraise() # bring a frame to the "top"

class StartPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        
        # set up start page window
        
        self.configure(bg="#baffc9")
        style = ttk.Style()
        style.configure("BW.TLabel", background="white")

        ttk.Label(self, text="     Lifestyle Analysis AI", font=('Calibri', 22), style="BW.TLabel", borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        
        
        
        ttk.Label(self, text="          To predict the risk of age-related diseases", font=('Calibri', 14), justify='center' , style="BW.TLabel", borderwidth=2, relief="ridge").pack(pady=20, padx=20, ipadx=25, ipady=23)

        

        start_button = ttk.Button(self, text="Begin!",  
            command=lambda: controller.show_frame(yesnoclass))
        start_button.pack(ipadx=20, ipady=15, pady=25)

        quit_button = ttk.Button(self, text="Quit", command=self.on_closing)
        quit_button.pack(ipady=3, pady=10)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Well, I hope you're not at any age-related risk, do you really don't want to see?"):
            self.controller.destroy() 

class yesnoclass(Frame):
    """
    Class that displays the window for the life style survey questions. 
    When the user answers a question, the answer saved to a list.  
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="#eecff4")
        global lifestyle_list
        
        style1 = ttk.Style()
        #style.configure("BW.TLabel", background="white")
        style1.configure('TButton', background = 'white', width = 30, height=20, borderwidth=5, focusthickness=5, focuscolor='green', relief="sunken")
        style1.map('TButton', background=[('active','green')])



        # Create header label
        ttk.Label(self, text="   Yes/No Questions", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        #self.questions = ["Have you ever fractured a bone?", "Have you ever experienced discomfort in your chest?"]        

        self.questions = ["Have you ever fractured a bone?", "Have you ever experienced discomfort in your chest?", 
                          "Does it happen while walking at ordinary pace?", "Does it happen when you are going uphill or in a hurry?",
                          "Does it stay even after resting for sometime?", "Has your doctor ever asked you to check your sugar?",
                          "Are you taking insulin/medication to lower your sugar?", "Do you smoke?",
                          "Are you friends or in closely shared space with someone who smokes regularly?", 
                          "Do you ignore nutrition information provided on the packaging? ",
                          "Do you eat your meals at unplanned time intervals?", "Do you have any issue with poor appetite or overeating?",
                          "Do you have any trouble in sleeping?", "Have you ever been advised by a doctor for the use of sleeping pills?",
                          "Do you consume any kind of drugs on regular basis?", "Do you consume any kind of alcohol on regular basis?", 
                          "Do you have issues in concentrating doing simple things like newspapers reading?", "Do you have any restless feelings?"
                          ]

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="Options。", font=('Calibri', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Yes", "No"]

        scale = [("         Yes", 2), ("         No", 1)]

        self.var = StringVar()
        self.var.set(0) # initialize


        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=0, ipady=0)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)
        
        
        
    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            #print(
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()
            lifestyle_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            ##next_survey_text = "End of Part 1."
            ##nextSurveyDialog("Next Survey", #next_survey_text, lambda: self.controller.show_frame(mcqclass))
            self.controller.show_frame(mcqclass)
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            lifestyle_list.append(selected_answer)
            user_inputs_list.append(selected_answer)       

            self.var.set(0) # reset value for next question

            time.sleep(.2) # delay between questions
            

class mcqclass(Frame):
    """
    Class that displays the window for the significant consumption trends survey questions. 
    When the user answers a question, the answer is written to a 
    csv file. 
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="#ffdddd")
        global mcq_ans_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)
        
        #self.questions = ["Have you ever got your bone fractured?", "How often do you workout?"]

        self.questions = ["How often do you skip workout?",
                          "How much time do you spend sitting on a typical day?", 
                          "Does your profession cause you to make sedentary lifestyle choices?",
                          "How often do you smoke?",
                          "How often do you consume fast food?",
                          "How often do you consume Drugs?", 
                          "How often do you consume Alcohol?",
                          "How often do you feel down depressed or hopeless in a day?", 
                          "Have you ever felt that you would be better off dead or hurting yourself?", 
                          "How active are you on social media?", 
                          "Are you inactive off social media?"
                          ]
                          
        #never, once , sometimes, often, very often

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="4 ops。", font=('Calibri', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        #scale_text = ["j", "k", "l", "m", "n"]

        scale = [("Never", 1), ("Once", 2), ("At times", 3), ("Often", 4)]

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        '''for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)'''

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)
        
    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            #print
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()
            mcq_ans_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            #next_survey_text = "End of Part 2."
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: self.controller.show_frame(num_mcqclass))
            self.controller.show_frame(num_mcqclass)
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            mcq_ans_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            self.var.set(0) # reset value for next question

            time.sleep(.2) # delay between questions

class num_mcqclass(Frame):
    """
    Class that displays the window for the future consumption trends survey questions. 
    When the user answers a question, the answer is written to a 
    csv file. 
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="#ffb3ba") 
        global bone_ans_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        self.questions = ["Do you maintain a calcium rich diet for your bones?", "How much distance you walk on a typical day? (in km)"]

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="qss", font=('Calibri', 10)).pack(padx=50)

        #scale_text = ["不同意", "不太同意", "基本同意", "非常同意", "完全同意"]

        # Not at all, somewhat, average, agree, strongly agree
        scale = [("Never", 4), ("1 or 2", 3), ("<=4", 2), (">4", 1)] #1/2/<=4/>4

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        '''for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)'''

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            #print("No Value Given", 
                print("You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()

            bone_ans_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            #next_survey_text = "End of Part 3."
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(gender_class)
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()

            bone_ans_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            self.var.set(0) # reset value for next question

            time.sleep(.2) # delay between questions

class gender_class(Frame):
    """
    Displays gender question from General questions.
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="#bae1ff") 

        global general_answers_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        self.question = "How would you describe your gender?"

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="1. {}".format(self.question), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")       
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="Que3。", font=('Calibri', 10)).pack(padx=50)

        scale = [("Male", "Male"), ("Female", "Female"),("Non-binary", "Non-binary")]

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            time.sleep(.2) # delay between questions
            #next_survey_text = 'Part 4'
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(bone_class)
            #self.controller.show_frame(bone_class)

class bone_class(Frame):
    """
    Displays marriage question from General questions.
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="#bae1ff") 
        global general_answers_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18),style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)
        self.question = "How old were you when you got your bone fractured?"

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.question)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}".format(self.question), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="qss", font=('Calibri', 10)).pack(padx=50)

        #scale_text = ["不同意", "不太同意", "基本同意", "非常同意", "完全同意"]

        # Not at all, somewhat, average, agree, strongly agree
        scale = [("I never ot my bone fractured", 1), ("Childhood", 2), ("Teenage", 3), ("Adulthood", 4)] #1/2/<=4/>4

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        '''for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)'''

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)
    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            time.sleep(.2) # delay between questions
            #next_survey_text='part 5'
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(sleep_class)
            #self.controller.show_frame(bone_class)

class sleep_class(Frame):
    """
    Displays age question from General questions.
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.configure(bg="#bae1ff") 
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18),style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        self.question = "How much do you sleep on weekdays? (in  hrs)? "

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.question)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="1. {}".format(self.question), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #(self, text="qss", font=('Calibri', 10)).pack(padx=50)


        # Not at all, somewhat, average, agree, strongly agree
        scale = [("<6", 2), ("6-8", 1), (">8", 3), ("irregular", 4)] #1/2/<=4/>4 <6/6-8/>8/irregular

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)

    def nextQuestion(self):
        answer = self.var.get()

        if answer == '0':
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            time.sleep(.2) # delay between questions
            #next_survey_text = ''
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(workout_class)
            #self.controller.show_frame(bone_class)

class workout_class(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.configure(bg="#bae1ff") 
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="       and some more...",font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

        self.question = "What is the intensity of your workout?"
        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.question)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="1. {}".format(self.question), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="qss", font=('Calibri', 10)).pack(padx=50)

        #scale_text = ["不同意", "不太同意", "基本同意", "非常同意", "完全同意"]

        # Not at all, somewhat, average, agree, strongly agree
        scale = [("I never workout", 4), ("Low", 3), ("Medium", 2), ("High", 1)] 

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        #checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        #checkbox_scale_frame.pack(pady=2)

        '''for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)'''

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)
        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)



    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            time.sleep(.2) # delay between questions
            #next_survey_text = ''
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(boneacc_class)
            #self.controller.show_frame(bone_class)

class boneacc_class(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.configure(bg="#bae1ff") 
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="       and some more...", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)
        self.question = "How did you get your bone fractured?"

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="1. {}".format(self.question), font=('Calibri', 14), background='white', borderwidth=2, relief="sunken")
        self.question_label.pack(anchor='center', padx=50, pady=30)
        #Label(self, text="选择最适合您的答案。", font=('Calibri', 10)).pack(padx=50)

        scale = [("I never got my bone fractured",1), ("Daily activities", 4), ("While playing", 3),
                 ("Vehicle accident", 2)]

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)


        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=4, relief="ridge")
        checkbox_frame.pack( anchor= 'center' , ipadx=2, ipady=2)

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(anchor='center', ipadx=25, ipady=5)

        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)

    def nextQuestion(self):
        answer = self.var.get()

        if answer == '0':
            print("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)
            user_inputs_list.append(selected_answer)

            time.sleep(.2) # delay between questions
            #next_survey_text = ''
            #nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(input_class)
            #self.controller.show_frame(bone_class)

class input_class(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.configure(bg="#d896ff")
        self.controller = controller

        global general_answers_list
        
        # store email address and password
        self.name = StringVar()
        #self.name.set(0) # initialize
        self.by = StringVar()
        #self.by.set(0) # initialize
        self.country = StringVar()
        #self.country.set(0) # initialize
        self.weight = StringVar()
        #self.weight.set(0) # initialize
        self.height = StringVar()
        #self.height.set(0) # initialize
        
        #inputs_ = [name,by,country,weight,height]

        # Create header label
        ttk.Label(self, text="      Last Few Questions..!", font=('Calibri', 18), style="BW.TLabel",
                  borderwidth=2, relief="ridge").pack(pady=25, padx=20, ipadx=15, ipady=15)

       # name
        #name_label = ttk.Label(self, text="Enter your name?", font=('Calibri', 16),  style="BW.TLabel",
         #         borderwidth=0, relief="ridge").pack(anchor = 'w', padx=20, pady=15)
        #email_label.pack(fill='x', expand=True)

        name_entry = ttk.Entry(self, textvariable=self.name, width=40)
        name_entry.insert(0, "Enter your name ")
        name_entry.pack(anchor = 'center')
        name_entry.focus()
        
        by_entry = ttk.Entry(self, textvariable=self.by, width=40)
        by_entry.insert(0, "Enter your birth year ")
        by_entry.pack(anchor = 'center')
        by_entry.focus()
        
        c_entry = ttk.Entry(self, textvariable=self.country,  width=40)
        c_entry.insert(0, "Enter your country name ")
        c_entry.pack(anchor = 'center')
        c_entry.focus()


        wt_entry = ttk.Entry(self, textvariable=self.weight,  width=40)
        wt_entry.insert(0, "Enter your weight (in kg) ")
        wt_entry.pack(anchor = 'center')
        wt_entry.focus()
        ht_entry = ttk.Entry(self, textvariable=self.height, width=40)
        ht_entry.insert(0, "Enter your height (in feet) ")
        ht_entry.pack(anchor = 'center')
        ht_entry.focus()
        
        
        enter_button = ttk.Button(self, text="PREDICT!!", command=self.nextQuestion)
        enter_button.pack(ipady=20, pady=40)


    def nextQuestion(self):
        #selection = self.lb_choices.curselection() 
        answer1 = self.name.get()
        answer2 = self.by.get()
        answer3 = self.country.get()
        answer4_ = self.weight.get()
        answer5_ = self.height.get()
        answer4 = int(answer4_)
        answer5 = int(answer5_)

        if False:
           print("No Value Given", 
              "You did not select an answer.\nPlease try again.")
        else:
            get_selection = [answer1,answer2,answer3,answer4,answer5]
            general_answers_list.append(get_selection)
            user_inputs_list.append(get_selection)
            print('Done-----------------------',get_selection)
            time.sleep(.2) # delay between questions
            self.writeToFile()
            ##next_survey_text = 'SAVING TO FILE'
            ##nextSurveyDialog("Next Survey", #next_survey_text, lambda: 
            self.controller.show_frame(predict_class)
            #self.controller.show_frame(bone_class)

            
    def writeToFile(self):
        df_userinfo = pd.DataFrame()
        # list of names and answer lists
        filenames = ['survey_answers_raw.csv']
        answers_lists = [lifestyle_list,mcq_ans_list,bone_ans_list,general_answers_list]
        for filename, answers in zip(filenames, user_inputs_list):
            writeToFile(filename, answers)
            print('ANSWERS LOGGED')
            #print(lifestyle_list)
            #print(mcq_ans_list)
            #print(bone_ans_list)
            #print(general_answers_list)
            #print(answers_lists)
            print(user_inputs_list)
        df_userinfo['user_info'] = user_inputs_list
        df_userinfo.to_csv('survey_answers.csv')
        testdf = pd.DataFrame()
        header_list = ['Diet', 'Stress', 'BMI', 'Physical_Activity', 'Sleep', 'Osteoporosis',
                      'Cardiovascular', 'Diabetes', 'Smoking', 'Drugs', 'Alcohol','chronological_age']
        testdf = testdf.reindex(columns = header_list)

        data = pd.read_csv('model_input_dataset.csv')
           
        # get the locations
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
           
        # split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
           
        model = DecisionTreeClassifier(max_depth = 5)
        model.fit(X_train, y_train)
        #model_predictions = model.predict(X_test)
        surdf = pd.read_csv('survey_answers.csv')
        diet_input = []
        basic_input = []
        sleep_input = []
        osteo_input = []
        bmi_input = []
        cardio_input = []
        diabt_input = []
        phyact_input = []
        drugs_input = []
        alcol_input = []
        smoke_input = []
        stress_input = []
        for i in range(len(surdf['user_info'])):
            if((i>=9 and i<=11) or i==22):
                diet_input.append(surdf['user_info'][i])
            elif(i==12 or i==13 or i==34):
                sleep_input.append(surdf['user_info'][i])
            elif(i==0 or i==29 or i==33 or i==35):
                osteo_input.append(surdf['user_info'][i]) 
            elif(i>=1 and i<=4):
                cardio_input.append(surdf['user_info'][i]) 
            elif(i==5 or i==6):
                diabt_input.append(surdf['user_info'][i])
            elif(i==18 or i==19 or i==20 or i==32 or i==34 or i==30):
                phyact_input.append(surdf['user_info'][i])
            elif(i==14 or i==23):
                drugs_input.append(surdf['user_info'][i])
            elif(i==15 or i==24):
                alcol_input.append(surdf['user_info'][i])
            elif(i==7 or i==8 or i==21):
                smoke_input.append(surdf['user_info'][i])
            elif(i==16 or i==17 or i==25 or i==26 or i==27 or i==28):
                stress_input.append(surdf['user_info'][i])
        diet_ = [ int(x) for x in diet_input]
        diet_sum = sum(diet_)
        sleep_ = [ int(x) for x in sleep_input]
        sleep_sum = sum(sleep_)+2
        o = [ int(x) for x in osteo_input]
        osteo_sum = sum(o)-4
        c = [ int(x) for x in cardio_input]
        cardio_sum = sum(c)+2
        d = [ int(x) for x in diabt_input]
        diabt_sum = sum(d)+6
        pa = [ int(x) for x in phyact_input]
        pa_sum = sum(pa)-6
        dr = [ int(x) for x in drugs_input]
        drugs_sum = sum(dr)+4
        alc = [ int(x) for x in alcol_input]
        alc_sum = sum(alc)+4
        sm = [ int(x) for x in smoke_input]
        smoke_sum = sum(sm)+2
        st = [ int(x) for x in stress_input]
        stress_sum = sum(st)-10
        ht = int(surdf['user_info'][36].split('\'')[6][6:7])
        ht = ht**2
        wt = int(surdf['user_info'][36].split('\'')[6][2:4])
        bmi_range = int(wt/(ht**2))
        if (bmi_range>=18 and bmi_range<=24):
            bmi_score = 0
        elif(bmi_range>=25 and bmi_range<=30):
            bmi_score = 1
        else:
            bmi_score = 2
        by = int(surdf['user_info'][36].split('\'')[3])
        current_year = date.today().year
        age = current_year - by
        header_list = ['Diet', 'Stress', 'BMI', 'Physical_Activity', 'Sleep', 'Osteoporosis',
                   'Cardiovascular', 'Diabetes', 'Smoking', 'Drugs', 'Alcohol','chronological_age']
        predict_this = pd.DataFrame()
        
        predict_this['Diet'] = diet_sum
        predict_this['Stress'] = stress_sum
        predict_this['BMI'] = bmi_score
        predict_this['Physical_Activity'] = pa_sum
        predict_this['Sleep'] = sleep_sum
        predict_this['Osteoporosis'] = osteo_sum
        predict_this['Cardiovascular'] = cardio_sum
        predict_this['Diabetes'] = diabt_sum
        predict_this['Smoking'] = smoke_sum
        predict_this['Drugs'] = drugs_sum
        predict_this['Alcohol'] = alc_sum
        predict_this['chronological_age'] = age
        
        input_list = []
        input_list.append(1)
        input_list.append(diet_sum)
        input_list.append(stress_sum)
        input_list.append(bmi_score)
        input_list.append(pa_sum)
        input_list.append(sleep_sum)
        input_list.append(osteo_sum)
        input_list.append(cardio_sum)
        input_list.append(diabt_sum)
        input_list.append(smoke_sum)
        input_list.append(drugs_sum)
        input_list.append(alc_sum)
        input_list.append(age)
        
        #X_test.append(input_list)
        print('-------len------',len(X_test))
        #X_test.to_csv('PRE-RESULTS'.csv)

        X_test.loc[len(X_test)] = input_list
        
        ans = model.predict(X_test)[-1]
        #X_test.to_csv('RESULTS'.csv)
        print('predicted ans:', ans)
        
        score = int((model.score(X_train, y_train) )*100)
        print('score:', score)

        if(ans == 0):
            classification = 'at very low risk'
        elif(ans == 1):
            classification = 'at major risk'
        elif(ans == 2):
            classification = 'at risk'
        elif(ans == 3):
            classification = 'at medium risk'
        else:
            classification = 'at low risk'
            
        print('classification:', classification)

            
        dialogBox(title =  '\nPrediction', message = 'Here are the results!\n\n\n You are ' + str(classification) + ' of getting an age-related disease in the future. \n\n\nLifestyle Analysis AI is ' + str(score) + '% confident about this prediction!!')                    
        print('Done')
        #pred_label = ttk.Label(Frame, text=ans, font=('Calibri', 22), borderwidth=5, relief="ridge").pack(padx=20, pady=20)4
        #prediction_text = 


        #enter_button = ttk.Button(Frame, text="QUIT", command=quit)
        #enter_button.pack(ipady=5, pady=20)
        


# Run program
if __name__ == "__main__":
    app = Survey()
    app.mainloop()
    
