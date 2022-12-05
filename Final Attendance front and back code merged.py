from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import pyttsx3
from PIL import Image,ImageTk
import matplotlib as plt
import customtkinter
import datetime
now = datetime.datetime.now()

customtkinter.set_default_color_theme('green')

present=pyttsx3.init()
unidentified=pyttsx3.init()
#defining login function

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
path="ImagesAttendance"
image=[]
classNames=[]
myList=os.listdir(path)
#print(myList)
for cl in myList:
    curImage=cv2.imread(f'{path}/{cl})')
    image.append(curImage)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

known_encodings = []
known_names = []
encodeList = []
def findEncodingImg():
    for file in os.listdir(path):
        img = cv2.imread(path + '/' + file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        known_encodings.append(encode[0])
        known_names.append(file.split('.')[0])
        # print(known_encodings)
        print(known_names)
        print('Encoded successfully')

findEncodingImg()

def findEncodingImg1(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        return encodeList



def MarkAttendance(name):
    with open("Attendance.csv",'r+')as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dstring=now.strftime("%Y-%m-%d %H:%M:%S")
            f.writelines(f'\n{name},{dstring}')

def check_name_state(name):
    pass

def live_camera():
    #write here backend code face recognition main function
    cap=cv2.VideoCapture(0)
    while True:
        success,img=cap.read()
        imgS=cv2.resize(img, (0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame=face_recognition.face_locations(imgS)
        encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)
        for encodeFace,faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches=face_recognition.compare_faces(known_encodings, encodeFace)
            faceDis=face_recognition.face_distance(known_encodings, encodeFace)
            #print(faceDis)
            matcheIndexes=np.argmin(faceDis)
            if(matches[matcheIndexes]):
                name=classNames[matcheIndexes].upper()
                print(name)
                present.say(name)
                present.runAndWait()
                    

                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0),2)
                cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0),cv2.FILLED)
                cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
                MarkAttendance(name)

                #check_name_state(name)
        cv2.putText(img, 'press q to exit' , (10,18), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,0,255),2)
        cv2.imshow('Attendance System', img)
        if(cv2.waitKey(1) & 0xFF== ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()


def showdata():
    # initalise the tkinter GUI
    global label_file
    global tv1
    root = customtkinter.CTk()

    root.geometry("5000x5000") # set the root dimensions
    root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
    #root.resizable(0, 0) # makes the root window fixed in size.
    root.configure(bg='white')

    # Frame for TreeView
    frame1 = LabelFrame(root, text="Excel Data")
    frame1.place(height=500, width=1000)
    

    # Frame for open file dialog
    file_frame = LabelFrame(root, text="Open File")
    file_frame.place(height=200, width=500, rely=0.65, relx=0)
    file_frame.configure(bg='white')

    # Buttons
    #button1 = Button(file_frame, text="Browse A File", command=lambda: File_dialog())
    #button1.place(rely=0.65, relx=0.50)

    button1 = customtkinter.CTkButton(master=root,
                                     width=120,
                                     height=32,
                                     border_width=0,
                                     corner_radius=8,
                                     text="Browse File",
                                     command=lambda: File_dialog())
    button1.place(relx=0.65, rely=0.50)

    #button2 = Button(file_frame, text="Load File", command=lambda: Load_excel_data())
    #button2.place(rely=0.65, relx=0.30)
    button = customtkinter.CTkButton(master=root,
                                     width=120,
                                     height=32,
                                     border_width=0,
                                     corner_radius=8,
                                     text="Display Data",
                                     command=lambda: Load_excel_data())
    button.place(relx=0.65, rely=0.30)

    # The file/file path text
    label_file = ttk.Label(file_frame, text="No File Selected")
    label_file.place(rely=0, relx=0)



    ## Treeview Widget
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

    treescrolly = Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    treescrollx = Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
    root.mainloop()

def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None



def ProjectCode():
    root= Tk()
    #Make a Canvas (i.e, a screen for your project
    canvas1 = Canvas(root, width = 5000, height = 5000)
    canvas1.pack()

    canvas1.config(bg='white')

    # Popularity label and input box
    label1 = Label(root, text='RecoFace Marking System',font=('Sans Serif',15))
    canvas1.create_window(250, 50, window=label1)

    #Add button in GUI
    button = customtkinter.CTkButton(master=root,
                                     width=120,
                                     height=32,
                                     border_width=0,
                                     corner_radius=8,
                                     text="Live Attendance",
                                     command=live_camera)
    button.place(relx=0.1, rely=0.3)
    #Add button in GUI
    #button3 = Button (root, text='ShowData', bg='white',command=showdata) # button to call the 'values' command above
    #canvas1.create_window(250, 350, window=button3)
    button = customtkinter.CTkButton(master=root,
                                     width=120,
                                     height=32,
                                     border_width=0,
                                     corner_radius=8,
                                     text="Data",
                                     command=showdata)
    button.place(relx=0.1, rely=0.5)

    if now.hour == 17 and now.minute == 39:
        print ('Late')
        #f.writelines(f'Late')
    else :
        print ('On time')
        #f.writelines(f'On time')
     

            

def login():
    #getting form data
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("fill the empty field!")
    else:
      if uname=="admin" and pwd=="1234":
       message.set("Login success")
       login_screen.destroy()
       ProjectCode()
      else:
       message.set("Wrong username or password!")

 
    
#defining loginform function
def Loginform():
    global login_screen
    login_screen = Tk()
    #Setting title of screen
    login_screen.title("Login Form")
    #setting height and width of screen
    login_screen.geometry("5000x5000")
    login_screen.configure(bg='white')
    #declaring variable
    global  message;
    global username
    global password
    username = StringVar()
    password = StringVar()
    message=StringVar()
    
    #Creating layout of login form
    Label(login_screen,width="350", text="Login", font=('Railway',20),bg='white', fg="black").pack()
    Label(login_screen,width="350", text="Reco",bg='white',fg='blue', font=('Impact',30)).pack()
    Label(login_screen,width='350', text='Face Marking',bg='white',fg='black', font=('Impact',30)).pack()
    #Username Label
    Label(login_screen, text="Username * ",bg='white', font=('Railway',15)).place(x=700,y=350)
    #Username textbox0
    #Entry(login_screen, textvariable=username, font=('Railway',15),borderwidth=2, relief="groove").place(x=850,y=250)
    entry = customtkinter.CTkEntry(master=login_screen,
                               placeholder_text="username",
                               textvariable=username,
                               font=('San Francisco',20),
                               width=200,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    entry.place(x=850, y=350)
    



    #Password Label
    Label(login_screen, text="Password * ",bg='white', font=('Railway',15)).place(x=700,y=450)
    #Password textbox
    #Entry(login_screen, textvariable=password,show="*", font=('Railway',15),borderwidth=2, relief="groove").place(x=850,y=350)

    entry = customtkinter.CTkEntry(master=login_screen,
                               placeholder_text="password",
                               textvariable=password,
                               show='*',
                               font=('San Francisco',20),
                               width=200,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    entry.place(x=850, y=450)

    #Label for displaying login status[success/failed]
    Label(login_screen, text="",textvariable=message).place(x=900,y=600)
    #Login button
    #Button(login_screen, text="Login", width=10, height=1, bg="blue", fg="white",font=('Railway',12),command=login).place(x=760,y=450)
    button = customtkinter.CTkButton(master=login_screen,
                                     width=120,
                                     height=32,
                                     border_width=0,
                                     corner_radius=8,
                                     text="Login",
                                     command=login)
    button.place(x=760, y=550)
    
    load = Image.open("Attendance.png")
    render = ImageTk.PhotoImage(load)
    img = Label(login_screen, image=render)
    img.image = render
    img.place(x=0, y=60)


    load = Image.open("Avatar.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(login_screen, image=render)
    img.image = render
    img.place(x=700, y=150)

    





#calling function Loginform
Loginform()
login_screen.mainloop()


