from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from difflib import SequenceMatcher
from tkinter import messagebox
from selenium import webdriver
from pathlib import Path
from time import sleep
from tkinter import *
# import webbrowser
import threading 
import datetime
import logging
import sqlite3
import pickle
# import psutil
import ctypes
import time
# import sys
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
##WINDOWS
CARDS_WIDTH=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
CARDS_HEIGTH=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)
LOGIN_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
LOGIN_HEIGHT=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
SETTINGS_WIDTH=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)
SETTINGS_HEIGHT=int(POX_X_SPACING*3.5)+(NORMAL_WIDTH*3)
##VERSION
VERSION="V1.15"
##CREDENTIALS
URL="https://store.steampowered.com/login/"
##PRICING
PRICE_MULTIPLIER=1.40
##SETTINGS
SETTINGS_FILE = f"{Path.home()}\\Documents\\YPPAHSOFT\\settings.pkl"
if os.path.exists(SETTINGS_FILE):
   with open(SETTINGS_FILE,"rb") as piklefile:
        SETTINGS = pickle.load(piklefile)
else:
    APP_DIRECTORY=f"{Path.home()}\\Documents\\YPPAHSOFT\\"
    SETTINGS = {
        "ACCID": None,
        "COUNTER": 0,
        "TIME": 0,
        "GRID": 0,
        "IPAGE": 0,
        "PRICE": 0,
        "STOP": False,
        "COOKIES": [],
        "S_DB_FILE": f"{Path.home()}\\Documents\\YPPAHSOFT\\cards.db",
        "APP_DIRECTORY": APP_DIRECTORY,
        "BG_COLOR": "SystemButtonFace",#'#1e1e1e'
        "TXT_COLOR": "black",#'white'
        "NAME": "",
        "VERSION_CD": None
    }
    if not os.path.exists(APP_DIRECTORY):
        os.mkdir(APP_DIRECTORY)
    # with open(SETTINGS_FILE,"wb") as piklefile:
    #     pickle.dump(SETTINGS, piklefile)

# if (SETTINGS["VERSION_CD"] == None or time.time()-SETTINGS["VERSION_CD"]) > 86400:
#     UPDATES_URL="https://github.com/YPPPAH/SteamTradingCards"
#     session = HTMLSession()
#     request = session.get(UPDATES_URL)
#     version = request.html.find("#repo-content-pjax-container", first=True).find(".markdown-title", first=True).text
#     if version != None:
#         if float(version) > VERSION:
#             messagebox.showwarning('', 'There is a newer version of the bot')
#             SETTINGS["VERSION_CD"]=time.time()


class Main():

    ###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
    ##console
    def Clean():
        mylist.delete(0,END)

    def print_console(text):
        mylist.insert(END, text)

    def All():
        Main.Clean()
        ##DB
        mylist.insert(END,"|  id  |  Card Name  |  Price  |  Percent  |  Game  |  Date  |  ")
        connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Cards''')
        select = cursor.fetchall()
        for doc in select:
            mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
        connection.commit()
        connection.close()
        mylist.see("end")

    def Del():
        text = txtInput1.get()
        if text!="":
            ##DB
            connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM Cards WHERE id = {}'''.format(text))
            connection.commit()
            connection.close()
            Main.All()
        else:
            Main.print_and_console("***NOT FOUND***")

    def Sel():
        Main.Clean()
        ##DB
        connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Cards''')
        select = cursor.fetchall()
        for doc in select:
            if Main.compare(txtInput1.get(),doc[4])>0.7:
                mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
        connection.commit()
        connection.close()

    def Quit():
        exit()

    def print_and_console(text):
        print(text)
        
    def compare(dbtext,imtext):
        return SequenceMatcher(None, dbtext, imtext).ratio()

    def Replace(string):
        return string.replace(",",".")

    def Get_inventory_grid(driver,num):
        sleep(0.5)
        Main.print_and_console("SEARCHING FOR GRID...")
        if num == 1:
            if Main.Get_number(driver)%25 == 0 and Main.Get_number(driver)!=0:
                Main.fnd(driver,"//a[@id='pagebtn_next']").click()
                SETTINGS["IPAGE"]+=1
        invetorygrid = driver.find_elements(By.XPATH,"//div[@class='itemHolder']")
        invetorygrid[Main.Get_number(driver)].click()
        Main.print_and_console("GRID FOUND")

    def Get_cookies(driver):
        for cookie in SETTINGS["COOKIES"]:
            driver.add_cookie(cookie)
        return driver

    def Get_number(driver):
        if SETTINGS["GRID"] == 0:
            try:
                gems = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text.split(" ")[1]
                if gems == "Gems" or gems == "Gemas":
                    SETTINGS["GRID"] = 1
                else:
                    SETTINGS["GRID"] = 0
            except IndexError:
                SETTINGS["GRID"] = 0
        return SETTINGS["GRID"]

    def reset_settings():
        SETTINGS["COUNTER"]=0
        SETTINGS["TIME"]=0
        SETTINGS["GRID"]=0
        SETTINGS["IPAGE"]=0
        SETTINGS["PRICE"]=0
     
    def sell_redirect():
        try:
            thread = threading.Thread(target=Main.cromos_sell)
            if not thread.is_alive():
                thread.start()
            else:
                Main.cromos_sell()
        except:
            pass

    def finish_sell(driver,price,name,gamename,inventory_url,Tstart):
        ##SELLING
        Main.Get_inventory_grid(driver,0,inventory_url)
        try:
            Main.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//span[2]").click()##sell btn
        except:
            try:
                Main.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//span[2]").click()##sell btn
            except:
                pass
        sleep(0.5)
        inputtext = Main.fnd(driver,"//input[@id='market_sell_buyercurrency_input']")##price input
        inputtext.send_keys(price)
        sleep(0.5)
        Main.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
        if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You must agree to the terms of the Steam Subscriber Agreement to sell this item.":
            Main.fnd(driver,"//input[@id='market_sell_dialog_accept_ssa']").click()##checkbox
            Main.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
        sleep(0.5)
        Main.fnd(driver,"//a[@id='market_sell_dialog_ok']").click()##btn ok 
        if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You already have a listing for this item pending confirmation. Please confirm or cancel the existing listing.":
            Main.fnd(driver,"//div[@id='market_sell_dialog']//div[@class='newmodal_close']").click()##close modal
            SETTINGS["GRID"]+=1
            Main.print_and_console("CARD ALREADY SOLD")
        else:
            sleep(0.5)
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You have too many listings pending confirmation. Please confirm or cancel some before attempting to list more.":
                SETTINGS["STOP"]=True
                Main.Clean()
                mylist.insert(END,"***************************************************MAX CONFIRMATIONS REACHED***********************************************")
                mylist.insert(END,"*********************************************PLEASE CONFIRM THE CARDS AND RESTART******************************************")
            else:
                sleep(0.5)
                try:
                    driver.find_element(By.XPATH,"//div[@class='newmodal_buttons']//span").click()##2fa x btn 
                except:
                    try:
                        Main.fnd(driver,"//div[@class='newmodal_header']//div").click()
                    except:
                        SETTINGS["GRID"]-=1
                #saving
                SETTINGS["COUNTER"]+=1
                SETTINGS["GRID"]+=1
                SETTINGS["TIME"]+=round((time.time() - Tstart),2)
                SETTINGS["PRICE"]=round(float(SETTINGS["PRICE"])+price,2)
                lblCounter["text"]=SETTINGS["COUNTER"]
                lblTime["text"] = SETTINGS["TIME"]
                lblPrice["text"] = SETTINGS["PRICE"]
                ##DB
                connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
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
                    Main.print_console("| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
                connection.commit()
                cursor.close()
                connection.close()
                mylist.see("end")
                #DB
                Main.print_and_console("SOLD")
                sleep(0.5)

    def info():
        Main.Clean()
        mylist.insert(END,"Sel-> Selects from the db the registres by game name, introduced in the user input")
        mylist.insert(END,"Del-> Deletes from the db the registry with the introduced id")
        mylist.insert(END,"C-> Cleans the Console")
        mylist.insert(END,"All-> Selects all registres from the db")
        mylist.insert(END,"LOGIN-> Input acc to sell cards and input 2FA if enabled")
        mylist.insert(END,"START-> Starts selling")
        mylist.insert(END,"Restart-> Resets all values to start over")
        mylist.insert(END,"Stop-> Stops selling when finishes the actual card")
        mylist.insert(END,"Quit-> Quits the program, please press stop before pressing this to avoid issues")
        mylist.insert(END,"ESTIMATED TIME 30m -> 250 cards (comfirmation cap)")

    def GotoPage(driver,inventory_url):
        driver.get(inventory_url)##load inv
        sleep(1)
        if SETTINGS["IPAGE"] > 0:##scroll
            sleep(0.5)
            for x in range(SETTINGS["IPAGE"]):
                driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                sleep(1)

    def fnd(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
            try:
                res = driver.find_element(By.XPATH,path)
                speed = False
                print("found1 {}".format(path))
            except:
                print("nfound1 {}".format(path))
                count+=1
                sleep(0.1)
        return res

    def fndcn(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
            try:
                res = driver.find_element(By.CLASS_NAME,path)
                speed = False
                print("found2 {}".format(path))
            except:
                print("nfound2 {}".format(path))
        return res

    def fnds(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
            try:
                res = driver.find_elements(By.XPATH,path)
                speed = False
                print("found3 {}".format(path))
            except:
                print("nfound3 {}".format(path))
                pass
        return res

    

    ###-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
    
    def cromos_sell():
        try:
            if not os.path.exists(SETTINGS["S_DB_FILE"]):
                ##DB
                connection = sqlite3.connect(SETTINGS["S_DB_FILE"])
                cursor = connection.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (id INT PRIMARY KEY,Name TEXT, Price FLOAT, Percent INT, Game TEXT, Date TEXT)''')
                connection.commit()
                connection.close()
            Main.Clean()
            lblCounter["text"]=SETTINGS["COUNTER"]
            lblPrice["text"]=SETTINGS["PRICE"]
            lblTime["text"]=SETTINGS["TIME"]
            driver = webdriver.Firefox()
            driver.implicitly_wait(3)
            driver.get("https://steamcommunity.com/")
            driver = Main.Get_cookies(driver)
            driver.execute_script('''window.open("","_blank");''')
            driver.switch_to.window(driver.window_handles[0])
            inventory_url = f"{SETTINGS['ACCID']}/inventory/#753"
            #---start doing sells
            driver.get(URL)
            driver.execute_script('''ChangeLanguage( 'english' );''')
            sleep(1)
            Main.GotoPage(driver,inventory_url)##load inv & scroll
            SETTINGS["STOP"]=False
            card_nameb = None
            name = ["",""]
            res = None
            for x in range(10000):
                if SETTINGS["STOP"]==False:
                    Tstart = time.time()
                    Main.Get_inventory_grid(driver,1,inventory_url)
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
                                name[0] = Main.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        try:
                            if res == 1:
                                name[1] = Main.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//a").get_attribute("href")
                        except:
                            pass
                        if name[0]=="":
                            card_url=name[1]
                        else:
                            card_url=name[0]
                        ##loking for price
                        Main.print_and_console("GETTING CARD PRICE...")
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
                            price = round(float(Main.Replace(price))*PRICE_MULTIPLIER,2)
                            Main.print_and_console("PRICE FOUND")
                            driver.switch_to.window(driver.window_handles[0])
                            Main.finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                        except ValueError:
                            SETTINGS["GRID"]+=1
                    else:
                        card_nameb = card_namea
                        Main.finish_sell(driver, price, card_namea, game_name, inventory_url,Tstart)
                else:
                    driver.quit()
                    Main.print_and_console("***STOPED***")
                    break
        except InvalidSessionIdException:
            Main.print_and_console("BROWSER CONNECTION LOST")
        except Exception as e:
            logging.error(e)
            messagebox.showerror(title="Error", message="Unexpected error")
            exit()
        
class Menus():

    def StartM():###############################################
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title(VERSION)
        win.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def login():
            win.destroy()
            Menus.LoginM()
        
        def cards():
            if SETTINGS["COOKIES"]==[]:
                messagebox.showinfo('', 'You need to login to do this')    
            else:
                win.destroy()
                Menus.CardsM()

        def games():
            if SETTINGS["COOKIES"]==[]:
                messagebox.showinfo('', 'You need to login to do this')
            else:
                win.destroy()
                #FIXME create games gui

        def settings():
            Menus.SettingsM() 

        def logout():
            SETTINGS["COOKIES"]=[]
            win.destroy()
            Menus.StartM()

        cardsb = Button(win, text="Sell Cards", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=cards)
        gamesb = Button(win, text="Buy Games", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=games)
        settingsb = Button(win, text="Settings", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=settings)

        cardsb.place(x=POS_COL1_X+60,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        gamesb.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        settingsb.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        if SETTINGS["COOKIES"]==[]:
            btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=login)
            btn.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        else:
            btnt = Label(win,text='✓ Logged as',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14", "bold"))
            btnt.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
            btnl = Button(win, text=SETTINGS["NAME"], relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=logout)
            btnl.place(x=POS_COL2_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
            # link = Label(win, text="Hyperlink", fg="black", cursor="hand2", bg=SETTINGS["BG_COLOR"])
            # link.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.google.com"))
            # link.place(x=POS_COL2_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def LoginM():##############################################
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title('Login')
        win.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def submit():
            u = usri.get()
            p = pswi.get()
            check_counter=0
            if p == "":
                warn = "Password can't be empty"
            else:
                check_counter += 1
            if u == "":
                warn = "Username can't be empty"
            else:
                check_counter += 1
            if check_counter == 2:
                driver = webdriver.Firefox()
                Main.print_and_console("LOGING...")
                driver.get(URL)
                user = Main.fnd(driver,"//input[@id='input_username']")
                password = Main.fnd(driver,"//input[@id='input_password']")
                user.send_keys(usri.get())
                password.send_keys(pswi.get())
                Main.fndcn(driver,'login_btn').click()
                sleep(3)
                Main.print_and_console("2FA...")
                _2fa = f2ai.get()
                if _2fa!="":
                    try:
                        twofactor = Main.fnd(driver,"//input[@id='twofactorcode_entry']")
                        twofactor.send_keys(_2fa)
                    except:
                        Main.print_and_console("NO 2FA FOUND")
                        pass
                else:
                    Main.print_and_console("NO USER INPUT")
                    pass
                Main.print_and_console("2FA DONE")
                Main.fnds(driver,"//div[@id='login_twofactorauth_buttonset_entercode']//div")[0].click()
                Main.print_and_console("LOGGED")
                SETTINGS["COOKIES"]=driver.get_cookies()
                SETTINGS["ACCID"]=Main.fnds(driver,"//div[@id='global_actions']//a")[-1].get_attribute("href")
                driver.quit()
                win.destroy()
                Menus.StartM()
            else:
                messagebox.showinfo('', warn)

        # labels
        usr = Label(win, text='Username ',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        psw = Label(win, text='Password ',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        f2a = Label(win,text='2fa',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))

        usr.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        psw.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        f2a.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        
        # Entry
        usri = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        pswi = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"], show="*")
        f2ai = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])

        usri.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        pswi.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        f2ai.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        # button 
        btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=submit)
        btn.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()
    
    def SettingsM():################################################
        import tkinter
        from tkinter import ttk
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = tkinter.Tk()
        win.title("Settings")
        win.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-250)}+{int(user32.GetSystemMetrics(1)/2)-250}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        CheckVar = IntVar(value=1)

        def dark_theme():
            if SETTINGS["BG_COLOR"] == "SystemButtonFace":
                SETTINGS["BG_COLOR"] = "#1e1e1e"
            else:
                SETTINGS["BG_COLOR"] = "SystemButtonFace"

            if SETTINGS["TXT_COLOR"] == "black":
                SETTINGS["TXT_COLOR"] = "white"
            else:
                SETTINGS["TXT_COLOR"] = "black"

            # try:
            #     p = psutil.Process(os.getpid())
            #     for handler in p.get_open_files() + p.connections():
            #         os.close(handler.fd)
            # except Exception as e:
            #     logging.error(e)
            # python = sys.executable
            # os.execl(python, python, *sys.argv)

            
        link = Button(win, text="Dark Theme", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=dark_theme)
        link.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def CardsM():#####################################################################
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.wm_title("Sell Cards")
        win.geometry(f"{CARDS_WIDTH}x{CARDS_HEIGTH}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2.5))}+{int(user32.GetSystemMetrics(1)/7)}")
        win.resizable(width=False, height=False)
        ###Title
        lblTitle = Label(win,text="CARDS")
        lblTitle.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Start
        btnStart = Button(win,text="Start", command=Main.sell_redirect)
        btnStart.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Quit
        btnQuit = Button(win,text="Quit", command=Main.Quit)
        btnQuit.place(x=POS_COL6_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Stop
        btnStop = Button(win,text="Stop", command=Main.Stop)
        btnStop.place(x=POS_COL6_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Restart
        btnRestart = Button(win,text="Reset", command=Main.reset_settings)
        btnRestart.place(x=POS_COL6_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###info
        btnRestart = Button(win,text="i", command=Main.info)
        btnRestart.place(x=POS_COL4_X,y=POS_ROW1_Y,width=NORMAL_WIDTH/2-20, height=NORMAL_HEIGTH)
        ###Buttons
        ##line
        lblLine1 = Label(win,text="", borderwidth=2, relief="groove")
        lblLine1.place(x=POS_COL1_X-4,y=POS_ROW2_Y-4,width=NORMAL_WIDTH*2+30, height=NORMAL_HEIGTH+10)
        ##CLS
        btnCls = Button(win,text="C", command=Main.Clean)
        btnCls.place(x=POS_COL1_X,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##ALL
        btnAll = Button(win,text="All", command=Main.All)
        btnAll.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##sel
        btnsel = Button(win,text="Sel", command=Main.Sel)
        btnsel.place(x=POS_COL1_X,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##del
        btndel = Button(win,text="Del", command=Main.Del)
        btndel.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##db input
        global txtInput1
        txtInput1=Entry(win)
        txtInput1.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Console
        ##scroll
        scrollbar = Scrollbar(win)
        global mylist 
        mylist = Listbox(win, yscrollcommand = scrollbar.set )
        mylist.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*7, height=NORMAL_HEIGTH*6)
        Main.info()
        scrollbar.config( command = mylist.yview )
        scrollbar.place(x=POS_COL7_X-POX_X_SPACING,y=POS_ROW4_Y,width=POX_X_SPACING, height=NORMAL_HEIGTH*6)
        ####Counter 
        ###sold
        Label1 = Label(win, text="CARDS DONE")
        Label1.place(x=POS_COL4_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        global lblCounter
        lblCounter = Label(win,text="0", borderwidth=2, relief="groove")
        lblCounter.place(x=POS_COL5_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###price
        Label2 = Label(win, text="CUR. TOTAL PRICE")
        Label2.place(x=POS_COL4_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        global lblPrice
        lblPrice = Label(win,text="0", borderwidth=2, relief="groove")
        lblPrice.place(x=POS_COL5_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##time
        Label3 = Label(win, text="TIME")
        Label3.place(x=POS_COL4_X+50,y=POS_ROW1_Y,width=NORMAL_WIDTH/2, height=NORMAL_HEIGTH)
        global lblTime 
        lblTime = Label(win,text="0", borderwidth=2, relief="groove")
        lblTime.place(x=POS_COL5_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

Menus.StartM()