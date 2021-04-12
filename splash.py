from tkinter import *
from PIL import ImageTk,Image

def splash():
	root = Tk()

	root.after(4000,root.destroy)

	root.title("Library")
	root.minsize(width=400,height=400)
	root.geometry("600x500+400+100")

	same=True
	n=0.25
	# Adding a background image
	background_image =Image.open("lib.jpg")
	[imageSizeWidth, imageSizeHeight] = background_image.size
	newImageSizeWidth = int(imageSizeWidth*n)
	if same:
	    newImageSizeHeight = int(imageSizeHeight*n) 
	else:
	    newImageSizeHeight = int(imageSizeHeight/n) 
	    
	background_image = background_image.resize((newImageSizeWidth,newImageSizeHeight),Image.ANTIALIAS)
	img = ImageTk.PhotoImage(background_image)
	Canvas1 = Canvas(root)
	Canvas1.create_image(300,340,image = img)      
	Canvas1.config(bg="white",width = newImageSizeWidth, height = newImageSizeHeight)
	Canvas1.pack(expand=True,fill=BOTH)

	headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
	headingFrame1.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.3)
	headingLabel = Label(headingFrame1, text="Welcome to \n Library Management \n System", bg='#0f3057', fg='white', font=('Courier',20,'bold'))
	headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

	root.mainloop()