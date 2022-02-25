import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk

#--- SETTINGS ---
WIDTH = 1100     #width of window
HEIGHT = 900    #height of window
COLOR1 = '#5A78DB'
COLOR2 = '#D1B18A'
COLOR3 = '#12664F'
COLOR4 = '#550C18'
COLOR5 = '#8AF3FF'
COLOR6 = '#E3D7FF'
FONT1 = ('Bahnschrift SemiBold', 25)
FONT2 = ('Verdana', 12)
#----------------


class TextEditor(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # add the frame classes into the list self.frames
        for F in (StartPage, NewBoard, EditBoard):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # function to navigate through frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #settings for ALL frames
        controller.geometry('450x500')
        controller.minsize(int(WIDTH/2.8), int(HEIGHT/2.8))
        controller.maxsize(int(WIDTH), int(HEIGHT))
        controller.title('Clue Crew - Text Editor')

        #background
        tk.Label(self, background=COLOR1).place(relheight=1,relwidth=1)

        #main label
        tk.Label(self, text='Welcome to the Question Editor!', background='black', font=FONT1, foreground='white', wraplength=300, justify='center').place(relx=0,relwidth=1,relheight=0.25)

        #options label
        tk.Label(self, text='Select to create a new board or edit an existing board.', background= COLOR1 ,font=FONT2, foreground=COLOR5, wraplength=300, justify='center').place(relx=0, rely=0.3,relwidth=1, relheight=0.2)

        #new board button
        button = tk.Button(self, text="Create new board", background = COLOR2, font=FONT2, command=lambda: controller.show_frame(NewBoard))
        button.place(relx=0.25,rely=0.53, relwidth=0.55)

        #edit board button
        button2 = tk.Button(self, text="Edit existing board", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(EditBoard))
        button2.place(relx=0.25,rely=0.68, relwidth=0.55)


class NewBoard(tk.Frame):

    def __init__(self, parent, controller):
        #
        self.newBoardData = []

        tk.Frame.__init__(self, parent)
        #background
        tk.Label(self, background=COLOR1).place(relheight=1,relwidth=1)

        #main label
        tk.Label(self, text='Create new board', background='black', font=FONT1, foreground='white', wraplength=300, justify='center').place(relx=0,relwidth=1,relheight=0.1)

        #category
        tk.Label(self, text='Category', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.02, rely= 0.12)
        self.category = tk.Entry(self, bd=3, font=FONT2)
        self.category.place(relx=0.2, rely=0.12, relwidth=0.75)

        #question
        tk.Label(self, text='Question', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.02, rely= 0.22)
        self.question = tk.Entry(self, bd=3, font=FONT2)
        self.question.place(relx=0.2, rely=0.22, relwidth=0.75)

        #answer 
        tk.Label(self, text='Answer', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.02, rely=0.32)
        self.answer = tk.Entry(self, bd=3, font=FONT2)
        self.answer.place(relx=0.2, rely=0.32, relwidth=0.75)

        #scrollview with file
        self.st = ScrolledText(self, width=50, background=COLOR6, state='disabled', height=7,  font=('Bahnschrift', 20),foreground='black')
        self.st.place(rely=0.45,relx=0.05,relwidth=0.9, relheight=0.35)

        #save question button
        button = tk.Button(self, text="Save Question", background = COLOR2, font=FONT2, command=lambda: self.addQuestion())
        button.place(relx=0.25,rely=0.85, relwidth=0.55)

        #return home button
        button3 = tk.Button(self, text="⬅️  Back to Home", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(StartPage))
        button3.place(relx=0.25,rely=0.92, relwidth=0.55)

    def addQuestion(self):
        #get user input
        category = self.category.get()
        question = self.question.get()
        answer = self.answer.get()

        #validate input...
        if (category != '' and question != '' and answer != ''):
            #Create a array
            newData = [category, question, answer]
            #if empty
            if (len(self.newBoardData) == 0):
                self.newBoardData.append(newData)
            #not empty
            else:
                #assume newData does not exist
                exists = False
                for i in range(len(self.newBoardData)):
                    #if same category and question -> replace answer and break
                    if (self.newBoardData[i][0] == newData[0] and self.newBoardData[i][1] == newData[1]):
                        self.newBoardData[i][2] = newData[2]
                        exists = True
                        break
                #if newData does not exist, add it
                if (exists == False):
                    self.newBoardData.append(newData)
                
            #update list into scrollview
            print(self.newBoardData)
            self.updateScrollView()

        else:
            messagebox.showerror('Error','Category/Questions/Answer cannot be empty!')

    def updateScrollView(self):
        #ENABLE widget
        self.st.config(state='normal')

        #DELETE contents of current ScrolledText
        self.st.delete(1.0,tk.END)

        #INSERT contents into tkinter widget
        for i in range(len(self.newBoardData)):
            data =  'Category: ' + self.newBoardData[i][0] + ' - Question: ' + self.newBoardData[i][1] + ' - Answer: ' + self.newBoardData[i][2] + '\n\n'
            self.st.insert(tk.END, data)
                
        #DISABLE widget
        self.st.config(state='disabled')



class EditBoard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #background
        tk.Label(self, background=COLOR1).place(relheight=1,relwidth=1)

        #main label
        tk.Label(self, text='Edit existing board', background='black', font=FONT1, foreground='white', wraplength=300, justify='center').place(relx=0,relwidth=1,relheight=0.25)

        #scrollview with file
        self.st = ScrolledText(self, width=50, background=COLOR6, state='disabled', height=7,  font=('Bahnschrift', 20),foreground='black')
        self.st.place(rely=0.27,relx=0.05,relwidth=0.9, relheight=0.55)

        #load file button
        button = tk.Button(self, text="Load File", background = COLOR2, font=FONT2, command=lambda: self.loadFile())
        button.place(relx=0.55,rely=0.85, relwidth=0.35)

        #save file button
        button2 = tk.Button(self, text="Save File", background = COLOR2, font=FONT2 ,command=lambda: self.saveFile())
        button2.place(relx=0.2,rely=0.85, relwidth=0.35)

        #return home button
        button3 = tk.Button(self, text="⬅️  Back to Home", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(StartPage))
        button3.place(relx=0.25,rely=0.92, relwidth=0.55)

    def loadFile(self):
        file = fd.askopenfilename(title='Open Text File', filetypes=(('Text Files', '*.txt'), ))
        file = open(file, 'r')
        content = file.read()

        #ENABLE widget
        self.st.config(state='normal')

        #DELETE contents of current ScrolledText
        self.st.delete(1.0,tk.END)

        #INSERT contents into tkinter widget
        self.st.insert(tk.END, content)
                
        #DISABLE widget
        #self.st.config(state='disabled')

        #close file
        file.close()

    def saveFile(self):
        text_file = fd.askopenfilename(title='Save Text File', filetypes=(('Text Files', '*.txt'), ))
        text_file = open(text_file,'w')
        text_file.write(self.st.get(1.0, tk.END))
        text_file.close()
        


#run program
app = TextEditor()
app.mainloop()