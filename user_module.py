import cv2
import numpy as np
import mysql.connector
import face_recognition
import os
import shutil
path = 'images'
us=input("ENTER USER NAME")
pa=input("ENTER PASSWORD")
mydb=mysql.connector.connect(
    host="remotemysql.com",
    user="GUXd9jBWXa",
    password="AyBfzODGTw",
    port="3306",
    database="GUXd9jBWXa"
)
mycursor=mydb.cursor()

if us=="admin" and pa=="admin":
    print("which process you are doing....select one from below \n 1.'insert new attendance date \n 2.attendance for workers")
    ans=int(input())
    if ans== 1:
        d=input("enter date format is -> DD_MM_YYYY\n")
        query = ("ALTER TABLE workers_attendance ADD {} text(50)".format(d))

        mycursor.execute(query)
        print("Date added successfully")
        mydb.commit()
    else:
        print("do you want to take attendance yes or no")
        ans=input()
        while(ans != "no"):
            aadhar=str(input("provide aadhar number"))
            query = ("SELECT encodeing FROM workers_data WHERE aadhar = {}".format(aadhar))
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            na = myresult[0][0]
            
            data=[]
            li=na.split("+")
            for i in li:
                if i[0]=="-":
                    tmp=i.replace("-","")
                    tmp=-abs(float(tmp))
                    data.append(tmp)
                else:
                    tmp = float(i)
                    data.append(tmp)
            print(data)
            ans=input("do you want to continue yes or no")
