import matplotlib.pyplot as plt
import pymysql

def topBooksAvailable():
	topBooks = "select bookTitle, bookQuantity from books order by bookQuantity DESC limit 3"
	con = None
	try:
		titles = []
		quantity = []
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(topBooks)

		for data in cur:
			titles.append(data[0])
			quantity.append(data[1])

		plt.bar(titles,quantity,color=['red','yellow','green'])

		plt.xlabel('Books')
		plt.ylabel('Available')
		plt.title("Top 3 Books Available")
		plt.show()

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def topBooksIssued():
	topBooks = "select bookTitle,count(i.bookId) as 'Total Issued' from issueDetails i, books b where i.bookId = b.bookId group by bookTitle limit 3"
	con = None
	try:
		titles = []
		quantity = []
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(topBooks)

		for data in cur:
			titles.append(data[0])
			quantity.append(data[1])

		plt.bar(titles,quantity,color=['red','yellow','green'])

		plt.xlabel('Books')
		plt.ylabel('Issued')
		plt.title("Top 3 Books Issued")
		plt.show()

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()

def topReaders():
	topReaders = "select lower(reader),count(lower(reader)) from issueDetails group by lower(reader) limit 3"
	con = None
	try:
		readers = []
		quantity = []
		con = pymysql.connect (host="localhost",user="root",password="abc456",database="library")
		cur = con.cursor()
		cur.execute(topReaders)

		for data in cur:
			readers.append(data[0])
			quantity.append(data[1])

		plt.bar(readers,quantity,color=['red','yellow','green'])

		plt.xlabel('Books Issued')
		plt.ylabel('Readers')
		plt.title("Top 3 Readers")
		plt.show()

	except Exception as e:
		showerror("Database Error",e)
	finally:
		if con is not None:
			con.close()