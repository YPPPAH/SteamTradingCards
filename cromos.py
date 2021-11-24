from tkinter import *
from tkinter import messagebox
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from pathlib import Path
import os
import threading 
from selenium.common.exceptions import InvalidSessionIdException,ElementClickInterceptedException

##WINDOW
WINDOW_WIDTH=560
WINDOW_HEIGTH=260
##SIZE
NORMAL_HEIGTH=30
NORMAL_WIDTH=100
BUTTON_WIDTH=80
COMMENT_WIDTH=220
COMMENT_HEIGTH=40
##AXIS X
POS_COL1_X=15
POS_COL2_X=130
POS_COL3_X=245
POS_COL4_X=360-15
POS_COL5_X=450
##AXIS Y
POS_ROW1_Y=10
POS_ROW2_Y=50
POS_ROW3_Y=90
POS_ROW4_Y=130
POS_ROW5_Y=170
POS_ROW6_Y=210
#POS_ROW7_Y=260
##CREDENTIALS
URL="https://store.steampowered.com/login/"
APP_DIRECTORY="{}\\Documents\\YPPAHSOFT\\".format(Path.home())
PIKLE_FILE_ACCID="pickle.pkl"
PIKLE_FILE_SOLD="pickle2.pkl"
PIKLE_FILE_LOGIN="pickle3.pkl"
PIKLE_FILE_GRID="pickle4.pkl"
PIKLE_FILE_IPAGE="pickle5.pkl"
##PRICING
PRICE_MULTIPLIER=1.40

class FrSuma(Frame):

    def Quit(self):
        exit()

    def __init__(self, master=None):
        super().__init__(master,width=WINDOW_WIDTH, height=WINDOW_HEIGTH)
        self.master = master
        self.pack()
        self.create_widgets()
        
    ###------------------------------------------------------------------------------------###

    def print_and_console(self,text):
        # print(text)
        self.lblConsole3["text"] = self.lblConsole2["text"]
        self.lblConsole2["text"] = self.lblConsole1["text"]
        self.lblConsole1["text"] = text

    def Create_Dir(self):
        try:
            os.mkdir(APP_DIRECTORY)
        except FileExistsError:
            pass

    def Get_accid(self,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING FOR PREVIOUS ID...")
            with open(APP_DIRECTORY+PIKLE_FILE_ACCID,"rb") as piklefile:
                _accid = pickle.load(piklefile)
            # self.print_and_console("ID RECOVERED")
        except FileNotFoundError:
            self.print_and_console("PREVIOUS USER NOT FOUND SEARCHING NEW ID...")
            driver.find_element(By.CLASS_NAME,"user_avatar").click()
            _accid = driver.current_url.split("/")[4]
            with open(APP_DIRECTORY+PIKLE_FILE_ACCID,"wb") as piklefile:
                pickle.dump(_accid, piklefile)
            # self.print_and_console("ID RECOVERED")
        return _accid
    
    def Clean(self):
        self.lblConsole3["text"] = ""
        self.lblConsole2["text"] = ""
        self.lblConsole1["text"] = ""

    def Replace(self, string):
        return string.replace(",",".")

    def Get_inventory_grid(self,driver):
        # self.print_and_console("SEARCHING FOR GRID...")
        invetorygrid = []
        invetorygrid = driver.find_elements(By.XPATH,"//div[@class='itemHolder']")
        invetorygrid[self.Get_number(driver)].click()
        # self.print_and_console("GRID FOUND")

    def Get_login(self,user,password):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING FOR PREVIOUS USER...")
            with open(APP_DIRECTORY+PIKLE_FILE_LOGIN,"rb") as piklefile:
                login = pickle.load(piklefile)
                user.send_keys(login[0])
                password.send_keys(login[1])
            # self.print_and_console("USER FOUND")
        except FileNotFoundError:
            self.print_and_console("PREVIOUS USER NOT FOUND SEARCHING NEW USER...")
            if self.txtInput1.get()=="" and self.txtInput2.get()=="":
                self.print_and_console("PLEASE IMPUT")
            else:
                if _user.get()==1:
                    login=[self.txtInput1.get(),self.txtInput2.get()]
                user.send_keys(self.txtInput1.get())
                password.send_keys(self.txtInput2.get())
                with open(APP_DIRECTORY+PIKLE_FILE_LOGIN,"wb") as piklefile:
                    pickle.dump(login, piklefile)
                # self.print_and_console("USER FOUND")
    ###SOLD
    def Get_sold(self):
        self.Create_Dir()
        try:
            # self.print_and_console("SEARCHING FOR COUNTER...")
            with open(APP_DIRECTORY+PIKLE_FILE_SOLD,"rb") as piklefile:
                num = pickle.load(piklefile)
            # self.print_and_console("COUNTER FOUND")
        except FileNotFoundError:
            # self.print_and_console("NOT FOUND SETTING DEFAULT...")
            num = 0
            with open(APP_DIRECTORY+PIKLE_FILE_SOLD,"wb") as piklefile:
                pickle.dump(num, piklefile)
            # self.print_and_console("COUNTED RESETED")
        return num

    def Set_sold(self,nums):
        self.Create_Dir()
        try:
            # self.print_and_console("SAVING COUNTER...")
            with open(APP_DIRECTORY+PIKLE_FILE_SOLD,"wb") as piklefile:
                pickle.dump(nums, piklefile)
            # self.print_and_console("COUNTER SAVED")
        except FileNotFoundError:
            pass
    ###PAGE
    def Set_page(self,nums):
        self.Create_Dir()
        try:
            # self.print_and_console("SAVING PAGE...")
            with open(APP_DIRECTORY+PIKLE_FILE_IPAGE,"wb") as piklefile:
                pickle.dump(nums, piklefile)
            # self.print_and_console("PAGE SAVED")
        except FileNotFoundError:
            pass

    def Get_page(self):
        self.Create_Dir()
        try:
            # self.print_and_console("SEARCHING PAGE...")
            with open(APP_DIRECTORY+PIKLE_FILE_IPAGE,"rb") as piklefile:
                num = pickle.load(piklefile)
            # self.print_and_console("PAGE FOUND")
        except FileNotFoundError:
            # self.print_and_console("PAGE NOT FOUND SETTING DEFAULT...")
            num = 0
            with open(APP_DIRECTORY+PIKLE_FILE_IPAGE,"wb") as piklefile:
                pickle.dump(num, piklefile)
            # self.print_and_console("PAGE RESETED")
        return num
    ###NUMBER
    def Get_number(self,driver):
        self.Create_Dir()
        try:
            # self.print_and_console("SEARCHING CARD NUMBER...")
            with open(APP_DIRECTORY+PIKLE_FILE_GRID,"rb") as piklefile:
                num = pickle.load(piklefile)
            # self.print_and_console("CARD NUMBER FOUND")
        except FileNotFoundError:
            # self.print_and_console("NOT FOUND SETTING DEFAULT...")
            gems = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text.split(" ")[1]
            if gems == "Gems":
                num = 1
            else:
                num = 0
            with open(APP_DIRECTORY+PIKLE_FILE_GRID,"wb") as piklefile:
                pickle.dump(num, piklefile)
            # self.print_and_console("NUMBER RESETTED")
        return num

    def Set_number(self,nums,driver):
        self.Create_Dir()
        try:
            # self.print_and_console("SAVING CARD NUMBER...")
            with open(APP_DIRECTORY+PIKLE_FILE_GRID,"wb") as piklefile:
                if nums%25 == 0:
                   driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                   self.Set_page(self.Get_page()+1)
                pickle.dump(nums, piklefile)
            # self.print_and_console("CARD SAVED")
        except FileNotFoundError:
            pass
    ###RESET
    def reset_settings(self):
        if _accidch.get() == 1:
            # self.print_and_console("DELETING ACCID FILE...")
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_ACCID):
                os.remove(APP_DIRECTORY+PIKLE_FILE_ACCID)
                self.print_and_console("DELETED ACCID FILE")
            else:
                self.print_and_console("ACCID FILE NOT FOUND")
        if _soldch.get() == 1:
            # self.print_and_console("DELETING COUNTER FILE...")
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_SOLD):
                os.remove(APP_DIRECTORY+PIKLE_FILE_SOLD)
                self.print_and_console("DELETED COUTER FILE")
            else:
                self.print_and_console("COUNTER FILE NOT FOUND")
        if _loginch.get() == 1:
            # self.print_and_console("DELETING LOGIN FILE...")
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_LOGIN):
                os.remove(APP_DIRECTORY+PIKLE_FILE_LOGIN)
                self.print_and_console("DELETED LOGIN FILE")
            else:
                self.print_and_console("LOGIN FILE NOT FOUND")
        if _cromoch.get() == 1:
            # self.print_and_console("DELETING GRID FILE...")
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_GRID):
                os.remove(APP_DIRECTORY+PIKLE_FILE_GRID)
                self.print_and_console("DELETED GRID FILE")
            else:
                self.print_and_console("GRID FILE NOT FOUND")
            # self.print_and_console("DELETING PAGE FILE...")
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_IPAGE):
                os.remove(APP_DIRECTORY+PIKLE_FILE_IPAGE)
                self.print_and_console("DELETED PAGE FILE")
            else:
                self.print_and_console("PAGE FILE NOT FOUND")
            
    def sell_redirect(self):
        try:
            thread = threading.Thread(target=self.cromos_sell)
            if not thread.is_alive():
                thread.start()
            else:
                self.cromos_sell()
        except:
            pass

    def finish_sell(self,driver,price,num):
        ##SELLING
        self.print_and_console("FINISHING SALE...")
        self.Get_inventory_grid(driver)
        sleep(2)
        driver.find_element(By.XPATH,"//span[@class='item_market_action_button_contents']").click()
        sleep(3)
        inputtext = driver.find_element(By.XPATH,"//input[@id='market_sell_buyercurrency_input']")
        inputtext.send_keys(price)
        if num == 0:
            driver.find_element(By.XPATH,"//input[@id='market_sell_dialog_accept_ssa']").click()
        sleep(3)
        driver.find_element(By.XPATH,"//a[@id='market_sell_dialog_accept']").click()
        sleep(3)
        driver.find_element(By.XPATH,"//a[@id='market_sell_dialog_ok']").click()
        sleep(3)
        try:
            driver.find_elements(By.XPATH,"//div[@class='newmodal_content_border']//span")[-1].click()
        except:
            pass
        #saving
        self.Set_sold(self.Get_sold()+1)
        self.lblCounter["text"]=(self.Get_sold())
        self.Set_number(self.Get_number(driver)+1,driver)
        self.print_and_console("SALE FINISHED")
        sleep(5)

    def fnd(self,driver,path):
        speed = True
        while speed:
            try:
                res = driver.find_element(By.XPATH,path)
                speed = False
            except:
                pass
        return res

    def fnds(self,driver,path):
        speed = True
        while speed:
            try:
                res = driver.find_elements(By.XPATH,path)
                speed = False
            except:
                pass
        return res

    def login(self,driver):
        driver.get(URL)
        user = self.fnd(driver,"//input[@id='input_username']")
        password = self.fnd(driver,"//input[@id='input_password']")
        self.Get_login(user,password)
        driver.find_element(By.CLASS_NAME,"login_btn").click()
        sleep(3)
        # self.print_and_console("2FA...")
        if chekbox.get() == 1:
            _2fa = self.txtInput3.get()
            if _2fa!="":
                try:
                    twofactor = driver.find_element(By.ID,"twofactorcode_entry")
                    twofactor.send_keys(_2fa)
                except:
                    self.print_and_console("NO 2FA FOUND")
            else:
                self.print_and_console("NO USER INPUT")
        else:
            self.print_and_console("NO 2FA CHECKBOX SELECTED")
        # self.print_and_console("2FA DONE")
        driver.find_elements(By.XPATH,"//div[@id='login_twofactorauth_buttonset_entercode']//div")[0].click()

    ###------------------------------------------------------------------------------------###

    def cromos_sell(self):
        try:
            self.reset_settings()
            ##---load window and login
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            ##---login
            self.print_and_console("LOGING...")
            self.login(driver)
            self.print_and_console("LOGGED")
            sleep(3)
            _accid = self.Get_accid(driver)
            inventory_url = "https://steamcommunity.com/id/{}/inventory/#753".format(_accid)
            driver.get(inventory_url)
            sleep(4)
            if self.Get_page() > 0:
                for x in range(self.Get_page()):
                    driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                    sleep(1)
            #---start doing reps
            card_nameb = None
            name = ["",""]
            res = None
            for x in range(10000):
                try:
                    self.Get_inventory_grid(driver)
                    sleep(3)
                    name = ["",""]
                    try:
                        name[0] = driver.find_element(By.XPATH,"//h1[@id='iteminfo0_item_name']").text
                    except:
                        pass
                    try:
                        name[1] = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text
                    except:
                        pass
                    if name[0]=="":
                        card_namea=name[1]
                        res = 1
                    else:
                        card_namea=name[0]
                        res = 0
                    # print(card_namea)
                    # print(card_nameb)
                    if card_namea != card_nameb:
                        card_nameb = card_namea
                        ##---selling
                        name = ["",""]
                        try:
                            if res ==0:
                                name[0] = driver.find_element(By.XPATH,"//div[@id='iteminfo0_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        try:
                            if res == 1:
                                name[1] = driver.find_element(By.XPATH,"//div[@id='iteminfo1_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        ##loking for price
                        if name[0]=="":
                            card_url=name[1]
                        else:
                            card_url=name[0]
                        self.print_and_console("GETTING CARD PRICE...") 
                        driver.get(card_url)##load card
                        sleep(3)     
                        text = driver.find_elements(By.XPATH,"//div[@id='market_commodity_forsale_table']//td")[0].text
                        price = str(text.split(" ")[1])
                        price = round(float(self.Replace(price))*PRICE_MULTIPLIER,2)
                        driver.get(inventory_url)##load inv
                        self.print_and_console("PRICE FOUND")
                        print(price)
                        sleep(2)
                        if self.Get_page() > 0:
                            for x in range(self.Get_page()):
                                driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                                sleep(1)
                        # sleep(1)
                        self.finish_sell(driver,price,0)
                    else:
                        card_nameb = card_namea
                        self.finish_sell(driver,price,1)
                except ElementClickInterceptedException:
                    self.print_and_console("CARD ALRREADY SOLD PASSING")
                    driver.find_element(By.XPATH,"//div[@class='newmodal_header']//div").click()
                    self.Set_sold(self,)

        except InvalidSessionIdException:
            self.print_and_console("BROWSER CONNECTION LOST")
        except EOFError:
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_GRID):
                os.remove(APP_DIRECTORY+PIKLE_FILE_GRID)
            if os.path.exists(APP_DIRECTORY+PIKLE_FILE_IPAGE):
                os.remove(APP_DIRECTORY+PIKLE_FILE_IPAGE)
        # except:
        #     self.print_and_console("*********UNEXPECTED ERROR*********")
        #     messagebox.showerror(title="Error", message="Unexpected error")
        
    def create_widgets(self):
        #Title
        self.lblTitle = Label(self,text="CROMOS")
        self.lblTitle.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH*3, height=NORMAL_HEIGTH)
        #LOGIN
        self.checkbox1 = Checkbutton(self, text="SAVE", variable=_user,onvalue=1, offvalue=0)
        self.checkbox1.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.txtInput1=Entry(self)
        self.txtInput1.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.txtInput2=Entry(self)
        self.txtInput2.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        #2FA
        self.checkbox3 = Checkbutton(self, text="2FA:", variable=chekbox,onvalue=1, offvalue=0)
        self.checkbox3.place(x=POS_COL3_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.txtInput3=Entry(self)
        self.txtInput3.place(x=POS_COL4_X-10,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        #Start
        self.btnStart = Button(self,text="Start", command=self.sell_redirect)
        self.btnStart.place(x=POS_COL3_X,y=POS_ROW3_Y,width=BUTTON_WIDTH, height=NORMAL_HEIGTH)
        #Quit
        self.btnQuit = Button(self,text="Quit", command=self.Quit)
        self.btnQuit.place(x=POS_COL5_X+10,y=POS_ROW6_Y+5,width=BUTTON_WIDTH, height=NORMAL_HEIGTH)
        #CLS
        self.btnQuit = Button(self,text="Clear", command=self.Clean)
        self.btnQuit.place(x=POS_COL4_X,y=POS_ROW3_Y,width=BUTTON_WIDTH, height=NORMAL_HEIGTH)
        #Console
        self.lblLine1 = Label(self,text="", borderwidth=2, relief="groove")
        self.lblLine1.place(x=POS_COL1_X,y=POS_ROW4_Y-5,width=NORMAL_WIDTH*4.20, height=NORMAL_HEIGTH*3+30)
        self.lblConsole3 = Label(self,text="")
        self.lblConsole3.place(x=POS_COL1_X+5,y=POS_ROW4_Y,width=NORMAL_WIDTH*4.10, height=NORMAL_HEIGTH)
        self.lblConsole2 = Label(self,text="")
        self.lblConsole2.place(x=POS_COL1_X+5,y=POS_ROW5_Y,width=NORMAL_WIDTH*4.10, height=NORMAL_HEIGTH)
        self.lblConsole1 = Label(self,text="SCRIPT PER VENDRE CROMOS")
        self.lblConsole1.place(x=POS_COL1_X+5,y=POS_ROW6_Y,width=NORMAL_WIDTH*4.10, height=NORMAL_HEIGTH)
        #Counter
        self.lblCounter = Label(self,text=self.Get_sold(), borderwidth=2, relief="groove")
        self.lblCounter.place(x=POS_COL4_X-10,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Reset
        ##LINEAS
        self.lblLine = Label(self,text="", borderwidth=2, relief="groove")
        self.lblLine.place(x=POS_COL5_X-5,y=POS_ROW1_Y-5,width=NORMAL_WIDTH+10, height=NORMAL_HEIGTH*6+20)
        ##CHEKBOX
        self.lblLabel = Label(self,text="RESET VARIABLES")
        self.lblLabel.place(x=POS_COL5_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.checkbox4 = Checkbutton(self, text="ID", variable=_accidch,onvalue=1, offvalue=0)
        self.checkbox4.place(x=POS_COL5_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.checkbox5 = Checkbutton(self, text="COUNTER", variable=_soldch,onvalue=1, offvalue=0)
        self.checkbox5.place(x=POS_COL5_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.checkbox6 = Checkbutton(self, text="LOGING", variable=_loginch,onvalue=1, offvalue=0)
        self.checkbox6.place(x=POS_COL5_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.checkbox7 = Checkbutton(self, text="GRID", variable=_cromoch,onvalue=1, offvalue=0)
        self.checkbox7.place(x=POS_COL5_X,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)


root = Tk()
chekbox = IntVar() 
_accidch = IntVar() 
_soldch = IntVar() 
_loginch = IntVar() 
_cromoch = IntVar() 
_user = IntVar() 
# _passw = IntVar() 
root.wm_title("")
root.resizable(width=False, height=False)
app = FrSuma(root)
app.mainloop()