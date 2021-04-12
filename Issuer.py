class Issuer:
	def __init__(self):
		self.__issueId = 0
		self.__bookId = 0
		self.__reader = ""
		self.__contact = 0
		self.__finePaid = False

	def setIssueId(self,issueId):
		self.__issueId = issueId

	def getIssueId(self):
		return self.__issueId

	def setFinePaid(self,finePaid):
		self.__finePaid = finePaid

	def getFinePaid(self):
		return self.__finePaid

	def setBookId(self,bookId):
		self.__bookId = bookId

	def getBookId(self):
		return self.__bookId

	def setReader(self,reader):
		self.__reader = reader

	def getReader(self):
		return self.__reader

	def setContact(self,contact):
		self.__contact = contact

	def getContact(self):
		return self.__contact