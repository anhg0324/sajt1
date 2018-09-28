#  Namena   :
#  Korisnik : CLI
#  Autor(i) : Aleksandar Mitrovic
#  Datum(i) : 2018-9-27

#This script is running on Python -v2

import paramiko #$ pip install paramiko (paramiko module)
import sys
import os

def sshCommand(hostname, port, username, password, command): #Funciton SSHCommand
    sshClient = paramiko.SSHClient()

    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(hostname, port, username, password)
    stdin, stdout, stderr = sshClient.exec_command(command)
    print(stdout.read())

if __name__=='__main__':

    scope = raw_input("Please enter scope: ") #You need to enter name of the scope here

    #This is file where we will put output
    #ODS extension is for LibreOffice Calc
    fd = open(r'linuxOutputFile.ods','w')
    old_stdout = sys.stdout
    sys.stdout = fd


    #Calling function 'SSHCommand' and giving her arguments:
    # - 1. Hostname or ip address
    # - 2. Port
    # - 3. Username
    # - 4. Password
    # - 5. Command
    sshCommand('cnr1.vektor.net', 22, '***', '***', 'nrcmd -N podrska -P Roo8kae2 -C cnr1 scope '+scope+' listLeases > linuxOutputFile.ods') #First command
    sshCommand('cnr1.vektor.net', 22, '***', '***', 'sed -n "/relay-agent-remote-id=/{s/.*relay-agent-remote-id=//;s/\S*=.*//;p}" linuxOutputFile.ods') #Second command

    fd.close() # Closing file
