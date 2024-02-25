import time
import selenium
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from pyshadow.main import Shadow
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

LOGIN = "..."
PASSWORD = "..."
CHROME_DRIVER = "C:\\chromedriver\\chromedriver.exe"
driver = None
tests_data = []
test_answers = []
questions_count = 0
current_question = 1

def ReadTestList():
    global tests_data
    file = open('tests.list','r',encoding="utf-8")
    tests_data = []
    is_title = True
    for line in file:
        if (is_title):
            is_title = False
            continue
        data = line.replace('\n','').split(';')
        tests_data.append({'test':data[0],'file':data[1]})
    file.close()
    print("File tests.list read successful!")

def ReadAnswersFile(filename):
    file = open(filename,'r',encoding="utf-8")
    is_title = True
    for line in file:
        if (is_title):
            is_title = False
            continue
        data = line.replace('\n','').split(';')
        test_answers.append({'question':data[0],'answer1':data[1],'answer2':data[2],'answer3':data[3],'answer4':data[4],'answer5':data[5]})
    file.close()
    print("File "+filename+" read successful!")

def PrepareString(string):
    return string.lower().strip().replace('&laquo','').replace('&nbsp','').replace('—','').replace("(","").replace(")","").replace("[","").replace("]","").replace("°","").replace(",","").replace("–","").replace("-","").replace(".","").replace("-","").replace('«','').replace('»','').replace('"','').replace("'","").replace(" ","").replace(";","").replace(":","").replace("?","").replace("\t","")

def GetAnswer(question):
    question = PrepareString(question)
    for answ in test_answers:
       if(question == answ.get('question')):
           return answ.get('answer1'),answ.get('answer2'),answ.get('answer3'),answ.get('answer4'),answ.get('answer5')
    print('Answer for question: "'+question+'" not found')
    return ('','','','')

def Auth():
    try:
        driver.get('https://a.edu.rosminzdrav.ru/idp/login.html')
        driver.implicitly_wait(10)
        login_input = driver.find_element_by_id('username')
        login_input.send_keys(LOGIN)
        password_input = driver.find_element_by_id('password')
        password_input.send_keys(PASSWORD)
        button = driver.find_element_by_xpath('/html/body/div/app-login/section/table/tbody/tr/td/form/div[5]/div[1]/button')
        button.click()
        driver.implicitly_wait(15)
        time.sleep(5)
    except Exception as ex:
        print("Error in authorisation \n Stack trace: \n",ex)

def GoToOtherPlan():
    try:
        button = driver.find_element_by_xpath('/html/body/rsmu-app-root/ui-view/app-root/div/div/app-user-account-root/div/div/app-cycle-select/div/div[1]/app-sidebar/aside/div[3]/app-outside-cycles/button')
        button.click()
        driver.implicitly_wait(3)
    except Exception as ex:
        print("Error when we go to my plan \n Stack trace: \n",ex)

def GoToMyPlan():
    try:
        button = driver.find_element_by_xpath('/html/body/rsmu-app-root/ui-view/app-root/div/div/app-user-account-root/div/div/app-cycle-select/div/div[2]/div/ui-view/app-edu-trajectory-helper/section/header/div[2]/div[2]/button')
        button.click()
        driver.implicitly_wait(3)
    except Exception as ex:
        print("Error when we go to my plan \n Stack trace: \n",ex)
        GoToMyPlan2()

def GoToMyPlan2():
    try:
        button = driver.find_element_by_xpath('/html/body/rsmu-app-root/ui-view/app-root/div/div/app-user-account-root/div/div/app-cycle-select/div/div[1]/app-sidebar/aside/div[2]/app-cycle-management/ul/div/li/button/span')
        button.click()
        driver.implicitly_wait(3)
    except Exception as ex:
        print("Error when we go to my plan (2) \n Stack trace: \n",ex)

#upd 10.04
def UnspinElements():
    try:
        button = driver.find_element_by_xpath("//span[contains(text(),'Образовательные элементы вне тем')]")
        button.click()
        time.sleep(5)
    except Exception as ex:
        print("Error when we get list of tests \n Stack trace: \n",ex)

def GoToTestSite(test_name):
    try:
        try:
            UnspinElements()
            grid_row = driver.find_element_by_xpath("//div[contains(text(),'"+test_name+"')]/ancestor::tr")
            grid_row.click()
            driver.implicitly_wait(3)
        except:
            UnspinElements()
            UnspinElements()
            grid_row = driver.find_element_by_xpath("//div[contains(text(),'"+test_name+"')]/ancestor::tr")
            grid_row.click()
            driver.implicitly_wait(3)
        button = driver.find_element_by_xpath("/html/body/rsmu-app-root/ui-view/app-root/div/div/app-user-account-root/div/div/ng-component/div[2]/div[1]/div[1]/app-iom-main-info/div/div/div[3]/button")
        button.click()
        driver.implicitly_wait(3)
        try:
            button_no_support_mobile = driver.find_element_by_xpath('//*[@id="cdk-overlay-0"]/div[2]/div/div/div/div/div/button[1]')
            button_no_support_mobile.click()
            driver.implicitly_wait(3)
            check_box = driver.find_element_by_xpath("//*[@id=\"cdk-overlay-1\"]/div[2]/div/div/div/form/div[1]/app-checkbox/div/label")
            check_box.click()
            driver.implicitly_wait(3)
            button = driver.find_element_by_xpath("//*[@id=\"cdk-overlay-1\"]/div[2]/div/div/div/form/div[2]/span/button")
            button.click()
        except:
            check_box = driver.find_element_by_xpath("//*[@id=\"cdk-overlay-0\"]/div[2]/div/div/div/form/div[1]/app-checkbox/div")
            check_box.click()
            driver.implicitly_wait(3)
            button = driver.find_element_by_xpath("//*[@id=\"cdk-overlay-0\"]/div[2]/div/div/div/form/div[2]/span/button")
            button.click()
        driver.implicitly_wait(10)
        return True
    except Exception as ex:
       print("Error when we go to test website \n Stack trace: \n",ex)
       return False

def SwitchTabs():
    try:
        old_tab = driver.current_window_handle
        for curr_tab in driver.window_handles:
            if(curr_tab != old_tab):
                driver.switch_to.window(curr_tab)
    except Exception as ex:
        print("Error when we swith tabs \n Stack trace: \n",ex)            

def GoToPreviousTest():
    CloseModalWindow()
    try:
        button = driver.find_element_by_xpath('//span[contains(text(),"Быстрый переход")]/parent::span/parent::div')
        button.click()
        driver.implicitly_wait(3)
        try:
            link =  driver.find_element_by_xpath('//span[contains(text(),"1 Предварительное тестирование")]/parent::span/parent::div')
        except Exception as ex:
            link =  driver.find_element_by_xpath('//span[contains(text(),"1 Итоговое тестирование")]/parent::span/parent::div')
        link.click()
        driver.implicitly_wait(3)
        button = driver.find_element_by_xpath('//span[contains(text(),"Получить новый вариант")]/parent::span/parent::div')
        button.click()
        driver.implicitly_wait(7)
        test_link = driver.find_element_by_xpath('//span[contains(text(),"не завершен")]')
        test_link.click()
        test_link.click()
        driver.implicitly_wait(10)
        return True
    except Exception as ex:
        print("Error when we go to previous test \n Stack trace: \n",ex)
        return False

def CloseModalWindow():
    try:
        driver.find_element_by_xpath('//*[@class="v-window-closebox"]').click()
        return
    except Exception as ex:
        print("X button not found")

def GoToFinalTest():
    CloseModalWindow()
    try:
        button = driver.find_element_by_xpath('//span[contains(text(),"Быстрый переход")]/parent::span/parent::div')
        button.click()
        driver.implicitly_wait(3)
        link =  driver.find_element_by_xpath('//span[contains(text(),"1 Итоговое тестирование")]/parent::span/parent::div')
        link.click()
        test_links = driver.find_elements_by_xpath('//span[contains(text(),"не завершен")]')
        if(len(test_links)>0):
            test_links[0].click()
            test_links[0].click()
        else:
            driver.implicitly_wait(3)
            button = driver.find_element_by_xpath('//span[contains(text(),"Получить новый вариант")]/parent::span/parent::div')
            button.click()
            time.sleep(2)
            driver.implicitly_wait(7)
            test_link = driver.find_element_by_xpath('//span[contains(text(),"не завершен")]')
            test_link.click()
            test_link.click()
        return True
    except Exception as ex:
        print("Error when we go to final test \n Stack trace: \n",ex)
        return False

def RunTest():
    try:
        global questions_count
        global current_question
        shadow = Shadow(driver)
        temp = WebDriverWait(shadow,900).until(lambda s :  shadow.find_elements('app-quiz-wrapper'))
        time.sleep(5)
        divs = shadow.find_elements('div')
        isFind = False
        for div in divs:
            if(div.text.startswith('Количество')):
               lines = div.text.split('\n');
               questions_count = int(lines[2])
               break
        print("Start test, questions count:",questions_count)         
        current_question = 1
        buttons = shadow.find_elements('button')#Перейти к первому вопросу
        buttons[2].click()
        driver.implicitly_wait(10)
        #Цикл по всем вопросам
        for i in range(questions_count):
            print("==================================")
            print("№",current_question)
            question, answers = GetQuestionAndAnswersText()
            right_answers = GetAnswer(question)
            btn_numbers = GetRightAnswerNumber(answers,right_answers)
            AnsweringQuestion(btn_numbers)
            driver.implicitly_wait(10)
            current_question+=1
    except Exception as ex:
       print("Error when we run test \n Stack trace: \n",ex) 

def GetRightAnswerNumber(answers, right_answers):
    try:
        btn_numbers = []
        i = 0
        for answ in answers:
            for ransw in right_answers:
                answ = PrepareString(answ)
                if(answ == ransw):
                    btn_numbers.append(i)
            i+=1
        print("Right answers number:",btn_numbers)
        return btn_numbers
    except Exception as ex:
        print("Error in AnsweringQuestion \n Stack trace: \n",ex)       

def GetQuestionAndAnswersText():
    try:
        shadow = Shadow(driver)
        question = ""
        answers = []
        i=0
        j=0
        divs = shadow.find_elements('div')
        answers_div = None
        flag=False
        count_radiobuttons = 0
        for div in divs:
            try:
                if (div.text.find("Вопрос "+str(current_question))>-1):
                    answers_div=div
                    break
            except Exception as ex:
                print("")
        lines = answers_div.text.split('\n')
        question = lines[2]
        for line in lines:
            if(line.find("Выберите ОДИН правильный ответ")>-1 or line.find("Выберите НЕСКОЛЬКО правильных ответов")>-1):
                flag = True
                continue
            if(flag):
                if(line.find("Предыдущий вопрос")==-1):
                    answers.append(line)
                else:
                    break
        print("Question : ", question)
        for answ in answers:
            print(j," answer : ", answ)
            j+=1
        return question, answers
    except Exception as ex:
       print("Error when we get current question \n Stack trace: \n",ex)


def GetCountRadioButtons():
    try:
        shadow = Shadow(driver)
        buttons = shadow.find_elements('mat-radio-button')
        return len(buttons)
    except Exception as ex:
        print("Error in GetCountRadioButtons \n Stack trace: \n",ex)
        return 0

def AnsweringQuestion(btn_numbers):
    try:
        shadow = Shadow(driver)
        buttons = shadow.find_elements('mat-checkbox')
        for numb in btn_numbers:
            buttons[numb].click()
    except:
        try:
            buttons = shadow.find_elements('mat-radio-button')
            buttons[btn_numbers[0]].click()
        except Exception as ex:
            print("Error in AnsweringQuestion \n Stack trace: \n",ex)
    try:
        next_buttons = shadow.find_elements('button')
        for btn in next_buttons:
            try:
                if (btn.text == 'Следующий вопрос'):
                    btn.click()
            except:
                continue
            if (btn.text == 'Завершить попытку'):
                btn.click()
        next_buttons = shadow.find_elements('button')
        for btn in next_buttons:
            try:
                if (btn.text == 'Далее'):
                    btn.click()
            except:
                continue
    except Exception as ex:
        print("Error in AnsweringQuestion (go to next_question) \n Stack trace: \n",ex)
    
def RunAllSteps(test_name, answer_file):
    try:
        global driver
        driver = webdriver.Chrome(CHROME_DRIVER)
        time.sleep(5)
        Auth() 
        GoToOtherPlan()
        if(not GoToTestSite(test_name)):
            GoToMyPlan()
            if(not GoToTestSite(test_name)):
                return False
        ReadAnswersFile(answer_file)
        SwitchTabs()
        two_tests = GoToPreviousTest()
        if(not two_tests):
            if(not GoToFinalTest()):
                return False
        RunTest()
        print("Test "+test_name+" passed!")
        time.sleep(10)
        driver.quit()
        return two_tests
    except Exception as ex:
        print("Error in RunAllSteps \n Stack trace: \n",ex)
        return False

if __name__ == '__main__':
    ReadTestList()
    print("="*80)
    print("                                         AutoTester 0.3")
    print("="*80)
    i=1
    for data in tests_data:
        print(i,' -\t',data.get('test'),' [',data.get('file'),']')
        i+=1
    print("="*80)
    print('Press "a" - go to all test automatically or press number for run single test')
    command = input();
    if(command=='a'):
        for data in tests_data:
            print('Run test: ',data.get('test'))
            if(RunAllSteps(data.get('test'),data.get('file'))):
               RunAllSteps(data.get('test'),data.get('file')) 
    try:
        number = int(command)
        if(RunAllSteps(tests_data[number-1].get('test'),tests_data[number-1].get('file'))):
            RunAllSteps(tests_data[number-1].get('test'),tests_data[number-1].get('file'))
    except Exception as ex:
        print("Wrong command!")
        input()
