#################################
#
# James Remer
# VirtualBox Automation
# Date Created: 4/5/19
# Late Updated: 5/1/19
#
# Description: Menu. Main program
#
#################################
from virtual_machines import VirtualMachine
from vboxautomation import *
#
# !!!Note!!! - Must start VBoxWebSrv before running!!!
# VBoxWebSrv can be found in c:\Program Files\Oracle\VirtualBox
# run this .exe from the command line before starting: .\VBoxWebSrv.exe -A null
#
# url to communicate with web server
url = 'http://localhost:18083'
# needed to create requests and read return values
headers = {'content-type':'text/xml'}
namespaces = {'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','vbox':'http://www.virtualbox.org/'}

#Log in
print("\n\nLogging in...")
sessionID = logon(url,headers,namespaces)
sessionObject = getSessionObject(url, headers, namespaces, sessionID)

#Main Menu
print("\nSelect an option:\n\n1. Create New Virtual Machine\n2. View Machine Status\n3. Exit\n")
select = eval(input())

#Create new VM
if select == 1:

    #Entering configuration settings for the new VM
    newName = input("\nEnter a name for the new machine:  ")
    newMachine = createMachine(url,headers,namespaces,sessionID,newName)
    newRAM = input("Enter the Memory Size:  ")
    setRAM(url,headers,newMachine,newRAM)
    newVRAM = input("Enter the Video RAM size:  ")
    setVideoRAM(url,headers,newMachine,newVRAM)
    newNetAdpt = input("Enter the Attachment Type:  ")
    setNetAdapter(url,headers,namespaces,newMachine,newNetAdpt)
    newOS = input("Enter the Operating System:  ")
    setOSType(url,headers,newMachine,newOS)

    saveSettings(url,headers,newMachine)
    registerMachine(url,headers,sessionID,newMachine)


#View VM Data
if select == 2:

    print("\n\nGetting Machine Data...\n\n")
    VMList = getMachines(url,headers,namespaces,sessionID)

    check = True
    while check == True:
        #Display Machine Names
        print("\n")
        for i in range(len(VMList)):

            x = str(i + 1)
            print(x +". " + VMList[i].name)
        
        y = len(VMList) + 1

        print(str(y) + ". Exit\n")
            #Wait for input
        selection = eval(input("Select a machine:  "))
        machineIndex = selection - 1

        if selection == y:
            check = False
        
        # Show status of selected machine
        else:

            machine = VMList[selection - 1].machineID
            print("\n\nName: "+ VMList[selection-1].name)
            print("Memory Size: " + VMList[selection-1].memorySize)
            print("Video RAM: " + VMList[selection-1].vramSize)
            print("OS Type: " + VMList[selection-1].osType)
            print("Attachment Type: " + VMList[selection-1].netAdapter)
            print("State: " + VMList[selection-1].state)

            print("\n\nOptions")
            print("1. Launch Machine")
            print("2. Change Settings")
            print("3. Exit\n")

            choice = eval(input("Select an option:  "))

            #Launch a Machine
            if choice == 1:
                print("\n\nLaunching Machine...")
                launchMachine(url,headers,sessionObject,machine)
            
            #Change settings menu
            if choice == 2:

                #Lock machine and get mutable copy
                lockMachine(url,headers,machine,sessionObject)
                machineCopy = getMachineCopy(url,headers,namespaces,sessionObject)
                
                check2 = True
                while check2 == True:

                    print("\n\n1. Set Name\n2. Set Memory Size\n3. Set video RAM\n4. Set Attachment Type\n5. Set OS Type\n6. Done")
                    print("\n")
                    a = eval(input("Select an option:  "))

                    if a == 1:
                        newName = input("Enter the new machine name:  ")
                        setName(url,headers,machineCopy,newName)
                        VMList[machineIndex].name = newName
                    if a == 2:
                        newRAM = input("Enter the new Memory Size:  ")
                        setRAM(url,headers,machineCopy,newRAM)
                        VMList[machineIndex].memorySize = newRAM
                    
                    if a == 3:
                        newVRAM = input("Enter the new Video RAM size:  ")
                        setVideoRAM(url,headers,machineCopy,newVRAM)
                        VMList[machineIndex].vramSize = newVRAM
                    
                    if a == 4:
                        newNetAdpt = input("Enter the new Attachment Type:  ")
                        setNetAdapter(url,headers,namespaces,machineCopy,newNetAdpt)
                        VMList[machineIndex].netAdapter = newNetAdpt

                    if a == 5:
                        newOS = input("Enter the new Operating System:  ")
                        setOSType(url,headers,machineCopy,newOS)
                        VMList[machineIndex].osType = newOS
                    
                    if a == 6:
                        check2 = False

                #Save changes and unlock the machine
                saveSettings(url,headers,machineCopy)
                unlockMachine(url,headers,sessionObject)



