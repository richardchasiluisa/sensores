
try:
        from BaseHTTPServe import BaseHTTPRequestHandler,HTTPServer
except:
        from http.server import BaseHTTPRequestHnadler,HTTPServer
from os import curdir, sep

try:
        from urlparse import urlparse
        from urlparse import urlparse,pare_qs
except:
        from urllib.parse import urlparse, parse_qs
import os
port = int(os.environ.get("PORT",8000))
                
PORT_NUMBER =port

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from urlparse import urlparse
from urlparse import urlparse, parse_qs




pot0=0
pot1=0
#This class will handles any incoming request from
#the browser 
def getArguments(path):
        global pot0,pot1
        try:
                print path
                query = urlparse(path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                print query_components
                try:
                        pot0= query_components['sen0']
                except:
                        pass
                try:
                        pot1= query_components['sen1']
                except:
                        pass
                print(pot0,pot1)


		#sensor= query_components['sensor']
		#print sensor
		#imsi = query_components["imsi"]

        except:
                print ('No argumentos')
def action(path):
	getArguments(path)
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		global pot0,pot1
		if self.path=="/":
			self.path="/index.html"
		elif self.path.find('?'):
			print self.path
			#query_components = parse_qs(urlparse(self.path).query)
			#imsi = query_components["imsi"] 
			action(self.path)
			self.path="/index.html"
			#print query_components

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				data=f.read()
				data= data.replace('pot0',str(pot0)).replace('pot1',str(pot1))
				try:
                                        self.wfile.write(data)
                                except:
                                        self.write.write(bytes(data,'UTF-8'))
				f.close()
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()



except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
