from selenium.common.exceptions import InvalidArgumentException, InvalidSessionIdException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from difflib import SequenceMatcher
from tkinter import messagebox
from selenium import webdriver
from pathlib import Path
from time import sleep
from tkinter import *
import threading 
import datetime
import sqlite3
import pickle
import time
import os

##SIZE
NORMAL_WIDTH=100#x
NORMAL_HEIGTH=30#y
##AXIS X
POX_X_SPACING=20
POS_COL1_X=POX_X_SPACING
POS_COL2_X=(POX_X_SPACING*2)+NORMAL_WIDTH
POS_COL3_X=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
POS_COL4_X=(POX_X_SPACING*4)+(NORMAL_WIDTH*3)
POS_COL5_X=(POX_X_SPACING*5)+(NORMAL_WIDTH*4)
POS_COL6_X=(POX_X_SPACING*6)+(NORMAL_WIDTH*5)
POS_COL7_X=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
##AXIS Y
POX_Y_SPACING=20
POS_ROW1_Y=POX_Y_SPACING
POS_ROW2_Y=(POX_Y_SPACING*2)+NORMAL_HEIGTH
POS_ROW3_Y=(POX_Y_SPACING*3)+(NORMAL_HEIGTH*2)
POS_ROW4_Y=(POX_Y_SPACING*4)+(NORMAL_HEIGTH*3)
POS_ROW5_Y=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
POS_ROW6_Y=(POX_Y_SPACING*6)+(NORMAL_HEIGTH*5)
POS_ROW7_Y=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
##WINDOW
WINDOW_WIDTH=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
WINDOW_HEIGTH=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)
##CREDENTIALS
URL="https://store.steampowered.com/login/"
APP_DIRECTORY="{}\\Documents\\YPPAHSOFT\\".format(Path.home())
PIKLE_FILE_ACCID=APP_DIRECTORY+"pickle.pkl"
PIKLE_FILE_COUNTER=APP_DIRECTORY+"pickle2.pkl"
PIKLE_FILE_TIME=APP_DIRECTORY+"pickle3.pkl"
PIKLE_FILE_GRID=APP_DIRECTORY+"pickle4.pkl"
PIKLE_FILE_IPAGE=APP_DIRECTORY+"pickle5.pkl"
PIKLE_FILE_PRICE=APP_DIRECTORY+"pickle6.pkl"
PIKLE_FILE_STOP=APP_DIRECTORY+"pickle7.pkl"
PIKLE_FILE_COOKIES=APP_DIRECTORY+"pikcle8.pkl"
DB_FILE=APP_DIRECTORY+"cards.db"
##PRICING
PRICE_MULTIPLIER=1.40

class Main(Frame):

    def __init__(self, master=None):
        super().__init__(master,width=WINDOW_WIDTH, height=WINDOW_HEIGTH)
        self.master = master
        self.pack()
        self.create_widgets()
        
    ###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###

    def Quit(self):
        exit()

    def print_and_console(self,text):
        print(text)

    def print_console(self,text):
        self.mylist.insert(END, text)

    def Create_Dir(self):
        try:
            os.mkdir(APP_DIRECTORY)
        except FileExistsError:
            pass

    def Get_accid(self,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING FOR PREVIOUS ID...")
            with open(PIKLE_FILE_ACCID,"rb") as piklefile:
                _accid = pickle.load(piklefile)
            self.print_and_console("ID RECOVERED")
        except FileNotFoundError:
            self.print_and_console("PREVIOUS USER NOT FOUND SEARCHING NEW ID...")
            _accid = self.fnds(driver,"//div[@id='global_actions']//a")[-1].get_attribute("href")
            with open(PIKLE_FILE_ACCID,"wb") as piklefile:
                pickle.dump(_accid, piklefile)
            self.print_and_console("ID RECOVERED")
        return _accid
    
    def Clean(self):
        self.mylist.delete(0,END)

    def All(self):
        self.Clean()
        ##DB
        self.mylist.insert(END,"|  id  |  Card Name  |  Price  |  Percent  |  Game  |  Date  |  ")
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Cards''')
        select = cursor.fetchall()
        for doc in select:
            self.mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
        connection.commit()
        connection.close()
        self.mylist.see("end")

    def Del(self):
        text = self.txtInput1.get()
        if not text=="":
            ##DB
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM Cards WHERE id = {}'''.format(text))
            connection.commit()
            connection.close()
            self.All()
        else:
            self.print_and_console("***NOT FOUND***")

    def Sel(self):
        self.Clean()
        ##DB
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Cards''')
        select = cursor.fetchall()
        for doc in select:
            if self.compare(self.txtInput1.get(),doc[4])>0.7:
                self.mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
        connection.commit()
        connection.close()

    def Stop(self):
        self.Set_stop(True)
        

    def compare(self,dbtext,imtext):
        return SequenceMatcher(None, dbtext, imtext).ratio()

    def Replace(self, string):
        return string.replace(",",".")

    def Get_inventory_grid(self,driver,num,inventory_url):
        sleep(0.5)
        self.print_and_console("SEARCHING FOR GRID...")
        if num == 1:
            if self.Get_number(driver)%25 == 0 and self.Get_number(driver)!=0:
                self.fnd(driver,"//a[@id='pagebtn_next']").click()
                self.Set_page(self.Get_page()+1)
        invetorygrid = driver.find_elements(By.XPATH,"//div[@class='itemHolder']")
        invetorygrid[self.Get_number(driver)].click()
        self.print_and_console("GRID FOUND")

    ###COOKIES
    def Set_cookies(self,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SAVING COOKIES...")
            with open(PIKLE_FILE_COOKIES,"wb") as piklefile:
                pickle.dump(driver.get_cookies(), piklefile)
            self.print_and_console("COOKIES SAVED")
        except FileNotFoundError:
            pass

    def Get_cookies(self,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING COOKIES...")
            with open(PIKLE_FILE_COOKIES,"rb") as piklefile:
                cookies = pickle.load(piklefile)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            self.print_and_console("COOKIES FOUND")
        except FileNotFoundError:
            self.print_and_console("NO COOKIES FOUND")
        return driver

    ###STOP
    def Set_stop(self,text):
        self.Create_Dir()
        try:
            self.print_and_console("SAVING STOP...")
            with open(PIKLE_FILE_STOP,"wb") as piklefile:
                pickle.dump(text, piklefile)
            self.print_and_console("STOP SAVED")
        except FileNotFoundError:
            pass

    def Get_stop(self):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING STOP...")
            with open(PIKLE_FILE_STOP,"rb") as piklefile:
                text = pickle.load(piklefile)
            self.print_and_console("STOP FOUND")
        except FileNotFoundError:
            self.print_and_console("STOP NOT FOUND SETTING DEFAULT...")
            text = False
            with open(PIKLE_FILE_STOP,"wb") as piklefile:
                pickle.dump(text, piklefile)
            self.print_and_console("STOP RESETED")
        return text

    ###SOLD
    def Get_sold(self):
        self.Create_Dir()
        #counter
        try:
            self.print_and_console("SEARCHING FOR COUNTER...")
            with open(PIKLE_FILE_COUNTER,"rb") as piklefile:
                num = pickle.load(piklefile)
            self.print_and_console("COUNTER FOUND")
        except FileNotFoundError:
            self.print_and_console("COUNTER NOT FOUND SETTING DEFAULT...")
            num = 0
            with open(PIKLE_FILE_COUNTER,"wb") as piklefile:
                pickle.dump(num, piklefile)
            self.print_and_console("COUNTED RESETED")
        #price
        try:
            self.print_and_console("SEARCHING FOR PRICE...")
            with open(PIKLE_FILE_PRICE,"rb") as piklefile:
                price = pickle.load(piklefile)
            self.print_and_console("PRICE FOUND")
        except FileNotFoundError:
            self.print_and_console("PRICE NOT FOUND SETTING DEFAULT...")
            price = 0
            with open(PIKLE_FILE_PRICE,"wb") as piklefile:
                pickle.dump(price, piklefile)
            self.print_and_console("PRICE RESETED")
        #time
        try:
            self.print_and_console("SEARCHING FOR TIME...")
            with open(PIKLE_FILE_TIME,"rb") as piklefile:
                time = pickle.load(piklefile)
            self.print_and_console("TIME FOUND")
        except FileNotFoundError:
            self.print_and_console("TIME NOT FOUND SETTING DEFAULT...")
            time = 0
            with open(PIKLE_FILE_TIME,"wb") as piklefile:
                pickle.dump(time, piklefile)
            self.print_and_console("TIME RESETED")
        return num, price, time

    def Set_sold(self,nums,price,time):
        self.Create_Dir()
        try:
            #counter
            self.print_and_console("SAVING COUNTER...")
            with open(PIKLE_FILE_COUNTER,"wb") as piklefile:
                pickle.dump(nums, piklefile)
            self.print_and_console("COUNTER SAVED")
            #price
            self.print_and_console("SAVING PRICE...")
            with open(PIKLE_FILE_PRICE,"wb") as piklefile:
                pickle.dump(price, piklefile)
            self.print_and_console("PRICE SAVED")
            #time
            self.print_and_console("SAVING TIME...")
            with open(PIKLE_FILE_TIME,"wb") as piklefile:
                pickle.dump(time, piklefile)
            self.print_and_console("TIME SAVED")
        except FileNotFoundError:
            pass
    ###PAGE
    def Set_page(self,nums):
        self.Create_Dir()
        try:
            self.print_and_console("SAVING PAGE...")
            with open(PIKLE_FILE_IPAGE,"wb") as piklefile:
                pickle.dump(nums, piklefile)
            self.print_and_console("PAGE SAVED")
        except FileNotFoundError:
            pass

    def Get_page(self):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING PAGE...")
            with open(PIKLE_FILE_IPAGE,"rb") as piklefile:
                num = pickle.load(piklefile)
            self.print_and_console("PAGE FOUND")
        except FileNotFoundError:
            self.print_and_console("PAGE NOT FOUND SETTING DEFAULT...")
            num = 0
            with open(PIKLE_FILE_IPAGE,"wb") as piklefile:
                pickle.dump(num, piklefile)
            self.print_and_console("PAGE RESETED")
        return num
    ###NUMBER
    def Get_number(self,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SEARCHING CARD NUMBER...")
            with open(PIKLE_FILE_GRID,"rb") as piklefile:
                num = pickle.load(piklefile)
            self.print_and_console("CARD NUMBER FOUND")
        except FileNotFoundError:
            self.print_and_console("NOT FOUND SETTING DEFAULT...")
            try:
                sleep(1)
                gems = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text.split(" ")[1]
                if gems == "Gems" or gems == "Gemas":
                    num = 1
                else:
                    num = 0
                with open(PIKLE_FILE_GRID,"wb") as piklefile:
                    pickle.dump(num, piklefile)
            except IndexError:
                num = 0
                with open(PIKLE_FILE_GRID,"wb") as piklefile:
                    pickle.dump(num, piklefile)
            self.print_and_console("NUMBER RESETTED")
        return num

    def Set_number(self,nums,driver):
        self.Create_Dir()
        try:
            self.print_and_console("SAVING CARD NUMBER...")
            with open(PIKLE_FILE_GRID,"wb") as piklefile:
                pickle.dump(nums, piklefile)
            self.print_and_console("CARD SAVED")
        except FileNotFoundError:
            pass
    ###RESET
    def reset_settings(self):
        #counter
        self.print_and_console("DELETING COUNTER FILE...")
        if os.path.exists(PIKLE_FILE_COUNTER):
            os.remove(PIKLE_FILE_COUNTER)
            self.print_and_console("DELETED COUTER FILE")
        else:
            self.print_and_console("COUNTER FILE NOT FOUND")
        #price
        self.print_and_console("DELETING PRICE FILE...")
        if os.path.exists(PIKLE_FILE_PRICE):
            os.remove(PIKLE_FILE_PRICE)
            self.print_and_console("DELETED PRICE FILE")
        else:
            self.print_and_console("PRICE FILE NOT FOUND")
        #time
        self.print_and_console("DELETING TIME FILE...")
        if os.path.exists(PIKLE_FILE_TIME):
            os.remove(PIKLE_FILE_TIME)
            self.print_and_console("DELETED TIME FILE")
        else:
            self.print_and_console("TIME FILE NOT FOUND")
        ##grid
        self.print_and_console("DELETING GRID FILE...")
        if os.path.exists(PIKLE_FILE_GRID):
            os.remove(PIKLE_FILE_GRID)
            self.print_and_console("DELETED GRID FILE")
        else:
            self.print_and_console("GRID FILE NOT FOUND")
        #page
        self.print_and_console("DELETING PAGE FILE...")
        if os.path.exists(PIKLE_FILE_IPAGE):
            os.remove(PIKLE_FILE_IPAGE)
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

    def finish_sell(self,driver,price,name,gamename,inventory_url,Tstart):
        ##SELLING
        self.Get_inventory_grid(driver,0,inventory_url)
        try:
            self.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//span[2]").click()##sell btn
        except:
            try:
                self.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//span[2]").click()##sell btn
            except:
                pass
        sleep(0.5)
        inputtext = self.fnd(driver,"//input[@id='market_sell_buyercurrency_input']")##price input
        inputtext.send_keys(price)
        sleep(0.5)
        self.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
        if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You must agree to the terms of the Steam Subscriber Agreement to sell this item.":
            self.fnd(driver,"//input[@id='market_sell_dialog_accept_ssa']").click()##checkbox
            self.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
        sleep(0.5)
        self.fnd(driver,"//a[@id='market_sell_dialog_ok']").click()##btn ok 
        if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You already have a listing for this item pending confirmation. Please confirm or cancel the existing listing.":
            self.fnd(driver,"//div[@id='market_sell_dialog']//div[@class='newmodal_close']").click()##close modal
            self.Set_number(self.Get_number(driver)+1,driver)
            self.print_and_console("CARD ALREADY SOLD")
        else:
            sleep(0.5)
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You have too many listings pending confirmation. Please confirm or cancel some before attempting to list more.":
                self.Stop()
                self.Clean()
                self.mylist.insert(END,"***************************************************MAX CONFIRMATIONS REACHED***********************************************")
                self.mylist.insert(END,"*********************************************PLEASE CONFIRM THE CARDS AND RESTART******************************************")
            else:
                sleep(0.5)
                try:
                    driver.find_element(By.XPATH,"//div[@class='newmodal_buttons']//span").click()##2fa x btn 
                except:
                    self.fnd(driver,"//div[@class='newmodal_header']//div").click()
                #saving
                self.Set_sold(self.Get_sold()[0]+1,self.lblPrice["text"],round((time.time() - Tstart)+float(self.lblTime["text"]),2))
                self.lblCounter["text"]=(self.Get_sold()[0])
                self.lblTime["text"] = self.Get_sold()[2]
                self.lblPrice["text"] = round(float(self.lblPrice["text"])+price,2)
                self.Set_number(self.Get_number(driver)+1,driver)
                ##DB
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute('''SELECT id FROM Cards ORDER BY id DESC LIMIT 1''')
                select = cursor.fetchall()
                try:
                    for doc in select:
                        number = int(doc[0]+1)
                except IndexError:
                    number = 0
                if not "number" in locals():
                    number = 0
                gamename = gamename.replace(" Trading Card","")
                dt = datetime.datetime.today()
                date = "{}-{}-{}".format(dt.day,dt.month,dt.year)
                name = name.replace('"','')
                cursor.execute('''INSERT INTO Cards (id, Name, Price, Percent, Game, Date) VALUES ({},"{}", {}, {}, "{}","{}")'''.format(number, name, price, str(PRICE_MULTIPLIER).split(".")[1]+"0",gamename,date))
                cursor.execute('''SELECT * FROM Cards ORDER BY id DESC LIMIT 1''')
                select = cursor.fetchall()
                for doc in select:
                    self.print_console("| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
                connection.commit()
                cursor.close()
                connection.close()
                self.mylist.see("end")
                #DB
                self.print_and_console("SOLD")
                sleep(0.5)

    def info(self):
        self.Clean()
        self.mylist.insert(END,"Sel-> Selects from the db the registres by game name, introduced in the user input")
        self.mylist.insert(END,"Del-> Deletes from the db the registry with the introduced id")
        self.mylist.insert(END,"C-> Cleans the Console")
        self.mylist.insert(END,"All-> Selects all registres from the db")
        self.mylist.insert(END,"LOGIN-> Input acc to sell cards and input 2FA if enabled")
        self.mylist.insert(END,"START-> Starts selling")
        self.mylist.insert(END,"Restart-> Resets all values to start over")
        self.mylist.insert(END,"Stop-> Stops selling when finishes the actual card")
        self.mylist.insert(END,"Quit-> Quits the program, please press stop before pressing this to avoid issues")
        self.mylist.insert(END,"ESTIMATED TIME 30m -> 250 cards (comfirmation cap)")

    def GotoPage(self,driver,inventory_url):
        driver.get(inventory_url)##load inv
        sleep(1)
        if self.Get_page() > 0:##scroll
            sleep(0.5)
            for x in range(self.Get_page()):
                driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                sleep(1)

    def fnd(self,driver,path):
        speed = True
        while speed:
            try:
                res = driver.find_element(By.XPATH,path)
                speed = False
                print("found1 {}".format(path))
            except:
                print("nfound1 {}".format(path))
                sleep(0.1)
                pass
        return res

    def fndcn(self,driver,path):
        speed = True
        while speed:
            try:
                res = driver.find_element(By.CLASS_NAME,path)
                speed = False
                print("found2 {}".format(path))
            except:
                print("nfound2 {}".format(path))
                pass
        return res

    def fnds(self,driver,path):
        speed = True
        while speed:
            try:
                res = driver.find_elements(By.XPATH,path)
                speed = False
                print("found3 {}".format(path))
            except:
                print("nfound3 {}".format(path))
                pass
        return res

    def login(self,driver):
        driver.get(URL)
        user = self.fnd(driver,"//input[@id='input_username']")
        password = self.fnd(driver,"//input[@id='input_password']")
        user.send_keys(self.txtInput1.get())
        password.send_keys(self.txtInput2.get())
        self.fndcn(driver,'login_btn').click()
        sleep(3)
        self.print_and_console("2FA...")
        _2fa = self.txtInput3.get()
        if _2fa!="":
            try:
                twofactor = self.fnd(driver,"//input[@id='twofactorcode_entry']")
                twofactor.send_keys(_2fa)
            except:
                self.print_and_console("NO 2FA FOUND")
                pass
        else:
            self.print_and_console("NO USER INPUT")
            pass
        self.print_and_console("2FA DONE")
        self.fnds(driver,"//div[@id='login_twofactorauth_buttonset_entercode']//div")[0].click()

    ###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###

    def cromos_sell(self):
        try:
            if not os.path.exists(DB_FILE):
                self.Create_Dir()
                ##DB
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (id INT PRIMARY KEY,Name TEXT, Price FLOAT, Percent INT, Game TEXT, Date TEXT)''')
                connection.commit()
                connection.close()
            self.Clean()
            self.lblCounter["text"]=(self.Get_sold()[0])
            self.lblPrice["text"]=(self.Get_sold()[1])
            self.lblTime["text"]=(self.Get_sold()[2])
            ##---load window and login
            driver = webdriver.Firefox()
            driver.get("https://steamcommunity.com/")
            if os.path.exists(PIKLE_FILE_COOKIES):
                driver = self.Get_cookies(driver)
            else:
                ##---login
                self.print_and_console("LOGING...")
                self.login(driver)
                self.print_and_console("LOGGED")
                sleep(2)
            driver.execute_script('''window.open("","_blank");''')
            driver.switch_to.window(driver.window_handles[0])
            inventory_url = "{}/inventory/#753".format(self.Get_accid(driver))
            driver.implicitly_wait(3)
            #---start doing sells
            self.GotoPage(driver,inventory_url)##load inv & scroll
            driver.execute_script('''ChangeLanguage( 'english' );''')
            sleep(1)
            self.GotoPage(driver,inventory_url)##load inv & scroll
            self.Set_stop(False)
            card_nameb = None
            name = ["",""]
            res = None
            if not os.path.exists(PIKLE_FILE_COOKIES):
                self.Set_cookies(driver)
            for x in range(10000):
                if self.Get_stop()==False:
                    Tstart = time.time()
                    self.Get_inventory_grid(driver,1,inventory_url)
                    name = ["",""]
                    gname = ["",""]
                    try:##find card name
                        name[0] = driver.find_element(By.XPATH,"//h1[@id='iteminfo0_item_name']").text
                        gname[0] = driver.find_element(By.XPATH,"//div[@id='iteminfo0_game_info']//div[3]").text
                    except:
                        pass
                    try:
                        name[1] = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text
                        gname[1] = driver.find_element(By.XPATH,"//div[@id='iteminfo1_game_info']//div[3]").text
                    except:
                        pass
                    if name[0]=="":
                        card_namea=name[1]
                        res = 1 
                    else:
                        card_namea=name[0]
                        res = 0
                    if gname[0]=="":
                        game_name = gname[1]
                    else:
                        game_name = gname[0]
                    if card_namea != card_nameb:
                        card_nameb = card_namea
                        ##---selling
                        name = ["",""]
                        sleep(1)
                        try:##find card link
                            if res ==0:
                                name[0] = self.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        try:
                            if res == 1:
                                name[1] = self.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        if name[0]=="":
                            card_url=name[1]
                        else:
                            card_url=name[0]
                        ##loking for price
                        self.print_and_console("GETTING CARD PRICE...")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(card_url)##load card
                        speed = True
                        refresh = 0
                        while speed:
                            refresh+=1
                            if refresh > 1:
                                driver.refresh()
                            try:
                                text = driver.find_elements(By.XPATH,"//div[@id='market_commodity_forsale_table']//td")[0].text
                                speed = False
                            except:
                                pass
                        price = str(text.split(" ")[1])
                        try:
                            price = round(float(self.Replace(price))*PRICE_MULTIPLIER,2)
                            self.print_and_console("PRICE FOUND")
                            driver.switch_to.window(driver.window_handles[0])
                            self.finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                        except ValueError:
                            self.Set_number(self.Get_number(driver)+1,driver)
                    else:
                        card_nameb = card_namea
                        self.finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                else:
                    self.print_and_console("***STOPED***")
                    break
        except InvalidSessionIdException:
            self.print_and_console("BROWSER CONNECTION LOST")
        # except:
        #     self.print_and_console("*********UNEXPECTED ERROR*********")
        #     messagebox.showerror(title="Error", message="Unexpected error")
        #     sleep(5)
        #     exit()
        
    def create_widgets(self):
        ###Title
        self.lblTitle = Label(self,text="CARDS")
        self.lblTitle.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Start
        self.btnStart = Button(self,text="Start", command=self.sell_redirect)
        self.btnStart.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Quit
        self.btnQuit = Button(self,text="Quit", command=self.Quit)
        self.btnQuit.place(x=POS_COL6_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Stop
        self.btnStop = Button(self,text="Stop", command=self.Stop)
        self.btnStop.place(x=POS_COL6_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Restart
        self.btnRestart = Button(self,text="Restart", command=self.reset_settings)
        self.btnRestart.place(x=POS_COL6_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###info
        self.btnRestart = Button(self,text="i", command=self.info)
        self.btnRestart.place(x=POS_COL4_X,y=POS_ROW1_Y,width=NORMAL_WIDTH/2-20, height=NORMAL_HEIGTH)
        ###Buttons
        ##line
        self.lblLine1 = Label(self,text="", borderwidth=2, relief="groove")
        self.lblLine1.place(x=POS_COL1_X-4,y=POS_ROW2_Y-4,width=NORMAL_WIDTH*2+30, height=NORMAL_HEIGTH+10)
        ##CLS
        self.btnCls = Button(self,text="C", command=self.Clean)
        self.btnCls.place(x=POS_COL1_X,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##ALL
        self.btnAll = Button(self,text="All", command=self.All)
        self.btnAll.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##sel
        self.btnsel = Button(self,text="Sel", command=self.Sel)
        self.btnsel.place(x=POS_COL1_X,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##del
        self.btndel = Button(self,text="Del", command=self.Del)
        self.btndel.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ###LOGIN
        ##text
        self.Label1 = Label(self, text="LOGIN")
        self.Label1.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##inputs
        self.txtInput1=Entry(self)
        self.txtInput1.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.txtInput2=Entry(self)
        self.txtInput2.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###2FA
        ##checkbox
        self.checkbox3 = Label(self, text="2FA")
        self.checkbox3.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##input
        self.txtInput3=Entry(self)
        self.txtInput3.place(x=POS_COL3_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Console
        ##scroll
        self.scrollbar = Scrollbar(root)
        self.mylist = Listbox(root, yscrollcommand = self.scrollbar.set )
        self.mylist.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*7, height=NORMAL_HEIGTH*6)
        self.info()
        self.scrollbar.config( command = self.mylist.yview )
        self.scrollbar.place(x=POS_COL7_X-POX_X_SPACING,y=POS_ROW4_Y,width=POX_X_SPACING, height=NORMAL_HEIGTH*6)
        ####Counter 
        ###sold
        self.Label1 = Label(self, text="CARDS DONE")
        self.Label1.place(x=POS_COL4_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.lblCounter = Label(self,text="0", borderwidth=2, relief="groove")
        self.lblCounter.place(x=POS_COL5_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###price
        self.Label2 = Label(self, text="CUR. TOTAL PRICE")
        self.Label2.place(x=POS_COL4_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        self.lblPrice = Label(self,text="0", borderwidth=2, relief="groove")
        self.lblPrice.place(x=POS_COL5_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##time
        self.Label3 = Label(self, text="TIME")
        self.Label3.place(x=POS_COL4_X+50,y=POS_ROW1_Y,width=NORMAL_WIDTH/2, height=NORMAL_HEIGTH)
        self.lblTime = Label(self,text="0", borderwidth=2, relief="groove")
        self.lblTime.place(x=POS_COL5_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)


root = Tk()
chekbox = IntVar()
root.wm_title("V1.1.2")
root.resizable(width=False, height=False)
# root.configure(background='#1e1e1e')
app = Main(root)
app.mainloop()