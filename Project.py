from tkinter import ttk,Tk,Toplevel,messagebox
from tkinter import *
import tkinter
import webbrowser
import speech_recognition as sr
from pygame import mixer
import pymysql.cursors
import time
import cv2
from datetime import date,datetime
from PIL import ImageTk,Image
from keras.models import model_from_json
import numpy as np 
connection = pymysql.connect(host = 'localhost',user = 'root',password = 'XXXX',db = 'ead',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
mycursor = connection.cursor()

face_cascad = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
flag = 0
flag_1 = 0

np.random.seed(7)
json_file = open('model_gray.json','r')
classifier_json = json_file.read()
json_file.close()

classifier = model_from_json(classifier_json)
classifier.load_weights("model_gray.h5")

def exit_the_system_welcome():
    answer = messagebox.askquestion("Exit","Do You Really Want To Exit")
    if answer == "yes":
        root.destroy()
    
    
def enter_the_system_welcome():
    root.withdraw()
#####################################################################################
    #Face Detection Running
#####################################################################################
    video = cv2.VideoCapture(1)
    start_time = time.time()
    flag = 0
    while True:
        ret,img_cam = video.read()
        faces = face_cascad.detectMultiScale(img_cam,scaleFactor = 1.25,minNeighbors= 3)
        for x,y,w,h in faces:
            img_cam = img_cam[y:y+h,x:x+w]
            img_cam = cv2.cvtColor(img_cam,cv2.COLOR_BGR2GRAY)
            cv2.imwrite("Face Detected.jpg",img_cam)
            flag = 1
        #cv2.imshow("SHOW",img_cam)           
        key = cv2.waitKey(1)
        if time.time() - start_time > 2:
            break
        if key == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()

    if flag == 0:
        print("Face Not Detected")
        messagebox.showerror("Warning","Face Not Detected")
        root.deiconify()
        
    def exit_the_system_login():
        '''
        answer = messagebox.askquestion("Exit","Do You Really Want To Exit")
        if answer == "yes":
        '''
        root.deiconify()
        root_1.withdraw()
    
    def enter_the_system_login():
        root_1.withdraw()       
        
        
        def exit_the_system_voice_search():
            root_1.deiconify()
            root_2.withdraw()
        
        def enter_the_system_voice_search():
            flag_1 = 0
            root_2.withdraw()
            mycursor.execute("Select * from emp_credentials")
            emp_id = emp_id_entry.get()
            password = password_entry.get()
            for row in mycursor:
                if(emp_id == row['emp_id'] and password == row['password']):
                    flag_1 = 1
            emp_id_entry.delete(0,END)
            password_entry.delete(0,END)
            if flag_1 == 0:
                messagebox.showerror("Warning","Invalid Credentials")
                root_2.deiconify()
            else:
                mycursor.execute("select emp_name from emp_information where emp_id = %s",(emp_id))
                for row in mycursor:
                    emp_name = row['emp_name']
                    
                query = ("Insert into login_time(emp_name,emp_id,login_date,login_time) values(%s,%s,%s,%s)")
                x = (date.today())
                y = datetime.now().time()
                z = str(y.hour)+":"+str(y.minute)+":"+str(y.second)
                val = (emp_name,emp_id,x,z)
                mycursor.execute(query,val)
                connection.commit()
                
                
                root_3 = Toplevel()
                root_3.title("Universal Search Bar")
                root_3.iconbitmap('./asset/mic.ico')
                
                frame_3 = Frame(root_3,width = 640,height = 480)
                
                #photo = ImageTk.PhotoImage(Image.open('download.jpg'))
                
                label1 = Label(root_3,text = "Search Engine")
                label1.config(font = ("Courier",35))
                label1.place(x = 140, y = 230)
                entry1 = Entry(root_3,width = 40,font=('Courier', 15))
                entry1.place(x = 80, y = 300)
                
                btn2 = tkinter.StringVar()
                
                def exit_the_system_last():
                    root_2.deiconify()
                    root_3.withdraw()
                
                
                def search(engine,searched_query):
                    x = (date.today())
                    #print(x)
                    y = datetime.now().time()
                    z = str(y.hour)+":"+str(y.minute)+":"+str(y.second)
                    #print(z)
                    query = ("Insert into search_date_time(emp_id,search_engine,search_query,search_date,search_time) values(%s,%s,%s,%s,%s)")
                    val = (emp_id,engine,searched_query,x,z)
                    mycursor.execute(query,val)
                    connection.commit()
                
                def callback():
                    if btn2.get() == 'google' and entry1.get() != " ":
                        search("Google",entry1.get())
                        webbrowser.open('http://google.com/search?q='+entry1.get())
                    elif btn2.get() == 'yahoo' and entry1.get() != " ":
                        search("Yahoo",entry1.get())
                        webbrowser.open('https://in.search.yahoo.com/search?p='+entry1.get()+'&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8')
                    elif btn2.get() == 'amazon' and entry1.get() != " ":
                        search("Amazon",entry1.get())
                        webbrowser.open('https://www.amazon.in/s?k=' + entry1.get()+ '&ref=nb_sb_noss_2')
                    elif btn2.get() == 'youtube' and entry1.get() != " ":
                        search("Youtube",entry1.get())
                        webbrowser.open("https://youtube.com/results?search_query="+entry1.get())
                    else:
                        pass
                		
                def get(event):
                    if btn2.get() == 'google' and entry1.get() != " ":
                        search("Google",entry1.get())
                        webbrowser.open('http://google.com/search?q='+entry1.get())
                    elif btn2.get() == 'yahoo' and entry1.get() != " ":
                        search("Yahoo",entry1.get())
                        webbrowser.open('https://in.search.yahoo.com/search?p='+entry1.get()+'&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8')
                    elif btn2.get() == 'amazon' and entry1.get() != " ":
                        search("Amazon",entry1.get())
                        webbrowser.open('https://www.amazon.in/s?k=' + entry1.get()+ '&ref=nb_sb_noss_2')
                    elif btn2.get() == 'youtube' and entry1.get() != " ":
                        search("Youtube",entry1.get())
                        webbrowser.open("https://youtube.com/results?search_query="+entry1.get())
                    else:
                        pass
                
                	
                def buttonClick():
                    mixer.init()
                    mixer.music.load('./asset/chime1.mp3')
                    mixer.music.play()
                    
                    r = sr.Recognizer()
                    r.pause_threshold = 0.7
                    r.energy_threshold = 400
                    
                    with sr.Microphone() as source:
                        audio = r.listen(source)
                        try:
                            text = (r.recognize_google(audio))
                            mixer.music.load('./asset/chime1.mp3')
                            mixer.music.play()
                            entry1.focus()
                            entry1.delete(0,END)
                            entry1.insert(0,text)
                            
                            if btn2.get() == 'google' and entry1.get() != " ":
                                search("Google",text)
                                webbrowser.open('http://google.com/search?q=' + text)
                            elif btn2.get() == 'yahoo' and entry1.get() != " ":
                                search("Yahoo",text)
                                webbrowser.open('https://in.search.yahoo.com/search?p='+text+'&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8')
                            elif btn2.get() == 'amazon' and entry1.get() != " ":
                                search("Amazon",text)
                                webbrowser.open('https://www.amazon.in/s?k=' + text+ '&ref=nb_sb_noss_2')
                            elif btn2.get() == 'youtube' and entry1.get() != " ":
                                search("Youtube",text)
                                webbrowser.open('https://youtube.com/results?search_query=' + text)
                            else:
                                pass
                            
                        except sr.UnknownValueError:
                            print("Could not understand audio")
                        except sr.RequestError as e:
                            print("Could not requests Results")
                        else:
                            pass
                            
                entry1.bind('<Return>',get)
                		
                MyButton1 = Button(root_3,text = 'Search',width = 15,borderwidth = 7,command = callback)
                MyButton1.place(x = 90, y = 400)
                MyButton1.config(font=("Courier", 10))
                
                MyButton_exit = Button(root_3,text = 'Go Back',width = 15,borderwidth = 7,command = exit_the_system_last)
                MyButton_exit.place(x = 410, y = 400)
                MyButton_exit.config(font=("Courier", 10))
                
                MyButton_voice = Button(root_3,text = "Voice Search",width = 15,borderwidth = 7,command = buttonClick)
                MyButton_voice.place(x = 250,y  = 400)
                MyButton_voice.config(font=("Courier", 10))
                
                MyButton2 = Radiobutton(root_3,text='Google',value = 'google',variable = btn2)
                MyButton2.config(font=("Courier", 15))
                MyButton2.place(x = 80, y = 350)
                
                MyButton3 = Radiobutton(root_3,text='Yahoo',value = 'yahoo',variable = btn2)
                MyButton3.place(x = 200, y = 350)
                MyButton3.config(font=("Courier", 15))
                
                MyButton4 = Radiobutton(root_3,text='Amazon',value = 'amazon',variable = btn2)
                MyButton4.place(x = 320, y = 350)
                MyButton4.config(font=("Courier", 15))
                
                MyButton5 = Radiobutton(root_3,text='Youtube',value = 'youtube',variable = btn2)
                MyButton5.place(x = 450 , y = 350)
                MyButton5.config(font=("Courier", 15))
                
                img_3 = ImageTk.PhotoImage(Image.open("./asset/images.jpg"))
                panel_3 = Label(root_3, image = img_3)
                panel_3.place(x = 220,y = 0)
                
                entry1.focus()
                root_3.wm_attributes('-topmost',1)
                btn2.set('google')
                frame_3.pack()
                root_3.mainloop()




        def show_databases():
            flag_1 = 0
            root_2.withdraw()
            mycursor.execute("Select * from emp_credentials")
            emp_id = emp_id_entry.get()
            password = password_entry.get()
            for row in mycursor:
                if(emp_id == row['emp_id'] and password == row['password']):
                    flag_1 = 1
            emp_id_entry.delete(0,END)
            password_entry.delete(0,END)
            if flag_1 == 0:
                messagebox.showerror("Warning","Invalid Credentials")
                root_2.deiconify()
            else:
                mycursor.execute("select emp_name from emp_information where emp_id = %s",(emp_id))
                for row in mycursor:
                    emp_name = row['emp_name']
                    
                query = ("Insert into login_time(emp_name,emp_id,login_date,login_time) values(%s,%s,%s,%s)")
                x = (date.today())
                y = datetime.now().time()
                z = str(y.hour)+":"+str(y.minute)+":"+str(y.second)
                val = (emp_name,emp_id,x,z)
                mycursor.execute(query,val)
                connection.commit()
                
                
                def display_login_time():
                    text = Text(root_3,width = 85)
                    text.config(font=("Courier", 15))
                    text.insert(END,"S_NO      EMP_NAME                EMP_ID              LOGIN_DATE         LOGIN_TIME\n")
                    mycursor.execute("Select * from login_time")
                    for row in mycursor:
                        line_new = '{:>1}  {:>17}  {:>19} {:>19}  {:>15}'.format(row['S_NO'], row['emp_name'], row['emp_id'],row['login_date'],row['login_time'])
                        text.insert(END,line_new + '\n')
                    text.config(state = DISABLED)
                    text.place(x = 35, y = 200)
                    
                def exit_data_display():
                    root_2.deiconify()
                    root_3.withdraw()

                def display_search_date_time():
                    text = Text(root_3,width = 85)
                    text.config(font=("Courier", 15))
                    text.insert(END,"S_NO  EMP_ID         SEARCH ENGINE    SEARCH_QUERY    SEARCH_DATE    SEARCH_TIME\n")
                    mycursor.execute("Select * from search_date_time")
                
                    for row in mycursor:
                        line_new = '{:>1}  {:>13}  {:>10} {:>16}  {:>17}  {:>11}'.format(row['S_NO'], row['emp_id'], row['search_engine'],row['search_query'],row['search_date'],row['search_time'])
                        text.insert(END,line_new + '\n')
                    text.config(state = DISABLED)
                    text.place(x = 35, y = 200)
    
                def display_employee_information():
                    text = Text(root_3,width = 85)
                    text.config(font=("Courier", 15))
                    text.insert(END,"S_NO    EMP_ID            EMP_NAME            EMP_DESIGNATION          EMP_SALARY\n")
                    mycursor.execute("Select * from emp_information")
                    for row in mycursor:
                        line_new = '{:>1}  {:>15}  {:>18} {:>24}  {:>13}'.format(row['S_NO'], row['emp_id'], row['emp_name'],row['emp_designation'],row['emp_salary'])
                        text.insert(END,line_new + '\n')
                    text.config(state = DISABLED)
                    text.place(x = 35, y = 200)
    
                def display_employee_personal_information():
                    text = Text(root_3,width = 85)
                    text.config(font=("Courier", 15))
                    text.insert(END,"S_NO  EMP_ID      EMP_NAME        EMP_AADHAR_NUMBER      EMP_DOB      EMP_CONTACT\n")
                    mycursor.execute("Select * from emp_personal")
                    for row in mycursor:
                        line_new = '{:>1}  {:>13}  {:>10} {:>17}  {:>16}  {:>12}'.format(row['S_no'], row['emp_id'], row['emp_name'],row['emp_aadhar_number'],row['emp_dob'],row['emp_contact'])
                        text.insert(END,line_new + '\n')
                    text.config(state = DISABLED)
                    text.place(x = 35, y = 200)
                    

                    
                root_3 = Tk()
                frame_3 = Frame(root_3,width = 1100,height = 600)
                
                label = Label(root_3,text = "SECURITY SYSTEM")
                label.config(font=("Courier", 60,'bold'))
                label.place(x = 170,y = 30)
                
                button_text_1 = Button(root_3,text = "Login Time",borderwidth = 10,command = display_login_time)
                button_text_1.place(x = 45,y = 150)
                button_text_1.config(font=("Courier", 15))
                
                button_text_2 = Button(root_3,text = "Search Date Time",borderwidth = 10,command = display_search_date_time)
                button_text_2.place(x = 195,y = 150)
                button_text_2.config(font=("Courier", 15))
                
                button_text_3 = Button(root_3,text = "Employee Information",borderwidth = 10,command = display_employee_information)
                button_text_3.place(x = 415,y = 150)
                button_text_3.config(font=("Courier", 15))
                
                button_text_4 = Button(root_3,text = "Employee Personal Information",borderwidth = 10,command = display_employee_personal_information)
                button_text_4.place(x = 685,y = 150)
                button_text_4.config(font=("Courier", 15))
                
                button_text_exit = Button(root_3,text = "Go Back",borderwidth = 10,command = exit_data_display)
                button_text_exit.place(x = 950,y = 50)
                button_text_exit.config(font=("Courier", 15))
                
                frame_3.pack()
                root_3.mainloop()

        
        root_2 = Toplevel()
        root_2.title("Enter Your Credentials")
        
        frame_2 = Frame(root_2,width = 640,height = 480)
        
        emp_id_label = Label(root_2,text = "Employee Id")
        emp_id_entry = Entry(root_2,width = 20)
        emp_id_entry.config(font=("Courier", 20))
        emp_id_entry.place(x = 250, y = 280)
        emp_id_label.config(font=("Courier", 20))
        emp_id_label.place(x = 40,y = 280)
        
        password_label = Label(root_2,text = "Password")
        password_label.config(font=("Courier", 20))
        password_label.place(x = 40,y = 330)
        
        password_entry = Entry(root_2,width= 20)
        password_entry.place(x = 250,y = 330)
        password_entry.config(font=("Courier", 20))
        
        button_login = Button(root_2,text = "Search Engine",width = 13,borderwidth = 7,command = enter_the_system_voice_search)
        button_login.config(font=("Courier", 15))
        button_login.place(x = 230, y = 400)
        
        button_data = Button(root_2,text = "DataBase",width = 13,borderwidth = 7,command = show_databases)
        button_data.config(font=("Courier", 15))
        button_data.place(x = 30, y = 400)
        
        button_exit = Button(root_2,text = "Go Back",width = 13,borderwidth = 7,command = exit_the_system_voice_search)
        button_exit.config(font=("Courier", 15))
        button_exit.place(x = 430, y = 400)
    
        
        img_2 = ImageTk.PhotoImage(Image.open("./asset/security_image.jpg"))
        panel_2 = Label(root_2, image = img_2)
        panel_2.place(x = 100,y = 30)
        
        frame_2.pack()
        root_2.mainloop()

    if flag == 1:
        image = cv2.imread('Face Detected.jpg')
        
        image = cv2.resize(image,(32,32))
        arr = np.array(image).reshape((32,32,3))
        arr = np.expand_dims(arr,axis = 0)
        prediction = classifier.predict(arr)
        if(prediction[0][0] == 1):
            name_detected = "Person_1"
        else:
            name_detected = "Person_2"  
            
        root_1 = Toplevel()
        root_1.title("Welcome To The Company")
        
        frame_1 = Frame(root_1,width = 640,height = 480)
        
        wel_label = Label(root_1,text = "Welcome To The Company\n Mr." + name_detected )
        wel_label.config(font=("Courier", 30))
        wel_label.place(x = 60,y = 50)
        
        button_exit = Button(root_1,text = "Go Back",width = 15,borderwidth = 7,command = exit_the_system_login)
        button_exit.config(font=("Courier", 15))
        button_exit.place(x = 330, y = 410)
        
        button_enter = Button(root_1,text = "Enter",width = 15,borderwidth = 7,command = enter_the_system_login)
        button_enter.config(font=("Courier", 15))
        button_enter.place(x = 130, y = 410)
        
        if name_detected == "Person_1":
            image_path = "./asset/Person_1.jpg"
        else:
            image_path = "./asset/Person_2.jpg"
        
        img_1 = ImageTk.PhotoImage(Image.open(image_path))
        panel_1= Label(root_1, image = img_1)
        panel_1.place(x = 200,y = 150)
    
        frame_1.pack()
        root_1.mainloop()
    


####################################################################################       
#First Window ( Bring Your Face )
####################################################################################       
root = Tk()
root.title("Security System")
frame = Frame(root,width = 640,height = 480)
wel_label = Label(root,text = "Please Bring Your \nFace In Front\n Of\nThe Camera")
wel_label.config(font=("Courier", 30))
wel_label.place(x = 210,y = 50)
wel_label_2 = Label(root,text = " Picture will\n be Clicked in\n 2 seconds")
wel_label_2.config(font=("Courier", 30))
wel_label_2.place(x = 250,y = 250)
button_exit = Button(root,text = "Exit",width = 13,borderwidth = 7,command = exit_the_system_welcome)
button_exit.config(font=("Courier", 15))
button_exit.place(x = 430, y = 410)
button_enter = Button(root,text = "OK",width = 13,borderwidth = 7,command = enter_the_system_welcome)
button_enter.config(font=("Courier", 15))
button_enter.place(x = 250, y = 410)
img = ImageTk.PhotoImage(Image.open("./asset/security.png"))
panel = Label(root, image = img)
panel.place(x = 20,y = 130)    
frame.pack()
root.mainloop()
####################################################################################
