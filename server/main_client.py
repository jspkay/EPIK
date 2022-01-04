import tkinter as tk
import tkinter.font as tkFont

font_size = -24

root = None
frame = None
ipString = None
fullscreen = False

root = tk.Tk()
root.title("Main")

frame = tk.Frame(root, bg='black')
frame.pack(fill=tk.BOTH, expand=1)
ipString = tk.StringVar()

ipString.set("192.168.1.1")

font = tkFont.Font(family='Courier New', size=font_size)

main_label = tk.Label( frame,
                        textvariable = ipString,
                        font = font,
                        fg = 'white',
                        bg = 'black')

main_label.grid(row = 0, column = 0, padx = 20, pady = 20)

frame.rowconfigure(0, weight = 10)
frame.columnconfigure(0, weight=1)

root.bind("<Escape>", lambda Event : exit() )

def setFont(event=None):
    global font
    new_size = -max(12, int(frame.winfo_height()/10))
    font.configure(size=new_size)

root.bind("<Configure>", setFont)
root.attributes('-fullscreen', True)
root.mainloop()
