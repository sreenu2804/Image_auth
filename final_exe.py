import cv2
import numpy as np
import mysql.connector
import face_recognition
import shutil
import os
from flask import *
src="/Users/naveenreddy/Desktop/srinu major project/images/"
path = 'images'
mydb=mysql.connector.connect(
    host="remotemysql.com",
    user="GUXd9jBWXa",
    password="AyBfzODGTw",
    port="3306",
    database="GUXd9jBWXa"
)
mycursor=mydb.cursor()
def datecreation(da):
    mycursor = mydb.cursor()
    # da = input("\nkindly provide Todays date format is -> DD_MM_YYYY")
    da=da
    # test = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'workers_attendance'"
    test = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'workers_attendance'"
    mycursor.execute(test)
    myresult = mycursor.fetchall()
    succ = False
    for y in myresult:
        if y.__contains__(da):
            succ = True
    if succ == False:
        d = da
        query = ("ALTER TABLE workers_attendance ADD {} text(50)".format(d))
        mycursor.execute(query)
        print("\nDate added successfully")
        mydb.commit()
def atten(da,aadhar):
    da=da
    mycursor = mydb.cursor()
    aadhar = aadhar
    srcimg="/Users/naveenreddy/Desktop/srinu major project/Input_image/face.jpg"
    query = ("SELECT encodeing FROM workers_data WHERE aadhar = {}".format(aadhar))
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    na = myresult[0][0]

    data = []
    li = na.split("+")
    for i in li:
        if i[0] == "-":
            tmp = i.replace("-", "")
            tmp = -abs(float(tmp))
            data.append(tmp)
        else:
            tmp = float(i)
            data.append(tmp)
    y = srcimg
    img = face_recognition.load_image_file(y)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodeElon = face_recognition.face_encodings(img)[0]

    s = np.float64(data[0])

    results = face_recognition.compare_faces(np.float64(data), [encodeElon])
    if results[0] == True:
        mycursor = mydb.cursor()
        query = ("UPDATE workers_attendance SET {} = 'present' WHERE aadhar = {}".format(da, aadhar))
        mycursor.execute(query)
        mydb.commit()

        return "success"
    else:
        return "failure"
def insertion():
    mycursor = mydb.cursor()
    Images = []
    classNames = []
    names = []
    id = []
    age = []
    gender = []
    myList = os.listdir(path)
    myList.remove('.DS_Store')
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        Images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        te = os.path.splitext(cl)[0]
        print("-----",te)
        names.append(te.split(" ")[0])
        id.append(te.split(" ")[1])
        age.append(te.split(" ")[2])
        gender.append(te.split(" ")[3])
    def FindEncodings(Images):
        encodeList = []
        for i in range(0, len(Images)):
            mycursor = mydb.cursor()
            txt = ""
            Images[i] = cv2.cvtColor(Images[i], cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(Images[i])[0]
            print(encode)
            for g in range(0, len(encode)):
                if g != (len(encode) - 1):
                    txt = txt + str(encode[g]) + "+"
                else:
                    txt = txt + str(encode[g])
            query = ("INSERT INTO workers_data (aadhar,name,encodeing,age,gender) VALUES (%s,%s,%s,%s,%s)")
            VALUES = (id[i], names[i], txt, age[i], gender[i])
            encodeList.append(encode)
            mycursor.execute(query, VALUES)
            mydb.commit()
            mycursor.close()
        for i in range(0, len(Images)):
            mycursor = mydb.cursor()
            query = ("INSERT INTO workers_attendance (aadhar,name,age,gender) VALUES (%s,%s,%s,%s)")
            VALUES = (id[i], names[i], age[i], gender[i])
            mycursor.execute(query, VALUES)
            mydb.commit()
            mycursor.close()
        return encodeList
    encodeListKnown = FindEncodings(Images)
    if len(classNames) != 0:
        for w in range(0, len(names)):
            src = "/Users/naveenreddy/Desktop/srinu major project/images/" + classNames[w] + ".jpg"
            dst = "/Users/naveenreddy/Desktop/srinu major project/Processed_images/" + classNames[w] + ".jpg"
            shutil.move(src, dst)
    print("Data was inserted successfully")
    return "success"
def renameimg1():
    fn = "/Users/naveenreddy/Desktop/srinu major project/Input_image/face.jpg"
    # src="C:/Users/sreenivas/Downloads/input_data_img(1).jpg"
    src="/Users/naveenreddy/Downloads/face.jpg"
    os.rename(src, fn)
    return "success"
def renameimg(name,aadhar,age,gender):
    fn = "/Users/naveenreddy/Desktop/srinu major project/Images/"+ name + " " + aadhar + " " + age + " " + gender + ".jpg"
    # src="C:/Users/sreenivas/Downloads/input_data_img(1).jpg"
    src="/Users/naveenreddy/Downloads/input_data_img.jpg"
    os.rename(src, fn)
    return "success"
def deletion(val):
    mycursor = mydb.cursor()
    d = str(val)
    query = ("SELECT name,age,gender FROM workers_attendance WHERE aadhar = {}".format(d))
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    print(myresult)
    na = myresult[0][0]
    age = myresult[0][1]
    gen = myresult[0][2]
    src = "/Users/naveenreddy/Desktop/srinu major project/Processed_images/" + na + " " + d + " " + age + " " + gen + ".jpg"
    dst = "/Users/naveenreddy/Desktop/srinu major project/Deleted_images/" + na + " " + d + " " + age + " " + gen + ".jpg"
    shutil.move(src, dst)
    query = ("DELETE FROM workers_attendance WHERE aadhar = {}".format(d))
    mycursor.execute(query)
    mydb.commit()
    query = ("DELETE FROM workers_data WHERE aadhar = {}".format(d))
    mycursor.execute(query)
    mydb.commit()
    mycursor.close()
    print("its from process")
app = Flask(__name__)
@app.route("/zero")
def process():
    if request.method == "POST" or "GET":
        print("hiiiiiii")
        tem=request.query_string
        print(tem,"jhjhvjygfrdtsyres")
        if tem == b'pro=DATA+INSERTION':
            print("insertion")
            insertion()
            return render_template("success_res.html")
        elif tem == b'pro=DATA+DELETION':
            print("deletion")
            #deletion()
            return render_template("deletion.html")
        elif tem == b'pro=ATTENDANCE+PROCESS':
            print("attendance")
            return render_template("attendance_process.html")
    return render_template("user_and_pass.html")
@app.route("/")
def home():
    if request.method == "GET" or "POST":
        li= request.query_string.split(b'&')
        print(li)
        if li == [b'']:
            return  render_template('user_and_pass.html')
        elif li[0] == b'usrname=admin' and li[1] == b'pass=admin':
            print("comp user")
            #insertion()
            return render_template('zero.html')
        elif li[0] != b'usrname=admin' or li[1] != b'pass=admin':
            return render_template('try_again.html')
    return render_template('try_again.html')
@app.route("/attendance_process")
def attendance_process():
    print("attendance_process")
    li= request.query_string.split(b'&')
    print(li)
    if request.method == "POST" or "GET":
        if li[0] == b'pro=NEW+DATE':
            return render_template('attendance.html')
        elif li[0] == b'pro=ATTENDANCE+PROCESS':
            return render_template('test1.html')
        elif li[0] == b'pro=RAW+DATA+FOR+DATABASE':
            return render_template('test2.html')
        elif li[0] == b'pro=EXIT':
            return render_template('zero.html')
    return render_template('attendance_process.html')
@app.route("/attendance")
def att():
    print("is cam")
    li= request.query_string.split(b'&')
    print(li)
    val=str(li[0])
    val=val[7:len(val)-1]
    if request.method == "POST" or "GET":
        val=val
        datecreation(val)
        print("sjhdfbs")
    return render_template('date_created.html')
@app.route("/tryagain")
def tryagain():
    #if request.method == "POST" or "GET":
    print("try again")
    return render_template('user_and_pass.html')
@app.route("/date_created")
def date_created():
    if request.method == "POST" or "GET":
        print("success")
    return render_template('attendance_process.html')
@app.route("/success_res")
def succ():
    if request.method == "POST" or "GET":
        print("success")
    return render_template('user_and_pass.html')
# @app.route("/cam")
# def cam():
#     if request.method == "POST" or "GET":
#         print("success",request.data)
#     return render_template('user_and_pass.html')
@app.route("/deletion")
def dele():
    if request.method == "POST" or "GET":
        li = request.query_string.split(b'&')
        val=li[0]
        val = str(val)
        val=val[9:len(val) - 1]
        print(val, type(val))
        deletion(val)
        print("it's web")
        #val = base64.b64encode(bytes(val, 'utf-8'))
    return render_template('success_res.html')
# @app.route("/details")
# def details():
#     if request.method == "POST" or "GET":
#         li = request.query_string.split(b'&')
#         print((li))
#         if li[1]!= b'aadhar=' and li[4]== b'pro=submit':
#             val=str(li[1])
#             d=val[9:len(val)-1]
#             mycursor = mydb.cursor()
#             query = ("SELECT name FROM workers_data WHERE aadhar = {}".format(d))
#             mycursor.execute(query)
#             myresult = mycursor.fetchall()
#             print(myresult)
#             if len(myresult)!=0:
#                 return render_template('try_again.html')
#             else:
#                 return render_template('test2.html')
#         #val = base64.b64encode(bytes(val, 'utf-8'))
#     return render_template('details.html')
@app.route("/test1")
def test1():
    li = request.query_string.split(b'&')
    if request.method == "POST" or "GET":
        print("success")
        print(li,"test1")
        if li[2] == b'pro=submit' and li[0]!=b'aadhar=' and li[1]!=b'date=':
            print("done")
            renameimg1()
            da=str(li[1])
            da=da[7:len(da)-1]
            print(da)
            aadhar=str(li[0])
            aadhar=aadhar[9:len(aadhar)-1]
            print(aadhar)
            re=atten(da,aadhar)
            os.remove("/Users/naveenreddy/Desktop/srinu major project/Input_image/face.jpg")
            if re=="success":
                return render_template('succ_attendance.html')
            else:
                return render_template('fail_attendance.html')
        elif li[2] == b'pro=delete':
            print("delete")
            os.remove("/Users/naveenreddy/Downloads/face.jpg")
            print("delete")
            return render_template('test1.html')
    return render_template('try_again.html')
@app.route("/succ_attendance")
def succ_attendance():
    li = request.query_string.split(b'&')
    print(li)
    if li[0] == b'pro=CONTINUE':
        return render_template('test1.html')
    elif li[0] == b'pro=EXIT':
        return render_template('attendance_process.html')
@app.route("/fail_attendance")
def fail_attendance():
    li = request.query_string.split(b'&')
    print(li)
    if li[0] == b'pro=TRY+AGAIN':
        return render_template('attendance_process.html')
    elif li[0] == b'pro=EXIT':
        return render_template('zero.html')
@app.route("/test2")
def test2():
    lii = request.query_string.split(b'&')
    li=[]
    for i in range(len(lii)):
        li.append(str(lii[i]))
    print(li,"test2")
    name=li[0][7:len(li[0])-1]
    aadhar=li[1][9:len(li[1])-1]
    age=li[2][6:len(li[2])-1]
    gender=li[3][9:len(li[3])-1]
    pro=li[4][6:len(li[4])-1]
    print(name,aadhar,age,gender)
    if request.method == "POST" or "GET":
        print("success")
        if aadhar!="" and pro=="submit":
            mycursor = mydb.cursor()
            query = ("SELECT name FROM workers_data WHERE aadhar = {}".format(aadhar))
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            print(myresult)
            if len(myresult) != 0:
                return render_template('try_again.html')
            else:
                q=renameimg(name, aadhar, age, gender)
                w=insertion()
                if q=="success" and w=="success":
                    return render_template('test2.html')
                else:
                    return render_template('try_again.html')
            print("done")
            return render_template('success_res.html')
        elif pro=="delete":
            print("delete")
            os.remove("/Users/naveenreddy/Downloads/input_data_img.jpg")
            print("delete")
            return render_template('test2.html')
    return render_template('try_again.html')
if __name__ == '__main__':
    app.run(debug=True)