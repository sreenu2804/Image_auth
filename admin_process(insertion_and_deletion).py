import cv2
import mysql.connector
import face_recognition
import os
import shutil
src="/Users/naveenreddy/Desktop/srinu major project/images/"
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
    print("\nwhich process do you want to execute 'DATA INSERTION {i} OR DATA DELETION{d}'\n")
    process = input()
    if process == "i" or process == "I":
        Images = []
        classNames = []
        names=[]
        id=[]
        val=[]
        myList = os.listdir(path)
        myList.remove('.DS_Store')
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            Images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
            te=os.path.splitext(cl)[0]
            names.append(te.split(" ")[0])
            id.append(te.split(" ")[1])
            val.append(te.split(" "))
        def FindEncodings(Images):
            encodeList = []

            for i in range(0,len(Images)):
                mycursor = mydb.cursor()
                txt=""
                Images[i] = cv2.cvtColor(Images[i], cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(Images[i])[0]
                for g in range(0,len(encode)):
                    if g != (len(encode)-1):
                        txt=txt+str(encode[g])+"+"
                    else:
                        txt=txt+str(encode[g])
                query=("INSERT INTO workers_data (name,aadhar,encodeing,age,gender) VALUES (%s,%s,%s,%s,%s)")
                VALUES = (val[i][0], val[i][1], txt,val[i][2],val[i][3])
                encodeList.append(encode)
                mycursor.execute(query, VALUES)
                mydb.commit()
                mycursor.close()
            for i in range(0,len(Images)):
                mycursor = mydb.cursor()
                query = ("INSERT INTO workers_attendance (name,aadhar,age,gender) VALUES (%s,%s,%s,%s)")
                VALUES = (val[i][0], val[i][1], val[i][2], val[i][3])
                mycursor.execute(query,VALUES)
                mydb.commit()
                mycursor.close()
            return encodeList



        encodeListKnown = FindEncodings(Images)
        if len(classNames)!=0:
            for w in range(0,len(names)):
                src="/Users/naveenreddy/Desktop/srinu major project/images/"+classNames[w]+".jpg"
                dst = "/Users/naveenreddy/Desktop/srinu major project/Processed_images/"+classNames[w]+".jpg"
                shutil.move(src,dst)
        print("Data was inserted successfully")
    else:
        mycursor = mydb.cursor()
        d = str(input("Enter Aadhar number to delete purpose "))
        query = ("SELECT name,aadhar,age,gender FROM workers_attendance WHERE aadhar = {}".format(d))
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        na=str(myresult[0][0])+" "+str(myresult[0][1])+" "+str(myresult[0][2])+" "+str(myresult[0][3])
        src="/Users/naveenreddy/Desktop/srinu major project/Processed_images/"+na+".jpg"
        dst="/Users/naveenreddy/Desktop/srinu major project/Deleted_images/"+na+".jpg"
        shutil.move(src,dst)
        query = ("DELETE FROM workers_attendance WHERE aadhar = {}".format(d))
        mycursor.execute(query)
        mydb.commit()

        query = ("DELETE FROM workers_data WHERE aadhar = {}".format(d))
        mycursor.execute(query)
        mydb.commit()

        mycursor.close()