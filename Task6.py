from tkinter import *
import os
def restart():
	os.system("shutdown /r /t 1")
def restart_Time():
	os.system("shutdown /r /t 20")
def log_Out():
	os.system("shutdown -1")
def shutdown():
	os.system("shutdown /s /t 30")
st=Tk()     #st is the object of TK class 
st.title("ShutDown App")
st.geometry("500x500")
st.config(bg="Blue")     # for changing te interface color
r_button=Button(st,text="Restart",font=("Time New Roman",20,"bold"),
	relief=RAISED,cursor="plus",command=restart)
r_button.place(x=150,y=60,height=50,width=200)
rt_button=Button(st,text="Restart Time",font=("Time New Roman",20,"bold"),
	relief=RAISED,cursor="plus",command=restart_Time)
rt_button.place(x=150,y=170,height=50,width=200)
lg_button=Button(st,text="Log-Out",font=("Time New Roman",20,"bold"),
	relief=RAISED,cursor="plus",command=log_Out)
lg_button.place(x=150,y=270,height=50,width=200)
sd_button=Button(st,text="Shutdown",font=("Time New Roman",20,"bold"),
	relief=RAISED,cursor="plus",command=shutdown)
sd_button.place(x=150,y=370,height=50,width=200)
st.mainloop()  #for graphical interface showing we use loop