# sign up endpoint
# import Flask
from flask import*
import pymysql 
import pymysql.cursors
import os # Its going to allow python code to communicate with the operating system  
# create flask app
app = Flask(__name__)
#configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/api/signup', methods=['POST'])
def signup():
    #  Extract values posted by the user request
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    # connection to Database
    connection = pymysql.connect(host='localhost',user='root',password='',database='dailyyougurts_twiga')

    # create a cursor to intialize the connection
    cursor = connection.cursor()
    # write SQL query
    sql = 'insert into users(username,email,password,phone) values(%s,%s,%s,%s)'
    # prepare data to replace the place holders
    data = (username,email,password,phone)
    # execute data and the sql using the cursor
    cursor.execute(sql,data,)
    # commit / save changes to the database
    connection.commit()
    return jsonify({'success':'Thanks for joining'})

# signing in

@app.route('/api/signin',methods=['POST'])
def signin():
    # Extarcting values from the user
    username = request.form['username']
    password = request.form['password']

    # connection to the database
    connection = pymysql.connect(host='localhost',user='root',password='',database='dailyyougurts_twiga')

    # create a cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # SQL query
    sql = 'Select* from users where username = %s and password = %s'
    # data that replaces the placeholders
    data = (username,password)
    # execution of the data
    cursor.execute(sql,data)
    # cursor count
    count = cursor.rowcount
    # the logic
    if count == 0:
        return jsonify ({'message':'login failed'})
    else:
        user = cursor.fetchone()
        user.pop('password',None)
        return jsonify({'message':'login successful','user':user})
    
    # add product
@app.route('/api/add_product',methods=['POST'])
def add_product():
    # User values
    product_name = request.form ['product_name']
    product_description = request.form['product_description']
    product_cost = request.form['product_cost']
    # Extarct image data
    product_photo = request.files['product_photo']  
    # Get the image file name
    filename = product_photo.filename
    # specify where evrything is going to be saved
    product_photo_path =os.path.join(app.config['UPLOAD_FOLDER'],filename)
    # save your images in the path specified above
    product_photo.save(product_photo_path)
    # connection
    connection = pymysql.connect(host='localhost',user='root' ,password='' ,database='dailyyougurts_twiga')
    # create a cursor
    cursor = connection.cursor()
    # sql
    sql = 'insert into product_details(product_name,product_description,product_cost,product_photo) values(%s,%s,%s,%s)'
    # data
    data =(product_name,product_description,product_cost,filename)
    # execute
    cursor.execute(sql,data)
    connection.commit()
    return jsonify ({'message':'Product add'})
# api/get_product_details
@app.route('/api/get_product_details')
def get_product_details():
    connection = pymysql.connect(host='localhost',user='root' ,password='' ,database='dailyyougurts_twiga')

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    #  sql
    sql = 'select* from product_details'
    cursor.execute(sql)

    product_details = cursor.fetchall()
    return jsonify(product_details)

    

if __name__ == '__main__':
    app.run(debug=True)