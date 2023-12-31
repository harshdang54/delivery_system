from flask import Flask, request, jsonify, session
import pandas as pd
import jwt
import json
import os
from twilio.rest import Client
import random
import math

# from scripts.water_reminder import water_blueprint
import psycopg2
from flask_cors import CORS

from config import config


app = Flask(__name__)
app.secret_key="otp"
CORS(app)

# app.register_blueprint(water_blueprint)

@app.route("/")
def Hello_World():
    return "<p>Hellow World</p>"

@app.route("/home")
def HomePage():
    return "<p>Home Page</p>"

def sendMessage(msg, nmber):
    account_sid = 'AC3b5fd7fdc5321a29c165be0f7eca502f'
    auth_token = '57d0e77b23568162d29762c08380fb35'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+15075853311',
        body=msg,
        to=f'+91{nmber}'
    ) 
    if(message.sid):
        return True
    else :
        return False    

@app.route("/about", methods=['GET'])
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    items = []
    return "darshan dang"
    try:
        # read connection parameters
        params = config()
  
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
          
        # create a cursor
        cur = conn.cursor()
          
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT * FROM users')
  
        # display the PostgreSQL database server version
        db_version = cur.fetchall()
        
        for item in db_version:
            temp = {}
            temp['name'] = item[0]
            items.append(temp) 
        print(items)
         
    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            account_sid = 'AC3b5fd7fdc5321a29c165be0f7eca502f'
            auth_token = '5d22fe1e3b2897c69e126720c11f8cfd'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
            from_='+15075853311',
            body='this is darshan',
            to='+919582620679'
            )

            if(message.sid):
                return True
            else :
                return error   
        return items
    

def genrateRandom6DigitCode():
    ## storing strings in a list
    digits = [i for i in range(0, 10)] 
    ## initializing a string
    random_str = "" 
    ## we can generate any lenght of string we want
    for i in range(6):
    ## generating a random index
    ## if we multiply with 10 it will generate a number between 0 and 10 not including 10
    ## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10) 
        random_str += str(digits[index])

    return random_str

@app.route("/otp_validate", methods=['POST'])
def otpValidate():
    otpC = request.get_json().get('code')  
    if 'response' in session:
        code = session['response']
        phone = session['phone']
        print('code', len(code),len(otpC), code,otpC)
        session.pop('response', None)
        if (code == otpC):
            return userVerified(phone)
        else:
            return jsonify({"res":'otp code is not matching'})
    return jsonify({"res":'error in validation'})   
       
def userVerified(phone): 
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    params = config()
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()
    try : 
        cur.execute(f"select * from users where phone='{phone}'")
        excuteResult = cur.fetchall()
        print('try len',  excuteResult, len(excuteResult))
        conn.close()    
        if len(excuteResult) > 0:
            return jsonify({"new_user":False, "data":excuteResult}) 
        else:
            return jsonify({"new_user":True, "data":excuteResult})
        # if new user true It means user already registered and we can send them to listing page else we need to insert the use detail into users table
    except (Exception, psycopg2.DatabaseError) as error:
        print('custom error', type(error))
        err = []
        err.append({"error":error})
        print('err',err)
        return jsonify({"error":str(error)})
    
@app.route("/otp_send", methods=['POST', 'GET'])
def dataSubmit():  
    print('post api', request.get_json()) 
    phone = request.get_json().get('phone')  
    otp =  genrateRandom6DigitCode()
    print('otp code is ', otp)
    session['response']= str(otp) 
    session['phone']= phone  
    if sendMessage(f'your 6 digit code is {otp}',phone): 
             
        return jsonify({'res':'data send'})

        # print('fetch len',  len(cur.fetchall())==0)
        # if len(cur.fetchall()):
            
        #     rData = request.data.decode('utf-8')
        #     first = request.get_json().get('name')
        #     pwd = request.get_json().get('pwd')  
        #     email = request.get_json().get('email')   
        #     #df= pd.read_csv(request.files['file'])
        #     #print('rData',pd.DataFrame())
        #     params = config()
        
        #     print('datasss', first, phone)
        #         # connect to the PostgreSQL server
        #     print('Connecting to the PostgreSQL database...')
        #     conn = psycopg2.connect(**params)
                
        #         # create a cursor
        #     cur = conn.cursor()
        #     cur.execute(f"SELECT * FROM users WHERE email='{email}'")
        #     print('fetch len',  len(cur.fetchall())==0)
        #     if len(cur.fetchall()):
        #         cur.execute("INSERT INTO users (name, pwd, email, phone) VALUES (%s, %s, %s, %s)", (first,pwd, email, phone))
        #         conn.commit()
        #         print("Records inserted........")
            
        #         #for item in df['Name']:
        #             #print('row', item)
            
        #             #cur.execute("INSERT INTO users (name) VALUES ('''"+str(item)+"''')")
        #             #conn.commit()
        #             #print("Records inserted........")
                
        #             #with open(request.files[item]) as dd:
        #             #   print('dd',dd.read())
        #         conn.close()     
        #         return 'ok'
        #         #if request.method=="POST":
        #         #print(f'request, {request}')
        #     return f'record already exist with this email {email}'


@app.route("/registeration", methods=['POST', 'GET'])
def registeration():  
    print('post api', request.get_json())  
    name = request.get_json().get('name') 
    email = request.get_json().get('email')  
    phone = session['phone'] 
    session.pop('phone', None)  
    # if sendMessage("This is Harsh",phone):
    if (name!="" and email!="" and phone!=""):    
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        params = config()
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        try : 
            cur.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name,email, phone))
            cur.execute(f"select * from users where phone='{phone}'")
            excuteResult = cur.fetchall()
            conn.commit() 
            conn.close()     
            return jsonify({"message":"user has beeen registered", "data":excuteResult})  
            # if new user true It means user already registered and we can send them to listing page else we need to insert the use detail into users table
        except (Exception, psycopg2.DatabaseError) as error:
            print('custom error', error) 
            return jsonify({"error":str(error)})
        
    else:
        return jsonify({'error':'Please fill all the required fields.'})

                

@app.route("/users", methods=['GET'])
def users(): 
    
    """ Connect to the PostgreSQL database server """
    conn = None
    items = []
    try:
        # read connection parameters
        params = config()
  
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
          
        # create a cursor
        cur = conn.cursor()
          
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT * FROM users')
  
        # display the PostgreSQL database server version
        db_version = cur.fetchall()
        
         
         
    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        return items  
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    rData = request.data.decode('utf-8')
    print('login', request.form['name'])
    encoded_jwt = jwt.encode({"name": request.form['name']}, "secret", algorithm="HS256")
    return encoded_jwt
    first = request.get_json().get('name')
    pwd = request.get_json().get('pwd')  
    email = request.get_json().get('email')  
    #df= pd.read_csv(request.files['file'])
    #print('rData',pd.DataFrame())
    params = config()
  
    print('datasss', first, pwd)
        # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
          
        # create a cursor
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE email='{email}'")
    print('fetch len',  len(cur.fetchall())==0)
    if len(cur.fetchall()):
        cur.execute("INSERT INTO users (name, pwd, email) VALUES (%s, %s, %s)", (first,pwd, email))
        conn.commit()
        print("Records inserted........")
       
        #for item in df['Name']:
            #print('row', item)
     
            #cur.execute("INSERT INTO users (name) VALUES ('''"+str(item)+"''')")
            #conn.commit()
            #print("Records inserted........")
           
            #with open(request.files[item]) as dd:
             #   print('dd',dd.read())
        conn.close()     
        return 'ok'
        #if request.method=="POST":
        #print(f'request, {request}')
    return f'record already exist with this email {email}'         


if __name__ == '__main__':
     app.run(host='0.0.0.0')
    # app.run(debug=True)
