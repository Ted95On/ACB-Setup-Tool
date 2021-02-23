import os
from os import path
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.filedialog import askdirectory
import subprocess
import csv
import shutil
import webbrowser


version = 1.0 # Complete base version

savefile = 'settings.ini'
accountsfile = 'accData/accounts.csv'
ACBSetupTool = "ACBSetupTool.py"      # Name of this file. Change it accordingly so the program automatically restarts

defaultSettings = {
				   "GamePath": "N/A",
				   "BootMethod": "0",
				   "ExtraLang": "0",
				   "SavePath": "N/A",
				   "SteamPath": "C:/Program Files (x86)/Steam/steam.exe",
				   "SelectedAccount": "0",
				   "LoadChallenges": "0",
				   "Username": "",
				   "Password": ""
				  }

default1 = "C:/Program Files (x86)/Steam/steamapps/common/Assassins Creed Brotherhood"               #default Steam directory
default2 = "C:/Program Files (x86)/Ubisoft/Ubisoft Games Launcher/games/Assassins Creed Brotherhood" #default UbisoftConnect/Uplay directory			

defaultpathExist = path.exists(default1+"/ACBSP.exe")
default2pathExist = path.exists(default2+"/ACBSP.exe")

#links
ANwebsite = 'https://assassins.network'
ANrulebookWeb = 'https://rulebook.assassins.network/'
ANleaderboard = 'https://assassins.network/manhunt'


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


def readAccounts():
	with open(accountsfile, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		return data

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

			userData = {}
			data = csv.reader(file)
			for row in data:
				setting, value = row
				userData[setting] = value
			
			if "GamePath" and "BootMethod" not in userData:
				print("Error reading " + savefile + ". Creating new file")
				return newUser()

			else:
				print("User data found!")
				return userData
	else:
		print(savefile + " file not found.")
		return newUser()

def newUser():
	with open(savefile, 'w') as file:

		for val, val1 in defaultSettings.items():
			file.write(val + "," + val1+"\n")

	print("New " + savefile + " file created!")
	return readUserData()

def writeUserData(data):
	with open(savefile, 'w') as file:

		for setting, value in data.items():
			file.write(setting + "," + value+"\n")
		print("Data saved!")

##########################################################tool start

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

def mapStatusSet(): #### Sets the toggles on the maps according to their status

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

	else:
		unsavedChanges.set("Up to date.")
		changeLabel.config(foreground="green")

def settings():		### Frame 3 Settings

	bootupLabel = tk.LabelFrame(frame3, bg=mapBG, font=mapFonts, text="Bootup Method")
	bootupLabel.grid(row=0, column=2, columnspan=3, pady=(15,5))

	options = ("Fastest Bootup\n(No Overlay)\n(Auto Login)", "Quick Bootup\n(With Steam Overlay)\n(Manual Login)", "Regular Bootup\n(Via Singleplayer)\n(Ubisoft Connect)", "Quick Singleplayer Bootup")
	bootMethod.set(int(userData["BootMethod"]))

	for x in range(4):
		ttk.Radiobutton(bootupLabel, style="boot.TRadiobutton", variable=bootMethod, value=x, text=options[x],
			takefocus=False).grid(row=0, column=x, padx=5, ipady=5)

	myTtkStyle.configure("boot.TRadiobutton", background=mapBG, font=mapFonts, justify=tk.CENTER)

	langLabel = tk.LabelFrame(frame3, bg=mapBG, font=mapFonts, text="Additional Languages")
	langLabel.grid(row=1, column=2, columnspan=3)
	
	extraLang.set(int(userData["ExtraLang"]))
	langCheck = ttk.Checkbutton(langLabel, style="lang.TCheckbutton", variable=extraLang, takefocus=False, text="Enable")
	langCheck.pack()
	myTtkStyle.configure("lang.TCheckbutton", background=mapBG, font=mapFonts)

	saveButton = tk.Button(frame3, bg="#38393F", font=mapFonts, text="Save Settings", takefocus=False, command=lambda: saveSettings())
	saveButton.grid(row=2, column=2, columnspan=3, pady=10, ipadx=10)

	################################### Save Directory

	challengeFrame = tk.LabelFrame(frame3, bg=mapBG, font=mapFonts, text="Save File Directory", takefocus=False)
	challengeFrame.grid(row=3, column=2, columnspan=3)

	setChallengeDir = tk.Button(challengeFrame, bg="#38393F", font=mapFonts, text="Set Save Path", command=lambda: setSavePath(), takefocus=False)
	setChallengeDir.grid(row=1, column=3, pady=2)

	challengeDir = tk.Entry(challengeFrame, font=mapFonts, textvariable=savePath, borderwidth=3, justify="center", relief="sunken", state="readonly",
								takefocus=False)
	challengeDir.grid(row=2, column=1, columnspan=5, ipadx=150, pady=(3,5), padx=5)

	####################################################

	openDir = tk.Button(frame3, bg="#38393F", font=mapFonts, text="Open Game Directory", command=lambda: openGameDir(), takefocus=False)
	openDir.grid(row=4, column=2, pady=3)

	openSaveDir = tk.Button(frame3, bg="#38393F", font=mapFonts, text="Open Save Directory", command=lambda: openSaveDir(), takefocus=False)
	openSaveDir.grid(row=4, column=3)

	info = tk.Button(frame3, bg="#38393F", font=mapFonts, text="About These Settings", command=lambda: aboutSettings(), takefocus=False)
	info.grid(row=4, column=4, ipadx=5, pady=3)

	if path.exists(userData["SavePath"]+"/OPTIONS"):
		setChallengeDir.config(state="disabled", text="Set!")
		savePath.set(userData["SavePath"])

	def setSavePath():

		messagebox.showinfo("Save Folder", "Select the folder containing your OPTIONS file.\n\nIts default location is \"C:\\Users\\USER\\Saved Games\\Assassin's Creed Brotherhood\\SAVES\".")
		optionsDir = askdirectory(initialdir="C:/Users", mustexist=True, title="Select your Save folder for Assassin's Creed Brotherhood.")

		if path.exists(optionsDir+"/OPTIONS"):

			if path.exists(optionsDir+"/BACKUP/OPTIONS.BACKUP"):
				pass
			else:
				os.mkdir(optionsDir+"/BACKUP")
				shutil.copy2(optionsDir+"/OPTIONS",optionsDir+"/BACKUP/OPTIONS.BACKUP")
				messagebox.showinfo("Directory set!", "Save directory has been succesfully set.\n\nA backup of your current OPTIONS file containing\nyour multiplayer challenge data has been created in\n"
					+ optionsDir+"/BACKUP.")

			userData["SavePath"] = str(optionsDir)
			writeUserData(userData)
			setChallengeDir.config(state="disabled", text="Set!")
			savePath.set(userData["SavePath"])
			print("Good dir")
		else:
			messagebox.showerror("Wrong directory!", "No OPTIONS file in selected folder.")

	def saveSettings():

		newBoot = bootMethod.get()
		userBoot = int(userData["BootMethod"])
		moreLang = extraLang.get()
		userMoreLang = int(userData["ExtraLang"])

		writeData = 0

		if moreLang != userMoreLang:
			userData["ExtraLang"] = str(moreLang)
			writeData = 1

			if moreLang == 1:
				os.rename(gamePath+"/localization.lang",gamePath+"/localization.lang.OFF")
			else:
				os.rename(gamePath+"/localization.lang.OFF",gamePath+"/localization.lang")

		if newBoot != userBoot:
			userData["BootMethod"] = str(newBoot)
			writeData = 1		

			if newBoot == 0 and userBoot == 1:

				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBMP.exe")
				os.rename(gamePath+"/ACBSP2.exe",gamePath+"/ACBSP.exe")
				print("Fastest boot")

			elif newBoot == 1 and userBoot == 0:

				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBSP2.exe")
				os.rename(gamePath+"/ACBMP.exe",gamePath+"/ACBSP.exe")
				print("Quick boot with Steam overlay")

			elif newBoot == 2 and userBoot == 1:
				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBMP.exe")
				os.rename(gamePath+"/ACBSP2.exe",gamePath+"/ACBSP.exe")
				print("Regular SP boot")

			elif newBoot == 1 and userBoot == 2:
				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBSP2.exe")
				os.rename(gamePath+"/ACBMP.exe",gamePath+"/ACBSP.exe")
				print("Quick boot with Steam overlay")

			elif newBoot == 3 and userBoot == 1:
				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBMP.exe")
				os.rename(gamePath+"/ACBSP2.exe",gamePath+"/ACBSP.exe")
				print("Fast SP Boot")

			elif newBoot == 1 and userBoot == 3:
				os.rename(gamePath+"/ACBSP.exe",gamePath+"/ACBSP2.exe")
				os.rename(gamePath+"/ACBMP.exe",gamePath+"/ACBSP.exe")
				print("Quick boot with Steam overlay")

		if writeData == 1:
			writeUserData(userData)
			print("New boot: ", newBoot)
			print("Old boot: ", userBoot)


	def openGameDir():
		if defaultpathExist:
			os.startfile(default1)
		elif default2pathExist:
			os.startfile(default2)
		else:
			try:
				os.startfile(userData["GamePath"])
			except:
				messagebox.showerror("No Directory Found", "No directory found.")

	def openSaveDir():

		if path.exists(userData["SavePath"] + "/OPTIONS"):
			os.startfile(userData["SavePath"])
		else: messagebox.showerror("No Directory Found", "No directory found.")

	def aboutSettings():

		infotext = "Bootup Method: Choose between 4 boot options:\n\n1: Launches the multiplayer directly without Steam or Uplay, and logs you in directly into"\
		" the chosen account.\n\n2: Steam Installation Only: Launches the multiplayer through Steam so you can have the overlay. It doesn't log you in automatically."\
		" but exiting to the singleplayer on the multiplayer menu launches the multiplayer again.\n\n3: Regular bootup into the singleplayer."\
		"\n\n4: Launches the singleplayer without the opening movies, straight into the main menu.\n\nAdditional Languages: Enables extra languages"\
		" ingame.\n\nSome languages like Korean or Japanese haven't been translated for the PC version, so some PC only features aren't working fully"\
		", such as the messagebox and invite system, but the game is still playable.\n\nSome languages, like Chinese, might not even work at all "\
		"on the multiplayer. Chinese has a singleplayer localization but the multiplayer will not boot.\nIf you get stuck with a"\
		" non working language, disable this option, or launch the game through the singleplayer and change the language."

		messagebox.showinfo("About These Settings", infotext)


def accountManagement():   ### Frame 4 Account Management

	selectYourAcc = tk.Label(frame4, bg=mapBG, image=pickAccount)
	selectYourAcc.grid(row=0, column=3)

	accountsFrame = tk.Canvas(frame4, bg=innerBG, borderwidth=2, relief="sunken")
	accountsFrame.grid(row=1, column=2, columnspan=3)

	selectedAccount = int(userData["SelectedAccount"])
	a.set(selectedAccount)

	marqfootLabel = tk.Label(frame4, image=marqfoot, bg=mapBG)
	marqfootLabel.grid(row=1, column=1, padx=15)
	courtyprowlLab = tk.Label(frame4, image=courtyprowl, bg=mapBG)
	courtyprowlLab.grid(row=1, column=5, padx=15)

	count=1
	for d in range(5):
		for x in range(3):
			ttk.Radiobutton(accountsFrame, style="acc.TRadiobutton", 
      		  text=accounts[count][0], variable=a, value=count, takefocus=False,
      		  command=lambda: selectAcc()).grid(row=d, column=x, padx=15, pady=5, sticky="w")
			count+=1

	pickYourOwn = tk.Label(frame4, bg=mapBG, image=ownAccount)
	pickYourOwn.grid(row=2, column=3)

	loadOptions.set(int(userData["LoadChallenges"]))

	challenges = ttk.Checkbutton(accountsFrame, style="acc.TCheckbutton", takefocus=False, variable=loadOptions, command=lambda: challengeSettings(),
		text="Load corresponding challenge file")
	challenges.grid(row=5, column=0,columnspan=3, pady=(0,5))

	personalAccount = tk.Frame(frame4, bg=innerBG, borderwidth=2, relief="sunken")
	personalAccount.grid(row=3, column=3, ipadx=20, pady=10)
	personalAccount.grid_columnconfigure(0, weight=1)
	personalAccount.grid_columnconfigure(2, weight=1)

	personalAcc = ttk.Radiobutton(personalAccount, style="acc.TRadiobutton", text="Use Personal Account", variable=a, takefocus=False,
		command=lambda: selectAcc(), value=0)
	personalAcc.grid(row=0, column=1)

	myTtkStyle.configure("acc.TRadiobutton", background=innerBG, font=mapFonts, justify="center")
	myTtkStyle.configure("acc.TCheckbutton", background=innerBG, font=mapFonts)

	def selectAcc():
		myAcc = a.get()
		mySave = accounts[myAcc][2]
		saveFolder = userData["SavePath"]

		if int(userData["LoadChallenges"]) == 1 and myAcc != 0:
			messagebox.showinfo("Challenge Progress Data", "The OPTIONS file with the challenges for this account is called \""
			+ mySave + "\". Find it in the \"accData/SAVES\" folder that came with this tool. \n\nRename it to \"OPTIONS\" and replace it"
			+ " with your current OPTIONS file in your " + saveFolder + " folder.\n\nDon't forget to properly backup your current OPTIONS file"
			+ " or rename it back to its original name to keep it safe.")

def challengeSettings():

	myAcc = a.get()
	mySave = accounts[myAcc][2]
	newOption = loadOptions.get()
	saveFolder = userData["SavePath"]

	if path.exists(userData["SavePath"]+"/OPTIONS") == False:
		messagebox.showerror("Save Directory Not Set", "The save directory hasn't been set yet.\nClick on the SETTINGS tab and set the path.")
	else:
		userData["LoadChallenges"] = str(newOption)
		writeUserData(userData)

		if newOption == 1 and myAcc != 0:
			messagebox.showinfo("Challenge Progress Data", "The OPTIONS file with the challenges for this account is called \""
			+ mySave + "\". Find it in the \"accData/SAVES\" folder that came with this tool. \n\nRename it to \"OPTIONS\" and replace it"
			+ " with your current OPTIONS file in your " + saveFolder + " folder.\n\nDon't forget to properly backup your current OPTIONS file"
			+ " or rename it back to its original name to keep it safe.")


def launchGame(gamePath):  ##### Launches the game
	
	bootConfig = int(userData["BootMethod"])
	myAcc = a.get()

	info = tk.Toplevel(root)
	info.geometry("300x150+300+300")
	info.title("Login Info")
	info.iconphoto(False, logo)
	info.resizable(False, False)
	info.grid_columnconfigure(0, weight=1)
	info.grid_columnconfigure(3, weight=1)
	info.grid_rowconfigure(0, weight=1)
	info.grid_rowconfigure(5, weight=1)
	info.config(bg=mapBG)

	labelUser = tk.Label(info, bg=mapBG, text="Username: ").grid(row=1, column=1)
	userUser = tk.Entry(info, bg=innerBG)
	userUser.grid(row=1, column=2)

	labelPass = tk.Label(info, bg=mapBG, text="Password: ").grid(row=2, column=1, pady=(3,0))

	playButton = ttk.Button(info, text="Play", command=lambda: login(myAcc)).grid(row=3, column=1, columnspan=2, ipadx=10, pady=(10,0))
	userPass = tk.Entry(info, bg=innerBG, show="•")
	userPass.grid(row=2, column=2, pady=(3,0))


	if myAcc != 0 and (bootConfig == 0 or bootConfig == 1):
		userUser.insert(0, str(accounts[myAcc][0]))
		userPass.insert(0, str(accounts[myAcc][1]))

	elif myAcc == 0 and bootConfig == 0:
		userUser.insert(0, str(userData["Username"]))
		userPass.insert(0, str(userData["Password"]))

	if bootConfig == 1 and myAcc != 0:
		userPass.config(show="")
		tk.Label(info, bg=mapBG, font=mapFonts, text="This is your login info.\nUse it on the login screen\nwhen the game launches.").grid(row=4, column=1, columnspan=2, pady=10)
	if bootConfig > 0:
		userUser.config(state="disabled")
		userPass.config(state="disabled")


	def login(myAcc):

		user = userUser.get()
		password = userPass.get()
		writeData = False
		if myAcc != int(userData["SelectedAccount"]):
			print("New default account set")
			userData["SelectedAccount"] = str(myAcc)
			writeData = True

		if myAcc == 0 and userUser.get() != userData["Username"]:
			userData["Username"] = userUser.get()
			writeData = True

		if writeData:
			writeUserData(userData)
	
		try:
			info.destroy()
			root.iconify()

			if int(userData["BootMethod"]) == 0:

				print("Running MP Only")
				subprocess.run([gamePath + "/ACBMP.exe", "/launchedfromotherexec", "/onlineUser:"+user, "/onlinePassword:"+password])

			elif int(userData["BootMethod"]) == 1:

				print("Running with Steam Overlay")
				subprocess.run([userData["SteamPath"], "steam://run/48190"])

			elif int(userData["BootMethod"]) == 2:

				print("Running regular bootup")
				subprocess.run([gamePath + "/ACBSP.exe"])

			else:

				print("Running fast SP bootup")
				subprocess.run([gamePath + "/ACBSP.exe", "/launchedfromotherexec"])

			root.deiconify()
			print("Game Launched")

		except:
			messagebox.showerror("Error Launching Game!", "Game not found.\n\nCheck your directory path.")
			root.deiconify()
			startGame.config(state="active", text="Launch Multiplayer")


pathExist, gamePath = checkDefaultPath() ### Checks if the default game path exists and returns it
print(pathExist, gamePath)

userData = readUserData()				### Reads user info

accError = False
try:
	accounts = readAccounts()			### Reads accounts file
except:
	print("Error loading accounts. Please check if the accounts file exists.")
	accError = True

root = tk.Tk()
root.title("Assassin's Creed: Brotherhood Setup Manager Tool")
root.minsize(height=0, width=150)
root.resizable(True, False)

try:
	homebanner = tk.PhotoImage(file = "images/homeBanner.png")
	ANicon = tk.PhotoImage(file = "images/ANicon.png")
	ANweb = tk.PhotoImage(file = "images/anWeb.png")
	ANlb = tk.PhotoImage(file = "images/anLeaderboards.png")
	ANrulebook = tk.PhotoImage(file = "images/anRulebook.png")
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
	tabSettings = tk.PhotoImage(file = "images/tabSettings.png")
	tabAcc = tk.PhotoImage(file = "images/tabAcc.png")
	launchMP = tk.PhotoImage(file = "images/launchMP.png")
	applyChangesIMG = tk.PhotoImage(file = "images/applyChanges.png")
	pickAccount = tk.PhotoImage(file = "images/pickaccount.png")
	ownAccount = tk.PhotoImage(file = "images/ownaccount.png")
	marqfoot = tk.PhotoImage(file = "images/marqfoot.png")
	courtyprowl = tk.PhotoImage(file = "images/courtyprowl.png")
	root.iconbitmap("images/favicon.ico")
	#root.iconphoto(False, logo)

except:
	print("Critical error! Image files are missing. Please redownload the tool.")

#window frames
myTtkStyle= ttk.Style()
a = tk.IntVar()
b = tk.IntVar()
bootMethod = tk.IntVar()
extraLang = tk.IntVar()
mySidePanel = tk.IntVar()
savePath = tk.StringVar()
loadOptions = tk.IntVar()
dirPath = tk.StringVar()
unsavedChanges = tk.StringVar()

mapFonts = "Arial, 8 italic bold"
mapBG = "#89b0b3" ##89b0b3 38393F
innerBG = "#6C6FB2" #6C6FB2

#sidePanel = tk.Label(root, borderwidth=2, relief="groove", image=sidepanel, bg="#89b0b3")
#sidePanel.pack(side="left", fill="y", anchor="w")

myNotebook = ttk.Notebook(root, takefocus=False) 
myNotebook.pack(fill="both", expand=1)

############################################################################### Frame1
frame1bg = "#232323"
frame1 = tk.Frame(myNotebook, bg=frame1bg, borderwidth=2, relief="groove")
frame1.pack(fill="both", expand=1, anchor="n")
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(3, weight=1)
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(3, weight=1)

bannerFrame = tk.Frame(frame1, bg=frame1bg)
bannerFrame.grid(row=1, column=1)
banner = tk.Label(bannerFrame, bg=frame1bg, image=homebanner).pack(side="top")

startGame = tk.Button(bannerFrame, bg=frame1bg, bd=0, image=launchMP, activebackground=frame1bg, command=lambda: launchGame(gamePath)).pack(side="bottom")

AnBG = "#232323"
Anframe = tk.Frame(frame1, bg=AnBG)
Anframe.grid(row=1, column=2)
Anframe.grid_rowconfigure(0, weight=1)
Anframe.grid_rowconfigure(5, weight=1)

AnInnerBG = "#3D3D3D"
ANlabel = tk.Label(Anframe, bg=AnBG, image=ANicon).grid(row=0, rowspan=5)
b1 = tk.Button(Anframe, bg=AnInnerBG, bd=0, image=ANweb, activebackground=AnInnerBG, command=lambda: webbrowser.open(ANwebsite)).grid(row=2, pady=(0,10))
b2 = tk.Button(Anframe, bg=AnInnerBG, bd=0, image=ANrulebook, activebackground=AnInnerBG, command=lambda: webbrowser.open(ANrulebookWeb)).grid(row=3, pady=(0,10))
b2 = tk.Button(Anframe, bg=AnInnerBG, bd=0, image=ANlb, activebackground=AnInnerBG, command=lambda: webbrowser.open(ANleaderboard)).grid(row=4, pady=(0,15))

###############################################################################


frame2 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove") 
frame2.pack(fill="both", expand=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(7, weight=1)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_rowconfigure(7, weight=1)


frame3 = tk.Frame(myNotebook, bg=mapBG, borderwidth=2, relief="groove")
frame3.pack(fill="both", expand=1)
frame3.grid_columnconfigure(0, weight=1)
frame3.grid_columnconfigure(6, weight=1)



frame4 = tk.Frame(myNotebook, height=100, bg=mapBG, borderwidth=2, relief="groove")
frame4.pack(fill="both", expand=1)
frame4.grid_columnconfigure(0, weight=1)
frame4.grid_columnconfigure(6, weight=1)


tabPadding = 5
myNotebook.add(frame1, text="   Home   ", image=tabHome, padding=tabPadding)
myNotebook.add(frame2, text="   Map Selection   ", image=tabMap, padding=tabPadding)
myNotebook.add(frame3, text="   Settings   ", image=tabSettings, padding=tabPadding)
myNotebook.add(frame4, text="   Account Management   ", image=tabAcc, padding=tabPadding)

settings() ### Frame 3 Settings

if accError == False:
	accountManagement() ### Frame 4 Account Management
else:
	myNotebook.add(frame4, state="disabled")


######################################################################## Images on Frame2
verIMG = tk.Label(frame2, bg=mapBG, image=verify)
verIMG.grid(row=1,column=1, columnspan=2, padx=(10,0))
fazzChar = tk.Label(frame2, bg=mapBG, image=fazz)
fazzChar.grid(row=1, column=4, padx=(0,125))
fouad = tk.Label(frame2, bg=mapBG, image=fouadIMG)
fouad.grid(row=2, column=5)
courtyChar = tk.Label(frame2, bg=mapBG, image=courty)
courtyChar.grid(row=2, column=1)
selectIMG = tk.Label(frame2, image=selectMaps, bg=mapBG)
selectIMG.grid(row=4, rowspan=2, column=5, padx=(0,10), pady=(0,25))
dripdell = tk.Label(frame2, image=engihelle, bg=mapBG)
dripdell.grid(row=5, rowspan=2,column=1, padx=5)
jigaudiChar = tk.Label(frame2, image=jigaudi, bg=mapBG)
jigaudiChar.grid(row=6, column=5, columnspan=1, padx=(0,10))
#######################################################################

acbFolder = tk.Button(frame2, text="Set Game Directory Path", bg="#38393F", font=mapFonts, command=lambda: choosePath())
acbFolder.grid(row=1, column=3, ipadx=20)

pathLabel = tk.Entry(frame2, textvariable=dirPath, bg="#38393F", font=mapFonts, borderwidth=3, justify="center", relief="sunken", state="readonly", takefocus=False)
pathLabel.grid(row=2, column=2, columnspan=3,ipadx=200)

######################################### Frame for the maps and their switches

insideBG = innerBG
mapFrame = tk.Canvas(frame2 ,borderwidth=1, bg=insideBG, relief="sunken")
mapFrame.grid(row=3, rowspan=3, column=2, columnspan=3)

#SanDon
labelSanDon = tk.Label(mapFrame, text="San Donato", font=mapFonts, bg=insideBG)
labelSanDon.grid(row=0, column=0, padx=(25,0), pady=(10,0))
buttonSanDon = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("San Donato"))
buttonSanDon.grid(row=0, column=1, pady=(10,0))

#Castel
labelCastel = tk.Label(mapFrame, text="Castel Gandolfo", font=mapFonts, bg=insideBG)
labelCastel.grid(row=1, column=0, pady=(5,0), padx=(25,0))
buttonCastel = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Castel Gandolfo"))
buttonCastel.grid(row=1, column=1, pady=(5,0))

#MSM
labelMSM = tk.Label(mapFrame, text="Mont St-Michel", font=mapFonts, bg=insideBG)
labelMSM.grid(row=2, column=0, pady=(5,0), padx=(25,0))
buttonMSM = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Mont St-Michel"))
buttonMSM.grid(row=2, column=1, pady=(5,0))

#Monti
labelMonteriggioni = tk.Label(mapFrame, text="Monteriggioni", font=mapFonts, bg=insideBG)
labelMonteriggioni.grid(row=3, column=0, pady=(5,10), padx=(25,0))
buttonMonteriggioni = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Monteriggioni"))
buttonMonteriggioni.grid(row=3, column=1, pady=(5,10))


#Alhambra
labelAlhambra = tk.Label(mapFrame, text="Alhambra", font=mapFonts, bg=insideBG)
labelAlhambra.grid(row=0, column=2, padx=(25,0), pady=(10,0))
buttonAlhambra = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Alhambra"))
buttonAlhambra.grid(row=0, column=3, pady=(10,0))

#Florence
labelFlorence = tk.Label(mapFrame, text="Florence", font=mapFonts, bg=insideBG)
labelFlorence.grid(row=1, column=2, pady=(5,0), padx=(25,0))
buttonFlorence = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Florence"))
buttonFlorence.grid(row=1, column=3, pady=(5,0))

#Pienza
labelPienza = tk.Label(mapFrame, text="Pienza", font=mapFonts, bg=insideBG)
labelPienza.grid(row=2, column=2, pady=(5,0), padx=(25,0))
buttonPienza = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Pienza"))
buttonPienza.grid(row=2, column=3, pady=(5,0))

#Venice
labelVenice = tk.Label(mapFrame, text="Venice", font=mapFonts, bg=insideBG)
labelVenice.grid(row=3, column=2, padx=(25,0), pady=(5,10))
buttonVenice = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Venice"))
buttonVenice.grid(row=3, column=3, pady=(5,10))


#Forli
labelForli = tk.Label(mapFrame, text="Forli", font=mapFonts, bg=insideBG)
labelForli.grid(row=0, column=4, padx=(25,0), pady=(10,0))
buttonForli = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Forli"))
buttonForli.grid(row=0, column=5, padx=(0,30), pady=(10,0))

#Siena
labelSiena = tk.Label(mapFrame, text="Siena", font=mapFonts, bg=insideBG)
labelSiena.grid(row=1, column=4, pady=(5,0), padx=(25,0))
buttonSiena = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Siena"))
buttonSiena.grid(row=1, column=5, pady=(5,0), padx=(0,30))


#Rome
labelRome = tk.Label(mapFrame, text="Rome", font=mapFonts, bg=insideBG)
labelRome.grid(row=2, column=4, pady=(5,0), padx=(25,0))
buttonRome = tk.Button(mapFrame, bg=insideBG, activebackground=insideBG, bd=0, image=onIMG, command=lambda: switchState("Rome"))
buttonRome.grid(row=2, column=5, pady=(5,0), padx=(0,30))


changeLabel = tk.Label(frame2, textvariable=unsavedChanges, bg=mapBG, font="Arial, 8 italic", foreground="red")
changeLabel.grid(row=6, column=2)

startGame = tk.Button(frame2, text="Launch Multiplayer", bg=mapBG, activebackground=mapBG, bd=0, font=mapFonts, image=launchMP, command=lambda: launchGame(gamePath))
startGame.grid(row=6, column=3)

applyChanges = tk.Button(frame2, text="Apply Changes", bg=mapBG, activebackground=mapBG, bd=0, font=mapFonts, image=applyChangesIMG, command=lambda: applyMapChanges())
applyChanges.grid(row=6, column=4)

checkPathandStatus()
print("Game path is: ", gamePath)

mapStatusSet() ### Sets the toggles on the maps according to their status

root.mainloop()