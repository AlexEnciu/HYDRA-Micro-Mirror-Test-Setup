import tkinter as tk
import serial
from tkinter import ttk
from ttkthemes import ThemedTk
import cv2
import time
import os
from tkinter import filedialog


ser = serial.Serial('COM5', 9600)

def on_daq():
    global daq_name_var
    global picture_number_var
    global daq_path_var
    global daq_window

    def take_global_params():
        global daq_name
        daq_name='\\' + daq_name_var.get()
        global picture_number
        picture_number=picture_number_var.get()
        global daq_path
        daq_path=daq_path_var.get()
        daq_window.destroy()
        print("Im Working",daq_path+daq_name+picture_number )
    daq_window = tk.Toplevel(root)
    daq_window.title("DAQ Settings")
    daq_window.geometry("330x140")

    # Create label and entry for daq_name
    daq_name_label = tk.Label(daq_window, text="DAQ Name:")
    daq_name_label.grid(row=0, column=0, padx=5, pady=5)

    daq_name_var = tk.StringVar()
    daq_name_entry = tk.Entry(daq_window, textvariable=daq_name_var)
    daq_name_entry.grid(row=0, column=1, padx=5, pady=5)
    daq_name_var.set("Default Name")
    
    daq_path_label = tk.Label(daq_window, text="Choose path")
    daq_path_label.grid(row=1, column=0, padx=5, pady=5)

    daq_path = tk.Button(daq_window, text = "Select Path", command = lambda: daq_path_var.set(filedialog.askdirectory()))
    daq_path.config(width=10, height=1)
    daq_path.grid(row=1, column=2, padx=5, pady=5)
    

    daq_path_var = tk.StringVar()
    daq_path_entry = tk.Entry(daq_window, textvariable=daq_path_var)
    daq_path_entry.grid(row=1, column=1, padx=5, pady=5)

    
    # Create label and entry for picture_number
    picture_number_label = tk.Label(daq_window, text="Picture Number:")
    picture_number_label.grid(row=2, column=0, padx=5, pady=5)

    picture_number_var = tk.StringVar()
    picture_number_entry = tk.Entry(daq_window, textvariable=picture_number_var)
    picture_number_entry.grid(row=2, column=1, padx=5, pady=5)
    picture_number_var.set("200")

    # Create start button
    start_button = tk.Button(daq_window, text="Start DAQ", command=take_global_params)
    start_button.config(width=10, height=1)
    start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def take_point_by_point():
    ser.write(f'L 1'.encode())
    on_daq()
    daq_window.wait_window()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("camera init done")
    steps_=0
    step_increment=1
    if int(picture_number)>35: numer_of_steps=35
    else: number_of_steps=picture_number  
    for i in range(number_of_steps):
        ret, frame = cap.read()
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
        cv2.imwrite(daq_path+daq_name+str(i)+".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        steps_=steps_+step_increment
        ser.write(f'M {steps_}'.encode())
        print('Current step =',ser.readline().decode('utf-8').strip()," Set Step = ",steps_*80*8/3)
    cap.release()
    cv2.destroyAllWindows()
    print("Snapshot Taken!")
    on_home()
    ser.write(f'L 0'.encode())

def take_continously():
    ser.write(f'L 1'.encode())
    on_daq()
    daq_window.wait_window()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("camera init done")
    ser.write(f'S 50'.encode())
    time.sleep(0.05)
    ser.write(f'M 35'.encode())
    time.sleep(1)
    for i in range(int(picture_number)):
        ret, frame = cap.read()
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
        cv2.imwrite(daq_path+daq_name+str(i)+".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print("Picture", i, "from", picture_number )
    cap.release()
    cv2.destroyAllWindows()
    print("Snapshot Taken!")
    on_home()
    ser.write(f'L 0'.encode())    

def on_home():
    ser.write(b'H')
    #time.sleep(0.05)
    print(ser.readline().decode('utf-8').strip())

def on_speed():
    speed = speed_var.get()
    ser.write(f'S {speed}'.encode())
    #time.sleep(0.05)
    print(ser.readline().decode('utf-8').strip())

def on_move():
    steps = steps_var.get()
    ser.write(f'M {steps}'.encode())
    #time.sleep(0.05)
    print('Current step =',ser.readline().decode('utf-8').strip()," Set Step = ",float(steps)*80*8/3)
    
def on_led():
    state = led_var.get()
    ser.write(f'L {state}'.encode())
    print(ser.readline().decode('utf-8').strip())

def on_exit():
    ser.close()
    root.destroy()



#root = tk.Tk()
root = ThemedTk(theme='blue')
print(root.get_themes())
root.title("Micro Mirror Test Software")
root.geometry("350x150")

max_length = max(len("RPM Value"), len("Abs Value mm"))


menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="Set COM Port", command=set_com_port)
filemenu.add_separator()
filemenu.add_command(label="Home", command=on_home)
filemenu.add_separator()
filemenu.add_command(label="DAQ point by point", command=take_point_by_point)
filemenu.add_separator()
filemenu.add_command(label="DAQ continuously", command=take_continously)
#filemenu.add_separator()
#filemenu.add_command(label="Function to be tested", command=on_daq)
menubar.add_cascade(label="Functions", menu=filemenu)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=on_exit)
menubar.add_cascade(label="Exit", menu=filemenu)
root.config(menu=menubar)

speed_frame = tk.Frame(root)
speed_frame.grid(row=1, column=0, padx=5, pady=5)

speed_label = tk.Label(speed_frame, text="RPM Value")
speed_label.config(width=max_length)
speed_label.grid(row=0, column=0, padx=5, pady=5)

speed_var = tk.StringVar()
speed_entry = tk.Entry(speed_frame, textvariable=speed_var)
speed_entry.grid(row=0, column=1, padx=5, pady=5)

speed_button = tk.Button(speed_frame, text="Set Speed", command=on_speed)
speed_button.config(width=10, height=1)
speed_button.grid(row=0, column=2,   padx=5, pady=5)

steps_frame = tk.Frame(root)
steps_frame.grid(row=2, column=0, padx=5, pady=5)

steps_label = tk.Label(steps_frame, text="Abs Value mm")
steps_label.config(width=max_length)
steps_label.grid(row=0, column=0, padx=5, pady=5)

steps_var = tk.StringVar()
steps_entry = tk.Entry(steps_frame, textvariable=steps_var)
steps_entry.grid(row=0, column=1, padx=5, pady=5)

steps_button = tk.Button(steps_frame, text="MoveTo", command=on_move)
steps_button.config(width=10, height=1)
steps_button.grid(row=0, column=2,  padx=5, pady=5)
    
led_frame = tk.Frame(root)
led_frame.grid(row=3, column=0, padx=5, pady=5)

led_var = tk.IntVar()
led_var.set(0)
led_on_button = tk.Radiobutton(led_frame, text='Laser On', variable=led_var, value=1, command=on_led)
led_on_button.grid(row=0, column=0, padx=5, pady=5)
led_off_button = tk.Radiobutton(led_frame, text='Laser Off', variable=led_var, value=0, command=on_led)
led_off_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
