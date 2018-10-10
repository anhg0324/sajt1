#  Purpose : Script for CNR (Cisco network registar)
#  Author : Aleksandar Mitrovic
#  Date : 2018-10-02

#This script is running on Python -v2
import getpass
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


    hostname = 'cnr1.vektor.net' #Hostname
    username = 'root' #Username
    password = getpass.getpass("Please enter password: ") #Password
    scope = raw_input("Please enter scope: ") #Name of scope

    #This is file where we will put output
    #ODS extension is for LibreOffice Calc
    fd = open(r'outputFile.ods','w')
    old_stdout = sys.stdout
    sys.stdout = fd


    #Calling function 'SSHCommand' and giving her arguments:
    # - 1. Hostname or ip address
    # - 2. Port
    # - 3. Username
    # - 4. Password
    # - 5. Command
    sshCommand(hostname, 22, username, password, 'nrcmd -N podrska -P Roo8kae2 -C cnr1 scope '+scope+' listLeases > outputFile.ods') #First command
    sshCommand(hostname, 22, username, password, 'sed -n "/relay-agent-remote-id=/{s/.*relay-agent-remote-id=//;s/\S*=.*//;p}" outputFile.ods') #Second command

    fd.close()

    os.system("xdg-open outputFile.ods")
