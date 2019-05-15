#################################
#
# James Remer
# VirtualBox Automation
# Date Created: 4/5/19
# Late Updated: 5/1/19
#
# Description: Request Functions
#
#################################
import requests
import xml.etree.ElementTree as ET
from virtual_machines import VirtualMachine

#Code for Logon Request provided by Joe Axberg (lines 16 - 57)
#here is the web url for the vbox webservice
url = 'http://localhost:18083'

#need to include http headers, so the server responds properly
headers = {'content-type':'text/xml'}

#define the namespace of the vbox webservice (trust me you need this)
namespaces = {'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','vbox':'http://www.virtualbox.org/'}

#here is the body of a SOAP require to start a Session with the webservice
#we firt need  to establish a session, so that we can access the API
#remember to start the vbox webservice without Authentication: 
#cd to c:\Program Files\Oracle\VirtualBox
#then run this .exe:  .\VBoxWebSrv.exe -A null
#the -A null mean start the web api with no authentication

def logon(url,headers,namespaces):

    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IWebsessionManager_logon>
    <username>?</username>
    <password>?</password>
    </vir:IWebsessionManager_logon>
    </soapenv:Body>
    </soapenv:Envelope>"""

    #now lets call the webservice and put the result in the variable response:
    response = requests.post(url,data=body,headers=headers)

    #use the xml parser to parse the raw XML and put into variable 
    xmltree = ET.fromstring(response.content)

    #now find the return value ID in the XML
    sessionval = xmltree.findall('./SOAP-ENV:Body''/vbox:IWebsessionManager_logonResponse''/returnval',namespaces)

    #print out the text of that element - it is a list
    #returnval is the session ID
    sessionID = sessionval[0].text
    
    print("\n\nSession ID is: "+ sessionID)
    
    return sessionID


def parseReturnVal(body, url, headers, namespaces):
    response = requests.post(url,data=body,headers=headers)

    xmltree = ET.fromstring(response.content)

    returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IVirtualBox_getMachinesResponse''/returnval',namespaces)

    return returnval

#
# Get Functions
#

def getNames(url,headers,namespaces,VMlist):
    for i in range(len(VMlist)):

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getName>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        </vir:IMachine_getName>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getNameResponse''/returnval',namespaces)

        #get the name of each machine
        VMlist[i].name = returnval[0].text
        #return VM list with machine names
    return VMlist


def getRAM(url, headers, namespaces, VMlist):
    for i in range(len(VMlist)):

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getMemorySize>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        </vir:IMachine_getMemorySize>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getMemorySizeResponse''/returnval',namespaces)
        memory = returnval[0].text + " MB"
        VMlist[i].memorySize = memory
    #get and return the RAM for each machine
    return VMlist


def getVideoRAM(url,headers, namespaces, VMlist):
     for i in range(len(VMlist)):

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getVRAMSize>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        </vir:IMachine_getVRAMSize>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getVRAMSizeResponse''/returnval',namespaces)
        vmemory = returnval[0].text + " MB"
        VMlist[i].vramSize = vmemory
    #return the video RAM for each machine
     return VMlist


def getOSType(url,headers,namespaces,VMlist):
    for i in range(len(VMlist)):

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getOSTypeId>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        </vir:IMachine_getOSTypeId>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getOSTypeIdResponse''/returnval',namespaces)
        
        VMlist[i].osType = returnval[0].text
    #Return the OS for each machine
    return VMlist


def getAttachmentType(url,headers,namespaces,VMlist):
    for i in range(len(VMlist)):

        #First get an ID for the machine's adapter
        #(One machine has 4 adapter slots)
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getNetworkAdapter>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        <slot>0</slot>
        </vir:IMachine_getNetworkAdapter>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getNetworkAdapterResponse''/returnval',namespaces)
        adapterID = returnval[0].text

        #Get the attachment type after getting the adapter ID
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:INetworkAdapter_getAttachmentType>
        <_this>"""+ adapterID +"""</_this>
        </vir:INetworkAdapter_getAttachmentType>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:INetworkAdapter_getAttachmentTypeResponse''/returnval',namespaces)

        VMlist[i].netAdapter = returnval[0].text
    #return each machine's attachment type
    return VMlist

def getState(url, headers, namespaces, VMlist):
    for i in range(len(VMlist)):

        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <vir:IMachine_getState>
        <_this>"""+ VMlist[i].machineID +"""</_this>
        </vir:IMachine_getState>
        </soapenv:Body>
        </soapenv:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        xmltree = ET.fromstring(response.content)
        returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getStateResponse''/returnval',namespaces)

        VMlist[i].state = returnval[0].text
    #return each machine's current state (PoweredOn, PoweredOff, Save State)
    return VMlist


def getMachines(url,headers,namespaces,sessionID):
    
    body= """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IVirtualBox_getMachines>
    <_this>""" + sessionID + """</_this>
    </vir:IVirtualBox_getMachines>
    </soapenv:Body>
    </soapenv:Envelope>"""

    #save the machine IDs
    machineIDList = parseReturnVal(body, url, headers, namespaces)

    VMlist = []
    
    #Create an object for each virtual machine and store them in a list
    for val in machineIDList:
        #Save the machine's ID as an attribute
        VMlist = VMlist + [VirtualMachine('null', 'null', 'null', 'null', 'null', 'null', val.text)]

    #Save attributes (name, memorySize, vRAMSize, OSType, AttachmentType, state)
    VMlist = getNames(url,headers,namespaces,VMlist)
    VMlist = getRAM(url,headers,namespaces,VMlist)
    VMlist = getVideoRAM(url,headers,namespaces,VMlist)
    VMlist = getOSType(url, headers, namespaces, VMlist)
    VMlist = getAttachmentType(url,headers,namespaces,VMlist)
    VMlist = getState(url,headers,namespaces,VMlist)
    
    return VMlist
    
#
# Changing Machine Settings
#

def getSessionObject(url,headers,namespaces,sessionID):

    #Get a session object ID needed for changing any machine settings
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IWebsessionManager_getSessionObject>
    <refIVirtualBox>"""+ sessionID +"""</refIVirtualBox>
    </vir:IWebsessionManager_getSessionObject>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    xmltree = ET.fromstring(response.content)
    returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IWebsessionManager_getSessionObjectResponse''/returnval',namespaces)

    sessionObjectID = returnval[0].text
    print("Session Object is: " + sessionObjectID)

    return sessionObjectID


def lockMachine(url,headers,Vmachine,sessionObjectID):

    #locks the selected machine using the generated session Object
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_lockMachine>
    <_this>"""+ Vmachine +"""</_this>
    <session>"""+ sessionObjectID +"""</session>
    <lockType>Write</lockType>
    </vir:IMachine_lockMachine>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

def getMachineCopy(url, headers,namespaces,sessionObjectID):

    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:ISession_getMachine>
    <_this>"""+ sessionObjectID +"""</_this>
    </vir:ISession_getMachine>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    xmltree = ET.fromstring(response.content)
    returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:ISession_getMachineResponse''/returnval',namespaces)
    machineCopy = returnval[0].text

    #return a mutable copy of the machine which can have changes made to it
    return machineCopy

def saveSettings(url,headers,machineCopy):

    #Saves setting changes made to the mutable copy to the real machine
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_saveSettings>
    <_this>"""+ machineCopy +"""</_this>
    </vir:IMachine_saveSettings>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

def unlockMachine(url,headers,sessionObjectID):

    #unlocks the machine after saving any changes
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:ISession_unlockMachine>
    <_this>"""+ sessionObjectID +"""</_this>
    </vir:ISession_unlockMachine>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

#
# Set Functions
#

def setName(url, headers, machineCopy, newName):

    #changes the name of a machine
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_setName>
    <_this>"""+ machineCopy +"""</_this>
    <name>"""+ newName +"""</name>
    </vir:IMachine_setName>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

def setRAM(url, headers, machineCopy, newRAM):

    #changes the RAM of a machine
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_setMemorySize>
    <_this>"""+ machineCopy +"""</_this>
    <memorySize>"""+ newRAM +"""</memorySize>
    </vir:IMachine_setMemorySize>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

def setVideoRAM(url,headers,machineCopy,newVRAM):

    #changes the video RAM of a machine
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_setVRAMSize>
    <_this>"""+ machineCopy +"""</_this>
    <VRAMSize>"""+ newVRAM +"""</VRAMSize>
    </vir:IMachine_setVRAMSize>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

def setNetAdapter(url, headers,namespaces, machineCopy, newNetAdpt):

    #changes the Attachment Type of a machine
    #(must first get a network adapter ID)
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_getNetworkAdapter>
    <_this>"""+ machineCopy +"""</_this>
    <slot>0</slot>
    </vir:IMachine_getNetworkAdapter>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    xmltree = ET.fromstring(response.content)
    returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IMachine_getNetworkAdapterResponse''/returnval',namespaces)
    adapterCopyID = returnval[0].text

    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:INetworkAdapter_setAttachmentType>
    <_this>"""+ adapterCopyID +"""</_this>
    <attachmentType>"""+ newNetAdpt +"""</attachmentType>
    </vir:INetworkAdapter_setAttachmentType>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return


def setOSType(url,headers,machineCopy,newOS):

    #changes the machine's OS Type ID
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_setOSTypeId>
    <_this>"""+ machineCopy +"""</_this>
    <OSTypeId>"""+ newOS +"""</OSTypeId>
    </vir:IMachine_setOSTypeId>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return



#
# Create Virtual Machine
#

def createMachine(url,headers,namespaces,sessionID,newName):

    #Will create a new machine
    #(the machine will not be recognizable by VirtualBox)
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IVirtualBox_createMachine>
    <_this>"""+ sessionID +"""</_this>
    <settingsFile></settingsFile>
    <name>"""+ newName +"""</name>
    <!--Zero or more repetitions:-->
    <groups></groups>
    <osTypeId></osTypeId>
    <flags></flags>
    </vir:IVirtualBox_createMachine>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    xmltree = ET.fromstring(response.content)
    returnval = xmltree.findall('./SOAP-ENV:Body''/vbox:IVirtualBox_createMachineResponse''/returnval',namespaces)
    newMachineID = returnval[0].text
    #returns an ID for the newly created machine
    return newMachineID


def registerMachine(url, headers, sessionID, newMachineID):

    #Registers the machine so it is recognized by VirtualBox
    #(Needed to create a new virtual machine)
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IVirtualBox_registerMachine>
    <_this>"""+ sessionID +"""</_this>
    <machine>"""+ newMachineID +"""</machine>
    </vir:IVirtualBox_registerMachine>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return

#
# Launch VM
#

def launchMachine(url, headers, sessionObjectID, machineID):

    #Will launch a selected VM
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vir="http://www.virtualbox.org/">
    <soapenv:Header/>
    <soapenv:Body>
    <vir:IMachine_launchVMProcess>
    <_this>"""+ machineID +"""</_this>
    <session>"""+ sessionObjectID +"""</session>
    <name></name>
    <environment></environment>
    </vir:IMachine_launchVMProcess>
    </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    return


#TEST: Logon and get a session ID
'''
sessionID = logon(url,headers,namespaces)
VMdata = getMachines(url,headers,namespaces,sessionID)
sessionObjectID = getSessionObject(url,headers,namespaces,sessionID)

launchID = VMdata[2].machineID

#test launching a VM
#launchMachine(url,headers,sessionObjectID,launchID)
'''