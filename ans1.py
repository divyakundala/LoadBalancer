import subprocess
import sys
import getpass
from csv import reader


def create_container(container_name, password):
    command = "ansible-playbook -i hosts cont.yml -e container="+ container_name + " -e password=" + password
    subprocess.call([command],shell=True)

def delete_container(container_name, password):
    command = "ansible-playbook -i hosts del.yml -e container=" + container_name + " -e password=" + password
    subprocess.call([command],shell=True)

if __name__ == '__main__':
    n = len(sys.argv)
    a=sys.argv[1]
    password = getpass.getpass(prompt='Password: ', stream=None)
    header=[]
    rows = []
    with open("toplology.csv") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
           if header == []:
               header = row
           else:
               rows.append(row)

    if a == "create":
        # create containers
        for container in header:
            create_container(container, password)

    elif a == "delete":
        # delete containers
        for container in header:
            delete_container(container, password)

