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

    #This is file where we will put output
    #ODS extension is for LibreOffice Calc
    fd = open(r'linuxOutputFile.ODS','w')
    old_stdout = sys.stdout
    sys.stdout = fd


    #Calling function 'SSHCommand' and giving her arguments:
    # - 1. Hostname or ip address
    # - 2. Port
    # - 3. Username
    # - 4. Password
    # - 5. Command
    sshCommand('cnr1.vektor.net', 22, 'root', 'ili/.Wae4d', 'nrcmd -N podrska -P Roo8kae2 -C cnr1 scope cpe-beograd-091-185-104-000/21 listLeases > linuxOutputFile.ODS') #First command
    sshCommand('cnr1.vektor.net', 22, 'root', 'ili/.Wae4d', 'sed -n "/relay-agent-remote-id=/{s/.*relay-agent-remote-id=//;s/\S*=.*//;p}" linuxOutputFile.ODS') #Second command

    fd.close() # Closing file
