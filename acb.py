import tkinter as tk

root = tk.Tk()
root.title("Assassin's Creed: Brotherhood Setup Manager Tool")
root.resizable(False, False)

photo = tk.PhotoImage(file = "images/icon.png")
root.iconphoto(False, photo)

canvas = tk.Canvas(root, height=300, width=800, bg="#89b0b3")
#canvas.pack(fill=tk.BOTH, expand=1)
canvas.pack()

root.mainloop()