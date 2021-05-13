import subprocess
import sys
import getpass
from csv import reader

def create_container(container_name, password):
    command = "ansible-playbook cont.yml -e container="+ container_name + " -e password=" + password
    subprocess.call([command],shell=True)

def delete_container(container_name, password):
    command = "ansible-playbook del.yml -e container=" + container_name + " -e password=" + password
    subprocess.call([command],shell=True)

def create_vethpair(c, ip, password):
    command="ansible-playbook veth.yml -e veth1=" + c[1] + " -e veth2="+ c[2] + " -e container1=" + c[0][0] + " -e container2=" + c[0][1] + " -e ip=" + ip + " -e password=" + password  
    subprocess.call([command],shell=True) 
    
# def delete_vethpair(veth1, password):
#     command="ansible-playbook -i hosts vethdel.yml -e veth1=" + veth1 + " -e password=" + password  
#     subprocess.call([command],shell=True)    

def assign_default_route(container, ip, password):
    command="ansible-playbook route.yml -e container=" + container + " -e default_ip=" + ip + " -e password=" + password  
    subprocess.call([command],shell=True)
    
def run_nginx(container, password):
    command="ansible-playbook nginx.yml -e container=" + container + " -e password=" + password
    subprocess.call([command],shell=True)

def create_haproxy_cfg(container_dict, def_ip):
    subprocess.call(["rm -rf templates/haproxy.cfg"], shell=True) 
    subprocess.call(["cp templates/haproxy-default.cfg templates/haproxy.cfg"], shell=True)
    f = open("templates/haproxy.cfg", "a")
    f.write("\nfrontend webapp\n")
    f.write("\tbind " + def_ip + ":80\n")
    f.write("\tdefault_backend webapp-servers\n")
    f.write("\nbackend webapp-servers\n")
    f.write("\tbalance roundrobin\n")
    f.write("\tmode http\n")
    i = 1
    for container in container_dict:
        if (container.startswith("S")):
            f.write("\tserver webserver" + str(i) + " " + container_dict[container] + ":80\n")
            i+=1
    f.close() 
    


def run_haproxy(container, ip, password):
    command="ansible-playbook -i hosts haproxy.yml -e container=" + container + " -e ip=" + ip + "/24 -e password=" + password  
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
    
    if a == "create":
        container_dict = {}
        
        # create containers
        mgmt_ip = 2
        for container in header:
            create_container(container, password)
            container_dict[container] = "172.17.0." + str(mgmt_ip)
            mgmt_ip+=1
        
        # create veth pairs
        ip = 0
        for c in conn:
            create_vethpair(c, str(ip), password)
            ip+=1
            
        i = 0
        for container in header:
            # run nginx in Servers and Haproxy in gateway
            if container.startswith("S"):
                run_nginx(container, password)
            elif container.startswith("G"):
                ip = "10.0." + str(i) + ".1"
                create_haproxy_cfg(container_dict, ip)
                run_haproxy(container, ip, password)
           
            # add default route
            if not container.startswith("G"):
                if container.startswith("H"):
                    ip = "192.168." + str(i) + ".2"
                else:
                    ip = "192.168." + str(i) + ".1"
                assign_default_route(container, ip, password)
                i+=1
   
            
    elif a == "delete":
        # delete containers
        for container in header:
            delete_container(container, password)
        
        # delete haproxy.cfg and index.html
        subprocess.call(["rm -rf templates/haproxy.cfg"], shell=True)
        subprocess.call(["rm -rf templates/index.html"], shell=True)
            
        # delete veth pairs
        # for c in conn:
        #     delete_vethpair(c[1], password)
