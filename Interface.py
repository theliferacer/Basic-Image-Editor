from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from transform import *

root = Tk()
root.title("Basic Image Editor")
root.geometry("1250x770")

#Definitions for buttons
#temp - current displaying image
#temp1 - temporary variable used to store prev image for Undo
#original - Original image accessed when clicked Original button 
def Open():
	global org_img
	global org_img_label
	global original
	global temp
	org_filename = filedialog.askopenfilename(initialdir = " ", title = "Open", filetypes = (("jpg files","*.jpg"),("all files","*.*")))
	org_img = Image.open(org_filename) 
	org_img = Resize(org_img)
	original = org_img.copy()
	temp = org_img.copy()
	temp1 = org_img.copy()
	org_img = ImageTk.PhotoImage(org_img)
	org_img_label = Label(root, image = org_img)
	org_img_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Save():
	global temp
	#Saves files in jpeg format
	file_name = s.get()
	if temp.mode != "RGB":
		temp = temp.convert("RGB")
	temp.save(file_name+ '.jpeg')

def Undo():
	global temp2
	global temp
	global temp2_label
	temp = temp1
	temp2 = ImageTk.PhotoImage(temp)
	temp2_label = Label(root, image = temp2)
	temp2_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Original():
	global init_img
	global init_img_label
	global temp
	init_img = original
	temp = original
	temp1 = original
	init_img = ImageTk.PhotoImage(init_img)
	init_img_label = Label(root, image = init_img)
	init_img_label.grid(row = 1, column = 0, columnspan = 5, rowspan = 3)

def Hist():
	global h_temp_label
	global h_temp
	global temp1
	global temp
	temp1 = temp #Used to acces while doing Undo
	temp = Histogram(temp1)
	h_temp = ImageTk.PhotoImage(temp)
	h_temp_label = Label(root, image = h_temp)
	h_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Log10():
	global l_temp_label
	global l_temp
	global temp1
	global temp
	temp1 = temp
	temp = Logarithm(temp1)
	l_temp = ImageTk.PhotoImage(temp)
	l_temp_label = Label(root, image = l_temp)
	l_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def N_Transform():
	global n_temp_label
	global n_temp
	global temp1
	global temp
	temp1 = temp
	temp = Negative(temp1)
	n_temp = ImageTk.PhotoImage(temp)
	n_temp_label = Label(root, image = n_temp)
	n_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def G_Transform():
	global d
	global g_temp_label
	global g_temp
	global temp1
	global temp
	d = float(g.get())
	temp1 = temp
	temp = Gamma(temp1,d)
	g_temp = ImageTk.PhotoImage(temp)
	g_temp_label = Label(root, image = g_temp)
	g_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Blurness():
	global d
	global b_temp_label
	global b_temp
	global temp1
	global temp
	d = int(blur.get())
	temp1 = temp
	temp = Blur(temp1,d)
	b_temp = ImageTk.PhotoImage(temp)
	b_temp_label = Label(root, image = b_temp)
	b_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Sharpness():
	global d
	global s_temp_label
	global s_temp
	global temp1
	global temp
	d = int(sharp.get())
	temp1 = temp
	temp = Sharp(temp1,d)
	s_temp = ImageTk.PhotoImage(temp)
	s_temp_label = Label(root, image = s_temp)
	s_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)


#Buttons
button_open = Button(root,text = "Open", command = Open)
button_save = Button(root, text = "Save", command = Save)
button_undo = Button(root, text = "Undo", command = Undo)
button_original = Button(root, text = "Original", command = Original)
button_equalize = Button(root, text = "Histogram \n Equalization", command = Hist)
button_log = Button(root, text = "Logarithm", command = Log10)
button_gamma = Button(root, text = "Gamma Transform", command = G_Transform)
button_negative = Button(root, text = "Negative", command = N_Transform)
button_blur = Button(root, text = "Blur Image", command = Blurness)
button_sharp = Button(root, text = "Sharpen Image", command = Sharpness)

#Placing of Buttons
button_open.grid(row = 0, column = 0)
button_undo.grid(row = 0, column = 3)
button_original.grid(row = 0, column = 4)
button_equalize.grid(row = 1, column = 5)
button_log.grid(row = 2, column = 5)
button_negative.grid(row = 3, column = 5)
button_gamma.grid(row = 5, column = 0)
button_blur.grid(row = 5, column = 1)
button_sharp.grid(row = 5, column = 3)
button_save.grid(row = 5, column = 5)

#Gamma Input
g = Entry(root) #for entering gamma value
g.grid(row = 4, column = 0)
#Save File Name Input
s = Entry(root)
s.grid(row = 4, column = 5)
#Sliders
blur = Scale(root, from_ = 3, to = 25, resolution = 2, orient = HORIZONTAL)
blur.grid(row = 4, column = 1)
sharp = Scale(root, from_ = 1, to = 15, orient = HORIZONTAL)
sharp.grid(row = 4, column = 3)

#Empty Space Widgets
label_empty = Label(root)
label_empty.grid(row = 0, column = 1,columnspan = 2)

label_empty2 = Label(root)
label_empty2.grid(row = 4, column = 2)

label_empty3 = Label(root)
label_empty3.grid(row = 4, column = 4)

#Quit Button
button_quit = Button(root, text = "Quit", command = root.quit)
button_quit.grid(row = 0, column = 5)

root.mainloop()