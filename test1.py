#question1 = ['History', {'How the...': 'Yes'}]
#question2 = ['Art', {'When the...': 'Maybe'}]
#question3 = ['Art', {'When Years...': 'Maybe'}]
#question4 = ['History', {'How the...': 'No'}]
#data = []
#data.append(question1)
#data.append(question2)
#data.append(question3)
#print(data[0][1])

#question = ''

#for i in range(len(data)):
#    for j in range (len(data[i])):
#        
#        if (j == 0):
#            question = 'Category: ' + data[i][j]
#        elif (j == 1):
#            data[i][j].update(question4[1])
#            print(data[i][j])
#            #for k, v in data[i][j].items():
            #    question += ' | Question: ' + k + ' | Answer: ' + v 

    #print(question)


question1 = ['History', 'How the..', 'Yes']
question2 = ['Art', 'When the..', 'Maybe']
question3 = ['Math', 'Sum the..', '10']
question4 = ['Art', 'When the..', 'No']

data = []
data.append(question1)
data.append(question2)
data.append(question3)
#fix...
data[1][2] = question4[2]

#print(question4[2])
print(data)