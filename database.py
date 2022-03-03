import xml.etree.ElementTree as ElementTree

class question:
    def __init__(self, question, answer, pointValue, isDouble = False):
        self.question = question
        self.answer = answer
        self.pointValue = pointValue
        self.isDouble = isDouble

class category:
    def __init__(self, title, questions):
        self.title = title
        self.questions = questions
    
class database:
    def __init__(self, xmlFilePath):
        self.xmlFilePath = xmlFilePath
        self.categories = []
        self.backgroundColor = ""
        self.foregroundColor = ""
        self.pointColor = ""

        self.tree = ElementTree.parse(self.xmlFilePath)
        self.root = self.tree.getroot()
        if self.root.tag == 'board':
            self.backgroundColor = self.root.get('background', self.backgroundColor)
            self.foregroundColor = self.root.get('foreground', self.foregroundColor)
            self.pointColor = self.root.get('pointcolor', self.pointColor)

            for cat in self.root:
                if cat.tag == "category":
                    questionList = []
                    categoryTitle = cat.get('title', 'Invalid')
                for q in cat:
                    isDouble = False
                    if q.get('dailyDouble') == "True":
                        isDouble = True
                    questionList.append(question(q.find('title').text, q.find('answer').text, q.get('points', 0), isDouble))
                self.categories.append(category(categoryTitle, questionList))

        else:
            raise InvalidXMLFile

    
    def getBoard(self):
        return self.categories
    
    def save(self, fileLocation = None):
        if fileLocation == None:
            fileLocation = self.xmlFilePath

        self.root.set('background', self.backgroundColor)
        self.root.set('foreground', self.foregroundColor)
        self.root.set('pointcolor', self.pointColor)

        for cat in self.root.findall('category'):
            self.root.remove(cat)
        
        for cat in self.categories:
            catItem = ElementTree.SubElement(self.root, 'category')
            catItem.set('title', cat.title)
            for q in cat.questions:
                questionElement = ElementTree.SubElement(catItem, 'question')
                titleElement = ElementTree.SubElement(questionElement, 'title')
                titleElement.text = q.question
                answerElement = ElementTree.SubElement(questionElement, 'answer')
                answerElement.text = q.answer
                questionElement.set('points', q.pointValue)
                if q.isDouble:
                    questionElement.set('dailyDouble', 'True')

        self.tree.write(fileLocation)

    def getBackgroundColor(self):
        return self.backgroundColor
    
    def getForegroundColor(self):
        return self.foregroundColor
    
    def getPointColor(self):
        return self.pointColor
    
    def printDebug(self):
        print(f'Background Color: {self.backgroundColor}')
        print(f'Foreground Color: {self.foregroundColor}')
        print(f'Point Color: {self.pointColor}')
        print()
        for cat in self.categories:
            print(f'Category Title: {cat.title}')
            for q in cat.questions:
                if q.isDouble:
                    print("*** DAILY DOUBLE ***")
                print(f'Question: {q.question} ({q.pointValue} points)')
                print(f'Answer: {q.answer}\n')

class InvalidXMLFile(Exception):
   pass
