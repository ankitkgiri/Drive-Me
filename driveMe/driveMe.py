from flask import Blueprint, render_template, request, redirect, session, Flask, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename


driveMe = Blueprint("driveMe",__name__, static_folder="/static", template_folder="templates")

@driveMe.route("/book")
def book():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    data =(cur.execute("SELECT car_id,car_name,seater,mileage,fuel_type,price,available FROM cars WHERE available=1")).fetchall()
    return render_template("book.html",cars = data)

@driveMe.route("/book_button",methods=["POST","GET"])
def book_button():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    car_id = int(request.form["car_id"])
    owner_phno=int(cur.execute("SELECT owner_phno FROM cars WHERE car_id IS "+str(car_id)).fetchall()[0][0])
    borrower_phno=session["user"]
    returned=0
    query="INSERT INTO transactions (borrower_id,lender_id,returned,car_id) VALUES ({a},{b},{c},{d})".format(a=borrower_phno,b=owner_phno,c=returned,d=car_id)
    cur.execute(query)
    query="UPDATE cars SET available={a} WHERE car_id={b}".format(a=0,b=car_id)
    cur.execute(query)
    conn.commit()
    return "<script>window.alert('Vehicle Booked!'); window.location.replace('/book');</script>"

@driveMe.route("/returned_button",methods=['POST','GET'])
def returned_button():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    car_id = int(request.form["car_id"])
    owner_phno=session["user"]
    query='UPDATE transactions SET returned=1 WHERE lender_id={a} AND car_id={b}'.format(a=owner_phno,b=car_id)
    cur.execute(query)
    query='UPDATE cars SET available=1 WHERE car_id={a}'.format(a=car_id)
    cur.execute(query)
    conn.commit()
    return "<script>window.alert('Vehicle Returned!'); window.location.replace('/book');</script>"


@driveMe.route("/lend", methods=["POST","GET"])
def lend():
    if "user" in session:
        if request.method == "POST":
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            try:
                car_name = request.form['car_name']
                owner_phno = int(session['user'])
                seater = request.form['seater']
                mileage = request.form['mileage']
                fuel_type = request.form['fuel_type']
                price = request.form['price']
                available = 1
                querry = "INSERT INTO cars (car_name,owner_phno,seater,mileage,fuel_type,price,available) VALUES ('{a}',{b},{c},{d},'{e}',{f},{h})".format(a=car_name, b=owner_phno, c=seater,d=mileage,e=fuel_type,f=price,h=available)
                cur.execute(querry)
                conn.commit()
                return "<script>window.alert('Vehicle Lended'); window.location.replace('/book');</script>"
            except:
                
                return "<script>window.alert('cannot register the vehicle'); window.location.replace('/register');</script>"
        else:
                return render_template("lend.html")
    else:
         return redirect(url_for("auth.login"))


@driveMe.route('/profile')
def profile():
    if "user" in session:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        phno = int(session["user"])
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        try:
            #for profile and my registered cars division
            data1 =cur.execute("SELECT car_id,car_name,seater,mileage,fuel_type,price  FROM cars WHERE owner_phno = {a}".format(a=phno)).fetchall()
            data2=cur.execute("SELECT phno,name,email FROM users WHERE phno={a}".format(a=phno)).fetchall()
        except:
            data1=[]
            data2 =[]
        try:
            #for my lended cars division
            car_id_lended=(cur.execute("SELECT car_id FROM transactions WHERE lender_id={a} AND returned=0".format(a=phno)).fetchall())
            for i in car_id_lended:
                data3.append(cur.execute("SELECT car_id,car_name,seater,mileage,fuel_type,price FROM cars WHERE car_id={a}".format(a=i[0])).fetchall())
            
        except:
            data3 = []
        try:
            #for my booked cars
            car_id_borrowed=(cur.execute("SELECT car_id FROM transactions WHERE borrower_id={a} AND returned=0".format(a=phno)).fetchall())
            for i in car_id_borrowed:
                data4.append(cur.execute("SELECT car_id,car_name,seater,mileage,fuel_type,price FROM cars WHERE car_id={a}".format(a=i[0])).fetchall())
            
        except:
            data4 = []
        
        return render_template("profile.html", cars=data1,user=data2,lended_cars=data3,borrowed_cars=data4  )
    else:
        return redirect(url_for('auth.login'))
    