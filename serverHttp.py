#!/usr/bin/python

try:
        from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
        from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
        from urlparse import urlparse
        from urlparse import urlparse, parse_qs
except:
        from urllib.parse import urlparse, parse_qs

import os
port = int(os.environ.get("PORT", 8080))        
PORT_NUMBER = port

sensor=0
#This class will handles any incoming request from
#the browser
s1=0
s2=0
def getArguments(path):
        global s1,s2
        try:
                #print path
                query = urlparse(path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                print (query_components)
                try:
                        s1= query_components['sensor1']
                except:#EVITA ERRORES JUNTO CON EL TRY
                        pass
                try:
                        s2= query_components['sensor2']
                except:
                        pass
                print (s1,s2)
                #print s2
                #imsi = query_components["imsi"]
        except:
                print ('No argumentos')
def action(path):
        getArguments(path)
class myHandler(BaseHTTPRequestHandler):
        
        #Handler for the GET requests
        def do_GET(self):
                if self.path=="/": #127.0.0.0:8080
                        self.path="/index.html"
                if self.path.find('?'):
                        print (self.path)
                        query_components = parse_qs(urlparse(self.path).query)
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
                                f = open(curdir + sep + self.path) #LEER DOCUMENTO DE TEXTO curdir da el directorio en donde se ejectuta el python es decir f=open("index.html";'r')
                                self.send_response(200)#200 valor de ok para la pag 503 erro de pagina
                                self.send_header('Content-type',mimetype)#mimetype = html
                                self.end_headers()
                                data=f.read()#a la variable data se le asigan el comando de lectura de la variable f
                                data=data.replace('s1',str(s1)).replace('s2',str(s2))#remplaza el texto s1 por el valor de la variable para q [puieda ser impresa como un string
                                try:
                                        self.wfile.write(data)
                                except:
                                        self.wfile.write(bytes(data, 'UTF-8'))
                                f.close()
                        return


                except IOError:
                        self.send_error(404,'File Not Found: %s' % self.path)

try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print ('Started httpserver on port ') , PORT_NUMBER
        
        #Wait forever for incoming htto requests
        server.serve_forever()

except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()
        
