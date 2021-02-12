import tkinter as tk
import gettext
_ = gettext.gettext


"""
sets tool language -> Meant to be a changeable setting on the tool later on
en = English (English)
de = German (Deutsch)
fr = French (Français)
pt = Portuguese (Português)
"""
def printLang():
	langlist = ["en = English","de = German", "fr = French", "pt = Portuguese"]
	langName = ["en", "de", "fr", "pt"]
	for x in langlist:
		print(x)
	answer = input("\nSelect a language: ")
	if answer in langName:
		return answer
	else:
		print("\nSelection failed!\n")
		return printLang()

setLang = printLang()
#setLang = "en"

lang = gettext.translation('base', localedir='locales', languages=[str(setLang)])
lang.install()
_ = lang.gettext

#tool.start

def openLangMenu():
	langMenu = tk.Toplevel(main)
	langMenu.title("Interface Language")
	langMenu.geometry("300x180")
	langMenu.resizable(False, False)
	langLabel = tk.Label(langMenu, pady=5, text="Choose a language").pack()
	langButton = tk.Button(langMenu, text="Kill it", command=langMenu.destroy).pack(side="top", pady=50)

root = tk.Tk()
root.title(_("Assassin's Creed: Brotherhood Setup Manager Tool"))
root.minsize(width=800, height=300)
#root.resizable(False, False)

logo = tk.PhotoImage(file = "images/icon.png")
root.iconphoto(False, logo)

#menus
bar_menu = tk.Menu(root)
filemenu = tk.Menu(bar_menu, tearoff=0)
settingsmenu = tk.Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(menu=filemenu, label="File")
bar_menu.add_cascade(menu=settingsmenu, label="Settings")

#file menu
filemenu.add_command(label="Placeholder")
filemenu.add_separator()
filemenu.add_command(label="Close", command=root.destroy)

#settings menu
settingsmenu.add_command(label="Change Interface Language", command=lambda: openLangMenu())

#main window frames

root.geometry("800x300+250+200")
main = tk.Frame(root, height=240, relief="solid", bg="#89b0b3", borderwidth=1)
main.pack(fill=tk.BOTH, expand=1)
main.pack()

frame1 = tk.Frame(root, height=1, bg="black", relief="solid")
frame1.pack(fill=tk.BOTH)

frame2 = tk.Frame(root, height=20, relief="solid", bg="#38393F", borderwidth=1)
frame2.pack(fill=tk.BOTH, expand=0)

quitIMG = tk.PhotoImage(file = r"images/power.png")

quitB = tk.Button(frame2, image=quitIMG, bg="lightblue", relief="raised", command=root.destroy)
quitB.pack(side="right", padx=5, pady=2)
root.config(menu=bar_menu)
root.mainloop()