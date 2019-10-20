###############################################  Libraries  ################################################################
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


######################## Functions for render return ########################################
def index(request):
    return render(request,'Basics.html')

def index1(request):
    return render(request,'instagram.html')


def index2(request):
    return render(request,'Twitter.html')   
    
def index3(request):
    return render(request,'LinkedIn.html')    
#######################################################################################33333

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

##################################### INSTAGRAM #########################################################
class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()    #For opening firefox browser

    def closeBrowser(self):    #Function to close browser
        self.driver.close()

    def login(self):           #Instagram login function
        driver = self.driver
        #opening the instagram link
        driver.get("https://www.instagram.com/")
        time.sleep(3)         #wait for loading of page
        #finding login button using  xpath
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()    
        time.sleep(3)
        #finding username element using xpath
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()                  #clear the previous id if any
        user_name_elem.send_keys(self.username) #Enters the new entered id
        #finding password element using xpath
        pwd = driver.find_element_by_xpath("//input[@name='password']")
        pwd.clear()                            #Clear the previous pwd if any
        pwd.send_keys(self.password)           #Enters the new entered pwd
        #Enter key
        pwd.send_keys(Keys.RETURN)
        time.sleep(3)



    #Function for liking process.....
    def like_photo(self,hashtag):   
        driver = self.driver
        #opening link for given hashtag
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(3)

        #collect post`s link.......
        lst = []
        for i in range(1, 7):
            try:
                #scroll down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)        #waiting for 2 seconds to load webpage
                
                #finding elements by tagname for "a"
                hv = driver.find_elements_by_tag_name('a') 
                #if hv have href coontaining ".com/p"
                hv = [elem.get_attribute('href') for elem in hv
                                 if '.com/p/' in elem.get_attribute('href')]
              
                #append in lst if href not in hv
                for href in hv:
                    if href not in lst:
                        lst.append(href)

            except Exception:
                continue

        # Like posts....
        photos = len(lst)
        for pic in lst:
            driver.get(pic) #here pic contains the link from the lst
            time.sleep(3)   #wait for loading of page
            #scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                #random loop for secuirty purpose
                time.sleep(random.randint(2, 4))
                #finding like-button using xpath and then click
                like_button = driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
               
                
            except Exception as e:
                time.sleep(3)
            photos -= 1

#function for connecting to django 
def insta_liker(request):   
    username = request.GET['uname']      #getting data from frontend
    password = request.GET['psw']
    print(username,password)
    ig = InstagramBot(username, password)  #calling of Instagram class and its functions 
    ig.login()
    hashtags=request.GET['Hashtag']
    while True:
        try:
            ig.like_photo(hashtags)
        except Exception:                        #if there occurs any error, turn off the browser and 
                                                 #and run again the browser and all the processes
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()

    return render(request,'instagram.html')   #after above code,display this page
      


######################################  TWITTER  #################################################
def Twitter_fun(request):
    class TwitterBot:
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.bot = webdriver.Firefox()

        def login(self):
            bot = self.bot
            bot.get('https://twitter.com/')
            time.sleep(3)

            email = bot.find_element_by_class_name('text-input')
            password = bot.find_element_by_name('session[password]')
            email.clear()
            password.clear()
            email.send_keys(self.username)
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            time.sleep(5)

       
        def T_like(self,hashtag):
            bot = self.bot
            bot.get('https://twitter.com/search?q='+hashtag+'&src=typed_query&f=image')
            time.sleep(3)

            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
            #liking starts here...
            c=0
            for _ in range(1,8):
                bot.find_element_by_xpath('//div[contains(@class,"css-1dbjc4n r-1awozwy r-1iusvr4 r-16y2uox r-5f2r5o r-1gmbmnb r-bcqeeo")]').click()
                try:
                    c=c+1
                    time.sleep(3)
                    heart=bot.find_element_by_xpath('//div[contains(@data-testid,"like")]')
                    heart.click()
                    time.sleep(2)
                    bot.back()
                    
                except:
                    c=c-1
                    continue
               
            
                time.sleep(5)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(3)
                    
            print("liked : ",c)

  
    hasta = request.GET['High']
    userna = request.GET['uname']
    passwor = request.GET['psw']

    T= TwitterBot(userna,passwor) 
    T.login()
    T.T_like(hasta)
         
    return render(request,'Twitter.html') 
################################################ LINKEDIN #########################################


def LinkedIn_fun(request):
    class LinkedINBot:
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.bot = webdriver.Firefox()

        def L_login(self):
            bot = self.bot
            bot.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
            time.sleep(3)
            
            email = bot.find_element_by_xpath("//input[@id='username']")
            password = bot.find_element_by_xpath("//input[@id='password']")
            email.clear()
            password.clear()
            email.send_keys(self.username)
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            time.sleep(5)

        def L_like(self,hashtag):
            bot = self.bot
            bot.get('https://www.linkedin.com/search/results/content/?keywords='+ hashtag +'&origin=SWITCH_SEARCH_VERTICAL')
            time.sleep(3)
            
            c=0
            for _ in range(0,8):
                
                try:    
                    like=bot.find_element_by_xpath('//*[@class="reactions-react-button ember-view"]')
                    like.click()
                    c=c+1
                    time.sleep(3)
                except:
                    c=c-1
                    continue   
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(5)

            print("No. of likes : ",c)

        
    hashtag_LinkedIn = request.GET['Hashtag_linked']
    username_LinkedIn = request.GET['username_linked']
    password_LinkedIn = request.GET['password_linked']
    print(username_LinkedIn)
    print(password_LinkedIn)
    print(hashtag_LinkedIn)
    L= LinkedINBot(username_LinkedIn,password_LinkedIn) 
    L.L_login()
    L.L_like(hashtag_LinkedIn)
    return render(request,'LinkedIn.html')
