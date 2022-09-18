# Python3 code to select
# data from excel
import xlwings as xw
 
# Specifying a sheet
ws = xw.Book("Book1.xlsx").sheets['Sheet1']

vlan_300_list = [   
                    "192.168.50",
                    "192.168.50.254",
                    "192.168.50.0/24",
                    "2001:db8:40ff:19::19:1",
                    "2001:db8:40ff:19::19:0/112"
                ]
#open file                
myFile = open("config.txt", "a")

curr_SGI_IP = ws.range("D" + str(7)).value

i = 7
while i <= 76:
    DP = ws.range("B" + str(i)).value
    UE_IP = ws.range("C" + str(i)).value

    vlan = "301"

    if curr_SGI_IP[:10] in vlan_300_list:
        vlan = "300"

    line = str(int(DP)) + " " + UE_IP + " " + curr_SGI_IP + " " + vlan
    
    myFile.write(line)
    myFile.write('\n')

    i += 1

    next_DP = ws.range("B" + str(i)).value

    if next_DP != DP:
        curr_SGI_IP = ws.range("D" + str(i)).value

myFile.close()

#read line in file

myFile = open("config.txt", "r")
myLine = myFile.readline()

while myLine:
    print(myLine)
    myLine = myFile.readline();
myFile.close()