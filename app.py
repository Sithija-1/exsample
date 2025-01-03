from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename
from flask import g
from datetime import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database setup
DATABASE = 'instance/my_database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with app.app_context():
        db = get_db()

        db.execute('''
            CREATE TABLE IF NOT EXISTS vehical_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                name TEXT,
                model TEXT,
                year_of_manufacture TEXT,
                vehicle_image TEXT,
                engine_number TEXT,
                chassis_number TEXT,
                fuel_type TEXT
            )
        ''')
        db.commit()
       
        db.execute('''
            CREATE TABLE IF NOT EXISTS insurence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insurence_number TEXT,
                start_date TEXT,
                expiry_date TEXT ,
                cost TEXT
            )
        ''')
        db.commit()

        db.execute('''                  
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                start_date TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                cost TEXT NOT NULL
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS emssion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                start_date TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                cost TEXT NOT NULL
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS permit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                start_date TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                driver_name TEXT NOT NULL,
                driver_license_ID_number TEXT NOT NULL,
                Driver_License_Image TEXT,
                Driver_Medical_Image TEXT,
                comment TEXT 
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS driverdetails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Driver_Name TEXT,
                Date_of_Birthday TEXT,
                Driver_Image TEXT,
                Email TEXT,
                Phone_Number TEXT,
                Address TEXT,
                ID_Image TEXT,
                License_Number_ID TEXT,
                License_Image TEXT 
                 
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS conductordetails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Conductor_Name TEXT NOT NULL,
                Date_of_Birthday TEXT NOT NULL,
                Conductor_Image TEXT NOT NULL,
                Email TEXT NOT NULL,
                Phone_Number TEXT NOT NULL,
                Address TEXT NOT NULL,
                ID_Image TEXT NOT NULL,
                Conductor_ID_Number TEXT NOT NULL,
                Conductor_ID_Image TEXT 
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS input (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_number TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                income TEXT NOT NULL,
                Address TEXT NOT NULL,
                start_mileage TEXT NOT NULL,
                end_mileage TEXT NOT NULL,
                comment TEXT NOT NULL
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                Fuel TEXT NOT NULL,
                Quantity TEXT NOT NULL,
                Cost TEXT NOT NULL,
                Lunch TEXT NOT NULL,
                Pay_Of_Driver TEXT NOT NULL,
                Pay_Of_Conductor TEXT NOT NULL,
                comment TEXT NOT NULL
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS oil (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                
                Quntity TEXT NOT NULL
                
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS service (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                
                Quntity TEXT NOT NULL,
                check_parts TEXT NOT NULL,
                Quntitys TEXT NOT NULL,
                Price TEXT NOT NULL
                
                
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS left_front_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS rigth_front_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS left_back_outside_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS left_back_inside_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS right_back_inside_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS rigth_back_outside_tyer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Tyer_Change_Data TEXT NOT NULL,
                Tyer_Type TEXT NOT NULL,
                Odometar TEXT NOT NULL,
                pressure TEXT NOT NULL,
                Tyer_Price TEXT NOT NULL,
                Bill_Image TEXT,
                comment TEXT
            )
        ''')
        db.commit()

        db.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issu_Date TEXT NOT NULL,
                comment TEXT NOT NULL
            )
        ''')
        db.commit()


  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def wel():
    return render_template('login.html')

name1 = ''
password1 = ''
                                                # login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:           
            name = str(request.form['name'])
            password = str(request.form['password'])
           
            if name1 == name and password1 == password :
                return render_template('vehical_details.html')
            else:
                return '<h1>name or password incorrect</h1>'
        except Exception as e:
            return f"An error occurred: {e}"



                                            #vehical_details

@app.route('/vehical_details')
def vehical_details():
    return render_template('vehical_details.html')

@app.route('/vehical_details', methods=['POST'])
def submit_vehical_details():
    type = request.form['type']
    name = request.form['name']
    model = request.form['model']
    year_of_manufacture = request.form['year_of_manufacture']
    vehicle_image = request.files['vehicle_image']
    engine_number = request.form['engine_number']
    chassis_number = request.form['chassis_number']
    fuel_type = request.form['fuel_type']
    
    if vehicle_image and allowed_file(vehicle_image.filename):
        filename = secure_filename(vehicle_image.filename)
        vehicle_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        vehicle_image.save(vehicle_image_path)
    else:
        filename = None
    
    db = get_db()
    db.execute('INSERT INTO vehical_details (type, name, model, year_of_manufacture, vehicle_image, engine_number, chassis_number, fuel_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
               (type, name, model, year_of_manufacture, filename, engine_number, chassis_number, fuel_type))
    db.commit()
    
    return 'Well done !!!!!'




@app.route('/insurence')                            #insurence
def insurence():
    return render_template('insurence.html')

@app.route('/insurence', methods=['POST'])
def submit_insurence():
    insurence_number = request.form['insurence_number']
    start_date = request.form['start_date']
    expiry_date = request.form['expiry_date']
    cost = request.form['cost']
    
    db = get_db()
    db.execute('''
        INSERT INTO insurence 
        (insurence_number, start_date, expiry_date, cost) 
        VALUES (?, ?, ?, ?)
    ''', (insurence_number, start_date, expiry_date, cost))
    db.commit()
    
    return 'Well done !!!!!'

@app.route('/revenue')                                     #revenue
def revenue():
    return render_template('revenue.html')

@app.route('/revenue', methods=['POST'])
def submit_revenue():
    number = request.form['number']
    start_date = request.form['start_date']
    expiry_date = request.form['expiry_date']
    cost = request.form['cost']
    
    db = get_db()
    db.execute('''
        INSERT INTO revenue 
        (number, start_date, expiry_date, cost) 
        VALUES (?, ?, ?, ?)
    ''', (number, start_date, expiry_date, cost))
    db.commit()
    
    return 'Well done !!!!!'

@app.route('/emssion')                          #emssion
def emssion():
    return render_template('emssion.html')

@app.route('/emssion', methods=['POST'])
def submit_emssion():
    number = request.form['number']
    start_date = request.form['start_date']
    expiry_date = request.form['expiry_date']
    cost = request.form['cost']
    
    db = get_db()
    db.execute('''
        INSERT INTO emssion 
        (number, start_date, expiry_date, cost) 
        VALUES (?, ?, ?, ?)
    ''', (number, start_date, expiry_date, cost))
    db.commit()
    
    return 'Well done !!!!!'
                                                #permit
@app.route('/permit')
def permit():
    return render_template('permit.html')

@app.route('/permit', methods=['POST'])
def submit():
    number = request.form['number']
    start_date = request.form['start_date']
    expiry_date = request.form['expiry_date']
    driver_name = request.form['driver_name']
    driver_license_ID_number = request.form['driver_license_ID_number']
    Driver_License_Image = request.files['Driver_License_Image']
    Driver_Medical_Image = request.files['Driver_Medical_Image']
    comment = request.form['comment']
    
    if Driver_License_Image and allowed_file(Driver_License_Image.filename):
        filename = secure_filename(Driver_License_Image.filename)
        Driver_License_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Driver_License_Image.save(Driver_License_Image_path)
    else:
        filename = None

    if Driver_Medical_Image and allowed_file(Driver_Medical_Image.filename):
        filename1 = secure_filename(Driver_Medical_Image.filename)
        Driver_Medical_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        Driver_Medical_Image.save(Driver_Medical_Image_path)
    else:
        filename1 = None

    db = get_db()
    db.execute('INSERT INTO permit (number, start_date, expiry_date, driver_name, driver_license_ID_number, Driver_License_Image, Driver_Medical_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (number, start_date, expiry_date, driver_name, driver_license_ID_number, filename, filename1, comment))
    db.commit()
    
    return 'Well done !!!!!'

                                                # driver details
@app.route('/driverdetails')
def driver_details():
    return render_template('driverdetails.html')

@app.route('/driverdetails', methods=['POST'])
def submit_driver_details():
    Driver_Name = request.form['Driver_Name']
    Date_of_Birthday = request.form['Date_of_Birthday']
    Driver_Image = request.files['Driver_Image']
    Email = request.form['Email']
    Phone_Number = request.form['Phone_Number']
    Address = request.form['Address']
    ID_Image = request.files['ID_Image']
    License_Number_ID = request.form['License_Number_ID']
    License_Image = request.files['License_Image']

    if Driver_Image and allowed_file(Driver_Image.filename):
        driver_image_filename = secure_filename(Driver_Image.filename)
        Driver_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], driver_image_filename)
        Driver_Image.save(Driver_Image_path)
    else:
        driver_image_filename = None

    if ID_Image and allowed_file(ID_Image.filename):
        id_image_filename = secure_filename(ID_Image.filename)
        ID_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], id_image_filename)
        ID_Image.save(ID_Image_path)
    else:
        id_image_filename = None

    if License_Image and allowed_file(License_Image.filename):
        license_image_filename = secure_filename(License_Image.filename)
        License_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], license_image_filename)
        License_Image.save(License_Image_path)
    else:
        license_image_filename = None

    db = get_db()
    db.execute('INSERT INTO driverdetails (Driver_Name, Date_of_Birthday, Driver_Image, Email, Phone_Number, Address, ID_Image, License_Number_ID, License_Image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
               (Driver_Name, Date_of_Birthday, driver_image_filename, Email, Phone_Number, Address, id_image_filename, License_Number_ID, license_image_filename))
    db.commit()
    
    return 'Well done !!!!!'


                                        #conductordetails
@app.route('/conductordetails')
def show_conductordetails():
    return render_template('conductordetails.html')

@app.route('/conductordetails', methods=['POST'])
def handle_conductordetails():
    Conductor_Name = request.form['Conductor_Name']
    Date_of_Birthday = request.form['Date_of_Birthday']
    Conductor_Image = request.files['Conductor_Image']
    Email = request.form['Email']
    Phone_Number = request.form['Phone_Number']
    Address = request.form['Address']
    ID_Image = request.files['ID_Image']
    Conductor_ID_Number = request.form['Conductor_ID_Number']
    Conductor_ID_Image = request.files['Conductor_ID_Image']

    if Conductor_Image and allowed_file(Conductor_Image.filename):
        filename = secure_filename(Conductor_Image.filename)
        Conductor_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Conductor_Image.save(Conductor_Image_path)
    else:
        filename = None

    if ID_Image and allowed_file(ID_Image.filename):
        filename1 = secure_filename(ID_Image.filename)
        ID_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        ID_Image.save(ID_Image_path)
    else:
        filename1 = None

    if Conductor_ID_Image and allowed_file(Conductor_ID_Image.filename):
        filename2 = secure_filename(Conductor_ID_Image.filename)
        Conductor_ID_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        Conductor_ID_Image.save(Conductor_ID_Image_path)
    else:
        filename2 = None

    db = get_db()
    db.execute('INSERT INTO conductordetails (Conductor_Name, Date_of_Birthday, Conductor_Image, Email, Phone_Number, Address, ID_Image, Conductor_ID_Number, Conductor_ID_Image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (Conductor_Name, Date_of_Birthday, filename, Email, Phone_Number, Address, filename1, Conductor_ID_Number, filename2))
    db.commit()
    
    return 'Well done !!!!!'
                                        #daily_input
@app.route('/input')
def show_input():
    return render_template('input.html')

@app.route('/input', methods=['POST'])
def submit_input():
    trip_number = request.form['trip_number']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    income = request.form['income']
    Address = request.form['Address']
    start_mileage = request.form['start_mileage']
    end_mileage = request.form['end_mileage']
    comment = request.form['comment']

    
    db = get_db()
    db.execute('INSERT INTO input (trip_number, start_time, end_time, income, Address, start_mileage, end_mileage, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
               (trip_number, start_time, end_time, income, Address, start_mileage, end_mileage, comment))
    db.commit()
    
    return 'Well done !!!!!'
                                        #expenses
@app.route('/expenses')
def show_expenses_form():
    return render_template('expenses.html')

@app.route('/expenses', methods=['POST'])
def submit_expenses():
    date = request.form['date']
    Fuel = request.form['Fuel']
    Quantity = request.form['Quantity']
    Cost = request.form['Cost']
    Lunch = request.form['Lunch']
    Pay_Of_Driver = request.form['Pay_Of_Driver']
    Pay_Of_Conductor = request.form['Pay_Of_Conductor']
    comment = request.form['comment']
    
    db = get_db()
    db.execute('INSERT INTO expenses (date, Fuel, Quantity, Cost, Lunch, Pay_Of_Driver, Pay_Of_Conductor, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
               (date, Fuel, Quantity, Cost, Lunch, Pay_Of_Driver, Pay_Of_Conductor, comment))
    db.commit()
    
    return 'Well done !!!!!'

                                        #oil
@app.route('/oil')
def oil():
    return render_template('oil.html')

@app.route('/oil', methods=['POST'])
def submit_oil():
    date = request.form['date']
    Odometar = request.form['Odometar']
    
    Quntity = request.form['Quntity']
    
    
    db = get_db()
    db.execute('INSERT INTO oil (date, Odometar, Quntity) VALUES (?, ?, ?)', 
               (date, Odometar, Quntity))
    db.commit()
    
    return 'Well done !!!!!'
                                        # service
@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/service', methods=['POST'])
def submit_service():
    Date = request.form['Date']
    Odometar = request.form['Odometar']
    
    Quntity = request.form['Quntity']
    check_parts = request.form['check_parts']
    Quntitys = request.form['Quntitys']
    Price = request.form['Price']
    
    
    db = get_db()
    db.execute('INSERT INTO service (Date, Odometar, Quntity, check_parts, Quntitys, Price) VALUES ( ?, ?, ?, ?, ?, ?)', 
               (Date, Odometar, Quntity, check_parts, Quntitys, Price))
    db.commit()
    
    return 'Well done !!!!!'
                                        #left_front_tyer
@app.route('/left_front_tyer')
def left_front_tyer():
    return render_template('left_front_tyer.html')

@app.route('/left_front_tyer', methods=['POST'])
def submit_left_front_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)
    else:
        filename = None

    db = get_db()
    db.execute('INSERT INTO left_front_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'
                                        #rigth_front_tyer
@app.route('/rigth_front_tyer')
def rigth_front_tyer():
    return render_template('rigth_front_tyer.html')

@app.route('/rigth_front_tyer', methods=['POST'])
def submit_rigth_front_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)
    else:
        filename = None

    db = get_db()
    db.execute('INSERT INTO rigth_front_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'
                                        #left_back_inside_tyer
@app.route('/left_back_inside_tyer')
def left_back_inside_tyer():
    return render_template('left_back_inside_tyer.html')

@app.route('/left_back_inside_tyer', methods=['POST'])
def submit_left_back_inside_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    filename = None
    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)

    db = get_db()
    db.execute('INSERT INTO left_back_inside_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'
                                        #left_back_outside_tyer
@app.route('/left_back_outside_tyer')
def left_back_outside_tyer():
    return render_template('left_back_outside_tyer.html')

@app.route('/left_back_outside_tyer', methods=['POST'])
def submit_left_back_outside_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)
    else:
        filename = None

    db = get_db()
    db.execute('INSERT INTO left_back_outside_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'
                                        #right_back_inside_tyer
@app.route('/right_back_inside_tyer')
def right_back_inside_tyer():
    return render_template('right_back_inside_tyer.html')

@app.route('/right_back_inside_tyer', methods=['POST'])
def submit_right_back_inside_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    filename = None
    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)

    db = get_db()
    db.execute('INSERT INTO right_back_inside_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'

                                        #rigth_back_outside_tyer
@app.route('/rigth_back_outside_tyer')
def rigth_back_outside_tyer():
    return render_template('rigth_back_outside_tyer.html')

@app.route('/rigth_back_outside_tyer', methods=['POST'])
def submit_rigth_back_outside_tyer():
    Tyer_Change_Data = request.form['Tyer_Change_Data']
    Tyer_Type = request.form['Tyer_Type']
    Odometar = request.form['Odometar']
    pressure = request.form['pressure']
    Tyer_Price = request.form['Tyer_Price']
    Bill_Image = request.files['Bill_Image']
    comment = request.form['comment']

    filename = None
    if Bill_Image and allowed_file(Bill_Image.filename):
        filename = secure_filename(Bill_Image.filename)
        Bill_Image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Bill_Image.save(Bill_Image_path)

    db = get_db()
    db.execute('INSERT INTO rigth_back_outside_tyer (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, Bill_Image, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', 
               (Tyer_Change_Data, Tyer_Type, Odometar, pressure, Tyer_Price, filename, comment))
    db.commit()
    
    return 'Well done !!!!!'

                                        #issues

@app.route('/issues', methods=['GET', 'POST'])
def issues():
    if request.method == 'POST':
        comment = request.form['comment']
        issu_Date = request.form['Date']

        # Validate inputs
        if not comment or not issu_Date:
            return "Error: Comment and Date are required!", 400

        # Insert data into the database
        db = get_db()
        db.execute('INSERT INTO issues (comment, issu_Date) VALUES (?, ?)', (comment, issu_Date))
        db.commit()
        return "Well done !!!!"

    # Render the form for GET requests
    return render_template('issues.html')
                                                                         ######## issues_view ##########    


@app.route('/issues_view')
def issues_view():
    db = get_db()
    
    # Fetch comment (issue description) and issu_Date ordered by id
    issues = db.execute('SELECT id, comment, issu_Date FROM issues ORDER BY id').fetchall()

    # Debugging: Print issues to check if the data is correct
    print(issues)

    return render_template('issues_view.html', issues=issues)

                                                                    ######## issue_reson_delete ########## 

@app.route('/delete_issue/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    db = get_db()
    # Delete the issue with the given ID
    db.execute('DELETE FROM issues WHERE id = ?', (issue_id,))
    db.commit()
    return redirect('/issues_view')  # Redirect back to the issues view



                                                 #Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    db = get_db()  # Connect to the database

                                                                                             ############## net profit ################

    # Fetch the total income from the 'input' table
    income_result = db.execute('SELECT SUM(income) AS total_income FROM input').fetchone()
    total_income = float(income_result[0]) if income_result[0] else 0

    # Fetch the total expenses from the 'expenses' table
    expenses_result = db.execute('''
        SELECT 
            SUM(Cost) AS total_cost, 
            SUM(Lunch) AS total_lunch, 
            SUM(Pay_Of_Driver) AS total_driver_pay, 
            SUM(Pay_Of_Conductor) AS total_conductor_pay, 
            SUM(Fuel) AS total_fuel 
        FROM expenses
    ''').fetchone()

    # Extract and ensure no null values
    total_cost = float(expenses_result[0]) if expenses_result[0] else 0
    total_lunch = float(expenses_result[1]) if expenses_result[1] else 0
    total_driver_pay = float(expenses_result[2]) if expenses_result[2] else 0
    total_conductor_pay = float(expenses_result[3]) if expenses_result[3] else 0
    total_fuel = float(expenses_result[4]) if expenses_result[4] else 0

    # Calculate daily profit
    total_expenses = total_cost + total_lunch + total_driver_pay + total_conductor_pay + total_fuel
    daily_profit = total_income - total_expenses

    # Automatically calculate the start date as the first day of the current month
    today = datetime.now()
    start_date = datetime(today.year, today.month, 1)  # First day of the current month
    day_difference = (today - start_date).days
    day_in_cycle = day_difference + 1  # Add 1 because day_difference starts from 0

    # Calculate daily_profit
    daily_profit = total_income - total_expenses

                                                                                   ################ yesterday profit ################
    # Fetch the last row of income
    last_income_result = db.execute('SELECT income FROM input ORDER BY id DESC LIMIT 1').fetchone()
    last_income = float(last_income_result[0]) if last_income_result else 0

    # Fetch the last row of expenses
    last_expenses_result = db.execute('''
        SELECT 
            Cost, 
            Lunch, 
            Pay_Of_Driver, 
            Pay_Of_Conductor, 
            Fuel 
        FROM expenses 
        ORDER BY id DESC LIMIT 1
    ''').fetchone()

    # Extract and ensure no null values for expenses
    last_cost = float(last_expenses_result[0]) if last_expenses_result and last_expenses_result[0] else 0
    last_lunch = float(last_expenses_result[1]) if last_expenses_result and last_expenses_result[1] else 0
    last_driver_pay = float(last_expenses_result[2]) if last_expenses_result and last_expenses_result[2] else 0
    last_conductor_pay = float(last_expenses_result[3]) if last_expenses_result and last_expenses_result[3] else 0
    last_fuel = float(last_expenses_result[4]) if last_expenses_result and last_expenses_result[4] else 0

    # Calculate total expenses for the last row
    last_total_expenses = last_cost + last_lunch + last_driver_pay + last_conductor_pay + last_fuel

    # Calculate yesterday's profit
    yesterday_profit = last_income - last_total_expenses

    

                                                                                      ################ expiry date insurence ################
    # Connect to the database
    db = sqlite3.connect('instance/my_database.db')  # Replace with your database file
    db.row_factory = sqlite3.Row  # Allow access to rows as dictionaries

    # Fetch the expiry date value from the 'insurence' table
    insurence = db.execute('SELECT expiry_date AS latest_date FROM insurence ORDER BY id DESC LIMIT 1').fetchone()

    try:
        # Parse the date if it exists
        if insurence and insurence['latest_date']:
            latest_date = datetime.strptime(insurence['latest_date'], '%Y-%m-%d')  # Ensure the format matches the database
        else:
            latest_date = None

        today = datetime.now()
        output = "0 days"

        # Perform the calculation and format the output
        if latest_date:
            difference = (latest_date - today).days
            if difference > 0:
                output = f"expires in {difference} days"
            elif difference < 0:
                output = f"expired {abs(difference)} days ago"
            else:
                output = "expires today"
            print(output)
        else:
            print("No valid expiry date found.")
    except Exception as e:
        print(f"An error occurred: {e}")

                                                                                         ################ expiry date revenue ################
    # Connect to the database
    db = sqlite3.connect('instance/my_database.db')  # Replace with your database file
    db.row_factory = sqlite3.Row  # Allow access to rows as dictionaries

    # Fetch the expiry date value from the 'revenue' table
    revenue = db.execute('SELECT expiry_date AS latest_date1 FROM revenue ORDER BY id DESC LIMIT 1').fetchone()

    try:
        # Parse the date if it exists
        if revenue and revenue['latest_date1']:
            latest_date1 = datetime.strptime(revenue['latest_date1'], '%Y-%m-%d')  # Ensure the format matches the database
        else:
            latest_date1 = None

        today = datetime.now()
        output1 = "No valid expiry date found"  # Initialize with a default message

        # Perform the calculation and format the output
        if latest_date1:
            difference = (latest_date1 - today).days
            if difference > 0:
                output1 = f"expires in {difference} days"
            elif difference < 0:
                output1 = f"expired {abs(difference)} days ago"
            else:
                output1 = "expires today"

        print(output1)

    except Exception as e:
        print(f"An error occurred: {e}")

                                                                                         ################ expiry date emssion ################
    # Connect to the database
    db = sqlite3.connect('instance/my_database.db')  # Replace with your database file
    db.row_factory = sqlite3.Row  # Allow access to rows as dictionaries

    # Fetch the expiry date value from the 'emssion' table
    emssion = db.execute('SELECT expiry_date AS latest_date2 FROM emssion ORDER BY id DESC LIMIT 1').fetchone()

    try:
        # Parse the date if it exists
        if emssion and emssion['latest_date2']:
            latest_date2 = datetime.strptime(emssion['latest_date2'], '%Y-%m-%d')  # Ensure the format matches the database
        else:
            latest_date2 = None

        today = datetime.now()
        output2 = "No valid expiry date found"  # Initialize with a default message

        # Perform the calculation and format the output
        if latest_date2:
            difference = (latest_date2 - today).days
            if difference > 0:
                output2 = f"expires in {difference} days"
            elif difference < 0:
                output2 = f"expired {abs(difference)} days ago"
            else:
                output2 = "expires today"

        print(output2)

    except Exception as e:
        print(f"An error occurred: {e}")

                                                                                         ################ expiry date permit ################
    # Connect to the database
    db = sqlite3.connect('instance/my_database.db')  # Replace with your database file
    db.row_factory = sqlite3.Row  # Allow access to rows as dictionaries

    # Fetch the expiry date value from the 'permit' table
    permit = db.execute('SELECT expiry_date AS latest_date3 FROM permit ORDER BY id DESC LIMIT 1').fetchone()

    try:
        # Parse the date if it exists
        if permit and permit['latest_date3']:
            latest_date3 = datetime.strptime(permit['latest_date3'], '%Y-%m-%d')  # Ensure the format matches the database
        else:
            latest_date3 = None

        today = datetime.now()
        output3 = "No valid expiry date found"  # Initialize with a default message

        # Perform the calculation and format the output
        if latest_date3:
            difference = (latest_date3 - today).days
            if difference > 0:
                output3 = f"expires in {difference} days"
            elif difference < 0:
                output3 = f"expired {abs(difference)} days ago"
            else:
                output3 = "expires today"

        print(output3)

    except Exception as e:
        print(f"An error occurred: {e}")


    

                                                                                          ################ maintance ################

    # Initialize profit_percentage to None
    profit_percentage = None

    # Check if daily_profit is greater than zero
    if daily_profit > 0:
    # Calculate 20% of daily_profit
        profit_percentage = daily_profit * 0.20

                                                                                        ################ more oil change ################

    Odo = db.execute('SELECT Odometar AS latest_end FROM oil ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(Odo[0]) if Odo and Odo[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0  # Ensure end is not None


    more = '0'

    more = latest_Odo - latest_end

    # Perform the calculation and format the output
    if more > 0:
        more1 = f"more {more} km"
    else :
        more1 = '0km'

                                                                                         ################ more service change ################

    services = db.execute('SELECT Odometar AS latest_end FROM service ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(services[0]) if services and services[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0 


    service = '0'

    service = latest_Odo - latest_end

    # Perform the calculation and format the output
    if service > 0:
        services1 = f"more {service} km"
    else :
        services1 = '0km'

                                                                                         ################ more left_front_tyer ################

    left = db.execute('SELECT Odometar AS latest_end FROM left_front_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(left[0]) if left and left[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0 


    left_front = '0'

    left_front = latest_Odo - latest_end

    # Perform the calculation and format the output
    if left_front > 0:
        left_front1 = f"more {left_front} km"
    else :
        left_front1 = '0km'

                                                                                            ################ more right_front_tyer ################

    right = db.execute('SELECT Odometar AS latest_end FROM rigth_front_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(right[0]) if right and right[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0


    right_front = '0'

    right_front = latest_Odo - latest_end

    # Perform the calculation and format the output
    if right_front > 0:
        right_front1 = f"more {right_front} km"
    else :
        right_front1 = '0km'

                                                                                         ################ more left_back_outside_tyer ################

    left_back_outside = db.execute('SELECT Odometar AS latest_end FROM left_back_outside_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(left_back_outside[0]) if left_back_outside and left_back_outside[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0


    left_back_outside_tyer = '0'

    left_back_outside_tyer = latest_Odo - latest_end

    # Perform the calculation and format the output
    if left_back_outside_tyer > 0:
        left_back_outside_tyer1 = f"more {left_back_outside_tyer} km"
    else :
        left_back_outside_tyer1 = '0km'

                                                                                      ################ more left_back_inside_tyer ################

    left_back_inside = db.execute('SELECT Odometar AS latest_end FROM left_back_inside_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(left_back_inside[0]) if left_back_inside and left_back_inside[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0


    left_back_inside_tyer = '0'

    left_back_inside_tyer = latest_Odo - latest_end

    # Perform the calculation and format the output
    if left_back_inside_tyer > 0:
        left_back_inside_tyer1 = f"more {left_back_inside_tyer} km"
    else :
        left_back_inside_tyer1 = '0km'


                                                                                     ################ more rigth_back_outside_tyer ################

    rigth_back_outside = db.execute('SELECT Odometar AS latest_end FROM rigth_back_outside_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(rigth_back_outside[0]) if rigth_back_outside and rigth_back_outside[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0


    rigth_back_outside_tyer = '0'

    rigth_back_outside_tyer = latest_Odo - latest_end

    # Perform the calculation and format the output
    if rigth_back_outside_tyer > 0:
        rigth_back_outside_tyer1 = f"more {rigth_back_outside_tyer} km"
    else :
        rigth_back_outside_tyer1 = '0km'

                                                                                        ################ more right_back_inside_tyer ################

    right_back_inside = db.execute('SELECT Odometar AS latest_end FROM right_back_inside_tyer ORDER BY id DESC LIMIT 1').fetchone()
    latest_Odo = float(right_back_inside[0]) if right_back_inside and right_back_inside[0] else 0  # Ensure Odo is not None

    end = db.execute('SELECT end_mileage AS latest_end FROM input ORDER BY id DESC LIMIT 1').fetchone()
    latest_end = float(end[0]) if end and end[0] else 0



    right_back_inside_tyer = '0'

    right_back_inside_tyer = latest_Odo - latest_end

    # Perform the calculation and format the output
    if right_back_inside_tyer > 0:
        right_back_inside_tyer1 = f"more {right_back_inside_tyer} km"
    else :
        right_back_inside_tyer1 = '0km'


                                                                                       ################ issues_counter ################

    result = db.execute('SELECT COUNT(id) FROM issues').fetchone()
    issue_count = result[0] if result else 0
                                                                                   ################ latest_comment ################  



    return  render_template(
        'dashboard.html',
        daily_profit=daily_profit,
        day_in_cycle=day_in_cycle,
        profit_percentage=profit_percentage,
        more1=more1,
        services1=services1,
        left_front1=left_front1,
        right_front1=right_front1,
        left_back_outside_tyer1=left_back_outside_tyer1,
        left_back_inside_tyer1=left_back_inside_tyer1,
        rigth_back_outside_tyer1=rigth_back_outside_tyer1,
        right_back_inside_tyer1=right_back_inside_tyer1,
        output=output,
        output1=output1,
        output2=output2,
        output3=output3,
        issue_count=issue_count, 
        yesterday_profit=yesterday_profit       
    
    )
                                           



if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    init_db()
    app.run(debug=True)

