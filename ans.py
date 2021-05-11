import subprocess
import sys
import getpass
n = len(sys.argv)
a=sys.argv[1]
password = getpass.getpass(prompt='Password: ', stream=None)
container = input("Container: ")
if a == "create":
    #password = getpass.getpass(prompt='Password: ', stream=None) 
    command = "ansible-playbook -i hosts cont.yml -e container=\"dolly\" -e password=" + password
    subprocess.call([command],shell=True)
if a == "delete":
    command = "ansible-playbook -i hosts del.yml -e container=\"dolly\" -e password=" + password
    subprocess.call([command],shell=True)
