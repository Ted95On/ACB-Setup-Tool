import os
from os import path
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.filedialog import askdirectory

import webbrowser
import gettext
_ = gettext.gettext

version = 0.1

global gamePath
gamePath = "C:/Program Files (x86)/Steam/steamapps/common/Assassins Creed Brotherhood" #default folder
pathExist = path.exists(gamePath+"/ACBSP.exe")
if pathExist == False:
	print("Can't find directory")

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

filename = ('settings.ini')
doesitexist = path.exists(filename)
if doesitexist == True:
	filestate = os.stat("settings.ini").st_size == 0

def readSettings():
	if doesitexist == False:
		createfile = open(filename, "w+")
		createfile.write("File ok\n")
		createfile.write("en\n")
		createfile.close()
		return "en"

	elif doesitexist == True and filestate == True:
		writetofile = open(filename, "w")
		writetofile.write("File ok\n")
		writetofile.write("en\n")
		return "en"

	else:
		opensettings = open(filename, "r")
		count = 0
		for i in opensettings:
			if count == 1:
				lang = i.rstrip("\n")
			count+=1
		opensettings.close()
		return lang


def replace_line(file_name, line_num, text):
	linesGet = open(file_name, "r")
	lines = linesGet.readlines()
	lines[line_num] = text+"\n"
	out = open(file_name, "w")
	out.writelines(lines)
	out.close()
	linesGet.close()   

getLang = readSettings()

lang = gettext.translation('base', localedir='locales', languages=[getLang])
lang.install()
_ = lang.gettext

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
		if newLang != getLang:
			replace_line(filename, 1, newLang)
			answer = messagebox.askyesno("", "The language has been changed.\nChanges will take effect upon restart.\n\n"
																						"Do you wish to restart now?")
			if answer == True:
				os.startfile("ACBSetupTool.py")
				root.destroy()
			else:
				pass

def choosePath():

	ACBpath = askdirectory(title="Select your Assassin's Creed Brotherhood installation folder")
	if path.exists(str(ACBpath)+"/ACBSP.exe") == False:
		messagebox.showerror("Path Error", "Wrong directory!\nCan't find \"ACBSP.exe\" in selected folder.")
	else:
		with open(filename, "a") as file:
			file.write(str(ACBpath) + "\n")
			dirPath.set(ACBpath)
			acbFolder['state'] = tk.DISABLED
			os.startfile("ACBSetupTool.py")
			root.destroy()

def switchState(mapName):
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

def applyMapChanges():
	#global mapStatus
	#global maps
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
		unsavedChanges.set("Your changes have been saved.")
		changeLabel.config(foreground="green")

def checkPathandStatus():
	global gamePath
	if pathExist == True:
		dirPath.set(gamePath)
		acbFolder["state"] = tk.DISABLED
		print("Directory found!")
	elif pathExist == False:
		with open(filename, "r") as info:
			fileInfo = info.readlines()

			try:
				newPath = fileInfo[2].strip("\n")
				if path.exists(str(newPath)+"/ACBSP.exe") == True:
					gamePath = newPath
					dirPath.set(gamePath)
					acbFolder["state"] = tk.DISABLED
			except:
				gamePath = ""
				print("Directory not yet set")
				fixSH["state"] = tk.DISABLED

############################################################################
############################################################################ Checks status of each map
	global mapStatus
	mapStatus = dict()
	for place, local in maps.items():
		value = path.exists(gamePath+"/multi/" + local)
		if value == True:
			mapStatus[place] = True
		else:
			mapStatus[place] = False

root = tk.Tk()
root.title(_("Assassin's Creed: Brotherhood Setup Manager Tool"))
root.minsize(width=800, height=300)
root.resizable(False, False)
root.geometry("800x300+250+200")

logo = tk.PhotoImage(file = "images/icon.png")
biglogo = tk.PhotoImage(file = "images/sidepanel.png")
onIMG = tk.PhotoImage(file = "images/OnSwitch.png", master=root)
offIMG = tk.PhotoImage(file = "images/OffSwitch.png", master=root)
root.iconphoto(False, logo)

#main window frames

v = tk.StringVar()
v.set(getLang)
dirPath = tk.StringVar()
unsavedChanges = tk.StringVar()

mapFonts = "FixedSys"
mapBG = "#89b0b3" ##89b0b3 38393F


b = ttk.Style()
b.configure("lang.TRadiobutton", padx=50, font="Helvetica, 9", background="#89b0b3")

logoLabel = tk.Label(root, image=biglogo, bg="#89b0b3")
logoLabel.pack(anchor="w",fill="y")

tabMain = ttk.Notebook(root, width=667, height=250, padding=2)#, 
tabMain.place(x=125)

frame2 = tk.Frame(tabMain, bg=mapBG)#, width=670, height=300, borderwidth=1, 
frame2.grid(row=0, column=1)
frame3 = tk.Frame(tabMain, borderwidth=1, bg=mapBG)#, width=670, height=300,
frame3.grid(row=0, column=1)

tabMain.add(frame2, text="   Map Selection   ")
tabMain.add(frame3, text="   Quick Bootup   ")

acbFolder = tk.Button(frame2, text="Set Directory Path", bg="#38393F", command=lambda: choosePath())
acbFolder.pack(pady=10, ipadx=30)

pathLabel = tk.Label(frame2, textvariable=dirPath, bg="#38393F", borderwidth=3, width=100, anchor="center", relief="sunken")
pathLabel.pack(padx=20)

########################################################################### Checks game path directory


############################################################################


mapFrame = tk.Frame(frame2, borderwidth=1, height=150, bg=mapBG, relief="sunken")
mapFrame.pack(fill="both", pady=10, padx=10)

#SanDon
labelSanDon = tk.Label(mapFrame, text="San Donato", font=mapFonts, bg=mapBG)
labelSanDon.grid(row=0, column=0, padx=30, pady=5)
buttonSanDon = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("San Donato"))
buttonSanDon.grid(row=0, column=1)

#Castel
labelCastel = tk.Label(mapFrame, text="Castel Gandolfo", font=mapFonts, bg=mapBG)
labelCastel.grid(row=1, column=0)
buttonCastel = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Castel Gandolfo"))
buttonCastel.grid(row=1, column=1)

#MSM
labelMSM = tk.Label(mapFrame, text="Mont St-Michel", font=mapFonts, bg=mapBG)
labelMSM.grid(row=2, column=0)
buttonMSM = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Mont St-Michel"))
buttonMSM.grid(row=2, column=1)


#Monti
labelMonteriggioni = tk.Label(mapFrame, text="Monteriggioni", font=mapFonts, bg=mapBG)
labelMonteriggioni.grid(row=3, column=0)
buttonMonteriggioni = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Monteriggioni"))
buttonMonteriggioni.grid(row=3, column=1)


#Alhambra
labelAlhambra = tk.Label(mapFrame, text="Alhambra", font=mapFonts, bg=mapBG)
labelAlhambra.grid(row=0, column=2, padx=25)
buttonAlhambra = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Alhambra"))
buttonAlhambra.grid(row=0, column=3)

#Florence
labelFlorence = tk.Label(mapFrame, text="Florence", font=mapFonts, bg=mapBG)
labelFlorence.grid(row=1, column=2, pady=5)
buttonFlorence = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Florence"))
buttonFlorence.grid(row=1, column=3)

#Pienza
labelPienza = tk.Label(mapFrame, text="Pienza", font=mapFonts, bg=mapBG)
labelPienza.grid(row=2, column=2, padx=10, pady=5)
buttonPienza = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Pienza"))
buttonPienza.grid(row=2, column=3)

#Venice
labelVenice = tk.Label(mapFrame, text="Venice", font=mapFonts, bg=mapBG)
labelVenice.grid(row=3, column=2, padx=10, pady=5)
buttonVenice = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Venice"))
buttonVenice.grid(row=3, column=3)


#Forli
labelForli = tk.Label(mapFrame, text="Forli", font=mapFonts, bg=mapBG)
labelForli.grid(row=0, column=4, padx=35)
buttonForli = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Forli"))
buttonForli.grid(row=0, column=5)

#Siena
labelSiena = tk.Label(mapFrame, text="Siena", font=mapFonts, bg=mapBG)
labelSiena.grid(row=1, column=4, padx=10)
buttonSiena = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Siena"))
buttonSiena.grid(row=1, column=5)


#Rome
labelRome = tk.Label(mapFrame, text="Rome", font=mapFonts, bg=mapBG)
labelRome.grid(row=2, column=4, padx=10, pady=5)
buttonRome = tk.Button(mapFrame, bg=mapBG, activebackground=mapBG, bd=0, image=onIMG, command=lambda: switchState("Rome"))
buttonRome.grid(row=2, column=5)



changeLabel = tk.Label(frame2, textvariable=unsavedChanges, bg=mapBG, font="Arial, 8 italic", foreground="red")
changeLabel.place(x=490, y=218)
fixSH = tk.Button(frame2, text="Apply Changes", bg="#38393F", command=lambda: applyMapChanges())
fixSH.pack()

checkPathandStatus()
print("\nGame path is: ", gamePath)

###############################################################################

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
bar_menu.add_cascade(menu=anmenu, label="Assassins Network")


#file menu
filemenu.add_command(label="Placeholder")
filemenu.add_separator()
filemenu.add_command(label="Close", command=root.destroy)

#settings menu
settingsmenu.add_command(label="Change Interface Language", command=lambda: openLangMenu())

#AN menu
anmenu.add_command(label="Website", command=lambda: webbrowser.open(ANwebsite))
anmenu.add_command(label="Rulebook", command=lambda: webbrowser.open(ANrulebook))
anmenu.add_command(label="Donate to Dellpit-san")

root.config(menu=bar_menu)
root.mainloop()