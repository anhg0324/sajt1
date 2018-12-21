
#  Purpose : GPON Script
#  Author : Aleksandar Mitrovic
#  Date : 2018-11-22

#  This script is running on Python -v2

import paramiko
import time

########################################################################################################################
# SSH Connect section
########################################################################################################################

hostname = raw_input("\n\nYou can type hostname or number:\n\n"
                     "OLT-VP-1 or 1\n"
                     "OLT-SC-1 or 2\n"
                     "OLT-SU-1 or 3\n\n"
                     "Your choice: "
                     )

if hostname == "OLT-VP-1" or hostname == "olt-vp-1" or hostname == "1":  # You can type number or hostname
    ip = "olt-vp-1.vektor.net"  # Enter FQDN or ip address
    username = "noc"  # Enter Username
    password = "ip5NaeZ*"  # Enter Password

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)

    remote_conn = remote_conn_pre.invoke_shell()
    output = remote_conn.recv(65535)
    print(output)

    remote_conn.send("show run int gpon-olt_1/1/1\n"
                     "show run int gpon-olt_1/1/2\n"
                     "show run int gpon-olt_1/1/3\n"
                     )
    time.sleep(.10)
    output = remote_conn.recv(65535)
    print(output)

    remote_conn.send("!\n!\n!\n!\n!\n!\nshow gpon onu uncfg\n!\n!\n!\n!\n!\n!\n")
    time.sleep(.1)
    output = remote_conn.recv(65535)
    print(output)

elif hostname == "OLT-SC-1" or hostname == "olt-sc-1" or hostname == "2":  # You can type number or hostname
    ip = "olt-sc-1.vektor.net"  # Enter FQDN or ip address
    username = "noc"  # Enter Username
    password = "ip5NaeZ*"  # Enter Password

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)

    remote_conn = remote_conn_pre.invoke_shell()
    output = remote_conn.recv(65535)
    print(output)

    print ("This OLT is not working.")

    time.sleep(.5)
    output = remote_conn.recv(65535)
    print(output)

    remote_conn.send("!\n!\n!\n!\n!\n!\nshow gpon onu uncfg\n!\n!\n!\n!\n!\n!\n")
    time.sleep(.1)
    output = remote_conn.recv(65535)
    print(output)

elif hostname == "OLT-SU-1" or hostname == "olt-su-1" or hostname == "3":  # You can type number or hostname
    ip = "olt-su-1.vektor.net"  # Enter FQDN or ip address
    username = "noc"  # Enter Username
    password = "ip5NaeZ*"  # Enter Password

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)

    remote_conn = remote_conn_pre.invoke_shell()
    output = remote_conn.recv(65535)
    print(output)

    remote_conn.send("show run int gpon-olt_1/1/1\n"
                     "show run int gpon-olt_1/1/2\n"
                     )
    time.sleep(.5)
    output = remote_conn.recv(65535)
    print(output)

    remote_conn.send("!\n!\n!\n!\n!\n!\nshow gpon onu uncfg\n!\n!\n!\n!\n!\n!\n")
    time.sleep(.1)
    output = remote_conn.recv(65535)
    print(output)

else:
    print ("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
           "\nWrong choice. Try again. \n"
           "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
           )
    exit()

remote_conn.send("configure terminal\n") # Config terminal CISCO Ios command
time.sleep(.1)
noOutput = remote_conn.recv(65535)


############################################################

############################################################

possibleNumberOfOlt = ["0", "1", "2", "3"]  # Maximum 2 phones

while True:
    NumberOfOltInterface = raw_input("Last number of OLT interface number (E.g. 1 - 16): ")

    if NumberOfOltInterface not in possibleNumberOfOlt:  # If number higher than 16, try again
        print ("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
               "\nWrong choice. Try again. \n"
               "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
               )
    else:

        remote_conn.send("interface gpon-olt_1/1/"+NumberOfOltInterface+"\n")  # E.g gpon-olt_1/1/(1)
        time.sleep(.1)

        ordinalNumberOfOnuInterface = raw_input("Ordinal number of ONU interface: ")
        typeOfOnuDevice = raw_input("Type of ONU device (E.g ZTE-F660): ")
        serialNumberOfOnuDevice = raw_input("Serial number of ONU device (Npr. ZTEGC80538EB): ")

        remote_conn.send("onu "+ordinalNumberOfOnuInterface+" type "+typeOfOnuDevice+" sn "+serialNumberOfOnuDevice+"\n")
        time.sleep(.1)

        remote_conn.send("exit\n")
        time.sleep(.1)

        remote_conn.send("interface gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n")
        time.sleep(.1)
        output = remote_conn.recv(65535)
        print(output)

        contractNumber = raw_input("Contract number: ")

        remote_conn.send("name "+contractNumber+"\n")
        time.sleep(.1)
        print("\n\nContract number is: "+contractNumber+"\n\n")

        remote_conn.send("sn-bind enable sn\n")
        time.sleep(.1)
        output = remote_conn.recv(65535)
        print(output)

        internetUploadSpeed = raw_input("Speed of UPLOAD packet ( Only number of speed e.g. 50): ")

        remote_conn.send("tcont 1 name INTERNET profile INTERNET-"+internetUploadSpeed+"M-UPLOAD\n")
        time.sleep(.1)
        print("\n\n Package is: INTERNET-"+internetUploadSpeed+"M-UPLOAD\n\n")

        possibleNumberOfPhones = ["0", "1", "2"]  # Maximum 2 phones

        while True:
            howManyPhoneNumbers = raw_input("How many phone numbers: (0, 1, 2): ")

            if howManyPhoneNumbers not in possibleNumberOfPhones:  # if number is higher than 2, try again
                print("You need to choose number from 0 to 2")

            else:  # if number is not higher than 2, continue

                ########################################################################################################################

                # Section for two phones

                ########################################################################################################################

                if howManyPhoneNumbers == "2":
                    phoneNumber1 = str(raw_input("Enter first phone number ( E.g. +381114285172 ): "))
                    print ("\n\nFirst phone number is: "+phoneNumber1+"\n\n")
                    passForPhoneNumber1 = raw_input("Enter password: ")

                    phoneNumber2 = str(raw_input("Enter second phone number ( E.g. +381114285172 ): "))
                    print ("\n\nSecond phone number is: "+phoneNumber2+"\n\n")
                    passForPhoneNumber2 = raw_input("Enter password: ")

                    remote_conn.send("tcont 2 name MNG profile MNG\n"
                                     "gemport 1 name INTERNET tcont 1\n"
                                     "gemport 2 name MNG tcont 2\n"
                                     "switchport mode hybrid vport 1\n"
                                     "switchport mode hybrid vport 2\n"
                                     "service-port 1 vport 1 user-vlan 64 vlan 64\n"
                                     "service-port 2 vport 2 user-vlan 63 vlan 63\n"
                                     )
                    time.sleep(.1)

                    internetDownloadSpeed = raw_input("Speed of DOWNLOAD packet ( Only number of speed e.g. 50): ")
                    remote_conn.send("traffic-profile INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD vport 1 direction egress\nexit\n")
                    time.sleep(.1)
                    print("\n\n Package is: INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD\n\n")

                    remote_conn.send("pon-onu-mng gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "voip protocol sip\n"                                                                        
                                     "voip-ip mode dhcp vlan-profile sip-netcast host 3\n"                                                                                                                                                                                                                      
                                     "flow 2 switch switch_0/1\n"
                                     "flow 3 switch switch_0/1\n"
                                                                                              
                                     "flow mode 1 tag-filter vlan-filter untag-filter discard\n"
                                     "flow mode 2 tag-filter vlan-filter untag-filter discard\n"
                                     "flow mode 3 tag-filter vlan-filter untag-filter discard\n"
                                                                                                                   
                                     "flow 1 pri 0 vlan 64\n"
                                     "flow 2 pri 2 vlan 63\n"
                                     "flow 3 pri 5 vlan 65\n"
                                                                                                                       
                                     "gemport 1 flow 1\n"
                                     "gemport 2 flow 2\n"
                                     "gemport 3 flow 3\n"
                                                                                                                      
                                     "switchport-bind switch_0/1 iphost 1\n"
                                     "switchport-bind switch_0/1 iphost 2\n"
                                                                                                                       
                                     "sip-service pots_0/1 profile sip-netcast userid "+phoneNumber1+" username "+phoneNumber1+" password "+passForPhoneNumber1+"\n"
                                     "sip-service pots_0/2 profile sip-netcast userid "+phoneNumber2+" username "+phoneNumber2+" password "+passForPhoneNumber2+"\n"                                                                                                  
                                                                                                                       
                                     "ip-host 1 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "ip-host 2 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "ip-host 2 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                                                                                                                                                
                                     "vlan-filter-mode iphost 1 tag-filter pri-vlan-filter untag-filter discard\n"
                                     "vlan-filter-mode iphost 2 tag-filter pri-vlan-filter untag-filter discard\n"
                                                                                                                                                                
                                     "vlan-filter iphost 1 pri 0 vlan 64\n"
                                     "vlan-filter iphost 2 pri 2 vlan 63\n"
                                                                                                                                                                
                                     "security-mgmt 10 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 10 start-src-ip 109.122.101.81 end-src-ip 109.122.101.94\n"
                                     "security-mgmt 20 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 20 start-src-ip 109.122.96.1 end-src-ip 109.122.96.31\n"
                                     "security-mgmt 30 state enable mode forward ingress-type iphost 2 protocol telnet\n"
                                     "security-mgmt 30 start-src-ip 192.168.100.1 end-src-ip 192.168.100.1\n"
                                     "security-mgmt 40 state enable ingress-type lan protocol telnet ssh snmp\n"
                                    
                                     "end\n"
                                     )
                    time.sleep(.30)
                    noOutput = remote_conn.recv(65535)

                    print ("\n\n\n\n\n\nConfiguration successful.\n\n\n\n\n\n")

                    remote_conn.send("show run int gpon-olt_1/1/"+NumberOfOltInterface+"\n"
                                     "show run int gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 1\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 2\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 3\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 4\n"
                                     "show pon power attenuation gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     )
                    time.sleep(.30)
                    output = remote_conn.recv(65535)
                    print(output)

                ########################################################################################################################

                # Section for one phone

                ########################################################################################################################

                elif howManyPhoneNumbers == "1":
                    phoneNumber = raw_input("Enter phone number ( E.g. +381114285172 ): ")
                    print ("\n\nPhone number is: "+phoneNumber+"\n\n")
                    passForPhoneNumber = raw_input("Enter password: ")

                    remote_conn.send("tcont 2 name MNG profile MNG\n"
                                     "tcont 3 name VOIP profile VOIP\n"
                                      
                                     "gemport 1 name INTERNET tcont 1\n"
                                     "gemport 2 name MNG tcont 2\n"
                                     "gemport 3 name VOIP tcont 3\n"
                                      
                                     "switchport mode hybrid vport 1\n"
                                     "switchport mode hybrid vport 2\n"
                                     "switchport mode hybrid vport 3\n"
                                      
                                     "service-port 1 vport 1 user-vlan 64 vlan 64\n"
                                     "service-port 2 vport 2 user-vlan 63 vlan 63\n"
                                     "service-port 3 vport 3 user-vlan 65 vlan 65\n"
                                     )

                    internetDownloadSpeed = raw_input("Speed of DOWNLOAD packet ( Only number of speed e.g. 50): ")
                    remote_conn.send("traffic-profile INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD vport 1 direction egress\nexit\n")
                    time.sleep(.1)

                    print("\n\n Package is: INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD\n\n")

                    remote_conn.send("pon-onu-mng gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "voip protocol sip\n"                                                                        
                                     "voip-ip mode dhcp vlan-profile sip-netcast host 3\n"                                                                                                                                                                                                                      
                                     "flow 2 switch switch_0/1\n"
                                     "flow 3 switch switch_0/1\n"
                                                                                              
                                     "flow mode 1 tag-filter vlan-filter untag-filter discard\n"
                                     "flow mode 2 tag-filter vlan-filter untag-filter discard\n"
                                     "flow mode 3 tag-filter vlan-filter untag-filter discard\n"
                                                                                                                   
                                     "flow 1 pri 0 vlan 64\n"
                                     "flow 2 pri 2 vlan 63\n"
                                     "flow 3 pri 5 vlan 65\n"
                                                                                                                       
                                     "gemport 1 flow 1\n"
                                     "gemport 2 flow 2\n"
                                     "gemport 3 flow 3\n"
                                                                                                                      
                                     "switchport-bind switch_0/1 iphost 1\n"
                                     "switchport-bind switch_0/1 iphost 2\n"
                                                                                                                       
                                     "sip-service pots_0/1 profile sip-netcast userid "+phoneNumber+" username "+phoneNumber+" password "+passForPhoneNumber+"\n"
                                                                                                                       
                                     "ip-host 1 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "ip-host 2 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "ip-host 2 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                                                                                                                                                
                                     "vlan-filter-mode iphost 1 tag-filter pri-vlan-filter untag-filter discard\n"
                                     "vlan-filter-mode iphost 2 tag-filter pri-vlan-filter untag-filter discard\n"
                                                                                                                                                                
                                     "vlan-filter iphost 1 pri 0 vlan 64\n"
                                     "vlan-filter iphost 2 pri 2 vlan 63\n"
                                                                                                                                                                
                                     "security-mgmt 10 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 10 start-src-ip 109.122.101.81 end-src-ip 109.122.101.94\n"
                                     "security-mgmt 20 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 20 start-src-ip 109.122.96.1 end-src-ip 109.122.96.31\n"
                                     "security-mgmt 30 state enable mode forward ingress-type iphost 2 protocol telnet\n"
                                     "security-mgmt 30 start-src-ip 192.168.100.1 end-src-ip 192.168.100.1\n"
                                     "security-mgmt 40 state enable ingress-type lan protocol telnet ssh snmp\n"
                                    
                                     "end\n"
                                     )
                    time.sleep(.30)
                    noOutput = remote_conn.recv(65535)

                    print ("\n\n\n\n\n\nConfiguration successful.\n\n\n\n\n\n")

                    remote_conn.send("show run int gpon-olt_1/1/"+NumberOfOltInterface+"\n"
                                     "show run int gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 1\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 2\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 3\n"
                                     "show pon power attenuation gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     )
                    time.sleep(.30)
                    output = remote_conn.recv(65535)
                    print(output)

                ########################################################################################################################

                # Section when there is no phone

                ########################################################################################################################

                else:
                    remote_conn.send("tcont 2 name MNG profile MNG\n"
                                     "gemport 1 name INTERNET tcont 1\n"
                                     "gemport 2 name MNG tcont 2\n"
                                     "switchport mode hybrid vport 1\n"
                                     "switchport mode hybrid vport 2\n"
                                     "service-port 1 vport 1 user-vlan 64 vlan 64\n"
                                     "service-port 2 vport 2 user-vlan 63 vlan 63\n"
                                     "ip dhcp snooping enable vport 1\n"
                                     "ip-source-guard enable sport 1\n"
                                     )
                    time.sleep(.1)
                    Output = remote_conn.recv(65535)

                    internetDownloadSpeed = raw_input("Speed of DOWNLOAD packet ( Only number of speed e.g. 50): ")
                    remote_conn.send("traffic-profile INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD vport 1 direction egress\nexit\n")
                    time.sleep(.1)
                    print("\n\n Package is: INTERNET-"+internetDownloadSpeed+"M-DOWNLOAD\n\n")

                    remote_conn.send("pon-onu-mng gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "flow 2 switch switch_0/1\n"
                                     "flow mode 1 tag-filter vlan-filter untag-filter discard\n"
                                     "flow mode 2 tag-filter vlan-filter untag-filter discard\n"
                                     "flow 1 pri 0 vlan 64\n"
                                     "flow 2 pri 2 vlan 63\n"
                                     "gemport 1 flow 1\n"
                                     "gemport 2 flow 2\n"
                                     "switchport-bind switch_0/1 iphost 1\n"
                                     "switchport-bind switch_0/1 iphost 2\n"
                                     "ip-host 1 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "ip-host 2 dhcp-enable enable ping-response enable traceroute-response enable\n"
                                     "vlan-filter-mode iphost 1 tag-filter pri-vlan-filter untag-filter discard\n"
                                     "vlan-filter-mode iphost 2 tag-filter pri-vlan-filter untag-filter discard\n"
                                     "vlan-filter iphost 1 pri 0 vlan 64\n"
                                     "vlan-filter iphost 2 pri 2 vlan 64\n"
                                     "security-mgmt 10 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 10 start-src-ip 109.122.101.81 end-src-ip 109.122.101.94\n"
                                     "security-mgmt 20 state enable mode forward ingress-type iphost 2 protocol web telnet\n"
                                     "security-mgmt 20 start-src-ip 109.122.96.1 end-src-ip 109.122.96.31\n"
                                     "security-mgmt 30 state enable mode forward ingress-type iphost 2 protocol telnet\n"
                                     "security-mgmt 30 start-src-ip 192.168.100.1 end-src-ip 192.168.100.1\n"
                                     "security-mgmt 40 state enable ingress-type lan protocol telnet ssh snmp\n"
                                    
                                     "end\n"
                                     )
                    time.sleep(.30)
                    noOutput = remote_conn.recv(65535)

                    print ("\n\n\n\n\n\nConfiguration successful.\n\n\n\n\n\n")

                    remote_conn.send("show run int gpon-olt_1/1/"+NumberOfOltInterface+"\n"
                                     "show run int gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 1\n"
                                     "show gpon remote-onu ip-host gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+" 2\n"
                                     "show pon power attenuation gpon-onu_1/1/"+NumberOfOltInterface+":"+ordinalNumberOfOnuInterface+"\n"
                                     )
                    time.sleep(.30)
                    output = remote_conn.recv(65535)
                    print(output)
                break
        break
