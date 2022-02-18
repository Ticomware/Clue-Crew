import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from PIL import Image, ImageTk

#--- SETTINGS ---
WIDTH = 900     #width of window
HEIGHT = 1000    #height of window
#----------------

class Menu:
    # ask only for one answer and one question
    def __init__(self):
        self.window = tk.Tk()   # tkinter root
        self.question = ''      # widget entry
        self.answer = ''        # widget entry
        self.st = ''            # widget scrolledtext
        self.data = {}          # questions stored here

    def run(self):
        # SETUP for Tkinter
        main_color = '#5a78db'
        color1 = '#d1b18a'
        color2 = '#2b1d85'
        self.window.minsize(WIDTH, HEIGHT)
        self.window.maxsize(WIDTH, HEIGHT)
        self.window.title('Wizard - Questions')
        img = ImageTk.PhotoImage(Image.open("textEditor_bg.jpg"))
        bg=tk.Label(self.window, image=img)
        bg.place(relheight=1,relwidth=1)

        #main label
        tk.Label(self.window, text='Welcome to the Question Editor!', background='black' ,font=('Bahnschrift SemiBold', 25), foreground='white').pack(pady=25, fill=tk.X)

        #question
        tk.Label(self.window, text="Question", background=main_color ,font=('Bahnschrift SemiBold', 25), foreground='white').place(relx=0.1, rely=0.197, relheight=0.06, relwidth=0.2)
        self.question = tk.Entry(self.window, bd=5, font=('Bahnschrift SemiBold', 25))
        self.question.place(relx=0.3, rely=0.2, relwidth=0.6)
        
        #answer
        tk.Label(self.window, text="Answer", background=main_color ,font=('Bahnschrift SemiBold', 25), foreground='white').place(relx=0.1, rely=0.397, relheight=0.06, relwidth=0.2)
        self.answer = tk.Entry(self.window, bd=5, font=('Bahnschrift SemiBold', 25))
        self.answer.place(relx=0.3, rely=0.4, relwidth=0.6)

        #addToList
        tk.Button(self.window, text="Add to List", font=('Bahnschrift SemiBold', 25), command=lambda:self.addQuestionToList(), bd=6).place(relx=0.37, rely=0.55, relheight=0.06, relwidth=0.25)

        #displayCurrentList
        self.st = ScrolledText(self.window, width=50, background=color1, state='disabled', height=7,  font=('Bahnschrift', 20),foreground=color2)
        self.st.place(rely=0.7,relx=0.15,relwidth=0.7)

        #run tkinter
        self.window.mainloop()
    
    def addQuestionToList(self):
        # GET user input
        q = self.question.get()
        a = self.answer.get()
        
        # if input not empty
        if (q != '' and a!= ''):
            entry  = {q: a}
            self.data.update(entry)
            self.updateScrolledText()
            self.addToDataBase()
        #else input empty
        else:
            messagebox.showerror('Error','Questions/Answer cannot be empty!')

    def updateScrolledText(self):
        #ENABLE widget
        self.st.config(state='normal')

        # DELETE contents of current ScrolledText
        self.st.delete(1.0,tk.END)
        
        # ADD current contents to ScrolledText
        for key, value in self.data.items():
            x = ' > Question: ' + key + " - Answer: " + value
            self.st.insert(tk.INSERT, (x + '\n\n'))
        
        #DISABLE widget
        self.st.config(state='disabled')

    def addToDataBase(self):
        # DATABASE PART
        pass
            

if __name__ == '__main__':
    menu = Menu()
    menu.run()
