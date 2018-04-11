from tkinter import *

root =Tk()

#Create Label Objects
#label1 = Label(root,text="Hello World")
#label1.pack()

#Create Frame Object
newframe = Frame(root)
newframe.pack()

otherframe = Frame(root)
otherframe.pack(side=BOTTOM)

button1 =Button(newframe, text="Click Here", fg="red")
button2 =Button(otherframe, text="Click Here", fg="blue")
button1.pack()
button2.pack()

root.mainloop()