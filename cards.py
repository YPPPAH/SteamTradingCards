from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from idlelib.tooltip import Hovertip
from difflib import SequenceMatcher
from tkinter import messagebox
from selenium import webdriver
from tkinter import filedialog
from pathlib import Path
from time import sleep
from tkinter import *
import subprocess
import webbrowser
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

## SIZE
NORMAL_WIDTH=100# x
NORMAL_HEIGTH=30# y
## AXIS X
POX_X_SPACING=20
POS_COL1_X=POX_X_SPACING
POS_COL2_X=(POX_X_SPACING*2)+NORMAL_WIDTH
POS_COL3_X=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)
POS_COL4_X=(POX_X_SPACING*4)+(NORMAL_WIDTH*3)
POS_COL5_X=(POX_X_SPACING*5)+(NORMAL_WIDTH*4)
POS_COL6_X=(POX_X_SPACING*6)+(NORMAL_WIDTH*5)
POS_COL7_X=(POX_X_SPACING*7)+(NORMAL_WIDTH*6)
## AXIS Y
POX_Y_SPACING=20
POS_ROW1_Y=POX_Y_SPACING
POS_ROW2_Y=(POX_Y_SPACING*2)+NORMAL_HEIGTH
POS_ROW3_Y=(POX_Y_SPACING*3)+(NORMAL_HEIGTH*2)
POS_ROW4_Y=(POX_Y_SPACING*4)+(NORMAL_HEIGTH*3)
POS_ROW5_Y=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
POS_ROW6_Y=(POX_Y_SPACING*6)+(NORMAL_HEIGTH*5)
POS_ROW7_Y=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
## WINDOWS
CARDS_WIDTH=(POX_X_SPACING*4)+(NORMAL_WIDTH*3)# cardsM
CARDS_HEIGTH=(POX_Y_SPACING*4)+(NORMAL_HEIGTH*3)
LOGIN_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)# loginM
LOGIN_HEIGHT=(POX_Y_SPACING*5)+(NORMAL_HEIGTH*4)
START_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)# startM
START_HEIGHT=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
SETTINGS_HEIGHT=(POX_Y_SPACING*8)+(NORMAL_HEIGTH*7)# settingsM
SETTINGS_WIDTH=int(POX_X_SPACING*3.5)+(NORMAL_WIDTH*3)
GPOP_WIDTH=int(POX_X_SPACING*3.5)+(NORMAL_WIDTH*3)# gamespop
GPOP_HEIGHT=(POX_Y_SPACING*7)+(NORMAL_HEIGTH*6)
GAMES_WIDTH=(POX_X_SPACING*3)+(NORMAL_WIDTH*2)# gamesM
GAMES_HEIGTH=(POX_Y_SPACING*4)+(NORMAL_HEIGTH*3)
## VERSION
VERSION="1.21"
## SETTINGS
SETTINGS_VER=10
class Settings():
    def save():
        with open(SETTINGS_FILE,"wb") as piklefile:
            pickle.dump(SETTINGS, piklefile)
    def GetWindowRectFromName(menu):
        name = SETTINGS["TITLE"]
        hwnd = ctypes.windll.user32.FindWindowW(0, name)
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
        SETTINGS[menu] = (rect.left, rect.top)
        Settings.save()
    def CheckForUpdates():
        if SETTINGS["VERSION_CD"] == None or (time.time()-SETTINGS["VERSION_CD"]) > 86400:
            UPDATES_URL="https://github.com/YPPPAH/SteamTradingCards"
            session = HTMLSession()
            request = session.get(UPDATES_URL)
            try:
                version = request.html.find("#repo-content-pjax-container", first=True).find(".markdown-title", first=True).text
                version = float(str(version).replace("V",""))
                # print(f"{version}>{VERSION}")
                SETTINGS["VERSION_CD"]=time.time()
                Settings.save()
                if version != None:
                    if float(version) > float(VERSION):
                        result = messagebox.askquestion("","There is a newer version of the bot, do you want to download?")
                        if result == 'yes':
                            webbrowser.open_new(UPDATES_URL)
            except Exception as e:
                logging.error(e)
    def DefaultSettings():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        return {
        "ACCID": None,
        "COUNTER": 0,
        "TIME": 0,
        "GRID": None,
        "IPAGE": 0,
        "PRICE": 0,
        "STOP": False,
        "sessionid": [],
        "steamLoginSecure": [],
        "COOKIES_CD": None,
        "LOGED_STATE": DISABLED,
        "DB_FILE": f"{Path.home()}\\Documents\\YPPAHSOFT\\cards.db",
        "APP_DIRECTORY": APP_DIRECTORY,
        "BG_COLOR": "SystemButtonFace",
        "TXT_COLOR": "black",
        "VERSION_CD": None,
        "PRICE_MULTIPLIER": 1.40,
        "START_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100), int(user32.GetSystemMetrics(1)/2)-200),
        "CARDS_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2.5)), int(user32.GetSystemMetrics(1)/7)),
        "SETTINGS_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-250), int(user32.GetSystemMetrics(1)/2)-250),
        "GAMES_POS": (int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2.5)), int(user32.GetSystemMetrics(1)/7)),
        "AUTO_POS": None,
        "TITLE": "CARD FARMER",
        "ICO": "cards.ico",
        "GPOP_FILTER": {
            "MAX_PRICE": None,
            "QUANTITY_ARS": None,
            "QUANTITY_GAM": None,
            "WALLET_QTTY": None,
        },
        "STEAM_DIR": None,
        "WALLET": {
            "AMOUNT": None,
            "LAST_CHECK": None
        },
        "SETTINGS_VER": SETTINGS_VER
    }
    def LoadSettings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE,"rb") as piklefile:
                seting = pickle.load(piklefile)
                if seting["SETTINGS_VER"]<SETTINGS_VER:
                    return Settings.DefaultSettings()
                else:
                    return seting
        else:
            seting = Settings.DefaultSettings()
            if not os.path.exists(APP_DIRECTORY):
                os.mkdir(APP_DIRECTORY)
            return seting
            
APP_DIRECTORY=f"{Path.home()}\\Documents\\YPPAHSOFT\\"
SETTINGS_FILE = f"{Path.home()}\\Documents\\YPPAHSOFT\\settings.pkl"
SETTINGS = Settings.LoadSettings()
Settings.save()    
# Settings.CheckForUpdates()

class Functions():
    def fnd(driver,path):
        speed = True
        count = 0
        while speed:
            if count > 20:
                speed = False
                res = None
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
                res = None
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
                res = None
            try:
                res = driver.find_elements(By.XPATH,path)
                speed = False
                print("found3 {}".format(path))
            except:
                print("nfound3 {}".format(path))
                pass
        return res
    
class Menus():

    def StartM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{START_WIDTH}x{START_HEIGHT}+{SETTINGS['START_POS'][0]}+{SETTINGS['START_POS'][1]}")

        def login():
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.LoginM()
        
        def cards():
            if SETTINGS["sessionid"]==[]:
                messagebox.showinfo('', 'You need to login to do this')    
            else:
                Settings.GetWindowRectFromName('START_POS')
                win.destroy()
                Menus.CardsM()

        def games():
            if SETTINGS["sessionid"]==[]:
                messagebox.showinfo('', 'You need to login to do this')
            else:
                if SETTINGS["GPOP_FILTER"]["MAX_PRICE"] != None:
                    result = messagebox.askquestion("","Do you want to Change buy filters?")
                    if result == 'yes':
                        Settings.GetWindowRectFromName('START_POS')
                        win.destroy()
                        Menus.GamesMPop()
                    else:
                        win.destroy()
                        Menus.GamesM()
                else:
                    Settings.GetWindowRectFromName('START_POS')
                    win.destroy()
                    Menus.GamesMPop()

        def settings():
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.SettingsM() 
            
        def logout():
            SETTINGS["sessionid"]=[]
            SETTINGS["steamLoginSecure"]=[]
            SETTINGS["VERSION_CD"]=None
            SETTINGS["COOKIES_CD"]=None
            SETTINGS["LOGED_STATE"]=DISABLED
            Settings.save()
            Settings.GetWindowRectFromName('START_POS')
            win.destroy()
            Menus.StartM()

        def idle():
            result = messagebox.askquestion("","Do you want to idle Games?")
            if result == 'yes':
                if not process_exists("Steam.exe"):
                    if SETTINGS["STEAM_DIR"] == None:
                        filename = 'C:\Program Files\Steam\steam.exe'
                        while not os.path.exists(filename):
                            messagebox.showinfo('', 'Select your steam exe')
                            filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Executable", "*.exe*"), ("all files", "*.*")))
                        SETTINGS["STEAM_DIR"] = filename
                        subprocess.Popen([SETTINGS['STEAM_DIR']])
                        Settings.save()
                        sleep(10)
                        windowHandle = ctypes.windll.user32.FindWindowW(None, "Steam")
                        ctypes.windll.user32.ShowWindow(windowHandle, 6)
                    subprocess.Popen([f"{os.path.abspath(os.path.dirname(__file__))}/idle_master_extended_v1.7/IdleMasterExtended.exe"])
                else:
                    if not process_exists("Steam.exe"):
                        subprocess.Popen([SETTINGS['STEAM_DIR']])
                        sleep(10)
                        windowHandle = ctypes.windll.user32.FindWindowW(None, "Steam")
                        ctypes.windll.user32.ShowWindow(windowHandle, 6)
                subprocess.Popen([f"{os.path.abspath(os.path.dirname(__file__))}/idle_master_extended_v1.7/IdleMasterExtended.exe"])

        def process_exists(process_name):
            call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split('\r\n')[-1]
            return last_line.lower().startswith(process_name.lower())
        
        def idle_redirect():
            try:
                thread = threading.Thread(target=idle)
                if not thread.is_alive():
                    thread.start()
                else:
                    idle()
            except:
                pass

        def auto():
            pass

        cardsb = Button(win, text="Sell Cards", state=SETTINGS["LOGED_STATE"], relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=cards)
        gamesb = Button(win, text="Buy Games", state=SETTINGS["LOGED_STATE"], relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=games)
        idleb = Button(win, text="Idle Games", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=idle_redirect)
        autob = Button(win, text="Auto", state=DISABLED, relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=auto)
        settingsb = Button(win, text="Settings", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=settings)

        cardsb.place(x=POS_COL1_X+60,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        gamesb.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        idleb.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        autob.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        settingsb.place(x=POS_COL1_X+60,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        if SETTINGS["sessionid"]==[]:
            btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=login)
            btn.place(x=POS_COL1_X+60,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        else:
            btnt = Label(win,text='Logged',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14", "bold"))
            btnt.place(x=POS_COL1_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
            btnl = Button(win, text="Logout?", relief="flat", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=logout)
            btnl.place(x=POS_COL2_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def LoginM():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{int(user32.GetSystemMetrics(0)-(user32.GetSystemMetrics(0)/2)-100)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def loging():
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
                driver.get("https://store.steampowered.com/login/")
                user = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//input[@id='input_username']")))
                user.send_keys(usri.get())
                password = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//input[@id='input_password']")))
                password.send_keys(pswi.get())
                loginbtn = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.CLASS_NAME,'login_btn')))
                loginbtn.click()
                _2fa = f2ai.get()
                if _2fa!="":
                    try:
                        twofactor = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//input[@id='twofactorcode_entry']")))
                        twofactor.send_keys(_2fa)
                    except:
                        print("NO 2FA FOUND")
                else:
                    print("NO USER INPUT")
                    pass
                print("2FA DONE")
                try:
                    WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='login_twofactorauth_buttonset_entercode']//div")))
                    sleep(1)
                    driver.find_elements(By.XPATH,"//div[@id='login_twofactorauth_buttonset_entercode']//div")[0].click()
                except:
                    element = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='error_display]'")))
                    sleep(1)
                    if element.text == "The account name or password that you have entered is incorrect.":
                        driver.quit()
                        messagebox.showinfo('', "Incorrect input, please try again")
                WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH,"//div[@id='global_actions']//a")))
                sleep(1)
                WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='global_actions']//a")))
                try:
                    while driver.find_elements(By.XPATH,"//div[@id='global_actions']//a")[-1].get_attribute("href") == "http://translation.steampowered.com/":
                        sleep(0.5)
                except:
                    driver.quit()
                    messagebox.showinfo('', "Incorrect input, please try again")
                accid = driver.find_elements(By.XPATH,"//div[@id='global_actions']//a")[-1].get_attribute("href")
                if accid == "http://translation.steampowered.com/":
                    messagebox.showwarning("","Error logging, please try again")
                else:
                    SETTINGS["steamLoginSecure"] = driver.get_cookie('steamLoginSecure')
                    SETTINGS["sessionid"] = driver.get_cookie('sessionid')
                    SETTINGS["ACCID"] = accid
                    driver.get(f"{SETTINGS['ACCID']}/inventory/#753")
                    SETTINGS["COOKIES_CD"] = time.time()
                    SETTINGS["LOGED_STATE"]=NORMAL
                    Settings.save()
                    print("Login Successful")
                driver.quit()
                win.destroy()
                Menus.StartM()
            else:
                messagebox.showinfo('', warn)

        def back():
            win.destroy()
            Menus.StartM()

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
        btn = Button(win, text="Login", relief="flat", fg=SETTINGS["TXT_COLOR"], bg=SETTINGS["BG_COLOR"], font=("Times", "14", "bold"), command=loging)
        btn.place(x=POS_COL1_X+60,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)

        win.mainloop()
    
    def SettingsM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}+{SETTINGS['SETTINGS_POS'][0]}+{SETTINGS['SETTINGS_POS'][1]}")

        def dark_theme():
            if SETTINGS["BG_COLOR"] == "SystemButtonFace":
                SETTINGS["BG_COLOR"] = "#1e1e1e"
                lblcolor["text"]="black"
            else:
                SETTINGS["BG_COLOR"] = "SystemButtonFace"
                lblcolor["text"]="white"

            if SETTINGS["TXT_COLOR"] == "black":
                SETTINGS["TXT_COLOR"] = "white"
            else:
                SETTINGS["TXT_COLOR"] = "black"
            Settings.GetWindowRectFromName('SETTINGS_POS')
            win.destroy()
            Menus.SettingsM()

        def savemulti():
            SETTINGS['PRICE_MULTIPLIER'] = float(priceval.get())
            messagebox.showinfo('', 'succesfully updated')
            
        def back():
            Settings.GetWindowRectFromName('SETTINGS_POS')
            win.destroy()
            Menus.StartM()
        
        def clear_cache():
            import shutil
            files = 0
            dirs = ["C:\\Windows\\Temp",f"{Path.home()}\\AppData\\Local\\Temp","C:\\Windows\\Prefetch"]
            for dir in dirs:
                folder = dir
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            files+=1
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            files+=1
                    except Exception as e:
                        print(f'Failed to delete {file_path}.')
            print(f"Deleted {files} files permanently")
            filecount()
            messagebox.showinfo("",f"Deleted {files} files permanently")
        
        def stats():
            pass
            #MARK fer stats

        def gneratepass():
            import pyperclip
            import random
            chars = "!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~"
            pas = ""
            randchars = ""
            for x in range(100000):
                randchars += random.choice(chars)
            for x in range(int(lengthval.get())):
                pas += random.choice(randchars)
            pyperclip.copy(pas)

        def clearclip():
            import pyperclip
            pyperclip.copy("")

        def filecount():
            import shutil
            files = 0
            dirs = ["C:\\Windows\\Temp",f"{Path.home()}\\AppData\\Local\\Temp","C:\\Windows\\Prefetch"]
            for dir in dirs:
                folder = dir
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            files+=1
                        elif os.path.isdir(file_path):
                            files+=1
                    except:
                        pass
            lblfilecount["text"] = f"{files} files"
        
        def process_exists(process_name):
            call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split('\r\n')[-1]
            return last_line.lower().startswith(process_name.lower())

        # def reset():
        #     SETTINGS = Settings.DefaultSettings()
        #     win.destroy()
        #     Menus.SettingsM()

        # def suport():
        #     link_trade = "https://steamcommunity.com/tradeoffer/new/?partner=293476493&token=rxl9LuiU"
        #     if process_exists("Steam.exe"):
        #         webbrowser.open_new(f"steam://openurl/{link_trade}")
        #     else:
        #         webbrowser.open_new(link_trade)
                

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        ##1
        darkbtn = Button(win, text="Dark Theme", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=dark_theme)
        darkbtn.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblLine1 = Label(win,text="-->",bg=SETTINGS["BG_COLOR"], relief="groove", fg=SETTINGS["TXT_COLOR"])
        lblLine1.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblcolor = Label(win,text="",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblcolor.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        if SETTINGS["BG_COLOR"] == "SystemButtonFace":
            lblcolor["text"]="white"
        else:
            lblcolor["text"]="black"
        ##2
        OPTIONS = ["1.0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0"]
        priceval = StringVar(win)
        priceval.set(OPTIONS[4])
        Option = OptionMenu(win, priceval, *OPTIONS)
        Option.configure(bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], cursor="hand2")
        Option.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        backbtn = Button(win, text="Save", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=savemulti)
        backbtn.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblmultiplier = Label(win,text=f"x{SETTINGS['PRICE_MULTIPLIER']}%",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblmultiplier.place(x=POS_COL3_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##3
        lblcache = Label(win,text="Clear tmp folder",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblcache.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        cachebtn = Button(win, text="Clear", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=clear_cache)
        cachebtn.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblfilecount = Label(win,text="",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblfilecount.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        filecount()
        ##4
        clipbtn = Button(win, text="Clear clipboard", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=clearclip)
        clipbtn.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        pasbtn = Button(win, text="Generate pass", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=gneratepass)
        pasbtn.place(x=POS_COL2_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        OPTIONS2 = ["10","15","20","25","30","35","40","45","50"]
        lengthval = StringVar(win)
        lengthval.set(OPTIONS2[4])
        Option = OptionMenu(win, lengthval, *OPTIONS2)
        Option.configure(bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], cursor="hand2")
        Option.place(x=POS_COL3_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ##5
        # suportbtn = Button(win, text="Support", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=gneratepass)
        # suportbtn.place(x=POS_COL2_X,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        # resetbtn = Button(win, text="Reset Settings", fg=SETTINGS["TXT_COLOR"], relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=reset)
        # resetbtn.place(x=POS_COL1_X,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        #

        win.mainloop()

    def Auto():
        pass
    
    def AutoPop():
        pass

    def GamesM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{GAMES_WIDTH}x{GAMES_HEIGTH}+{SETTINGS['GAMES_POS'][0]}+{SETTINGS['GAMES_POS'][1]}")

        def back():
            Settings.GetWindowRectFromName('GAMES_POS')
            win.destroy()
            Menus.StartM()
        
        def Get_cookies(driver):
            driver.add_cookie(SETTINGS["sessionid"])
            driver.add_cookie(SETTINGS["steamLoginSecure"])
            return driver

        def games_redirect():
            try:
                thread = threading.Thread(target=games_buy)
                if not thread.is_alive():
                    thread.start()
                else:
                    games_buy()
            except:
                pass

        def games_buy():
            driver = webdriver.Firefox()
            driver.implicitly_wait(3)
            driver.get("https://store.steampowered.com/")
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"a.global_action_link")))
            sleep(0.5)
            driver.delete_all_cookies()
            driver = Get_cookies(driver)
            driver.execute_script('''ChangeLanguage( 'english' );''')
            print("a")
            sleep(1)
            driver.get("https://store.steampowered.com/")
            sleep(2)
            SETTINGS["STOP"]=False
            if SETTINGS["WALLET"]["LAST_CHECK"] == None or (time.time()-SETTINGS["WALLET"]["LAST_CHECK"]) > 60:
                wallet = driver.find_element(By.XPATH,"//a[@id='header_wallet_balance']").text
                sleep(0.5)
                wallet = float(str(wallet).split(" ")[1].replace(".","").replace(",","."))
                SETTINGS["WALLET"]["AMOUNT"] = wallet
                SETTINGS["WALLET"]["LAST_CHECK"] = time.time()
            driver.get("https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=70&category1=998&category2=29")
            sleep(20)
            gamenum = 0
            games = {}
            totalp = 0.00
            warn = ""
            startbuytime = time.time()
            filters = {"wallet": float(SETTINGS["WALLET"]["AMOUNT"])}
            if SETTINGS["GPOP_FILTER"]["WALLET_QTTY"] != None:
                filters["wallet_lim"] = float(SETTINGS["WALLET"]["AMOUNT"])-float(SETTINGS["GPOP_FILTER"]["WALLET_QTTY"])
            if SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"] != None:
                filters["ars_qtty"] = float(SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"])
            if SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"] != None:
                filters["game_qtty"] = float(SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"])
            rows = driver.find_elements(By.CLASS_NAME,"search_result_row")
            rowschkd = 0
            while warn == "":
                rowsres = 0
                if rowschkd == len(driver.find_elements(By.CLASS_NAME,"search_result_row"))-100:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                    rows = driver.find_elements(By.CLASS_NAME,"search_result_row")
                for row in rows:
                    if rowschkd == len(driver.find_elements(By.CLASS_NAME,"search_result_row"))-100:
                        break
                    rowsres+=1
                    if rowschkd <= rowsres:
                        rowschkd+=1
                        if not 'ds_owned' in row.get_attribute('class').split():
                            gameprice = row.find_elements(By.CLASS_NAME,"search_price")[0].text
                            try:
                                gameprice = float(str(gameprice).split(" ")[2].replace(",","."))
                            except:
                                break
                            gamename = row.find_elements(By.CLASS_NAME,"search_name")[0].text
                            gamelink = row.get_attribute('href')
                            try:
                                session = HTMLSession()
                                request = session.get(gamelink)
                                script = request.html.find(".btn_green_steamui", first=True).attrs['href']
                                if len(script) > 31:
                                    script = request.html.find(".btn_green_steamui")[1].attrs['href']
                            except:
                                script = ""
                            add = False
                            game = {"name": gamename,"price": gameprice, "link":gamelink, "script": script}
                            gamename = ""
                            gameprice = 0.00
                            gamelink = ""
                            script = ""
                            if "wallet_lim" in filters:
                                if filters["wallet_lim"] > totalp:#prior 1
                                    add = True
                                else:
                                    warn = "Wallet limit reached"
                                    break
                            if "ars_qtty" in filters:
                                if filters["ars_qtty"] > game["price"]:#prior 2
                                    add = True
                                else:
                                    warn = "ARS qtty reached"
                                    break
                            if "game_qtty" in filters:
                                if filters["game_qtty"] > gamenum:#prior 3
                                    add = True
                                else:
                                    warn = "GAME qtty reached"
                                    break
                            if float(game["price"]) <= float(SETTINGS["GPOP_FILTER"]["MAX_PRICE"]):
                                if filters["wallet"] > (totalp+game["price"]):
                                    if add:
                                        totalp+=game["price"]
                                        games[gamenum] = game ## save game
                                        # filters["wallet"] -= game["price"]##update wallet
                                        gamenum+=1##next game
                                        lblCounter["text"] = gamenum
                                        if "ars_qtty" in filters:  
                                            filters["ars_qtty"] -= game["price"]## update filter
                                        game = {}
                                        # print(f'{gamenum}/{int(filters["game_qtty"])}')
                                else:
                                    warn = "Not enough founds"
                                    break
                            else:
                                warn = "Price too high"
                                break

            res = messagebox.askquestion("",f'Do u want to buy {gamenum} Games for {round(totalp,2)} Ars,\nREASON: {warn}')
            if res == "yes":
                driver.get("https://store.steampowered.com/cart/")
                sleep(0.5)
                for x in range(gamenum):
                    try:
                        driver.execute_script(games[x]["script"])
                    except:
                        print(f"Error in adding game {x}")
                    sleep(2.5)
                    try:
                        if driver.find_element(By.CLASS_NAME,"cart_status_message").text != "Your item has been added!":
                            print(games[x]["name"])
                            gamenum-=1
                    except:
                        pass
                sleep(1)
                finishbuytime = time.time()
                Label1["text"] = "GAMES BOUGHT"
                lblCounter["text"] = gamenum
                lblTime["text"] = str(int(finishbuytime-startbuytime))+"s"
                driver.find_element(By.XPATH,'//*[@id="btn_purchase_self"]').click()
                sleep(3)
                # if driver.find_element(By.XPATH,'//*[@id="error_display"]').text == "Please confirm your password to continue.":
                #     messagebox.showinfo("","Please log in to finish the buy, then press accept")
                print("done")
            else:
                driver.close()
            # except Exception as e:
            #     logging.error(e)
        
        def changefilter():
            win.destroy()
            Menus.GamesMPop()

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        ##time
        Label3 = Label(win, text="TIME",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label3.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblTime = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblTime.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###sold
        Label1 = Label(win, text="GAMES SELECTED",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label1.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblCounter = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblCounter.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Start
        btnStart = Button(win,text="Start", command=games_redirect,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStart.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###filter
        btnStart = Button(win,text="Change filter", command=changefilter,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStart.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        win.mainloop()

    def GamesMPop():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.geometry(f"{GPOP_WIDTH}x{GPOP_HEIGHT}+{int((user32.GetSystemMetrics(0)/2)+50)}+{int(user32.GetSystemMetrics(1)/2)-200}")
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)

        def back():
            win.destroy()
            Menus.StartM()

        def save():
            if gamepric.get() != "":
                SETTINGS["GPOP_FILTER"]["MAX_PRICE"] = None
                SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"] = None
                SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"] = None
                SETTINGS["GPOP_FILTER"]["WALLET_QTTY"] = None
                if qttars.get() == "" and qttgam.get() == "" and limitwa.get() == "":
                    messagebox.showinfo('', 'You have to enter atleast one filter')
                else:
                    SETTINGS["GPOP_FILTER"]["MAX_PRICE"] = gamepric.get()
                    if qttars.get() != "":
                        SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"] = qttars.get()
                    if qttgam.get() != "":
                        SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"] = qttgam.get()
                    if limitwa.get() != "":
                        SETTINGS["GPOP_FILTER"]["WALLET_QTTY"] = limitwa.get()
                    Settings.save()
                    win.destroy()
                    Menus.GamesM()
            else:
                messagebox.showinfo('', 'Enter max price')

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        gamepricl = Label(win, text='Max price per game (Ars$)',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        qttarsl = Label(win, text='A Quantity of (Ars$)',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        qttgaml = Label(win, text='A Quantity of (Games)', bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        limitwal = Label(win, text='Limiting min wallet (Ars$)', bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))

        gamepricl.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        qttarsl.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        qttgaml.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)
        limitwal.place(x=POS_COL1_X,y=POS_ROW5_Y,width=NORMAL_WIDTH*2, height=NORMAL_HEIGTH)

        buyby = Label(win, text='BUY BY, PRIORITY \/',bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"], font=("Times", "14"))
        buyby.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH*3, height=NORMAL_HEIGTH)

        gamepric = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        qttars = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        qttgam = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        limitwa = Entry(win, fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), bg=SETTINGS["BG_COLOR"])
        if SETTINGS["GPOP_FILTER"]["MAX_PRICE"] != None:
            gamepric.insert(0,SETTINGS["GPOP_FILTER"]["MAX_PRICE"])
        if SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"] != None:
            qttars.insert(0,SETTINGS["GPOP_FILTER"]["QUANTITY_ARS"])
        if SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"] != None:
            qttgam.insert(0,SETTINGS["GPOP_FILTER"]["QUANTITY_GAM"])
        if SETTINGS["GPOP_FILTER"]["WALLET_QTTY"] != None:
            limitwa.insert(0,SETTINGS["GPOP_FILTER"]["WALLET_QTTY"])

        gamepric.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        qttars.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        qttgam.place(x=POS_COL3_X,y=POS_ROW4_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        limitwa.place(x=POS_COL3_X,y=POS_ROW5_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        backbtn = Button(win, text="Continue", fg=SETTINGS["TXT_COLOR"], font=("Times", "14"), relief="groove" , cursor="hand2", bg=SETTINGS["BG_COLOR"], command=save)
        backbtn.place(x=POS_COL2_X,y=POS_ROW6_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)

        win.mainloop()

    def StatsM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{CARDS_WIDTH}x{CARDS_HEIGTH}+{SETTINGS['CARDS_POS'][0]}+{SETTINGS['CARDS_POS'][1]}")

        # cursor.execute('''SELECT * FROM Cards ORDER BY id DESC LIMIT 1''')
        # select = cursor.fetchall()
        # # for doc in select:
        #     # print_console("| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
        # mylist.see("end")

        def compare(dbtext,imtext):
            return SequenceMatcher(None, dbtext, imtext).ratio()

        def Clean():
            mylist.delete(0,END)

        def print_console(text):
            mylist.insert(END, text)

        def All():
            Clean()
            ##DB
            mylist.insert(END,"|  id  |  Card Name  |  Price  |  Percent  |  Game  |  Date  |  ")
            connection = sqlite3.connect(SETTINGS["DB_FILE"])
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
                connection = sqlite3.connect(SETTINGS["DB_FILE"])
                cursor = connection.cursor()
                cursor.execute('''DELETE FROM Cards WHERE id = {}'''.format(text))
                connection.commit()
                connection.close()
                All()
            else:
                print("***NOT FOUND***")

        def info():
            Clean()
            mylist.insert(END,"Sel-> Selects from the db the registres by game name, introduced in the user input")
            mylist.insert(END,"Del-> Deletes from the db the registry with the introduced id")
            mylist.insert(END,"C-> Cleans the Console")
            mylist.insert(END,"All-> Selects all registres from the db")
            mylist.insert(END,"START-> Starts selling")
            mylist.insert(END,"Restart-> Resets all values to start over")
            mylist.insert(END,"Stop-> Stops selling when finishes the actual card")
            mylist.insert(END,"Back-> Quits to the menu, please press stop before pressing this to avoid issues")
            mylist.insert(END,"ESTIMATED TIME 30m -> 250 cards (comfirmation cap)")

        def Sel():
            Clean()
            ##DB
            connection = sqlite3.connect(SETTINGS["DB_FILE"])
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM Cards''')
            select = cursor.fetchall()
            for doc in select:
                if compare(txtInput1.get(),doc[4])>0.7:
                    mylist.insert(END, "| nº{} | {} | ARS${} | {}% | {} | {} |".format(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5]))
            connection.commit()
            connection.close()

        ###info
        btnRestart = Button(win,text="i", command=info,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnRestart.place(x=POS_COL1_X,y=POS_ROW1_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ###Buttons
        ##line
        lblLine1 = Label(win,text="", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblLine1.place(x=POS_COL1_X-4,y=POS_ROW2_Y-4,width=NORMAL_WIDTH*2+30, height=NORMAL_HEIGTH+10)
        ##CLS
        btnCls = Button(win,text="C", command=Clean,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnCls.place(x=POS_COL1_X,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##ALL
        btnAll = Button(win,text="All", command=All,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnAll.place(x=POS_COL1_X+60,y=POS_ROW3_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##sel
        btnsel = Button(win,text="Sel", command=Sel,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnsel.place(x=POS_COL1_X,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##del
        btndel = Button(win,text="Del", command=Del,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btndel.place(x=POS_COL1_X+60,y=POS_ROW2_Y,width=(NORMAL_WIDTH-20)/2, height=NORMAL_HEIGTH)
        ##db input
        txtInput1=Entry(win,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        txtInput1.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###Console
        ##scroll
        scrollbar = Scrollbar(win,bg=SETTINGS["BG_COLOR"])
        mylist = Listbox(win, yscrollcommand = scrollbar.set ,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        mylist.place(x=POS_COL1_X,y=POS_ROW4_Y,width=NORMAL_WIDTH*7, height=NORMAL_HEIGTH*6)
        info()
        scrollbar.config( command = mylist.yview )
        scrollbar.place(x=POS_COL7_X-POX_X_SPACING,y=POS_ROW4_Y,width=POX_X_SPACING, height=NORMAL_HEIGTH*6)

    def CardsM():
        win = Tk()
        win.title(SETTINGS['TITLE'])
        win.iconbitmap(SETTINGS['ICO'])
        win.config(bg=SETTINGS["BG_COLOR"])
        win.resizable(width=False, height=False)
        win.geometry(f"{CARDS_WIDTH}x{CARDS_HEIGTH}+{SETTINGS['CARDS_POS'][0]}+{SETTINGS['CARDS_POS'][1]}")

        def stop():
            SETTINGS["STOP"]=True

        def back():
            Settings.GetWindowRectFromName('CARDS_POS')
            win.destroy()
            Menus.StartM()
        
        def sell_redirect():
            try:
                thread = threading.Thread(target=cromos_sell)
                if not thread.is_alive():
                    thread.start()
                else:
                    cromos_sell()
            except:
                pass

        def Replace(string):
            return string.replace(",",".")

        def Get_cookies(driver):
            driver.add_cookie(SETTINGS["sessionid"])
            driver.add_cookie(SETTINGS["steamLoginSecure"])
            return driver

        def reset_settings():
            SETTINGS["COUNTER"]=0
            SETTINGS["TIME"]=0
            SETTINGS["GRID"]=0
            SETTINGS["IPAGE"]=0
            SETTINGS["PRICE"]=0

        def GotoPage(driver):
            driver.get(f"{SETTINGS['ACCID']}/inventory/#753")##load inv
            sleep(1)
            if SETTINGS["IPAGE"] > 0:##scroll
                sleep(0.5)
                for x in range(SETTINGS["IPAGE"]):
                    driver.find_element(By.XPATH,"//a[@id='pagebtn_next']").click()
                    sleep(1)

        def cromos_sell():
            try:
                if not os.path.exists(SETTINGS["DB_FILE"]):
                    ##DB
                    connection = sqlite3.connect(SETTINGS["DB_FILE"])
                    cursor = connection.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (id INT PRIMARY KEY,Name TEXT, Price FLOAT, Percent INT, Game TEXT, Date TEXT)''')
                    connection.commit()
                    connection.close()
                lblCounter["text"]=SETTINGS["COUNTER"]
                lblPrice["text"]=SETTINGS["PRICE"]
                lblTime["text"]=SETTINGS["TIME"]
                print("x")
                driver = webdriver.Firefox()
                print("x")
                driver.implicitly_wait(3)
                driver.get("https://steamcommunity.com/")
                WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.CSS_SELECTOR,".responsive_page_content")))
                sleep(1)
                driver = Get_cookies(driver)
                driver.execute_script('''window.open("","_blank");''')
                driver.switch_to.window(driver.window_handles[0])
                sleep(1)
                driver.execute_script('''ChangeLanguage( 'english' );''')
                sleep(1)
                GotoPage(driver)##load inv & scroll
                SETTINGS["STOP"]=False
                card_nameb = None
                name = ["",""]
                res = None
                for x in range(10000):
                    if SETTINGS["STOP"]==False:
                        Tstart = time.time()
                        Get_inventory_grid(driver,1)
                        name = ["",""]
                        gname = ["",""]
                        try:##find card name
                            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//h1[@id='iteminfo0_item_name']")))
                            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='iteminfo0_game_info']//div[3]")))

                            name[0] = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//h1[@id='iteminfo0_item_name']"))).text
                            gname[0] = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='iteminfo0_game_info']//div[3]"))).text
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
                                    name[0] = Functions.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//a").get_attribute("href")
                            except:
                                pass
                            try:
                                if res == 1:
                                    name[1] = Functions.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//a").get_attribute("href")
                            except:
                                pass
                            if name[0]=="":
                                card_url=name[1]
                            else:
                                card_url=name[0]
                            ##loking for price
                            print("GETTING CARD PRICE...")
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
                                price = round(float(Replace(price))*SETTINGS["PRICE_MULTIPLIER"],2)
                                print("PRICE FOUND")
                                driver.switch_to.window(driver.window_handles[0])
                                finish_sell(driver, price, card_namea, game_name,Tstart)
                            except ValueError:
                                SETTINGS["GRID"]+=1
                        else:
                            card_nameb = card_namea
                            finish_sell(driver, price, card_namea, game_name,Tstart)
                    else:
                        driver.quit()
                        print("***STOPED***")
                        break
            except InvalidSessionIdException:
                print("BROWSER CONNECTION LOST")
            except Exception as e:
                logging.error(e)

                messagebox.showerror(title="Error", message="Unexpected error")

        def Get_inventory_grid(driver,num):
            sleep(0.5)
            if num == 1:
                if Get_number(driver)%25 == 0 and Get_number(driver)!=0:
                    Functions.fnd(driver,"//a[@id='pagebtn_next']").click()
                    SETTINGS["IPAGE"]+=1
            element = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@class='itemHolder']")))
            invetorygrid = driver.find_elements(By.XPATH,"//div[@class='itemHolder']")
            invetorygrid[Get_number(driver)].click()
        
        def Get_number(driver):
            if SETTINGS["GRID"] == None:
                try:
                    element = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@class='itemHolder']")))
                    '//*[@id="iteminfo0_item_type"]'
                    '//*[@id="iteminfo1_item_type"]'
                    # gems = driver.find_element(By.XPATH,"//h1[@id='iteminfo1_item_name']").text.split(" ")[1]
                    # if gems == "Gems" or gems == "Gemas":
                    #     SETTINGS["GRID"] = 1
                    # else:
                    #     SETTINGS["GRID"] = 0
                except :
                    SETTINGS["GRID"] = 0
            return SETTINGS["GRID"]
        
        def finish_sell(driver,price,name,gamename,Tstart):
            ##SELLING
            Get_inventory_grid(driver,0)
            try:
                Functions.fnd(driver,"//div[@id='iteminfo0_item_market_actions']//span[2]").click()##sell btn
            except:
                try:
                    Functions.fnd(driver,"//div[@id='iteminfo1_item_market_actions']//span[2]").click()##sell btn
                except:
                    pass
            sleep(0.5)
            inputtext = Functions.fnd(driver,"//input[@id='market_sell_buyercurrency_input']")##price input
            inputtext.send_keys(price)
            sleep(0.5)
            Functions.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You must agree to the terms of the Steam Subscriber Agreement to sell this item.":
                Functions.fnd(driver,"//input[@id='market_sell_dialog_accept_ssa']").click()##checkbox
                Functions.fnd(driver,"//a[@id='market_sell_dialog_accept']").click()##btn put for sale 
            # sleep(0.5)
            btnok = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//a[@id='market_sell_dialog_ok']")))
            btnok.click()
            # Functions.fnd(driver,"//a[@id='market_sell_dialog_ok']").click()##btn ok 
            if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You already have a listing for this item pending confirmation. Please confirm or cancel the existing listing.":
                Functions.fnd(driver,"//div[@id='market_sell_dialog']//div[@class='newmodal_close']").click()##close modal
                SETTINGS["GRID"]+=1
                print("CARD ALREADY SOLD")
            else:
                sleep(0.5)
                if driver.find_element(By.XPATH,("//div[@id='market_sell_dialog_error']")).text == "You have too many listings pending confirmation. Please confirm or cancel some before attempting to list more.":
                    SETTINGS["STOP"]=True
                    print("***************************************************MAX CONFIRMATIONS REACHED***********************************************")
                    print("*********************************************PLEASE CONFIRM THE CARDS AND RESTART******************************************")
                else:
                    try:
                        element = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH,"//div[@class='newmodal_buttons']//span")))##2fa x btn 
                        element.click()
                    except:
                        try:
                            Functions.fnd(driver,"//div[@class='newmodal_header']//div").click()
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
                    connection = sqlite3.connect(SETTINGS["DB_FILE"])
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
                    cursor.execute('''INSERT INTO Cards (id, Name, Price, Percent, Game, Date) VALUES ({},"{}", {}, {}, "{}","{}")'''.format(number, name, price, str(SETTINGS["PRICE_MULTIPLIER"]).split(".")[1]+"0",gamename,date))

                    connection.commit()
                    cursor.close()
                    connection.close()
                    #DB
                    print("SOLD")

        Backbt = Button(win, text="<", fg=SETTINGS["TXT_COLOR"], cursor="hand2", bg=SETTINGS["BG_COLOR"], command=back)
        Backbt.place(x=0,y=0,width=POX_X_SPACING, height=POX_Y_SPACING)
        ###Start
        btnStart = Button(win,text="Start", command=sell_redirect,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStart.place(x=POS_COL3_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        Hovertip(btnStart,'Start selling cards',500)
        ###Stop
        btnStop = Button(win,text="Stop", command=stop,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnStop.place(x=POS_COL3_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        Hovertip(btnStop,'Stops selling cards',500)
        ###Restart
        btnRestart = Button(win,text="Reset cur.", command=reset_settings,bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        btnRestart.place(x=POS_COL3_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        Hovertip(btnRestart,'Resets current inventory position and sesion stats',500)
        ####Counter 
        ##time
        Label3 = Label(win, text="CUR. TIME",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label3.place(x=POS_COL1_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblTime = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblTime.place(x=POS_COL2_X,y=POS_ROW1_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###price
        Label2 = Label(win, text="CUR. PRICE",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label2.place(x=POS_COL1_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblPrice = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblPrice.place(x=POS_COL2_X,y=POS_ROW2_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        ###sold
        Label1 = Label(win, text="CURR. CARDS",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        Label1.place(x=POS_COL1_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        lblCounter = Label(win,text="0", borderwidth=2, relief="groove",bg=SETTINGS["BG_COLOR"], fg=SETTINGS["TXT_COLOR"])
        lblCounter.place(x=POS_COL2_X,y=POS_ROW3_Y,width=NORMAL_WIDTH, height=NORMAL_HEIGTH)
        win.mainloop()

Menus.StartM()