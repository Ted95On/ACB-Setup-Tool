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
	for x in langlist:
		print(x)
	return input("\nSelect a language: ")

setLang = printLang()
#setLang = "en"

lang = gettext.translation('base', localedir='locales', languages=[str(setLang)])
lang.install()
_ = lang.gettext

#tool.start

def close_window():
	root.destroy()

root = tk.Tk()
root.title(_("Assassin's Creed: Brotherhood Setup Manager Tool"))
root.minsize(width=800, height=300)
#root.resizable(False, False)

logo = tk.PhotoImage(file = "images/icon.png")
root.iconphoto(False, logo)

main = tk.Frame(root, height=240, relief="solid", bg="#89b0b3", borderwidth=1)
main.pack(fill=tk.BOTH, expand=1)
root.geometry("800x300+250+200")
main.pack()

frame1 = tk.Frame(root, height=1, bg="black", relief="solid")
frame1.pack(fill=tk.BOTH)

frame2 = tk.Frame(root, height=20, relief="solid", bg="#38393F", borderwidth=1)
frame2.pack(fill=tk.BOTH, expand=0)

quitIMG = tk.PhotoImage(file = r"images/power.png")

quitB = tk.Button(frame2, image=quitIMG, bg="lightblue", relief="raised", command=lambda: close_window())
quitB.pack(side="right", padx=5, pady=2)

root.mainloop()