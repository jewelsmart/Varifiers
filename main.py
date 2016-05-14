from Tkinter import *
import urllib2

"""
response = urllib2.urlopen('http://localhost/my-site/j.html')
html = response.read()
print html
import json

data = json.loads(html)

print(data['score'])
"""

class Applicaion(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		
		self.text = Entry(self)
		self.text.grid()
		
		self.button1 = Button(self, text="Verify", command=self.updateLabel)
		self.button1.grid()
		
		#res = self.check("hopeso.inc@gmail.com")
				
	def updateLabel(self):
		var = StringVar()
		label = Label( self, textvariable=var )		
		self.data = self.text.get()
		var.set(self.check(self.data))
		label.grid()
		
	def check(self,addressToVerify):
		#################################SYNTAX#################################
		import re
		#addressToVerify = raw_input("email:")
		if addressToVerify!="":
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
			if match == None:
				print('Bad Syntax')
				#raise ValueError('Bad Syntax')
				return "Invalid Syntax"
			else:
				mailName = addressToVerify.split('@')[0]
				mailDomain = addressToVerify.split('@')[1]
				print "mail name: " + mailName + " mail domain: " + mailDomain			
				print mailName + " syntax is Valid"
		else:
			print "Address is empty."
			return 0

		###################################MX###################################
		import dns.resolver
		print "checking mx record..."

		try:
			records = dns.resolver.query(mailDomain, 'MX')
		except Exception as exc:
			print "no MX record found"
			exit()
			
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
		print mxRecord 

		##################################SMTP##################################
		import socket
		import smtplib

		print "checking smtp..."
		# Get local server hostname
		host = socket.gethostname()

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(1)

		# SMTP Conversation
		con = server.connect(mxRecord)
		#print "connected "
		print con

		helo = server.helo(host)
		#print "helo success" 
		print helo

		source = server.mail('admin@imail.sunway.edu.my')
		#print "mail from:"
		print source

		code, message = server.rcpt(str(addressToVerify))
		#print "rcpt result: "
		print code

		server.quit()
		#print "connection quit normal"

		# Assume 250 as Success
		if code == 250:
			return addressToVerify+" is valid."
		else:
			return addressToVerify+" is invalid."


root = Tk()
root.title("Email Verifier")
root.geometry("200x100")

app = Applicaion(root)

root.mainloop()
