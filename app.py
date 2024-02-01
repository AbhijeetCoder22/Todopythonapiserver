from flask import Flask, jsonify, request
from flask_cors  import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)



def db_cred(host="sql6.freesqldatabase.com",user="sql6680885",password="p4CCflVjtz",database="sql6680885"):
    mydb = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database,
    )
    return mydb


@app.route('/',methods=['POST'])
@app.route('/login',methods=['POST'])
def login():
    
    data = request.get_json()

    mydb = db_cred()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT password FROM user where username=%s",(data['usrname'],))
    paswrd =  mycursor.fetchall()

    if paswrd:
        if data['password'] == paswrd[0][0]:
            result = 'Success'
        else:
            result = 'Incorrect Password'
    else:
        result = 'No user'
    return jsonify(result)

@app.route('/Register',methods=['POST'])
def register():
    
    data = request.get_json()
    
    if data['usrnm'] and data['paswrd'] and data['cnfrm']:
        if data['paswrd'] == data['cnfrm']:
            val = (data['usrnm'],data['cnfrm'],data['act_date'])
            mydb = db_cred()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT password FROM user where username=%s",(data['usrnm'],))
            paswrd =  mycursor.fetchall()

            if not paswrd:
                mycursor.execute("Insert into user (username,password,created_date) values(%s,%s,%s)",val)
                mydb.commit()
                if mycursor.rowcount:
                    result="Sucesfully Registered!!! "
                else:
                    result="Something Went Wrong!!! "
            else:
                result='User Exist!!! '
        else:
            result='New password and confirm password doesnot match!!! '
    else:
        result = 'All are mandetory!!! '
        
    return jsonify(result)

@app.route('/Homeinput',methods=['POST'])
def Homeinput():
    data = request.get_json()
    if data['Description'] and data['title']:
        mydb = db_cred()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id FROM user where username=%s",(data['user'],))
        user_id =  mycursor.fetchall()[0][0]
        mycursor.execute("SELECT id FROM to_do_list where title = %s and user_id=%s",(data['title'],user_id,))
        to_do_list_title_id = mycursor.fetchall()
        mycursor.execute("SELECT id FROM to_do_list where descrition = %s and user_id=%s",(data['Description'],user_id,))
        to_do_list_desription_id = mycursor.fetchall()
            
        if not (to_do_list_title_id or to_do_list_desription_id):
            val = (user_id,data['title'],data['Description'])
            mycursor.execute("Insert into to_do_list (user_id,title,descrition) values(%s,%s,%s)",val)
            mydb.commit()
            if mycursor.rowcount:
                result = 'Done'
            else:
                result = 'Try After Some time'
        else:
            result = 'Already exist'
    else:
        result = "All Fields are mandetory"
        
    return jsonify(result)

@app.route('/Homeoutput',methods=['POST'])
def Homeoutput():
    title = []
    description = []
    id = []
    actual_data = {"id":id,
                   "title":title,
                   "description":description
                   }
    data = request.get_json()
    mydb = db_cred()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM user where username=%s",(data,))
    user_id =  mycursor.fetchall()[0][0]
    mycursor.execute("SELECT title,descrition,id from to_do_list where user_id=%s",(user_id,))
    get_data = mycursor.fetchall()
    for ind in get_data:
        title.append(ind[0])
        description.append(ind[1])
        id.append(ind[2])
    
    actual_data["id"] = id
    actual_data["description"] = description
    actual_data["title"] = title
    
    return jsonify(actual_data)

@app.route('/deletetask',methods=['POST'])
def deletetsk():
    data = request.get_json()
    print(data)
    if data:
        mydb = db_cred()
        mycursor = mydb.cursor()
        mycursor.execute('DELETE from to_do_list where id = %s',(data,))
        mydb.commit()
        print(mycursor.rowcount)
        if mycursor.rowcount == 1:
            result = 'Deleted'
        else:
            result = 'Not Possible to delete'
    else:
        result = 'No Task to delete'
    return jsonify(result)

if __name__ == 'main':
    app.run(debug = True)