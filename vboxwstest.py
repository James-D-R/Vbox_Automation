import requests
import xml.etree.ElementTree as ET

#here is the web url for the vbox webservice
url = 'http://localhost:18083'

#need to include http headers, so the server responds properly
headers = {'content-type':'text/xml'}

#here is the body of a SOAP require to start a Session with the webservice
#we firt need  to establish a session, so that we can access the API
#remember to start the vbox webservice without Authentication: 
#cd to c:\Program Files\Oracle\VirtualBox
#then run this .exe:  .\VBoxWebSrv.exe -A null
#the -A null mean start the web api with no authentication
body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
<soapenv:Header/>
<soapenv:Body>
<vir:IWebsessionManager_logon>
<username>?</username>
<password>?</password>
</vir:IWebsessionManager_logon>
</soapenv:Body>
</soapenv:Envelope>"""

#define the namespace of the vbox webservice (trust me you need this)
namespaces = {'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','vbox':'http://www.virtualbox.org/'}

#now lets call the webservice and put the result in the variable response:
response = requests.post(url,data=body,headers=headers)

print("\n\nHere is the raw XML response:\n\n\n" , response.content)

#use the xml parser to parse the raw XML and put into variable 
xmltree = ET.fromstring(response.content)

#now find the return value ID in the XML
sessionval = xmltree.findall('./SOAP-ENV:Body''/vbox:IWebsessionManager_logonResponse''/returnval',namespaces)

print("\n\nHere is the element in the XML we're looking for: \n\n", sessionval)

#print out the text of that element - it is a list

returnval = sessionval[0]
print("\n\nThe return value is: ", returnval.text)

#or iterate through
for val in sessionval:
    print("\n\nIterating instead...")
    print("\nHere are the values", val.text)

