import requests
import bs4
from tkinter.messagebox import *

def getQuote():
	try:
		wa = "https://www.brainyquote.com/quotes/marcus_tullius_cicero_104340"
		res = requests.get(wa)
		data = bs4.BeautifulSoup(res.text,'html.parser')
		info = data.find('img')
		msg = info['alt'].split(',')
		return msg
	except Exception as e:
		showerror('Failure',e)