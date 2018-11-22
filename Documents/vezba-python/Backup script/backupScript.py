#  Purpose : Backup script (show running-config)
#  Author : Aleksandar Mitrovic
#  Date : 2018-10-02

#This script is running on Python -v2
import getpass
import paramiko #$ pip install paramiko (paramiko module)
import sys
import os

def sshCommand(hostname, port, username, password, command): #Funciton sshCommand
    sshClient = paramiko.SSHClient()

    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(hostname, port, username, password)
    stdin, stdout, stderr = sshClient.exec_command(command)
    print(stdout.read())

if __name__=='__main__':

    hostname = raw_input("Please enter SSH hostname: ") #You need to enter SSH hostname or IP address
    username = raw_input("Please enter Username: ") #You need to enter Username
    password = getpass.getpass("Please enter Password: ") #You need to enter Password

    #This is file where we will put output
    fd = open(r'outputFile.txt','w')
    old_stdout = sys.stdout
    sys.stdout = fd


    #Calling function 'SSHCommand' and giving her arguments:
    # - 1. Hostname or ip address
    # - 2. Port
    # - 3. Username
    # - 4. Password
    # - 5. Command
    sshCommand(hostname, 22, username, password, 'show  running-config') #First command
    sshCommand(hostname, 22, username, password, 'show ip interface brief') #First command


    fd.close()

    os.system("subl outputFile.txt")
