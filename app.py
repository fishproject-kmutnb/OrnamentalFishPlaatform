from flask import Flask,render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_mail import Mail,Message
from email.message import EmailMessage

import secrets
import pymysql

import os
import smtplib


EMAIL_ADDRESS = "earthprimo@gmail.com"
EMAIL_PASSWORD = "vigilante008"

EMAIL_RECIEVER = "earthprimo@gmail.com"
subject = "คุณได้สั่งซื้อสินค้าผ่านเว็บ Ordamental Fish Platform"
body = "Hell Yeah"


app = Flask(__name__)

mail = Mail(app)


app.config['SUPERSECRETKEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://fishja/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = EMAIL_ADDRESS
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

db = SQLAlchemy(app)

connect=pymysql.connect("localhost","root","0997952384","ornamentalfishv2")
################Email#############################

@app.route("/sendemail",methods=['GET','POST'])
def sendmail():
    count = request.form['count'] #ค่าที่รับมาจากเว็บ
    message = EmailMessage()
    message['subject']=subject  #หัวข้อเมล
    message['from']=os.environ.get('') #ผู้ส่ง?
    message['to']=EMAIL_RECIEVER #ผู้รับ
    message.set_content(count) #เนื้อหา
    with smtplib.SMTP_SSL("smtp.gmail.com", 465)as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD) #อีเมล,รหัสเมลเรา
        smtp.send_message(message) #ส่งเมล
    

    return render_template("home.html") 
 

#@app.route("/sendmail",methods=['GET','POST'])
#def sendmail():
#    if request.method == "POST":
#       count = request.form['count']
#       message = Message(subject,sender=EMAIL_RECIEVER,recipients=[EMAIL_RECIEVER]) 

#       message.body = count

#       mail.send(message) 
       
#       success = "Message Sent"

#       return render_template("success.html",success=success)


#############################################

@app.route("/")
def home():

    return render_template("home.html")

##########################################

@app.route("/shop")
def shop():

    mycursor = connect.cursor()

    mycursor.execute("SELECT * FROM product")

    myresult = mycursor.fetchall()

    mycursor.execute("SELECT * FROM seller")

    myresult2 = mycursor.fetchall()

    return render_template("shop.html",datas=myresult,datas2=myresult2)

#########################################

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method=="POST":
        sname=request.form['fishname']
        mycursor = connect.cursor()
        mycursor.execute("SELECT * FROM fish_doc WHERE Name LIKE CONCAT('%%', %s, '%%')",sname)
        myresult=mycursor.fetchall()
        connect.commit()
        return render_template("home.html",datas=myresult)

@app.route("/searchshop",methods=["POST","GET"])
def searchshop():
    if request.method=="POST":
        sname=request.form['shopname']
        mycursor = connect.cursor()
        mycursor.execute("SELECT * FROM seller WHERE Seller_Name LIKE CONCAT('%%', %s, '%%')",sname)
        myresult=mycursor.fetchall()
        print(myresult)
        connect.commit()
        return render_template("result.html",datas=myresult)

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)
    
