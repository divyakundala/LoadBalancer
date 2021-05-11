from csv import reader
with open("topology.csv") as read_obj:
    csv_reader = reader(read_obj)
    header = []
    row_num = 0
    conn = []
    for row in csv_reader:
       if header == []:
           header = row
       else:
           for col in range(row_num,len(row)):
               if row[col] == '1':
                    conn.append((header[row_num], header[col]))
           row_num +=1
    print(conn)
