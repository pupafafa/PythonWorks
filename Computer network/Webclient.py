import http.client
import pprint
import json
import urllib
import urllib.parse
import requests

def GET(ip,port):
    header = {"User-Agent":"2016024957/LEEWONSEOK/WEBCLIENT/COMPUTERNETWORK"}

    connection = http.client.HTTPConnection(ip,port)
    connection.request("GET", "/test/index.html",body=None,headers=header)
    response = connection.getresponse()

    data = response.read()
    
    print(data)
    connection.close()
   # connection.close() GET 에는 연결 해제 하지 않음!!
def POST(ip,port):

#   header ={'User-Agent': '2016024957 LEEWONSEOK'"Accept": "text/plain"}
    headers = {"Content-type": "text/html", "Accept": "text/plain","User-Agent":"2016024957/LEEWONSEOK/WEBCLIENT/COMPUTERNETWORK"}
  
    # 1. "/test/picResult"
    # 2. "/test/postHandleTest"
    path = int(input("input path number : (1. /test/picResult    2. /test/postHandleTest  :  "))

    connection = http.client.HTTPConnection(ip,port)

    if path==1:
        message=input('Input the answer (Format : student number/Answer number) :  ')
        connection.request("POST",'/test/picResult',message,headers)
        connection.close()

     #   response = connection.getresponse()
      #  data = response.read()
       # print(data)

    if path==2:
        message=input('Input the student number :  ')
        
        connection.request("POST",'/test/postHandleTest',message,headers)
        response = connection.getresponse()
        
        data = response.read()
        print(data)   
        connection.close()
        
     #            
#print("Status: {} and reason: {}".format(response.status, response.reason))

#print("Request headers : {}",format(r_headers)
if __name__=='__main__':
    ip= '127.0.0.1' # std input is also available
    port= int(input('input port number first :  '))
    

    while(True):
        command = int(input("Select Command 1:GET     2:POST    3:Exit  :  "))
        
        if command ==3:
            print("Terminate client")
            break

        if command ==1:
            GET(ip,port)
        
        elif command ==2:
            POST(ip,port)
       

    