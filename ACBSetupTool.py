import os
from os import path
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.filedialog import askdirectory
import subprocess
import csv

import webbrowser
import gettext
_ = gettext.gettext

version = 1.0 # Map functionality complete

savefile = 'settings.ini'
ACBSetupTool = "ACBSetupTool.py"
userStruct = ('Language', 'GamePath')
defaultValues = ('en,notdefined')

default1 = "C:/Program Files (x86)/Steam/steamapps/common/Assassins Creed Brotherhood"              #default Steam directory
default2 = "C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games/Assassins Creed Brotherhood" #default UbisoftConnect/Uplay directory			

defaultpathExist = path.exists(default1+"/ACBSP.exe")
default2pathExist = path.exists(default2+"/ACBSP.exe")

#links
ANwebsite = 'https://assassins.network'
ANrulebook = 'https://rulebook.assassins.network/'

languages = [("English", "en"),
   	     	("German", "de"),
    	    ("French", "fr"),
            ("Portuguese", "pt")]

global maps
maps = {
		"Alhambra": "DataPC_AC2MP_Alhambra_dlc.forge",
		"Florence": "DataPC_AC2MP_Firenze.forge",
		"Forli": "DataPC_AC2MP_Forli.forge",
		"Mont St-Michel": "DataPC_AC2MP_MtStMichel_dlc.forge",
		"Castel Gandolfo": "DataPC_AC2MP_Palazzio.forge",
		"Pienza": "DataPC_AC2MP_Pienza_dlc.forge",
		"San Donato": "DataPC_AC2MP_SanDonato.forge",
		"Venice": "DataPC_AC2MP_SanMarco.forge",
		"Siena": "DataPC_AC2MP_Siena.forge",
		"Monteriggioni": "DataPC_AC2MP_Villa.forge",
		"Rome": "DataPC_ACR_Rome_Multi.forge"
		}

def checkDefaultPath():

	if defaultpathExist:
		pathExist = True
		gamePath = default1

	elif default2pathExist:
		pathExist = True
		gamePath = default2	

	else:
		pathExist = False
		gamePath = ""
		print("Can't find default directory")
		
	return pathExist, gamePath

def readUserData():
	if path.exists(savefile):
		with open(savefile, 'r') as file:

			reader = csv.DictReader(file, fieldnames=userStruct)
			userData = dict()

			for row in reader:
				userData = row
			print(savefile + " file found.")
			return userData
	else:
		print(savefile + " file not found.")
		return newUser()

def newUser():
	with open(savefile, 'w') as file:

		file.write(defaultValues)
		print(savefile + " successfully created!")

	return readUserData()

def writeUserData(data):
	with open(savefile, 'w') as file:

		writer = csv.DictWriter(file, fieldnames=userStruct)
		writer.writerow(data)
		print("Data saved!")

def getLocalization():

	try:
		lang = gettext.translation('base', localedir='locales', languages=[getLang])
		lang.install()

	except:
			print("Could not retrieve user language. Defaulting to English. Check your " + savefile + " file.")
			lang = gettext.translation('base', localedir='locales', languages=["en"])
			lang.install()

	return lang.gettext

##########################################################tool start

def openLangMenu():

	langMenu = tk.Toplevel(root)
	langMenu.title("Interface Language")
	langMenu.geometry("300x180+525+300")
	langMenu.iconphoto(False, logo)
	langMenu.config(bg="#89b0b3")
	langMenu.resizable(False, False)
	langLabel = tk.Label(langMenu, bg="#89b0b3", pady=5, text=_("Choose a language\n")).pack()

	for language, val in languages:

    		ttk.Radiobutton(langMenu, 
        	text=language,
        	style="lang.TRadiobutton", 
            variable=v,
            value=val).pack(side="top", fill=tk.X, padx=100)

	langButton = tk.Button(langMenu, text="Apply changes", bd=2, relief="raised", command=lambda: applyLang()).pack(side=tk.BOTTOM, pady=5)

	def applyLang():

		langMenu.destroy()
		newLang = v.get()

		if newLang != userData["Language"]:

			userData["Language"] = newLang
			writeUserData(userData)
			os.startfile(ACBSetupTool)
			root.destroy()

def choosePath(): ########################## Manually sets the directory

	ACBpath = askdirectory(title="Select your Assassin's Creed Brotherhood installation folder")

	if path.exists(str(ACBpath)+"/ACBSP.exe") == False:

		messagebox.showerror("Path Error", "Wrong directory!\nCan't find \"ACBSP.exe\" in selected folder.")
	else:

		userData["GamePath"] = ACBpath
		writeUserData(userData)
		os.startfile(ACBSetupTool)
		root.destroy()

def checkPathandStatus(): ######### Automatically searches for directory path and map status

	global gamePath

	if path.exists(userData["GamePath"]+"/ACBSP.exe"):

		gamePath = userData["GamePath"]
		dirPath.set(gamePath)
		acbFolder.config(state="disabled", text="Directory Set!")
		print("User set directory")

	elif pathExist:

		dirPath.set(gamePath)
		acbFolder.config(state="disabled", text="Directory Set!")
		print("Default directory found!")

	else:

		messagebox.showinfo("No Directory Located", "No directory has been detected.\n\nClick on \"Set Directory\" and" +
					" manually select your folder containing \"ACBSP.exe\".")
		gamePath = ""
		print("Directory not yet set")
		applyChanges["state"] = tk.DISABLED
		startGame["state"] = tk.DISABLED

#################### Checks status of each map

	global mapStatus
	mapStatus = dict()
	for mapName, mapFile in maps.items():

		value = path.exists(gamePath+"/multi/" + mapFile)

		if value == True:
			mapStatus[mapName] = True
		else:
			mapStatus[mapName] = False

##############################################

def switchState(mapName):   ################################################ Switches button state

	global mapStatus
	if mapName == "Alhambra":
		if mapStatus[mapName] == True:
			buttonAlhambra.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonAlhambra.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Florence":
		if mapStatus[mapName] == True:
			buttonFlorence.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonFlorence.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Forli":
		if mapStatus[mapName] == True:
			buttonForli.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonForli.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Mont St-Michel":
		if mapStatus[mapName] == True:
			buttonMSM.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonMSM.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Castel Gandolfo":
		if mapStatus[mapName] == True:
			buttonCastel.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonCastel.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Pienza":
		if mapStatus[mapName] == True:
			buttonPienza.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonPienza.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "San Donato":
		if mapStatus[mapName] == True:
			buttonSanDon.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonSanDon.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Venice":
		if mapStatus[mapName] == True:
			buttonVenice.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonVenice.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Siena":
		if mapStatus[mapName] == True:
			buttonSiena.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonSiena.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Monteriggioni":
		if mapStatus[mapName] == True:
			buttonMonteriggioni.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonMonteriggioni.config(image=onIMG)
			mapStatus[mapName] = True

	if mapName == "Rome":
		if mapStatus[mapName] == True:
			buttonRome.config(image=offIMG)
			mapStatus[mapName] = False
		elif mapStatus[mapName] == False:
			buttonRome.config(image=onIMG)
			mapStatus[mapName] = True

	changesFound = 0
	for place, local in maps.items():

		value = path.exists(gamePath+"/multi/" + local)

		if value != mapStatus[place]:
			changesFound+=1

	if changesFound != 0:

		unsavedChanges.set("You have unsaved changes.")
		changeLabel.config(foreground="red")

	else: unsavedChanges.set("")

	if gamePath == "":
		unsavedChanges.set("No directory has been set.")

def applyMapChanges():  ##### Applies the map changes by checking the difference between
						##### the map's existance and the local variable with the user set status
	changesMade = 0
	for place, local in maps.items():

		value = path.exists(gamePath+"/multi/" + local)

		if value != mapStatus[place] and value == True:

			print("Map turned off: ", place)
			os.rename(gamePath+"/multi/"+local,gamePath+"/multi/"+local+".OFF")
			changesMade+=1

		if value != mapStatus[place] and value == False:

			print("Map turned on: ", place)
			os.rename(gamePath+"/multi/"+local+".OFF",gamePath+"/multi/"+local)
			changesMade+=1
	
	if changesMade != 0:

		unsavedChanges.set("Saved! Ready to play.")
		changeLabel.config(foreground="green")

def launchGame(gamePath):  ##### Launches the game
	
	info = tk.Toplevel(root)
	info.geometry("250x100+300+300")
	info.title("Login Info")
	info.iconphoto(False, logo)
	info.resizable(False, False)
	info.grid_columnconfigure(0, weight=1)
	info.grid_columnconfigure(3, weight=1)
	info.grid_rowconfigure(0, weight=1)
	info.grid_rowconfigure(4, weight=1)

	labelUser = tk.Label(info, text="Username: ").grid(row=1, column=1)
	userUser = tk.Entry(info)
	userUser.grid(row=1, column=2)
	labelPass = tk.Label(info, text="Password: ").grid(row=2, column=1, pady=(3,0))
	userPass = tk.Entry(info, show="•")
	userPass.grid(row=2, column=2, pady=(3,0))

	playButton = tk.Button(info, text="Play", command=lambda: login()).grid(row=3, column=1, columnspan=2, pady=(10,0))

	def login():
	
		try:
			user = userUser.get()
			password = userPass.get()
			info.destroy()
			startGame.config(state="disabled", text="Game running")
			root.iconify()
			subprocess.run([gamePath + "/ACBMP.exe", "/launchedfromotherexec", "/onlineUser:"+user, "/onlinePassword:"+password])
			root.deiconify()
			startGame.config(state="active", text="Launch Multiplayer")

		except:
			messagebox.showerror("Error Launching Game!", "Game not found.\n\nCheck your directory path.")
			root.deiconify()
			startGame.config(state="active", text="Launch Multiplayer")


pathExist, gamePath = checkDefaultPath() ### Checks if the default game path exists and returns it
print(pathExist, gamePath)

userData = readUserData()				### Returns user info
getLang = userData["Language"]			### Reads user language

try:
	_ = getLocalization()   			### Retrieves localization files
except:
	print("Could not find localization files. Check your locales folders.")

root = tk.Tk()
root.title(_("Assassin's Creed: Brotherhood Setup Manager Tool"))
root.minsize(height=0, width=150)
root.resizable(True, False)

try:
	logo = tk.PhotoImage(file = "images/icon.png")
	sidepanel = tk.PhotoImage(file = "images/sidepanel.png")
	onIMG = tk.PhotoImage(file = "images/OnSwitch.png")
	offIMG = tk.PhotoImage(file = "images/OffSwitch.png")
	engihelle = tk.PhotoImage(file = "images/engihelle.png")
	fazz = tk.PhotoImage(file = "images/blacksmith.png")
	verify = tk.PhotoImage(file = "images/verify.png")
	jigaudi = tk.PhotoImage(file = "images/jigaudi.png")
	courty = tk.PhotoImage(file = "images/courty.png")
	fouadIMG = tk.PhotoImage(file = "images/fouad.png")
	selectMaps = tk.PhotoImage(file = "images/selectmaps.png")
	tabHome = tk.PhotoImage(file = "images/tabHome.png")
	tabMap = tk.PhotoImage(file = "images/tabMap.png")
	tabBoot = tk.PhotoImage(file = "images/tabBoot.png")
	tabSettings = tk.PhotoImage(file = "images/tabSettings.png")
	tabAcc = tk.PhotoImage(file = "images/tabAcc.png")
	launchMP = tk.PhotoImage(file = "images/launchMP.png")
	applyChangesIMG = tk.PhotoImage(file = "images/applyChanges.png")
	root.iconphoto(False, logo)

except:
	print("Critical error! Image files are missing. Please redownload the tool.")

#window frames

v = tk.StringVar()
v.set(getLang)
dirPath = tk.StringVar()
unsavedChanges = tk.StringVar()

mapFonts = "FixedSys"
mapBG = "#89b0b3" ##89b0b3 38393F

b = ttk.Style()
b.configure("lang.TRadiobutton", padx=50, font="Helvetica, 9", background="#89b0b3")

sidePanel = tk.Label(root, borderwidth=2, relief="groove", image=sidepanel, bg="#89b0b3")
sidePanel.pack(side="left", fill="y", anchor="w")

myNotebook = ttk.Notebook(root, takefocus=False) 
myNotebook.pack(fill="both", expand=1)

frame1 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove")

frame2 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove") 
frame2.pack(fill="both", expand=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(7, weight=1)

frame3 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove")
frame3.pack(fill="both", expand=1)
frame4 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove")

tabPadding = 5
myNotebook.add(frame1, text="   Home   ", image=tabHome, padding=tabPadding, state="disabled")
myNotebook.add(frame2, text="   Map Selection   ", image=tabMap, padding=tabPadding)
myNotebook.add(frame3, text="   Settings   ", image=tabSettings, padding=tabPadding)
myNotebook.add(frame4, text="   Account Management   ", image=tabAcc, padding=tabPadding)

######################################################################## Images on Frame2
verIMG = tk.Label(frame2, bg=mapBG, image=verify)
verIMG.grid(row=0,column=1, columnspan=2, padx=(10,0))
fazzChar = tk.Label(frame2, bg=mapBG, image=fazz)
fazzChar.grid(row=0, column=4, padx=(0,125))
fouad = tk.Label(frame2, bg=mapBG, image=fouadIMG)
fouad.grid(row=1, column=5)
courtyChar = tk.Label(frame2, bg=mapBG, image=courty)
courtyChar.grid(row=1, column=1)
selectIMG = tk.Label(frame2, image=selectMaps, bg=mapBG)
selectIMG.grid(row=3, rowspan=2, column=5, padx=(0,10), pady=(0,25))
dripdell = tk.Label(frame2, image=engihelle, bg=mapBG)
dripdell.grid(row=4, rowspan=2,column=1, padx=5)
jigaudiChar = tk.Label(frame2, image=jigaudi, bg=mapBG)
jigaudiChar.grid(row=5, column=5, columnspan=1, padx=(0,10))
#######################################################################

acbFolder = tk.Button(frame2, text="Set Game Directory Path", bg="#38393F", font=mapFonts, command=lambda: choosePath())
acbFolder.grid(row=0, column=3, ipadx=20)

pathLabel = tk.Entry(frame2, textvariable=dirPath, bg="#38393F", font=mapFonts, borderwidth=3, justify="center", relief="sunken", state="readonly", takefocus=False)
pathLabel.grid(row=1, column=2, columnspan=3,ipadx=200)

######################################### Frame for the maps and their switches

mapFrame = tk.Frame(frame2 ,borderwidth=1, bg=mapBG, relief="sunken")
mapFrame.grid(row=2, rowspan=3, column=2, columnspan=3)

#SanDon
labelSanDon = tk.Label(mapFrame, text="San Donato", font=mapFonts, bg=mapBG)
labelSanDon.grid(row=0, column=0, padx=(25,0))
buttonSanDon = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("San Donato"))
buttonSanDon.grid(row=0, column=1)


#Castel
labelCastel = tk.Label(mapFrame, text="Castel Gandolfo", font=mapFonts, bg=mapBG)
labelCastel.grid(row=1, column=0, pady=(5,0), padx=(25,0))
buttonCastel = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Castel Gandolfo"))
buttonCastel.grid(row=1, column=1, pady=(5,0))

#MSM
labelMSM = tk.Label(mapFrame, text="Mont St-Michel", font=mapFonts, bg=mapBG)
labelMSM.grid(row=2, column=0, pady=(5,0), padx=(25,0))
buttonMSM = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Mont St-Michel"))
buttonMSM.grid(row=2, column=1, pady=(5,0))


#Monti
labelMonteriggioni = tk.Label(mapFrame, text="Monteriggioni", font=mapFonts, bg=mapBG)
labelMonteriggioni.grid(row=3, column=0, pady=(5,0), padx=(25,0))
buttonMonteriggioni = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Monteriggioni"))
buttonMonteriggioni.grid(row=3, column=1, pady=(5,0))


#Alhambra
labelAlhambra = tk.Label(mapFrame, text="Alhambra", font=mapFonts, bg=mapBG)
labelAlhambra.grid(row=0, column=2, padx=(25,0))
buttonAlhambra = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Alhambra"))
buttonAlhambra.grid(row=0, column=3)

#Florence
labelFlorence = tk.Label(mapFrame, text="Florence", font=mapFonts, bg=mapBG)
labelFlorence.grid(row=1, column=2, pady=(5,0), padx=(25,0))
buttonFlorence = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Florence"))
buttonFlorence.grid(row=1, column=3, pady=(5,0))

#Pienza
labelPienza = tk.Label(mapFrame, text="Pienza", font=mapFonts, bg=mapBG)
labelPienza.grid(row=2, column=2, pady=(5,0), padx=(25,0))
buttonPienza = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Pienza"))
buttonPienza.grid(row=2, column=3, pady=(5,0))

#Venice
labelVenice = tk.Label(mapFrame, text="Venice", font=mapFonts, bg=mapBG)
labelVenice.grid(row=3, column=2, padx=(25,0))
buttonVenice = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Venice"))
buttonVenice.grid(row=3, column=3, pady=(5,0))


#Forli
labelForli = tk.Label(mapFrame, text="Forli", font=mapFonts, bg=mapBG)
labelForli.grid(row=0, column=4, padx=(25,0))
buttonForli = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Forli"))
buttonForli.grid(row=0, column=5, padx=(0,30))

#Siena
labelSiena = tk.Label(mapFrame, text="Siena", font=mapFonts, bg=mapBG)
labelSiena.grid(row=1, column=4, pady=(5,0), padx=(25,0))
buttonSiena = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Siena"))
buttonSiena.grid(row=1, column=5, pady=(5,0), padx=(0,30))


#Rome
labelRome = tk.Label(mapFrame, text="Rome", font=mapFonts, bg=mapBG)
labelRome.grid(row=2, column=4, pady=(5,0), padx=(25,0))
buttonRome = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Rome"))
buttonRome.grid(row=2, column=5, pady=(5,0), padx=(0,30))


changeLabel = tk.Label(frame2, textvariable=unsavedChanges, bg=mapBG, font="Arial, 8 italic", foreground="red")
changeLabel.grid(row=5, column=2)

applyChanges = tk.Button(frame2, text="Apply Changes", bg=mapBG, activebackground=mapBG, bd=0, font=mapFonts, image=applyChangesIMG, command=lambda: applyMapChanges())
applyChanges.grid(row=5, column=4)

startGame = tk.Button(frame2, text="Launch Multiplayer", bg=mapBG, activebackground=mapBG, bd=0, font=mapFonts, image=launchMP, command=lambda: launchGame(gamePath))
startGame.grid(row=5, column=3)

checkPathandStatus()
print("Game path is: ", gamePath)

############################################################################### Sets map status on tool start

if mapStatus["Alhambra"] == True: buttonAlhambra.config(image=onIMG)
else: buttonAlhambra.config(image=offIMG)

if mapStatus["Florence"] == True: buttonFlorence.config(image=onIMG)
else: buttonFlorence.config(image=offIMG)

if mapStatus["Forli"] == True: buttonForli.config(image=onIMG)
else: buttonForli.config(image=offIMG)

if mapStatus["Pienza"] == True: buttonPienza.config(image=onIMG)
else: buttonPienza.config(image=offIMG)

if mapStatus["Siena"] == True: buttonSiena.config(image=onIMG)
else: buttonSiena.config(image=offIMG)

if mapStatus["Castel Gandolfo"] == True: buttonCastel.config(image=onIMG)
else: buttonCastel.config(image=offIMG)

if mapStatus["Venice"] == True: buttonVenice.config(image=onIMG)
else: buttonVenice.config(image=offIMG)

if mapStatus["Monteriggioni"] == True: buttonMonteriggioni.config(image=onIMG)
else: buttonMonteriggioni.config(image=offIMG)

if mapStatus["Rome"] == True: buttonRome.config(image=onIMG)
else: buttonRome.config(image=offIMG)

if mapStatus["San Donato"] == True: buttonSanDon.config(image=onIMG)
else: buttonSanDon.config(image=offIMG)

if mapStatus["Mont St-Michel"] == True: buttonMSM.config(image=onIMG)
else: buttonMSM.config(image=offIMG)

#menus
bar_menu = tk.Menu(root)
filemenu = tk.Menu(bar_menu, tearoff=0)
settingsmenu = tk.Menu(bar_menu, tearoff=0)
anmenu = tk.Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(menu=filemenu, label="File")
bar_menu.add_cascade(menu=settingsmenu, label="Settings")
bar_menu.add_cascade(menu=anmenu, label="Assassins' Network")

#file menu
filemenu.add_command(label="Placeholder")
filemenu.add_separator()
filemenu.add_command(label="Close", command=root.destroy)

#settings menu
settingsmenu.add_command(label="Change Interface Language", command=lambda: openLangMenu())


#AN menu
anmenu.add_command(label="Website", command=lambda: webbrowser.open(ANwebsite))
anmenu.add_command(label="Rulebook", command=lambda: webbrowser.open(ANrulebook))

root.config(menu=bar_menu)
root.mainloop()