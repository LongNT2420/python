import os

numbPackage = "4"
ethernet = "eth6."
hostName = "8.8.8.8" 

#get UE_IP, SGI_IP, VLAN 
def getInf(info): 
    #global variable
    global DP      
    global UE_IP   
    global SGI_IP  
    global VLAN

    listInfo = info.split()
    DP      = listInfo[0]
    UE_IP   = listInfo[1]
    SGI_IP  = listInfo[2]
    VLAN    = listInfo[3]

#check ipv4 or ipv6
def isIPv6():
    status = UE_IP.find(':')
    return status
    
#add UE_IP For interface
def addIP():   
    global specificUE_IP 
    if(isIPv6() > 0):
        splitUE_IP = UE_IP.split("/", 1)
        tempSplitUE_IP = splitUE_IP[0]
        specificUE_IP = tempSplitUE_IP + '1'
    else:
        splitUE_IP = UE_IP.split("/", 1)
        tempSplitUE_IP = splitUE_IP[0]
        specificUE_IP = tempSplitUE_IP[:len(tempSplitUE_IP) - 1] + '1'
        
    command = "ip addr add " + specificUE_IP + " dev " + ethernet + VLAN
    print(command)
    #os.system(command)

# add static route
def addRoute():
    # ip route add 10.10.20.0/24 via 192.168.50.100 dev eth0
    command = "ip route add " + UE_IP +  " via " + SGI_IP + " dev " + ethernet + VLAN
    print(command)
    #os.system(command)

def pingFunc():
    # ping -c 4 2402:800:f890::/44 8.8.8.8
    command = "ping -c " + numbPackage + " -I " + specificUE_IP + " " + hostName + " > output.txt"
    print(command)
    #os.system(command)

logFile = open("log.txt", "a")

def checkStatus():
    myFile = open("output.txt", "r")
    myLine = myFile.readline()
    status = 0
    while myLine:
        if myLine[0] == numbPackage:
            if myLine[23] != '0': 
                status = 1
            break
        myLine = myFile.readline()
    myFile.close()
    return status

def writeLog():
    status_check = str(checkStatus())
    print(status_check)
    log = specificUE_IP + " " + hostName + " " + status_check
    logFile.write(log)
    logFile.write('\n')

#open config file
configFile = open("config.txt", "r")

lineConfigFile = configFile.readline()

while lineConfigFile:
    getInf(lineConfigFile)
    addIP()
    addRoute()
    pingFunc()
    writeLog()
    lineConfigFile = configFile.readline()
    print('\n')
logFile.close()