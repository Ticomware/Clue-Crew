import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog as fd
import database as db
import os
import xml.etree.ElementTree as ET
import re
#from PIL import Image, ImageTk


#--- SETTINGS ---
SAVEFILE = 'default.xml'    #default save file
WIDTH = 1100                #width of window
HEIGHT = 900                #height of window
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
        for F in (StartPage, NewBoard, EditBoard, AdvancedEditBoard):

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
        self.categories = []
        self.questions = []

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

        #points
        tk.Label(self, text='Points', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.02, rely=0.42)
        self.points = tk.Entry(self, bd=3, font=FONT2)
        self.points.place(relx=0.2, rely=0.42, relwidth=0.15)
        
        #isDouble
        self.doublePoints = tk.StringVar()
        tk.Label(self, text='Double?', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.45, rely=0.42)
        yd = tk.Radiobutton(self, text='Yes', background=COLOR4, selectcolor=COLOR3,font=FONT2,foreground='WHITE', wraplength=300, justify='center', variable=self.doublePoints, value='y', indicator=0)
        yd.place(relx=0.65, rely=0.42,relwidth=0.1)
        nd = tk.Radiobutton(self, text='No', background=COLOR4, selectcolor=COLOR3, font=FONT2, foreground='WHITE', wraplength=300, justify='center', variable=self.doublePoints, value='n', indicator=0)
        nd.place(relx=0.8, rely=0.42, relwidth=0.1)

        #scrollview with file
        self.st = ScrolledText(self, width=50, background=COLOR6, state='disabled', height=7,  font=('Bahnschrift', 20),foreground='black')
        self.st.place(rely=0.48,relx=0.05,relwidth=0.9, relheight=0.35)

        #save question button
        button = tk.Button(self, text="Add Question", background = COLOR2, font=FONT2, command=lambda: self.addQuestion())
        button.place(relx=0.25,rely=0.85, relwidth=0.55)

        #update database button
        button = tk.Button(self, text="Save", background = COLOR2, font=FONT2, command=lambda: self.pushDatabase())
        button.place(relx=0.06,rely=0.88, relwidth=0.15)

        #return home button
        button3 = tk.Button(self, text="⬅️  Back to Home", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(StartPage))
        button3.place(relx=0.25,rely=0.92, relwidth=0.55)

    def addQuestion(self):
        #get user input
        category = self.category.get()
        question = self.question.get()
        answer = self.answer.get()
        points = self.points.get()
        isDouble = self.doublePoints.get()

        #validate input...
        if (category != '' and question != '' and answer != ''):
            #Create an array
            newData = [category, question, answer, points, isDouble]
            #if empty
            if (len(self.newBoardData) == 0):
                #insert data into newBoardData
                self.newBoardData.append(newData)
                #add category to array
                self.categories.append([category,1])
            #not empty
            else:
                #assume newData does not exist
                exists = False
                for i in range(len(self.newBoardData)):
                    #if same category and question -> replace answer and break
                    if (self.newBoardData[i][0] == newData[0] and self.newBoardData[i][1] == newData[1]):
                        self.newBoardData[i][2] = newData[2]
                        self.newBoardData[i][3] = newData[3]
                        self.newBoardData[i][4] = newData[4]
                        exists = True
                        break
                #if newData does not exist, add it
                if (exists == False):
                    self.newBoardData.append(newData)
                    #update categories
                    exists = False
                    for i in range(len(self.categories)):
                        if (self.categories[i][0] == category):
                            self.categories[i][1] += 1
                            exists = True
                            break
                    if (exists == False):
                        self.categories.append([category,1])
                
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
            data =  'Category: ' + self.newBoardData[i][0] + ' - Question: ' + self.newBoardData[i][1] + ' - Answer: ' + self.newBoardData[i][2] + '(' + self.newBoardData[i][3] + ')' + '\n\n'
            self.st.insert(tk.END, data)
                
        #DISABLE widget
        self.st.config(state='disabled')

    def deleteCurrentDefaultFile(self):
        tree = ET.parse(SAVEFILE)
        root = tree.getroot()
        for cat in root.findall('category'):
            print(cat.attrib)
            root.remove(cat)
        tree.write(SAVEFILE)

    def pushDatabase(self):
        #IF there is at least one new data entry, we earse default and start the creation of new file
        if self.newBoardData:
            #DELETE all contents of file
            self.deleteCurrentDefaultFile()
            #call database - using existing file
            database = db.database(SAVEFILE)
            
            #loop through categories
            for c in range(len(self.categories)):
                #empty list that holds db.question objects
                self.questions = []
                #print(self.categories[c][0])
                #loop through questions
                for i in range(len(self.newBoardData)):
                    # 0 = category | 1 = question | 2 = answer | 3 = points | 4 = isDouble
                    # if new question is in the current category, we work on the question
                    if (self.newBoardData[i][0] == self.categories[c][0]):
                        double = False
                        if (self.newBoardData[i][4] == 'y'):
                            double = True
                        print(double)
                        q = db.question(self.newBoardData[i][1], self.newBoardData[i][2], self.newBoardData[i][3], double)
                        self.questions.append(q)
                        #print (q.question, q.answer)
                #create db.category object and insert current list of questions
                cat = db.category(self.categories[c][0], self.questions)
                #push category into database
                database.categories.append(cat)

            #save new data into default file
            database.save()

            #open default file and create string of all content
            contents = ''
            with open(SAVEFILE) as f:
                contents += f.read()

            #ask to save as new file
            text_file = fd.asksaveasfilename(title='Save XML File', filetypes=[("XML files", ".xml")])
            text_file = open(text_file,'w')
            text_file.write(contents)
            text_file.close()
            #let user know data is being saved....
            messagebox.showinfo('Success','Your current content has been saved to the new board!')


        #ELSE we ask for new questions
        else:
            messagebox.showerror('Invalid','Type new questions to continue')
        
        
        #Finally, erase everything
        self.category.delete(0,tk.END)
        self.question.delete(0,tk.END)
        self.answer.delete(0,tk.END)
        self.points.delete(0,tk.END)
        self.deleteCurrentDefaultFile()
        self.newBoardData.clear()
        self.categories.clear()
        self.questions.clear()
        #ENABLE widget
        self.st.config(state='normal')
        #DELETE contents of current ScrolledText
        self.st.delete(1.0,tk.END)         
        #DISABLE widget
        self.st.config(state='disabled')


class AdvancedEditBoard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #background
        tk.Label(self, background=COLOR1).place(relheight=1,relwidth=1)

        #main label
        tk.Label(self, text='Advanced board editor', background='black', font=FONT1, foreground='white', wraplength=300, justify='center').place(relx=0,relwidth=1,relheight=0.25)

        #scrollview with file
        self.st = ScrolledText(self, width=50, background=COLOR6, state='disabled', height=7,  font=('Bahnschrift', 20),foreground='black')
        self.st.place(rely=0.27,relx=0.05,relwidth=0.9, relheight=0.55)

        #save file button
        button = tk.Button(self, text="Save File", background = COLOR2, font=FONT2 ,command=lambda: self.saveFile())
        button.place(relx=0.15,rely=0.85, relwidth=0.35)

        #load file button
        button2 = tk.Button(self, text="Load File", background = COLOR2, font=FONT2, command=lambda: self.loadFile())
        button2.place(relx=0.5,rely=0.85, relwidth=0.35)

        #return home button
        button3 = tk.Button(self, text="⬅️  Back to Home", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(StartPage))
        button3.place(relx=0.22,rely=0.92, relwidth=0.55)

    def loadFile(self):
        file = fd.askopenfilename(title='Open XML File', filetypes=(('Boad File', '*.xml'), ('Text','*.txt')))
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
        text_file = fd.asksaveasfilename(title='Save XML File', filetypes=[("XML files", ".xml")])
        text_file = open(text_file,'w')
        text_file.write(self.st.get(1.0, tk.END))
        text_file.close()


class EditBoard(tk.Frame):

    def __init__(self, parent, controller):
        #
        self.file = ''
        self.questions = []
        self.contents = ''
        self.count = 0
        self.cat = ''

        tk.Frame.__init__(self, parent)
        #background
        tk.Label(self, background=COLOR1).place(relheight=1,relwidth=1)

        #main label
        tk.Label(self, text='Edit existing board', background='black', font=FONT1, foreground='white', wraplength=300, justify='center').place(relx=0,relwidth=1,relheight=0.1)

        #category entry
        tk.Label(self, text='Category', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.02, rely= 0.12)
        self.category = tk.Entry(self, bd=3, font=FONT2)
        self.category.place(relx=0.2, rely=0.12, relwidth=0.25)

        #double number entry
        tk.Label(self, text='Double Question #', background=COLOR1, font=FONT2, foreground='WHITE', wraplength=300, justify='center').place(relx=0.5, rely= 0.12)
        self.double = tk.Entry(self, bd=3, font=FONT2)
        self.double.insert(0,0)
        self.double.place(relx=0.88, rely=0.12, relwidth=0.1)

        #search category button
        button = tk.Button(self, text="Search", background = COLOR3, font=FONT2 ,command=lambda: self.searchCategory())
        button.place(relx=0.35,rely=0.19, relwidth=0.35)

        #scrollview for current category
        self.st = ScrolledText(self, width=50, background=COLOR6, state='disabled', height=7,  font=('Bahnschrift', 20),foreground='black')
        self.st.place(rely=0.27,relx=0.05,relwidth=0.9, relheight=0.55)

        #save file button
        button2 = tk.Button(self, text="Save File", background = COLOR2, font=FONT2 ,command=lambda: self.saveFile())
        button2.place(relx=0,rely=0.85, relwidth=0.5)

        #load file button
        button3 = tk.Button(self, text="Load File", background = COLOR2, font=FONT2, command=lambda: self.loadFile())
        button3.place(relx=0.5,rely=0.85, relwidth=0.5)

        #return home button
        button4 = tk.Button(self, text="⬅️  Back to Home", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(StartPage))
        button4.place(relx=0,rely=0.92, relwidth=0.5)

        #advanced editor button
        button5 = tk.Button(self, text="Advanced Editor  ➡️", background = COLOR2, font=FONT2 ,command=lambda: controller.show_frame(AdvancedEditBoard))
        button5.place(relx=0.5,rely=0.92, relwidth=0.5)

    def loadFile(self):
        try:
            f = fd.askopenfilename(title='Open XML File', filetypes=[("All files", ".xml")])
            self.file = os.path.basename(f)
            messagebox.showinfo('Files Success', 'File is loaded, search for category and make changes')
        except:
            messagebox.showerror('File Error','That file could not be opened! Try again!')


    def saveFile(self):
        try:
            self.saveText = self.st.get('1.0', tk.END)  # Get all text in widget.
            text = self.saveText.replace('\n', '')
            newDataList = []
            print(text)
            #Modify string so it becomes an array that hold the important data
            rawText = re.split('Points: |Question: |Answer: ', text)
            rawText.remove('')
            print(rawText)
            # print(int(len(rawText)/3))
            print(self.double.get())
            #create questions using database
            x = 0
            for i in range(int(len(rawText)/3)):
                # question, answer, points
                if i == int(self.double.get())-1:
                    q = db.question(rawText[x+1],rawText[x+2],rawText[x], True)
                else:
                    q = db.question(rawText[x+1],rawText[x+2],rawText[x])
                newDataList.append(q)
                x += 3
            #delete all current categories
            tree = ET.parse(self.file)
            root = tree.getroot()
            for cat in root:
                if (cat.get('title') == self.cat):
                    root.remove(cat)
            tree.write(self.file)

            #create category
            c = db.category(self.cat,newDataList)
            #create database to save on file
            database = db.database(self.file)
            #insert into file
            database.categories.append(c)
            #database save
            database.save()

        except:
            messagebox.showerror('Something went wrong!', 'Please check your input and follow the right patterns! \n Points: p \n Question: q \n Answer: a')
        

    def searchCategory(self):
        if (self.file != ''):
            found = False
            self.questions = [] # to clear?
            self.contents = ''
            self.cat = (self.category.get().lower()).capitalize()
            tree = ET.parse(self.file)
            root = tree.getroot()
            self.count = 0
            #list =[131]
            for cat in root:
                for ques in  cat:
                    if (cat.get('title') == self.cat):
                        self.count += 1
                        found = True
                        self.questions.append([ques.get('points'),ques[0].text,ques[1].text])
                        p = 'Points: ' + ques.get('points') + '\n'
                        q = 'Question: ' + ques[0].text + '\n'
                        a = 'Answer: ' + ques[1].text + '\n' + '\n'
                        self.contents += p + q + a

            # if category was not found, we alert the user
            if not found:
                messagebox.showinfo('Not Found', 'That category was not found on your file')
            else:
                print (self.questions)
                #ENABLE widget
                self.st.config(state='normal')

                #DELETE contents of current ScrolledText
                self.st.delete(1.0,tk.END)

                #INSERT contents into tkinter widget
                self.st.insert(tk.END, self.contents)
                        
                #DISABLE widget
                #self.st.config(state='disabled')
        else:
            messagebox.showerror('No File Found!', 'Please load a file first')


#run program
if __name__ == '__main__':
    app = TextEditor()
    app.mainloop()