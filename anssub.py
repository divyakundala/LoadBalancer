import sys
import os 
# total arguments
n = len(sys.argv)
#print("Total arguments passed:", n)
 
# Arguments passed

#print("\nName of Python script:", sys.argv[0])
 
#print("\nArguments passed:", end = " ")

for i in range(1, n):
    a=sys.argv[i]
print(a) 

if a == "1234":
    print(os.system('ps -cax|grep dock'))
	   

