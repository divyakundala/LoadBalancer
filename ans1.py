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

def create_vethpair(c, password):
    command="ansible-playbook -i hosts veth.yml -e veth1=" + c[1] + " -e veth2="+ c[2] + " -e container1=" + c[0][0] + " -e container2=" + c[0][1] + " -e password=" + password  
    subprocess.call([command],shell=True) 
    
def delete_vethpair(veth1, password):
    command="ansible-playbook -i hosts vethdel.yml -e veth1=" + veth1 + " -e password=" + password  
    subprocess.call([command],shell=True)    
    
if __name__ == '__main__':
    n = len(sys.argv)
    a=sys.argv[1]
    password = getpass.getpass(prompt='Password: ', stream=None)
    header=[]
    conn= []
    row_num = 0
    with open("toplology.csv") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
           if header == []:
               header = row
           else:
               for col in range(row_num,len(row)):
                   if row[col] == '1':
                       conn.append([(header[row_num], header[col]), header[row_num] + header[col], header[col] + header[row_num]])
               row_num +=1    

    print(conn)
    if a == "create":
        # create containers
        for container in header:
            create_container(container, password)
        
        # create veth pairs
        for c in conn:
            create_vethpair(c, password)
            
    elif a == "delete":
        # delete containers
        for container in header:
            delete_container(container, password)
            
        # delete veth pairs
        for c in conn:
            delete_vethpair(c[1], password)
