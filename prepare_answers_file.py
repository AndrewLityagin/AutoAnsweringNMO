import tkinter as tk
from tkinter import filedialog

def open_dir(init_dir):
    root = tk.Tk()
    root.withdraw()
    dirname = tk.filedialog.askopenfilename()     
    root.destroy()
    return dirname

def PrepareString(string):
    return string.lower().strip().replace('—','').replace("(","").replace(")","").replace("[","").replace("]","").replace("°","").replace(",","").replace("–","").replace("-","").replace(".","").replace("-","").replace('«','').replace('»','').replace('"','').replace("'","").replace(" ","").replace(";","").replace(":","").replace("?","").replace("\t","")


def ReadAnswersFile(filename,test_answers):
    file = open(filename,'r',encoding="utf-8")
    is_title = True
    test_answers=[]
    for line in file:
        try:
            if (is_title):
                is_title = False
                continue
            data = line.replace('\n','').split(';')
            test_answers.append({'question':data[0],'answer1':data[1],'answer2':data[2],'answer3':data[3],'answer4':data[4],'answer5':data[5]})
        except Exception as ex:
            print("Error in read file:'"+line+"' \n Stack trace: \n",ex)    
    file.close()
    print(test_answers)
    print("File "+filename+" read successful!")
    return test_answers


def WriteAnswersFile(filename,test_answers):
    file = open(filename,'w',encoding="utf-8")
    file.write('question;answer1;answer2;answer3;answer4;answer5\n')
    for line in test_answers:
        file.write(PrepareString(line.get('question'))+';'+
                   PrepareString(line.get('answer1'))+';'+
                   PrepareString(line.get('answer2'))+';'+
                   PrepareString(line.get('answer3'))+';'+
                   PrepareString(line.get('answer4'))+';'+
                   PrepareString(line.get('answer5'))+'\n')
    file.close()

if __name__=='__main__':
    for i in range(34):
        filename="test_"+str(i+1)+".csv";
        test_answers=[]
        try:
            test_answers = ReadAnswersFile(filename,test_answers)
            WriteAnswersFile(filename,test_answers)
        except Exception as ex:
            print("Error in prepare file "+filename+" \n Stack trace: \n",ex)
    print("Prepare "+filename+" complete successful")
        
