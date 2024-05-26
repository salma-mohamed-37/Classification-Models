from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
from models import run

file=""

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        global file
        file = file_path
        file_name = os.path.basename(file_path)
        label1.config(text=f"{file_name}")

def submit():
    samplePercentage = float(txt1.get())
    testingPercentage = float(txt2.get())
    
    global file 
    result = run(file, samplePercentage, testingPercentage)
    view_results(result)


def view_results(result):
    # Create a new Frame within the existing frame to contain the Text widget and Scrollbar
    frame_results = Frame(frame)
    frame_results.grid(row=6, column=0, columnspan=3, sticky="nsew")

    # Create a Text widget for displaying the results
    text_widget = Text(frame_results, wrap=WORD, font=('Arial', 14), width=120)
    text_widget.pack(side=LEFT, fill=BOTH, expand=YES)

    # Create a Scrollbar widget and associate it with the Text widget
    scrollbar = Scrollbar(frame_results, command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the Text widget to use the Scrollbar
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the result into the Text widget
    text_widget.insert(END, result)

    # Adjust the scrollbar when the Text widget is updated
    def on_text_configure(event):
        text_widget.update_idletasks()
        text_widget.yview_moveto(1.0)

    text_widget.bind('<Configure>', on_text_configure)

    text_widget.yview_moveto(0.0)
    scrollbar_label = Label(frame_results, font=('Arial', 12))
    scrollbar_label.pack(pady=(10, 0))\

# Create root window
root = Tk()
root.configure(bg="white")
root.title("Data Mining Assignment 3")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

# Create a frame to hold the widgets
frame = Frame(root, bg="white")
frame.pack()  # Expand to fill the window


# Create widgets inside the frame
title = Label(frame, text="Problem 1", font=('Arial', 16, 'bold'), fg="pink", bg="white")
title.grid(row=0, column=1)

btn1 = Button(frame, text="Upload File", command=open_file_dialog, fg="white", bg="pink", font=('Arial', 16))
btn1.grid(row=1, column=1)
  
label1 =Label(frame, text="", font=('Arial', 16), fg="pink", bg="white")  
label1.grid(row=2, column=1)

label2 = Label(frame, text="Percentage of the file to use: ", font=('Arial', 16), fg="pink", bg="white")
label2.grid(row=3, column=0)

txt1 = Entry(frame, width=20, fg="white", bg="pink", font=('Arial', 16))
txt1.grid(row=3, column=2)

label3 = Label(frame, text="Percentage for testing: ", font=('Arial', 16), fg="pink", bg="white")
label3.grid(row=4, column=0)

txt2 = Entry(frame, width=20,font=('Arial', 16), fg="white", bg="pink")
txt2.grid(row=4, column=2)

btn2 = Button(frame, text="Submit",font=('Arial', 16), fg="white", bg="pink", command=submit)
btn2.grid(row=5, column=1)

root.mainloop()
