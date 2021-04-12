from tkinter.messagebox import *
from Book import *
from Issuer import *
import pymysql
from datetime import date

def addBookDetails(b):
	insertBook = "INSERT INTO books VALUES(%i,'%s','%s',%i,%i)" % (b.getBookId(),b.getBookTitle(),b.getBookAuthor(),b.getBookISBN(),b.getBookQuantity())
	con = None
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(insertBook)
		con.commit()
		showinfo("Successful","Book added successfully!")
	except Exception as e:
		showerror("Database Error","Book Id or ISBN already exists")
	finally:
		if con is not None:
			con.close()

def updateBookDetails(b):
	updateBook = "UPDATE books SET bookTitle='%s', bookAuthor='%s', bookISBN=%i, bookQuantity=%i WHERE bookId=%i" % (b.getBookTitle(),b.getBookAuthor(),b.getBookISBN(),b.getBookQuantity(),b.getBookId())
	con = None
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(updateBook)
		con.commit()
		return cur.rowcount
	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def deleteBookDetails(b):
	deleteBook = "DELETE FROM books WHERE bookId=%i" % (b)
	con = None
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(deleteBook)
		con.commit()
		return cur.rowcount
	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()


def issueBooks(issue):
	today = date.today()
	
	con = None
	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()

		# Checking for available books
		booksAvaialable = 0
		getQuantity = "select bookQuantity from books where bookId=%i" % (issue.getBookId())
		cur.execute(getQuantity)
		for i in cur:
			booksAvaialable = int(i[0])

		# if books available the insert and update record
		if booksAvaialable > 1:
			issue_book = "INSERT INTO issueDetails(bookId,reader,contact,issueDate) VALUES(%i,'%s',%i,'%s')" % (issue.getBookId(),issue.getReader(),issue.getContact(),today)
			cur.execute(issue_book)
			update_book = "UPDATE books SET bookQuantity = %i where bookId = %i" % (booksAvaialable-1,issue.getBookId())
			cur.execute(update_book)
			con.commit()
			showinfo("Success","Book Issued Successfully")
		else:
			showerror("Book Error","Book is not Available")

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def returnBooks(issue):
	today = date.today()
	con = None

	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()

		# Checking for available books
		returned = ""
		checkReturned = "select returnDate from issueDetails where issueId=%i and bookId=%i" % (issue.getIssueId(),issue.getBookId())
		cur.execute(checkReturned)
		for i in cur:
			returned = i[0]

		# if books available the insert and update record
		if returned == 'Not Returned':

			return_book = "UPDATE issueDetails SET returnDate = '%s' where issueId = %i" % (today,issue.getIssueId())
			cur.execute(return_book)
			update_book = "UPDATE books SET bookQuantity = bookQuantity + 1 where bookId = %i" % (issue.getBookId())
			cur.execute(update_book)
			con.commit()
			showinfo("Success","Book returned Successfully")
		else:
			showerror("Book Error","Book is already returned or Information provided is wrong")

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def checkFineReturn(issue):
	today = date.today()
	totalDays = 0
	con = None

	try:
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()

		# Checking for available books
		returned = ""
		checkReturned = "select returnDate from issueDetails where issueId=%i and bookId=%i" % (issue.getIssueId(),issue.getBookId())
		cur.execute(checkReturned)
		for i in cur:
			returned = i[0]

		# if books are not returned
		if returned == 'Not Returned':

			getIssueDate = "SELECT issueDate from issueDetails where issueId=%i" % (issue.getIssueId())
			cur.execute(getIssueDate)

			for dt in cur:
				issueDate = dt[0]

			if issueDate != today:
				days = today - issueDate
				totalDays = int(str(days).split(',')[0].split(' ')[0])

			return totalDays

		else:
			showerror("Book Error","Book is already returned or Information provided is wrong")

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()