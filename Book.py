class Book:
	def __init__(self):
		self.__bookId = 0
		self.__bookTitle = ""
		self.__bookAuthor = ""
		self.__bookISBN = 0
		self.__bookQuantity = 0

	def setBookId(self,bookId):
		self.__bookId = bookId

	def getBookId(self):
		return self.__bookId

	def setBookTitle(self,bookTitle):
		self.__bookTitle = bookTitle

	def getBookTitle(self):
		return self.__bookTitle

	def setBookAuthor(self,bookAuthor):
		self.__bookAuthor = bookAuthor

	def getBookAuthor(self):
		return self.__bookAuthor

	def setBookISBN(self,bookISBN):
		self.__bookISBN = bookISBN

	def getBookISBN(self):
		return self.__bookISBN

	def setBookQuantity(self,bookQuantity):
		self.__bookQuantity = bookQuantity

	def getBookQuantity(self):
		return self.__bookQuantity