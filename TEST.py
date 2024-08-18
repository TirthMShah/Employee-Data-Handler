import sys
import pandas as pd
import numpy as np
# import mysql.connector

class Employee:
    def __init__(self):
        self.Employee_id=0
        self.df=pd.read_csv(r"GRP\Demo_data.csv")
        self.file_df=''
    
    def login(self):
        database=''
        database_name=''
        while True:
            try:
                emp_id=int(input("Enter your Employee ID : "))
            except Exception as e:
                print("Enter numeric values only")
            
            if not(self.linear_search(emp_id,"Employee_ID")):
                print("Invalid Employee ID")
            else:
                break
        while True:
            password=input("Enter your password : ")
            index=self.df.index.get_loc(self.df[self.df['Employee_ID'] == emp_id].index[0])
            if password == self.df.iloc[index]["Password"]:
                print("Login successfull")
                break
            else:
                print("Invalid password")
        while True:
            try:
                choice=int(input("Which type of file do you have?\n1) CSV file\n2) Excel file\n3) From database\n4) Exit\nEnter your choice : "))
            except Exception as e:
                print("Enter only numeric values")
            if choice == 1:
                file_path=input("Enter filepath : ")
                try:
                    self.file_df=pd.read_csv(file_path)
                    break
                except Exception as e:
                    print(e)
            
            elif choice == 2:
                file_path=input("Enter filepath : ")
                try:
                    self.file_df=pd.read_csv(file_path)
                    break
                except Exception as e:
                    print(e)
            elif choice == 3:
                database_name=input("Enter database name : ")
                # try:
                #     database=mysql.connector.connect(
                #     host="localhost",
                #     user="root",password="",
                #     database=database_name)
                #     break
                # except Exception as e:
                #     print(e)
            
            elif choice == 4:
                print("Thnk you for using this system")
                sys.exit(0)
            else:
                print("Enter valid values")
                
            
        while True:
            try:
                choice=int(input("1) Add Employee\n2) Sort Data\n3) Exit system\nEnter your choice : "))
            except Exception as e:
                print("Enter numeric values only")
            if choice == 1:
                self.add_employee(database)
                break
            elif choice == 2:
                self.sort_data(database)
                break
            elif choice == 3:
                print("Thank you for using this system!")
                sys.exit(0)
            else:
                print("Enter value from given choices only")
                    
    def linear_search(self,value,column):
        for i in self.df[column]:
            if i == value:
                return True
        else:
            return False
   

    def add_employee(self,database=''):
        column_list=[]
        if database=='':
            for i in self.file_df:
                column_list.append(i)
            data_list=dict()
            print("Enter data")
            for i in range(len(column_list)):
                Input=input(column_list[i]+" : ")
                data_list[column_list[i]]=Input
            self.file_df=self.file_df.append(data_list,ignore_index=True)
            print(self.file_df)
        else:
            cursor=database.cursor()
            query="SHOW TABLES"
            cursor.execute(query)
            table_list=[]
            result=cursor.fetchall()
#             for i in result[0]:
#                 table_list.append(i)
            table_list.extend(result)
            for i in range(len(table_list)):
                print(i+1,")",table_list[i][0])
            choice=int(input("Enter the table you like to add employees : "))
            table_name=table_list[choice-1][0]
            query="SHOW COLUMNS FROM "+table_name
            cursor.execute(query)
            result=cursor.fetchall()
            data_list=[]
            data=''
            col_names=''
            print("Insert new data :-")
            for i in range(len(result)):
                Input=input(result[i][0]+" : ")
                data_list.append(Input)
                if i == 0:
                    col_names+=result[i][0]
                    data+="%s"
                else:
                    col_names+=","+result[i][0]
                    data+=",%s"
            
            print(tuple(data_list))
            query='INSERT INTO '+table_name+' VALUES('+data+')'
            values=tuple(data_list)
            cursor.execute(query,values)
            database.commit()
            print(cursor.rowcount)
        
    def sort_data(self,database=''):
        if database=='':
            column_list=[]
            column_name_list=[]
            count=1
            for i in self.file_df:
                print(count,")",i)
                count+=1
                column_name_list.append(i)
                array=np.array([])
                for j in self.file_df[i]:
                    array=np.append(array,[j])
                column_list.append(array)
            index=int(input("By which column you would like to sort the data"))
            self.bubble_Sort(column_name_list,column_list,index-1)
            
        else:
            cursor=database.cursor()
            query="SHOW TABLES"
            cursor.execute(query)
            table_list=[]
            result=cursor.fetchall()
            table_list.extend(result)
            for i in range(len(table_list)):
                print(i+1,")",table_list[i][0])
            choice=int(input("Enter the table you like to add employees : "))
            table_name=table_list[choice-1][0]
            query="SHOW COLUMNS FROM "+table_name
            cursor.execute(query)
            result=cursor.fetchall()
            column_name_list=[]
            count=1
            for i in result:
                column_name_list.append(i[0])
                print(count,")",i[0])
                count+=1
            index=int(input("Enter the column you like to sort : "))
            print(column_name_list)
            column_list=[]
            for i in range(len(column_name_list)):
                cursor=database.cursor()
                query="SELECT "+column_name_list[i]+" FROM "+table_name
                cursor.execute(query)
                result=cursor.fetchall()
                array=np.array([])
                for j in result:
                    array=np.append(array,[j[0]])
                column_list.append(array)
#                 result_list.append(result)
#             column_list=[]
#             for i in result_list:
#                 array=np.array([])
#                 for j in i:
#                     array=np.append(array,[j])
#                 column_list.append(array)
# #                 del array
#             print(result_list[index-1])
            self.bubble_Sort(column_name_list,column_list,index-1)
              
    def bubble_Sort(self,column_name,array_list,index):
        n = len(array_list[index])
        for i in range(n):
            for j in range(0, n - i - 1):
                
                if array_list[index][j] > array_list[index][j + 1]:
                    
                    array_list[index][j], array_list[index][j + 1] = array_list[index][j + 1],array_list[index][j]
                    for k in range(len(array_list)):
                        if k == index:
                            continue
                        else:
                             array_list[k][j], array_list[k][j + 1] = array_list[k][j + 1],array_list[k][j]
        df=pd.DataFrame()
        for i in range(len(array_list)):
            df.insert(i,column_name[i],array_list[i])
        print(df)
            
def main():
    try:
        choice=int(input("1) Login \n2) Exit\nEnter your choice from above options : "))
    except Exception as e:
        print("Enter numeric values only!")
        main()
    if choice == 1:
        employee=Employee()
        employee.login()
    elif choice == 2:
        print("Thank you for using he system")
        sys.exit(0)
    else:
        print("Enter from given choice only")
        main()
main()