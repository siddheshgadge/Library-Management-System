from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from quote import *
from Book import *
from Issuer import *
from database import *
from plot import *
from splash import *

b = Book()
issue_obj = Issuer()

def closeWindow(num):
	if askokcancel("quit","Sure you want to quit?"):
		if num == 1:
			main_window.destroy()
		elif num == 2:
			add_window.destroy()
		elif num == 3:
			view_window.destroy()
		elif num ==4:
			delete_window.destroy()
		elif num == 5:
			update_window.destroy()
		elif num == 6:
			issue_window.destroy()
		elif num == 7:
			return_window.destroy()
		elif num == 8:
			issuedDetails_window.destroy()
		elif num == 9:
			chart_window.destroy()

def backBtnClicked(num):
	if num == 1:
		main_window.deiconify()
		add_window.withdraw()
	elif num == 2:
		main_window.deiconify()
		view_window.withdraw()
	elif num == 3:
		main_window.deiconify()
		delete_window.withdraw()
	elif num == 4:
		main_window.deiconify()
		update_window.withdraw()
	elif num == 5:
		main_window.deiconify()
		issue_window.withdraw()
	elif num == 6:
		main_window.deiconify()
		return_window.withdraw()
	elif num == 7:
		main_window.deiconify()
		issuedDetails_window.withdraw()
	elif num == 8:
		main_window.deiconify()
		chart_window.withdraw()

def addBookClicked():
	add_window.deiconify()
	main_window.withdraw()

def viewBookClicked():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0,END)
	# showing data
	con = None
	getBooks = "select * from books"
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(getBooks)
		con.commit()
		for book in cur:
			info = "Book Id: {} \t Book Title: {} \n Book Author: {} \n Book ISBN: {} \n Available Books: {} \n\n".format(book[0],book[1],book[2],book[3],book[4])
			view_window_st_data.insert(INSERT,info)

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def deleteBookClicked():
	delete_window.deiconify()
	main_window.withdraw()

def updateBookClicked():
	update_window.deiconify()
	main_window.withdraw()

def issueBookClicked():
	issue_window.deiconify()
	main_window.withdraw()

def issuedDetailsClicked():
	issuedDetails_window.deiconify()
	main_window.withdraw()
	issuedDetails_window_st_data.delete(1.0,END)
	# showing data
	con = None
	getDetails = "select issueId,reader,b.bookId,bookTitle,issueDate,returnDate,contact from issueDetails i, books b where b.bookId = i.bookId order by issueId"
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(getDetails)

		for details in cur: 
			info = "Issue Id: {} \t Reader: {} \n BookId: {} \t Book Title: {} \n Issued On: {} \t Returned On: {} \n Contact no: {} \n\n".format(details[0],details[1],details[2],details[3],details[4],details[5],details[6])
			issuedDetails_window_st_data.insert(INSERT,info)
	
	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def returnBookClicked():
	return_window.deiconify()
	main_window.withdraw()

def chartsClicked():
	chart_window.deiconify()
	main_window.withdraw()

def registerBook():
	val = validateAdd()
	if val:
		addBookDetails(b)
		inBookId.delete(0,END)
		inBookId.focus()
		inBookTitle.delete(0,END)
		inBookAuthor.delete(0,END)
		inBookISBN.delete(0,END)
		inBookQuantity.delete(0,END)

def deleteBook():
	val = validateDelete()
	if val:
		rowcount = deleteBookDetails(b.getBookId())
		if rowcount > 0:
			showinfo("Success","Book deleted successfully!")
		else:
			showerror("Invalid Id","Book Id not exists!")
		inBookId_del.delete(0,END)
		inBookId_del.focus()


def updateBook():
	val = validateUpdate()
	if val:
		rowcount = updateBookDetails(b)
		if rowcount > 0:
			showinfo("Success","Book details updated successfully!")
		else:
			showerror("Invalid Id","Book Id not exists!")
		inBookId_update.delete(0,END)
		inBookId_update.focus()
		inBookTitle_update.delete(0,END)
		inBookAuthor_update.delete(0,END)
		inBookISBN_update.delete(0,END)
		inBookQuantity_update.delete(0,END)

def issueBook():
	val = validateIssue()
	if val:
		issueBooks(issue_obj)
		inBookId_issue.delete(0,END)
		inBookId_issue.focus()
		reader.delete(0,END)
		contact.delete(0,END)

def returnBook():
	if issue_obj.getFinePaid():
		returnBooks(issue_obj)
		inBookId_return.delete(0,END)
		inBookId_return.focus()
		inIssueId_return.delete(0,END)
	else:
		val = validateReturn()
		if val:
			showerror("Fine","Pay Fine first!")

def checkFine():
	val = validateReturn()
	if val:
		totalDays = checkFineReturn(issue_obj)
		fine = 0
		remark = "Returning on time! No Fine!"

		# Late return Fine
		lbl_fine = Label(labelFrame,text="Fine : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))

		if totalDays != None:
			if totalDays > 15:
				remark = "Book returning date overdue!"
				fine = (totalDays-15) * 25

			lbl_fine_val = Label(labelFrame,text="\u20B9" + str(fine), bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))

			lbl_fine_remark = Label(labelFrame,text=remark, bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
			
			lbl_fine.place(relx=0.05,rely=0.8)
			lbl_fine_remark.place(relx=0.3,rely=0.65)
			lbl_fine_val.place(relx=0.3,rely=0.80)

			if totalDays > 15:
				if askokcancel("Pay Fine","Fine Paid"):
					issue_obj.setFinePaid(True)
				else:
					showerror("Pay Fine","First Pay and then check for fine and say ok!")
			else:
				issue_obj.setFinePaid(True)

def booksAvailable():
	topBooksAvailable()

def booksIssued():
	topBooksIssued()

def bookReaders():
	topReaders()


""" Validating input Fields """

def validateAdd():
	try:
		bookId = int(inBookId.get())
		if bookId < 0:
			showerror("Invalid bookId","Id must be positive")
			inBookId.delete(0,END)
			inBookId.focus()
			return False
		b.setBookId(bookId)
	except ValueError as e:
		showerror("Wrong input","Enter correct bookId")
		inBookId.delete(0,END)
		inBookId.focus()
		return False

	try:
		bookTitle = inBookTitle.get().strip().capitalize()
		if len(bookTitle) < 5 or bookTitle.isdigit():
			showerror("Invalid Book Title","Enter Correct Book Title")
			inBookTitle.delete(0,END)
			inBookTitle.focus()
			return False
		b.setBookTitle(bookTitle)
	except ValueError as e:
		showerror("Wrong input","Enter correct book Title")
		inBookTitle.delete(0,END)
		inBookTitle.focus()
		return False

	try:
		bookAuthor = inBookAuthor.get().strip().capitalize()
		if len(bookAuthor) < 2 or not bookAuthor.replace(" ","").isalpha():
			showerror("Invalid Book Author","Enter Correct Book Author")
			inBookAuthor.delete(0,END)
			inBookAuthor.focus()
			return False
		b.setBookAuthor(bookAuthor)
	except ValueError as e:
		showerror("Wrong input","Enter correct book Author")
		inBookAuthor.delete(0,END)
		inBookAuthor.focus()
		return False

	try:
		bookISBN = inBookISBN.get()
		if len(bookISBN) not in(10,13) or not bookISBN.isdigit():
			showerror("Invalid Book ISBN","Enter Correct Book ISBN")
			inBookISBN.delete(0,END)
			inBookISBN.focus()
			return False
		b.setBookISBN(int(bookISBN))
	except ValueError as e:
		showerror("Wrong input","Enter correct book ISBN")
		inBookISBN.delete(0,END)
		inBookISBN.focus()
		return False

	try:
		bookQuantity = int(inBookQuantity.get())
		if bookQuantity < 1:
			showerror("Invalid Book Quantity","Should have atleast 1 book")
			inBookQuantity.delete(0,END)
			inBookQuantity.focus()
			return False
		b.setBookQuantity(int(bookQuantity))
	except ValueError as e:
		showerror("Wrong input","Enter correct book Quantity")
		inBookQuantity.delete(0,END)
		inBookQuantity.focus()
		return False

	return True

def validateUpdate():
	try:
		bookId = int(inBookId_update.get())
		if bookId < 0:
			showerror("Invalid bookId","Id must be positive")
			inBookId_update.delete(0,END)
			inBookId_update.focus()
			return False
		b.setBookId(bookId)
	except ValueError as e:
		showerror("Wrong input","Enter correct bookId")
		inBookId_update.delete(0,END)
		inBookId_update.focus()
		return False

	try:
		bookTitle = inBookTitle_update.get().strip().capitalize()
		if len(bookTitle) < 5 or bookTitle.isdigit():
			showerror("Invalid Book Title","Enter Correct Book Title")
			inBookTitle_update.delete(0,END)
			inBookTitle_update.focus()
			return False
		b.setBookTitle(bookTitle)
	except ValueError as e:
		showerror("Wrong input","Enter correct book Title")
		inBookTitle_update.delete(0,END)
		inBookTitle_update.focus()
		return False

	try:
		bookAuthor = str(inBookAuthor_update.get()).strip().capitalize()
		
		if len(bookAuthor) < 2 or not bookAuthor.replace(" ","").isalpha():
			showerror("Invalid Book Author","Enter Correct Book Author")
			inBookAuthor_update.delete(0,END)
			inBookAuthor_update.focus()
			return False
		b.setBookAuthor(bookAuthor)
	except ValueError as e:
		showerror("Wrong input","Enter correct book Author")
		inBookAuthor_update.delete(0,END)
		inBookAuthor_update.focus()
		return False

	try:
		bookISBN = inBookISBN_update.get()
		if len(bookISBN) not in(10,13) or not bookISBN.isdigit():
			showerror("Invalid Book ISBN","Enter Correct Book ISBN")
			inBookISBN_update.delete(0,END)
			inBookISBN_update.focus()
			return False
		b.setBookISBN(int(bookISBN))
	except ValueError as e:
		showerror("Wrong input","Enter correct book ISBN")
		inBookISBN_update.delete(0,END)
		inBookISBN_update.focus()
		return False

	try:
		bookQuantity = int(inBookQuantity_update.get())
		if bookQuantity < 1:
			showerror("Invalid Book Quantity","Should have atleast 1 book")
			inBookQuantity_update.delete(0,END)
			inBookQuantity_update.focus()
			return False
		b.setBookQuantity(int(bookQuantity))
	except ValueError as e:
		showerror("Wrong input","Enter correct book Quantity")
		inBookQuantity_update.delete(0,END)
		inBookQuantity_update.focus()
		return False

	return True

def validateIssue():
	try:
		bookId = int(inBookId_issue.get())
		if bookId < 0:
			showerror("Invalid bookId","Id must be positive")
			inBookId_issue.delete(0,END)
			inBookId_issue.focus()
			return False
		issue_obj.setBookId(bookId)
	except ValueError as e:
		showerror("Wrong input","Enter correct bookId")
		inBookId_issue.delete(0,END)
		inBookId_issue.focus()
		return False

	try:
		issuer = reader.get().strip().capitalize()
		if len(issuer) < 2 or not issuer.replace(" ","").isalpha():
			showerror("Invalid Issuer name","Enter Correct Reader Name")
			reader.delete(0,END)
			reader.focus()
			return False
		issue_obj.setReader(issuer)
	except ValueError as e:
		showerror("Wrong input","Enter correct Reader Name")
		reader.delete(0,END)
		reader.focus()
		return False

	try:
		reader_contact = contact.get()
		if len(reader_contact) != 10 or not reader_contact.isdigit():
			showerror("Invalid Contact number","Enter Correct Contact")
			contact.delete(0,END)
			contact.focus()
			return False
		issue_obj.setContact(int(reader_contact))
	except ValueError as e:
		showerror("Wrong input","Enter correct Contact number")
		contact.delete(0,END)
		contact.focus()
		return False

	return True

def validateDelete():
	try:
		bookId = int(inBookId_del.get())
		if bookId < 0:
			showerror("Invalid bookId","Id must be positive")
			inBookId_del.delete(0,END)
			inBookId_del.focus()
			return False
		b.setBookId(bookId)
	except ValueError as e:
		showerror("Wrong input","Enter correct bookId")
		inBookId_del.delete(0,END)
		inBookId_del.focus()
		return False
	return True

def validateReturn():
	try:
		bookId = int(inBookId_return.get())
		if bookId < 0:
			showerror("Invalid bookId","Id must be positive")
			inBookId_return.delete(0,END)
			inBookId_return.focus()
			return False
		issue_obj.setBookId(bookId)
	except ValueError as e:
		showerror("Wrong input","Enter correct bookId")
		inBookId_return.delete(0,END)
		inBookId_return.focus()
		return False

	try:
		issueId = int(inIssueId_return.get())
		if issueId < 0:
			showerror("Invalid issueId","Id must be positive")
			inissueId_return.delete(0,END)
			inissueId_return.focus()
			return False
		issue_obj.setIssueId(issueId)
	except ValueError as e:
		showerror("Wrong input","Enter correct issueId")
		inissueId_return.delete(0,END)
		inissueId_return.focus()
		return False
	return True

""" MainFrame """	
splash()

main_window = Tk()
main_window.title("Library Management System")
main_window.geometry("400x400+500+100")

#background
main_window.configure(background='#0a043c')

#Heading Frame  
headingFrameMain = Frame(main_window,bg="#FFBB00",bd=5)
headingFrameMain.place(relx=0.13,rely=0.1,relwidth=0.75,relheight=0.19)
headingLabelMain = Label(headingFrameMain, text="Library Management \n System", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelMain.place(relx=0,rely=0, relwidth=1, relheight=1)

# Adding buttons
btn_add = Button(main_window,text="Add new Book",bg='#0f3057', fg='white', command=addBookClicked)
btn_add.place(relx=0.06,rely=0.4, relwidth=0.42,relheight=0.1)
    
btn_delete = Button(main_window,text="Delete Book",bg='#0f3057', fg='white', command=deleteBookClicked)
btn_delete.place(relx=0.53,rely=0.4, relwidth=0.42,relheight=0.1)
    
btn_view = Button(main_window,text="View Book List",bg='#0f3057', fg='white', command=viewBookClicked)
btn_view.place(relx=0.06,rely=0.48, relwidth=0.42,relheight=0.1)
    
btn_update = Button(main_window,text="Update Book detais",bg='#0f3057', fg='white', command=updateBookClicked)
btn_update.place(relx=0.53,rely=0.48, relwidth=0.42,relheight=0.1)
    
btn_issue = Button(main_window,text="Issue Book to student",bg='#0f3057', fg='white',command=issueBookClicked)
btn_issue.place(relx=0.06,rely=0.56, relwidth=0.42,relheight=0.1)

btn_issue_details = Button(main_window,text="Issued Details",bg='#0f3057', fg='white',command=issuedDetailsClicked)
btn_issue_details.place(relx=0.53,rely=0.56, relwidth=0.42,relheight=0.1)

btn_return = Button(main_window,text="Return Book",bg='#0f3057', fg='white',command=returnBookClicked)
btn_return.place(relx=0.06,rely=0.64, relwidth=0.42,relheight=0.1)

btn_chart = Button(main_window,text="charts",bg='#0f3057', fg='white', command=chartsClicked)
btn_chart.place(relx=0.53,rely=0.64, relwidth=0.42,relheight=0.1)

#Quote for the library
msg = getQuote()
if msg != None:
	lbl_quote = Label(main_window,text=msg[0] + '\n' + msg[1], bg='#a3ddcb', fg='black',font=('Arial', 10, 'bold'))
	lbl_quote.place(relx=0.05,rely=0.82)

""" Add Books window Frame """

#	Add_window
add_window = Toplevel(main_window)
add_window.title("ADD NEW BOOKS")
add_window.geometry("600x450+400+100")

#background
add_window.configure(background='#0a043c')

#Heading Frame  
headingFrameAdd = Frame(add_window,bg="#FFBB00",bd=5)
headingFrameAdd.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelAdd = Label(headingFrameAdd, text="Add New Books", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelAdd.place(relx=0,rely=0, relwidth=1, relheight=1)

#Adding labels and input boxes
labelFrame = Frame(add_window,bg='#a3ddcb')
labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.50)
        
# Book ID
lbl_bookId = Label(labelFrame,text="Book ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookId.place(relx=0.05,rely=0.2, relheight=0.11)
        
inBookId = Entry(labelFrame)
inBookId.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.11)
        
# Title
lbl_bookTitle = Label(labelFrame,text="Title : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookTitle.place(relx=0.05,rely=0.35, relheight=0.11)
        
inBookTitle = Entry(labelFrame)
inBookTitle.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.11)
        
# Book Author
lbl_bookAuthor = Label(labelFrame,text="Author : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookAuthor.place(relx=0.05,rely=0.50, relheight=0.11)
        
inBookAuthor = Entry(labelFrame)
inBookAuthor.place(relx=0.3,rely=0.50, relwidth=0.62, relheight=0.11)

# ISBN number
lbl_bookISBN = Label(labelFrame,text="ISBN : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookISBN.place(relx=0.05,rely=0.65, relheight=0.11)
        
inBookISBN = Entry(labelFrame)
inBookISBN.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.11)

# Books quantity
lbl_bookQuantity = Label(labelFrame,text="Quantity : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookQuantity.place(relx=0.05,rely=0.80, relheight=0.11)
        
inBookQuantity = Entry(labelFrame)
inBookQuantity.place(relx=0.3,rely=0.80, relwidth=0.62, relheight=0.11)
        
# Adding buttons
btn_submit_add = Button(add_window,text="Add",bg='#0f3057', fg='white',command=registerBook)
btn_submit_add.place(relx=0.28,rely=0.87, relwidth=0.20,relheight=0.09)
		    
btn_back_add = Button(add_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(1))
btn_back_add.place(relx=0.48,rely=0.87, relwidth=0.20,relheight=0.09)

add_window.withdraw()

"""	View Books Frame """
#	View_window
view_window = Toplevel(main_window)
view_window.title("VIEW BOOKS")
view_window.geometry("650x450+300+100")

#background
view_window.configure(background='#0a043c')

#Heading Frame  
headingFrameView = Frame(view_window,bg="#FFBB00",bd=5)
headingFrameView.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelView = Label(headingFrameView, text="View Books", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelView.place(relx=0,rely=0, relwidth=1, relheight=1)

#View Text area
labelFrame = Frame(view_window,bg='black')
labelFrame.place(relx=0.05,rely=0.3,relwidth=0.88,relheight=0.5)
y = 0.25

view_window_st_data = ScrolledText(view_window, width=80, height=40, font=('Arial', 20, 'bold'))
view_window_st_data.place(relx=0.05,rely=0.3,relwidth=0.88,relheight=0.5)

        
# Adding buttons		    
btn_back_view = Button(view_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(2))
btn_back_view.place(relx=0.40,rely=0.87, relwidth=0.20,relheight=0.09)

view_window.withdraw()

""" Delete Book """
#	Delete_window
delete_window = Toplevel(main_window)
delete_window.title("DELETE BOOKS")
delete_window.geometry("600x300+400+130")

#background
delete_window.configure(background='#0a043c')

#Heading Frame  
headingFrameDelete = Frame(delete_window,bg="#FFBB00",bd=5)
headingFrameDelete.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelDelete = Label(headingFrameDelete, text="Delete Books", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelDelete.place(relx=0,rely=0, relwidth=1, relheight=1)

labelFrame = Frame(delete_window,bg='#a3ddcb')
labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)   
        
# Book ID to Delete
lbl_bookId = Label(labelFrame,text="Book ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookId.place(relx=0.05,rely=0.4)
        
inBookId_del = Entry(labelFrame)
inBookId_del.place(relx=0.3,rely=0.4, relwidth=0.62, relheight=0.25)
    
#Submit Button
btn_delete = Button(delete_window,text="Delete",bg='#0f3057', fg='white',command=deleteBook)
btn_delete.place(relx=0.28,rely=0.80, relwidth=0.20,relheight=0.12)
		    
btn_back_del = Button(delete_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(3))
btn_back_del.place(relx=0.48,rely=0.80, relwidth=0.20,relheight=0.12)

delete_window.withdraw()

""" Update Books window Frame """

#	Update_window
update_window = Toplevel(main_window)
update_window.title("UPDATE BOOK DETAILS")
update_window.geometry("600x450+400+100")

#background
update_window.configure(background='#0a043c')

#Heading Frame  
headingFrameAdd = Frame(update_window,bg="#FFBB00",bd=5)
headingFrameAdd.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelAdd = Label(headingFrameAdd, text="Update Book Details", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelAdd.place(relx=0,rely=0, relwidth=1, relheight=1)

#Adding labels and input boxes
labelFrame = Frame(update_window,bg='#a3ddcb')
labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.50)
        
# Book ID
lbl_bookId = Label(labelFrame,text="Book ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookId.place(relx=0.05,rely=0.2, relheight=0.11)
        
inBookId_update = Entry(labelFrame)
inBookId_update.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.11)
        
# Title
lbl_bookTitle = Label(labelFrame,text="Title : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookTitle.place(relx=0.05,rely=0.35, relheight=0.11)
        
inBookTitle_update = Entry(labelFrame)
inBookTitle_update.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.11)
        
# Book Author
lbl_bookAuthor = Label(labelFrame,text="Author : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookAuthor.place(relx=0.05,rely=0.50, relheight=0.11)
        
inBookAuthor_update = Entry(labelFrame)
inBookAuthor_update.place(relx=0.3,rely=0.50, relwidth=0.62, relheight=0.11)

# ISBN number
lbl_bookISBN = Label(labelFrame,text="ISBN : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookISBN.place(relx=0.05,rely=0.65, relheight=0.11)
        
inBookISBN_update = Entry(labelFrame)
inBookISBN_update.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.11)

# Books quantity
lbl_bookQuantity = Label(labelFrame,text="Quantity : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookQuantity.place(relx=0.05,rely=0.80, relheight=0.11)
        
inBookQuantity_update = Entry(labelFrame)
inBookQuantity_update.place(relx=0.3,rely=0.80, relwidth=0.62, relheight=0.11)
        
# Adding buttons
btn_update = Button(update_window,text="Update",bg='#0f3057', fg='white',command = updateBook)
btn_update.place(relx=0.28,rely=0.87, relwidth=0.20,relheight=0.09)
		    
btn_back_update = Button(update_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(4))
btn_back_update.place(relx=0.48,rely=0.87, relwidth=0.20,relheight=0.09)

update_window.withdraw()

""" Issue book to the readers """

#	Issue_window
issue_window = Toplevel(main_window)
issue_window.title("ISSUE BOOKS")
issue_window.geometry("600x450+400+100")

#background
issue_window.configure(background='#0a043c')

#Heading Frame  
headingFrameIssue = Frame(issue_window,bg="#FFBB00",bd=5)
headingFrameIssue.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelIssue = Label(headingFrameIssue, text="Issue Books", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelIssue.place(relx=0,rely=0, relwidth=1, relheight=1)

labelFrame = Frame(issue_window,bg='#a3ddcb')
labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)  
        
# Book ID
lbl_bookId = Label(labelFrame,text="Book ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookId.place(relx=0.05,rely=0.2)
        
inBookId_issue = Entry(labelFrame)
inBookId_issue.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.11)
    
# Issued To Student name 
lbl_reader = Label(labelFrame,text="Issued To : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_reader.place(relx=0.05,rely=0.4)
        
reader = Entry(labelFrame)
reader.place(relx=0.3,rely=0.4, relwidth=0.62, relheight=0.11)
    
# Issued To Student contact 
lbl_contact = Label(labelFrame,text="Contact : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_contact.place(relx=0.05,rely=0.6)
        
contact = Entry(labelFrame)
contact.place(relx=0.3,rely=0.6, relwidth=0.62, relheight=0.11)
    
#Issue Button
issueBtn = Button(issue_window,text="Issue",bg='#0f3057', fg='white',command=issueBook)
issueBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    
backBtn_issue = Button(issue_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(5))
backBtn_issue.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)

issue_window.withdraw()

"""	Issued Details Books Frame """
#	View_window
issuedDetails_window = Toplevel(main_window)
issuedDetails_window.title("Issued Books Details")
issuedDetails_window.geometry("910x550+200+90")

#background
issuedDetails_window.configure(background='#0a043c')

#Heading Frame  
headingFrameIssuedDetails = Frame(issuedDetails_window,bg="#FFBB00",bd=5)
headingFrameIssuedDetails.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelIssuedDetails = Label(headingFrameIssuedDetails, text="Issued Details Books", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelIssuedDetails.place(relx=0,rely=0, relwidth=1, relheight=1)

#View Text area
labelFrame = Frame(issuedDetails_window,bg='black')
labelFrame.place(relx=0.05,rely=0.3,relwidth=0.92,relheight=0.5)
y = 0.25

issuedDetails_window_st_data = ScrolledText(issuedDetails_window, width=100, height=40, font=('Arial', 15, 'bold'))
issuedDetails_window_st_data.place(relx=0.05,rely=0.3,relwidth=0.92,relheight=0.5)

        
# Adding buttons		    
btn_back_issuedDetails = Button(issuedDetails_window,text="Back",bg='#0f3057', font=('Arial', 15, 'bold'),fg='white',command=lambda:backBtnClicked(7))
btn_back_issuedDetails.place(relx=0.40,rely=0.87, relwidth=0.20,relheight=0.09)

issuedDetails_window.withdraw()

""" Return book """

#	Return_window
return_window = Toplevel(main_window)
return_window.title("RETURN BOOKS")
return_window.geometry("600x550+400+100")

#background
return_window.configure(background='#0a043c')

#Heading Frame  
headingFrameReturn = Frame(return_window,bg="#FFBB00",bd=5)
headingFrameReturn.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabelReturn = Label(headingFrameReturn, text="Return Book", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelReturn.place(relx=0,rely=0, relwidth=1, relheight=1)

labelFrame = Frame(return_window,bg='#a3ddcb')
labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)  
        
# Book ID
lbl_bookId = Label(labelFrame,text="Book ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_bookId.place(relx=0.05,rely=0.16)
        
inBookId_return = Entry(labelFrame)
inBookId_return.place(relx=0.3,rely=0.18, relwidth=0.62, relheight=0.11)

lbl_issueId = Label(labelFrame,text="Issue ID : ", bg='#a3ddcb', fg='black',font=('Arial', 15, 'bold'))
lbl_issueId.place(relx=0.05,rely=0.4)
        
inIssueId_return = Entry(labelFrame)
inIssueId_return.place(relx=0.3,rely=0.42, relwidth=0.62, relheight=0.11)
 
checkFineBtn = Button(labelFrame,text="Check Fine",bg='#0f3057', fg='white',command=checkFine)
checkFineBtn.place(relx=0.48,rely=0.55, relwidth=0.18,relheight=0.08)

#Issue Button
returnBtn = Button(return_window,text="Return",bg='#0f3057', fg='white',command=returnBook)
returnBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.07)
    
backBtn_return = Button(return_window,text="Back",bg='#0f3057', fg='white',command=lambda:backBtnClicked(6))
backBtn_return.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.07)

return_window.withdraw()

''' chart window '''

#	chart window
chart_window = Toplevel(main_window)
chart_window.title("Graphs")
chart_window.geometry("400x350+500+100")

#background
chart_window.configure(background='#0a043c')

#Heading Frame  
headingFramechart = Frame(chart_window,bg="#FFBB00",bd=5)
headingFramechart.place(relx=0.13,rely=0.1,relwidth=0.78,relheight=0.19)
headingLabelchart = Label(headingFramechart, text="Statistics \n Graphical Representation", bg='#0f3057', fg='white', font=('Courier',15))
headingLabelchart.place(relx=0,rely=0, relwidth=1, relheight=1)

btn_books_available = Button(chart_window,text="Top 3 Books Available",bg='#0f3057', fg='white',command=booksAvailable)
btn_books_available.place(relx=0.30,rely=0.40, relwidth=0.42,relheight=0.1)

btn_books_issued = Button(chart_window,text="Top 3 Books Issued",bg='#0f3057', fg='white',command=booksIssued)
btn_books_issued.place(relx=0.30,rely=0.5, relwidth=0.42,relheight=0.1)

btn_readers = Button(chart_window,text="Top 3 Readers",bg='#0f3057', fg='white',command=bookReaders)
btn_readers.place(relx=0.30,rely=0.6, relwidth=0.42,relheight=0.1)

btn_back_chart = Button(chart_window,text="Back",bg='#0f3057', fg='white', command=lambda:backBtnClicked(8))
btn_back_chart.place(relx=0.30,rely=0.7, relwidth=0.42,relheight=0.1)

chart_window.withdraw()

''' Close window protocol '''
main_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(1))
add_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(2))
view_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(3))
delete_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(4))
update_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(5))
issue_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(6))
return_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(7))
issuedDetails_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(8))
chart_window.protocol("WM_DELETE_WINDOW",lambda:closeWindow(9))

main_window.mainloop()