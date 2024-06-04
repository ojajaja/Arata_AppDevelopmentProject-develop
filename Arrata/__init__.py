from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import *
from random import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shelve, os, re, uuid, json
from datetime import date
from . import Staff, Customer
from . import database
from . import CRUD
from . import ReneQueue
from . import PaymentEason
from . import WenkaiVoucher
from . import Summon
from . import GabMenuCart
from . import Creditcard
from flask.cli import with_appcontext
import datetime



app = Flask(__name__)
app.secret_key = 'App Development Project'
mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'arata.group.sg@gmail.com'
app.config["MAIL_PASSWORD"] = 'Arata.Group.SG'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
otp_number = randint(000000,999999)
UPLOAD_FOLDER = 'Arrata/static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# create_database
customer_dict = {}
staff_dict = {}
db = shelve.open('Account_Management_System.db', 'c')
try:
    customer_dict = {}
    staff_dict = {}
    if 'Customer' in db and 'Staff' in db:
        customer_dict = db['Customer']
        staff_dict = db['Staff']
    else:
        db['Customer'] = customer_dict
        db['Staff'] = staff_dict
except IOError:
    print("Error in opening Account Management System.db.db")
db.close()


# create_admin
staff_dict = {}
db = shelve.open('Account_Management_System.db', 'c')
try:
    staff_dict = db['Staff']
except:
    print("Error in retrieving Staff from Account_Management_System.db.")
email = 'admin@admin.com'
password_type = 'admin'
staff_profile_image = 'default_profile.jpg'
password = generate_password_hash(password_type, method='sha256')
date_added = date.today()
admin_staff = Staff.Staff(email, password, date_added, 1, staff_profile_image)
staff_dict[admin_staff.get_staff_id()] = admin_staff
db['Staff'] = staff_dict
db.close()


def customer_count():
    customer_dict = {}
    db = shelve.open('Account_Management_System.db', 'r')
    customer_dict = db['Customer']
    db.close()
    customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        customer_list.append(customer)
    if len(customer_list) > 0:
        customer_counter = customer_list[-1].get_customer_id() + 1
    else:
        customer_counter = 1

    return customer_counter


def staff_count():
    staff_dict = {}
    db = shelve.open('Account_Management_System.db', 'r')
    staff_dict = db['Staff']
    db.close()
    staff_list = []
    for key in staff_dict:
        staff = staff_dict.get(key)
        staff_list.append(staff)
    if len(staff_list) > 0:
        staff_counter = staff_list[-1].get_staff_id() + 1
    else:
        staff_counter = 0

    return staff_counter


def valid(phone_number):
    phone_number_pattern = re.compile("(6|8|9)[0-9]{7}")
    return phone_number_pattern.match(phone_number)


def check_password(password_retype):
    value = True

    if len(password_retype) < 8:
        print('length should be at least 8')
        value = False

    if not any(char.isdigit() for char in password_retype):
        print('Password should have at least one numeral')
        value = False

    if not any(char.isupper() for char in password_retype):
        print('Password should have at least one uppercase letter')
        value = False

    if not any(char.islower() for char in password_retype):
        print('Password should have at least one lowercase letter')
        value = False

    if value:
        return value


@app.route('/')
def base():
    if 'customer_id' in session:
        return render_template('home.html', loggedin=True)
    else:
        return render_template('home.html')


@app.route('/home')
def home():
    if 'customer_id' in session:
        return render_template('home.html', loggedin=True)
    else:
        return render_template('home.html')


@app.route('/customer_signin_signup')
def customer_signin_signup():
    if 'customer_id' in session:
        return redirect(url_for('customer_id'))
    else:
        return render_template('AccountManagement/customer_signin_signup.html')


@app.route('/customer_signin_signup/signin', methods=['GET', 'POST'])
def customer_signin():
    if request.method == "POST":
        password_type = request.form['signin_password']
        customer_email = request.form['signin_email']
        customer_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        customer_dict = db['Customer']
        for customer_id in customer_dict:
            customer = customer_dict[customer_id].get_email()
            if customer_email == customer:
                get_password = customer_dict[customer_id].get_password_type()
                if check_password_hash(get_password, password_type):
                    session["customer_id"] = customer_id
                    db.close()
                    return redirect(url_for('customer_id'))
                else:
                    flash('Incorrect email or password')
                    return redirect(url_for('customer_signin_signup'))
            else:
                continue
        flash('Incorrect email or password')
        return redirect(url_for('customer_signin_signup'))
    else:
        if 'customer_id' in session:
            return redirect(url_for('customer_id'))
        else:
            return redirect(url_for('customer_signin_signup'))


@app.route('/otp', methods=['GET','POST'])
def otp():
    if 'temporary' in session:
        if request.method == "GET":
            staff_dict = {}
            db = shelve.open('Account_Management_System.db', 'r')
            staff_dict = db['Staff']
            for staff_id in staff_dict:
                if staff_id == session['temporary']:
                    try:
                        email = staff_dict[staff_id].get_email()
                        msg = Message('OTP', sender='arata.group.sg@gmail.com', recipients=[email])
                        msg.body = str(otp_number)
                        mail.send(msg)
                        return render_template('AccountManagement/otp.html')
                    except:
                        flash("error in sending otp")
                        return redirect(url_for('staff_signin'))
        if request.method == "POST":
            type_otp = request.form['type_otp']
            if str(otp_number) == type_otp:
                staff_dict = {}
                db = shelve.open('Account_Management_System.db', 'r')
                staff_dict = db['Staff']
                for staff_id in staff_dict:
                    if staff_id == session['temporary']:
                        session['staff_id'] = staff_id
                        return redirect(url_for('staff_id'))
            else:
                return redirect(url_for('staff_signin'))
    else:
        return redirect(url_for('customer_signin_signup'))


@app.route('/customer_signin_signup/signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == "POST":
        session.pop("customer_id", None)
        password_type = request.form['signup_password']
        password_retype = request.form['signup_retype_password']
        phone_number = request.form['signup_phone_number']
        profile_picture = 'default_profile.jpg'
        if valid(phone_number):
            pass
        else:
            flash('Incorrect phone number')
            return render_template('AccountManagement/customer_signin_signup.html')
        gender = request.form['signup_gender']
        if gender == 'Male' or gender == 'Female':
            pass
        else:
            flash('Gender can only be male or female')
            return render_template('AccountManagement/customer_signin_signup.html')
        if check_password(password_retype):
            if password_retype != password_type:
                flash('Incorrect password and retype password')
                return render_template('AccountManagement/customer_signin_signup.html')
            else:
                name = request.form['signup_name']
                date_of_birth = request.form['signup_date_of_birth']
                customer_email = request.form['signup_email']
                password = generate_password_hash(password_retype, method='sha256')
                customer_dict = {}
                db = shelve.open('Account_Management_System.db', 'c')
                try:
                    customer_dict = db['Customer']
                except:
                    print("Error in retrieving Customers from Account Management System.db.")
                for customer_id in customer_dict:
                    get_customer_email = customer_dict[customer_id].get_email()
                    if customer_email == get_customer_email:
                        flash('This email is used. If you forgot you password, please select forgot password')
                        return redirect(url_for('customer_signin_signup'))
                    else:
                        break
                initial_point = 5000
                customer_info = Summon.Point(customer_email, password, name, gender, date_of_birth, phone_number,customer_count(), profile_picture, initial_point)
                customer_info.account_type_added()
                customer_dict[customer_info.get_customer_id()] = customer_info
                db['Customer'] = customer_dict
                session["customer_id"] = customer_info.get_customer_id()


                # my_voucher_dict = {}
                # ab = shelve.open('my_voucher.db', 'c')
                # try:
                #     my_voucher_dict = ab['my_voucher']
                # except:
                #     print("Error in customer signup")

                with shelve.open('my_voucher.db', 'c') as ab:
                    my_voucher_dict = {}
                    try:
                        my_voucher_dict = ab['my_voucher']
                    except:
                        print("Error in customer signup")
                    temp_dict = {}
                    voucher_info = ''
                    temp_dict[customer_info.get_customer_id()] = voucher_info
                    my_voucher_dict.update(temp_dict)
                    ab['my_voucher'] = my_voucher_dict

                # voucher_info = ''
                # my_voucher_dict[customer_info.get_customer_id()] = voucher_info
                # ab['my_voucher'] = my_voucher_dict
                # ab.close()
                db.close()
                return redirect(url_for("customer_id"))
        else:
            flash('Please ensure that your password must have 1 uppercase, 1 lowercase, 1 special character and at least 8 digit.')
            return render_template('AccountManagement/customer_signin_signup.html')

    return render_template('AccountManagement/customer_signin_signup.html')


@app.route('/staff_signin', methods=['GET', 'POST'])
def staff_signin():
    if request.method == "POST":
        staff_email = request.form['email']
        password_type = request.form['password']
        staff_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        staff_dict = db['Staff']
        for staff_id in staff_dict:
            staff = staff_dict[staff_id].get_email()
            if staff_email == staff:
                dict_password = staff_dict[staff_id].get_password_type()
                if check_password_hash(dict_password, password_type):
                    db.close()
                    if staff_dict[staff_id].get_email() == 'admin@admin.com':
                        session['staff_id'] = staff_id
                        return redirect(url_for('staff_id'))
                    else:
                        session['temporary'] = staff_id
                        return redirect(url_for('otp'))
                else:
                    flash('Incorrect email or password')
                    return render_template('AccountManagement/staff_signin.html')
            else:
                continue
        flash('Incorrect email or password')
        return render_template('AccountManagement/staff_signin.html')
    else:
        if 'staff_id' in session:
            return redirect(url_for('staff_id'))
        else:
            return render_template('AccountManagement/staff_signin.html')


@app.route('/staff_logout')
def staff_logout():
    session.pop("staff_id", None)
    return redirect(url_for('staff_signin'))


@app.route('/staff_id')
def staff_id():
    if 'staff_id' in session:
        return redirect(url_for('staff_management_home'))
    else:
        return redirect(url_for('staff_signin'))


@app.route('/staff_management_home')
def staff_management_home():
    if 'staff_id' in session:
        staff_dict = {}
        staff = []
        db = shelve.open('Account_Management_System.db', 'r')
        staff_dict = db['Staff']
        for staff_id in staff_dict:
            staff.append(staff_id)
        number_of_staff = len(staff)

        customer_dict = {}
        customer = []
        db = shelve.open('Account_Management_System.db', 'r')
        customer_dict = db['Customer']
        for customer_id in customer_dict:
            customer.append(customer_id)
        number_of_customer = len(customer)
        return render_template('AccountManagement/staff_management_home.html', number_of_staff=number_of_staff, number_of_customer=number_of_customer)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff_dict = {}
    db = shelve.open('Account_Management_System.db', 'w')
    staff_dict = db['Staff']

    staff_dict.pop(staff_id)

    db['Staff'] = staff_dict
    db.close()
    return redirect(url_for('staff_account_management'))


@app.route('/staff_account_management', methods=['GET', 'POST'])
def staff_account_management():
    if 'staff_id' in session:
        staff_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff_list = []
        for key in staff_dict:
            staff = staff_dict.get(key)
            staff_list.append(staff)
        return render_template('AccountManagement/staff_account_management.html', staff_list=staff_list)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/add_staff_account', methods=['GET', 'POST'])
def add_staff_account():
    if 'staff_id' in session:
        if request.method == 'POST':
            staff_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            staff_dict = db['Staff']
            email = request.form['email']
            for staff_id in staff_dict:
                staff = staff_dict[staff_id].get_email()
                if staff == email:
                    flash('Account found')
                    return redirect(url_for("staff_account_management"))
                else:
                    continue
            password_type = request.form['password']
            date_added = date.today()
            staff_profile_image = 'default_profile.jpg'
            password = generate_password_hash(password_type, method='sha256')
            staff_info = Staff.Staff(email, password, date_added, staff_count(), staff_profile_image)
            staff_info.account_type_added()
            staff_dict[staff_info.get_staff_id()] = staff_info
            db['Staff'] = staff_dict
            db.close()
            flash('New Staff is added')
            return redirect(url_for("staff_account_management"))
    else:
        return redirect(url_for("staff_signin"))
    return render_template('AccountManagement/add_staff_account.html')


@app.route('/add_customer_account', methods=['GET', 'POST'])
def add_customer_account():
    if 'staff_id' in session:
        if request.method == "POST":
            session.pop("customer_id", None)
            password_type = request.form['password']
            name = request.form['name']
            gender = request.form['gender']
            date_of_birth = request.form['date_of_birth']
            phone_number = request.form['phone_number']
            customer_email = request.form['email']
            password = generate_password_hash(password_type, method='sha256')
            initial_point = 5000
            if valid(phone_number):
                pass
            else:
                flash('Incorrect phone number')
                return redirect(url_for('add_customer_account'))
            if gender == 'Male' or gender == 'Female':
                pass
            else:
                flash('Gender can only be male or female')
                return redirect(url_for('add_customer_account'))
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'c')
            try:
                customer_dict = db['Customer']
            except:
                print("Error in retrieving Customers from Account Management System.db.")
            for customer_id in customer_dict:
                get_customer_email = customer_dict[customer_id].get_email()
                if customer_email == get_customer_email:
                    flash('This email is used')
                    return redirect(url_for('add_customer_account'))
                else:
                    break
            profile_picture = 'default_profile.jpg'
            customer_info = Summon.Point(customer_email, password, name, gender, date_of_birth, phone_number,
                                         customer_count(), profile_picture, initial_point)
            customer_info.account_type_added()
            customer_dict[customer_info.get_customer_id()] = customer_info

            db['Customer'] = customer_dict


            # my_voucher_dict = {}
            # ab = shelve.open('my_voucher.db', 'c')
            # try:
            #     my_voucher_dict = ab['my_voucher']
            # except:
            #     print("Error in customer signup")

            with shelve.open('my_voucher.db', 'c') as ab:
                my_voucher_dict = {}
                try:
                    my_voucher_dict = ab['my_voucher']
                except:
                    print("Error in customer signup")
                temp_dict = {}
                voucher_info = ''
                temp_dict[customer_info.get_customer_id()] = voucher_info
                my_voucher_dict.update(temp_dict)
                ab['my_voucher'] = my_voucher_dict

            # voucher_info = ''
            # my_voucher_dict[customer_info.get_customer_id()] = voucher_info
            # ab['my_voucher'] = my_voucher_dict
            # ab.close()
            db.close()
            flash('Add Successfully')
            return redirect(url_for("customer_account_management"))
    else:
        return redirect(url_for('staff_signin'))
    return render_template('AccountManagement/add_customer_account.html')


@app.route('/update_staff_account/<int:staff_id>', methods=['GET', 'POST'])
def update_staff_account(staff_id):
    if 'staff_id' in session:
        if request.method == 'POST':
            email = request.form['email']
            password_type = request.form['password']
            staff_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            staff_dict = db['Staff']
            try:
                staff_dict = db['Staff']
            except:
                print("Error in creating staff from Account Management System.db.")
            staff_profile_image = staff_dict[staff_id].get_staff_profile_image()
            date_added = staff_dict[staff_id].get_date_added()
            if email == '':
                get_email = staff_dict[staff_id].get_email()
            else:
                get_email = email
            if password_type == '':
                get_password_type = staff_dict[staff_id].get_password_type()
            else:
                password = generate_password_hash(
                    password_type, method='sha256')
                get_password_type = password
            staff_info = Staff.Staff(
                get_email, get_password_type, date_added, staff_id, staff_profile_image)
            staff_dict[staff_info.get_staff_id()] = staff_info
            db['Staff'] = staff_dict
            db.close()
            flash('Update Successfully')
            return redirect(url_for("staff_account_management"))
        else:
            staff_dict = {}
            db = shelve.open('Account_Management_System.db', 'r')
            staff_dict = db['Staff']
            db.close()

            staff_list = []
            for key in staff_dict:
                if key == staff_id:
                    staff = staff_dict.get(key)
                    staff_list.append(staff)
            return render_template('AccountManagement/update_staff_account.html', staff_list=staff_list)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/update_customer_account/<int:customer_id>', methods=['GET', 'POST'])
def update_customer_account(customer_id):
    if 'staff_id' in session:
        if request.method == 'POST':
            email = request.form['email']
            password_type = request.form['password']
            name = request.form['name']
            gender = request.form['gender']
            date_of_birth = request.form['date_of_birth']
            phone_number = request.form['phone_number']
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            try:
                customer_dict = db['Customer']
            except:
                print("Error in creating staff from Account Management System.db.")
            profile_picture = customer_dict[customer_id].get_profile_picture()
            if email == '':
                get_email = customer_dict[customer_id].get_email()
            else:
                get_email = email
            if password_type == '':
                get_password_type = customer_dict[customer_id].get_password_type()
            else:
                password = generate_password_hash(
                    password_type, method='sha256')
                get_password_type = password
            if name == '':
                get_name = customer_dict[customer_id].get_name()
            else:
                get_name = name
            if gender == '':
                get_gender = customer_dict[customer_id].get_gender()
            else:
                get_gender = gender
            if date_of_birth == '':
                get_date_of_birth = customer_dict[customer_id].get_date_of_birth()
            else:
                get_date_of_birth = date_of_birth
            if phone_number == '':
                get_phone_number = customer_dict[customer_id].get_phone_number()
            else:
                get_phone_number = phone_number
            customer_info = Customer.Customer(get_email, get_password_type, get_name, get_gender, get_date_of_birth, get_phone_number, customer_id, profile_picture)
            customer_dict[customer_info.get_customer_id()] = customer_info
            db['Customer'] = customer_dict
            db.close()
            flash('Update successful')
            return redirect(url_for("customer_account_management"))
        else:
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'r')
            customer_dict = db['Customer']
            db.close()

            customer_list = []

            for key in customer_dict:
                if key == customer_id:
                    customer = customer_dict.get(key)
                    customer_list.append(customer)
            return render_template('AccountManagement/update_customer_account.html', customer_list=customer_list)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/staff_profile', methods=['GET', 'POST'])
def staff_profile():
    if 'staff_id' in session:
        staff_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff_list = []
        for key in staff_dict:
            if key == session['staff_id']:
                staff = staff_dict.get(key)
                staff_list.append(staff)
        for staff in staff_list:
            profile = staff.get_staff_profile_image()
        return render_template('AccountManagement/staff_profile.html', profile=profile, staff_list=staff_list)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/Staff_change_password', methods=['GET', 'POST'])
def staff_change_password():
    if 'staff_id' in session:
        if request.method == "POST":
            new_password = request.form['new_password']
            confirm_new_password = request.form['confirm_new_password']
            staff_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            staff_dict = db['Staff']
            for staff_id in staff_dict:
                get_staff_id = session['staff_id']
                if staff_id == get_staff_id:
                    if new_password == confirm_new_password:
                        staff_email = staff_dict[staff_id].get_email()
                        date_added = staff_dict[staff_id].get_date_added()
                        staff_profile_image = staff_dict[staff_id].get_staff_profile_image()
                        password = generate_password_hash(confirm_new_password, method='sha256')
                        staff_info = Staff.Staff(staff_email, password, date_added, staff_id, staff_profile_image)
                        staff_dict[staff_info.get_staff_id()] = staff_info
                        db['Staff'] = staff_dict
                        flash('Password change successfully')
                        return redirect(url_for('staff_profile'))
                    else:
                        break
                else:
                    continue
            flash('Password was not change. Please ensure that all the information is correct')
            db.close()
        return render_template('AccountManagement/Staff_change_password.html')
    else:
        return render_template('AccountManagement/staff_signin.html')


@app.route('/customer_account_management', methods=['GET', 'POST'])
def customer_account_management():
    if 'staff_id' in session:
        customer_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        customer_dict = db['Customer']
        db.close()

        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            customer_list.append(customer)
        return render_template('AccountManagement/customer_account_management.html', customer_list=customer_list)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer_dict = {}
    db = shelve.open('Account_Management_System.db', 'w')
    customer_dict = db['Customer']

    customer_dict.pop(customer_id)

    db['Customer'] = customer_dict
    db.close()
    flash('Delete Successfully')

    return redirect(url_for('customer_account_management'))


@app.route('/customer_logout')
def customer_logout():
    session.pop("customer_id", None)
    return redirect(url_for('customer_signin_signup'))


@app.route('/customer_id')
def customer_id():
    if 'customer_id' in session:
        customer_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        customer_dict = db['Customer']
        for customer_id in customer_dict:
            if customer_id == session['customer_id']:
                

                birthday_date = customer_dict[customer_id].get_date_of_birth()
                birthday = str(birthday_date[5:10])
                current_date = date.today()
                current_month = current_date.month
                current_day = current_date.day
                if current_month < 10:
                    current_month = '0' + str(current_month)
                if current_day < 10:
                    current_day = '0' + str(current_day)
                current = str(current_month) + '-' + str(current_day)
                if birthday == current:
                    name = customer_dict[customer_id].get_name()
                    email = customer_dict[customer_id].get_email()
                    msg = Message('Happy Birthday', sender='arata.group.sg@gmail.com', recipients=[email])
                    msg.body = str('Your birthday promo code is Birthday')
                    mail.send(msg)
                    my_voucher_dict = {}
                    ab = shelve.open('my_voucher.db', 'w')
                    my_voucher_dict = ab['my_voucher']

                    for voucher in my_voucher_dict:
                        print(session['customer_id'])

                        key_list = list(my_voucher_dict.keys())
                        print(key_list)
                        new_voucher_list = []
                        my_voucher_list = []
                        customer_list = []
                        if session['customer_id'] in key_list:
                            customer = customer_dict.get(session['customer_id'])
                            customer_list.append(customer)

                            customers = customer_list[0]
                            id = customers.get_customer_id()
                            tday = datetime.date.today()
                            tdelta = datetime.timedelta(days=31)

                            expiring_date = tday + tdelta
                            print('customer_id in session')
                            voucher = my_voucher_dict.get(session['customer_id'])
                            if isinstance(voucher, list):
                                new_voucher = Summon.my_voucher('Birthday Voucher', expiring_date)
                                new_voucher_list.append(new_voucher)
                                final_list = voucher + new_voucher_list

                            else:
                                my_voucher_list.append(voucher)

                                new_voucher = Summon.my_voucher('Birthday Voucher', expiring_date)
                                new_voucher_list.append(new_voucher)
                                final_list = my_voucher_list + new_voucher_list
                                if final_list[0] == '':
                                    final_list.pop(0)
                                else:
                                    pass
                            my_voucher_dict[id] = final_list
                            ab['my_voucher'] = my_voucher_dict
                            ab.close()
                            break
                    return render_template('AccountManagement/happy_birthday.html', name=name, loggedin=True)
        return render_template('home.html', loggedin=True)
    else:
        return redirect(url_for('customer_signin_signup'))


@app.route('/customer_forgot_password', methods=['GET', 'POST'])
def customer_forgot_password():
    if request.method == "POST":
        password = request.form['new_password']
        date_of_birth = request.form['date_of_birth']
        confirm_new_password = request.form['confirm_new_password']
        customer_email = request.form['email']
        name = request.form['name']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        customer_dict = {}
        db = shelve.open('Account_Management_System.db', 'w')
        customer_dict = db['Customer']
        for customer_id in customer_dict:
            customer = customer_dict[customer_id].get_email()
            if customer_email == customer:
                if check_password(confirm_new_password):
                    get_date_of_birth = customer_dict[customer_id].get_date_of_birth()
                    if date_of_birth == get_date_of_birth:
                        get_name = customer_dict[customer_id].get_name()
                        if name == get_name:
                            get_gender = customer_dict[customer_id].get_gender()
                            if gender == get_gender:
                                get_phone_number = customer_dict[customer_id].get_phone_number()
                                if phone_number == get_phone_number:
                                    profile_picture = customer_dict[customer_id].get_profile_picture()
                                    password = generate_password_hash(confirm_new_password, method='sha256')
                                    customer_info = Customer.Customer(customer_email, password, name, gender, date_of_birth, phone_number, customer_id, profile_picture)
                                    customer_dict[customer_info.get_customer_id()] = customer_info
                                    db['Customer'] = customer_dict
                                    flash('Password was change successful')
                                    return render_template('AccountManagement/customer_signin_signup.html')
                                else:
                                    break
                            else:
                                break
                        else:
                            break
                    else:
                        break
            else:
                continue
        db.close()
        flash('Password was not change. Please ensure that all the information is correct. The password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters')
        return render_template("AccountManagement/customer_forgot_password.html")
    return render_template("AccountManagement/customer_forgot_password.html")


@app.route('/customer_profile', methods=['GET', 'POST'])
def customer_profile():
    if 'customer_id' in session:
        customer_dict = {}
        db = shelve.open('Account_Management_System.db', 'r')
        customer_dict = db['Customer']
        db.close()

        customer_list = []
        for key in customer_dict:
            if key == session['customer_id']:
                customer = customer_dict.get(key)
                customer_list.append(customer)
        for customer in customer_list:
            profile = customer.get_profile_picture()
        return render_template('AccountManagement/customer_profile.html', customer_list=customer_list, profile=profile, loggedin=True)
    else:
        return render_template('AccountManagement/customer_signin_signup.html')


@app.route('/upload_image', methods=['POST','GET'])
def upload_image():
    if 'customer_id' in session:
        if request.method == "POST":
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_name = str(uuid.uuid1()) + "_" + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                customer_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                customer_dict = db['Customer']
                for customer_id in customer_dict:
                    if customer_id == session['customer_id']:
                        email = customer_dict[customer_id].get_email()
                        name = customer_dict[customer_id].get_name()
                        gender = customer_dict[customer_id].get_gender()
                        date_of_birth = customer_dict[customer_id].get_date_of_birth()
                        phone_number = customer_dict[customer_id].get_phone_number()
                        password = customer_dict[customer_id].get_password_type()
                        customer_info = Customer.Customer(email, password, name, gender, date_of_birth, phone_number, customer_id, file_name)
                        customer_dict[customer_info.get_customer_id()] = customer_info
                        db['Customer'] = customer_dict
                        db.close()
                        return redirect(url_for('customer_profile'))
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)
        return render_template('AccountManagement/upload_image.html', loggedin=True)
    else:
        return redirect(url_for('customer_signin_signup'))


@app.route('/display_image/<profile>')
def display_image(profile):
    return redirect(url_for('static', filename='uploads/' + profile), code=301)


@app.route('/staff_upload_image', methods=['POST','GET'])
def staff_upload_image():
    if 'staff_id' in session:
        if request.method == "POST":
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_name = str(uuid.uuid1()) + "_" + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                staff_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                staff_dict = db['Staff']
                for staff_id in staff_dict:
                    if staff_id == session['staff_id']:
                        email = staff_dict[staff_id].get_email()
                        password_type = staff_dict[staff_id].get_password_type()
                        date_added = staff_dict[staff_id].get_date_added()
                        staff_profile_image = staff_dict[staff_id].get_staff_profile_image()
                        staff_info = Staff.Staff(email, password_type, date_added, staff_id, file_name)
                        staff_dict[staff_info.get_staff_id()] = staff_info
                        db['Staff'] = staff_dict
                        db.close()
                        return redirect(url_for('staff_profile'))
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)
        return render_template('AccountManagement/staff_upload_image.html', loggedin=True)
    else:
        return redirect(url_for('staff_signin'))


@app.route('/staff_display_image/<profile>')
def staff_display_image(profile):
    return redirect(url_for('static', filename='uploads/' + profile), code=301)


@app.route('/customer_change_password', methods=['GET', 'POST'])
def customer_change_password():
    if 'customer_id' in session:
        if request.method == "POST":
            new_password = request.form['new_password']
            confirm_new_password = request.form['confirm_new_password']
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            customer_dict = db['Customer']
            for customer_id in customer_dict:
                get_customer_id = session['customer_id']
                if customer_id == get_customer_id:
                    if new_password == confirm_new_password:
                        if check_password(confirm_new_password):
                            customer_email = customer_dict[customer_id].get_email()
                            name = customer_dict[customer_id].get_name()
                            gender = customer_dict[customer_id].get_gender()
                            date_of_birth = customer_dict[customer_id].get_date_of_birth()
                            phone_number = customer_dict[customer_id].get_phone_number()
                            profile_picture = customer_dict[customer_id].get_profile_picture()
                            password = generate_password_hash(confirm_new_password, method='sha256')
                            customer_info = Customer.Customer(customer_email, password, name, gender, date_of_birth, phone_number, customer_id, profile_picture)
                            customer_dict[customer_info.get_customer_id()] = customer_info
                            db['Customer'] = customer_dict
                            flash('Password change successful')
                            return render_template("AccountManagement/customer_change_password.html", loggedin=True)
                        else:
                            break
                    else:
                        break
                else:
                    continue
            flash('Password was not change. Please ensure that there is at least one number and one uppercase and lowercase letter, and at least 8 or more characters')
            return render_template("AccountManagement/customer_change_password.html", loggedin=True)
            db.close()
        return render_template("AccountManagement/customer_change_password.html", loggedin=True)
    else:
        return render_template('AccountManagement/customer_signin_signup.html')


@app.route('/edit_customer_information', methods=['GET', 'POST'])
def edit_customer_information():
    if 'customer_id' in session:
        if request.method == 'POST':
            email = request.form['email']
            name = request.form['name']
            gender = request.form['gender']
            date_of_birth = request.form['date_of_birth']
            phone_number = request.form['phone_number']
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'w')
            try:
                customer_dict = db['Customer']
            except:
                print("Error in creating staff from Account Management System.db.")
            if email == '':
                get_email = customer_dict[customer_id].get_email()
            else:
                get_email = email
            if name == '':
                get_name = customer_dict[customer_id].get_name()
            else:
                get_name = name
            if gender == '':
                get_gender = customer_dict[customer_id].get_gender()
            else:
                get_gender = gender
            if date_of_birth == '':
                get_date_of_birth = customer_dict[customer_id].get_date_of_birth()
            else:
                get_date_of_birth = date_of_birth
            if phone_number == '':
                get_phone_number = customer_dict[customer_id].get_phone_number()
            else:
                get_phone_number = phone_number
            for find_customer_id in customer_dict:
                get_customer_id = session['customer_id']
                if find_customer_id == get_customer_id:
                    password = customer_dict[find_customer_id].get_password_type()
                    profile_picture = customer_dict[find_customer_id].get_profile_picture()
                    customer_info = Customer.Customer(get_email, password, get_name, get_gender, get_date_of_birth, get_phone_number, find_customer_id, profile_picture)
                    customer_dict[customer_info.get_customer_id()] = customer_info
                    db['Customer'] = customer_dict
                    db.close()
                    flash('Update Successfully')
            return redirect(url_for('customer_profile'))
        else:
            customer_dict = {}
            db = shelve.open('Account_Management_System.db', 'r')
            customer_dict = db['Customer']
            db.close()

            customer_list = []

            for key in customer_dict:
                if key == session['customer_id']:
                    customer = customer_dict.get(key)
                    customer_list.append(customer)
            return render_template('AccountManagement/edit_customer_information.html', customer_list=customer_list, loggedin=True)
    else:
        return render_template('AccountManagement/customer_signin_signup.html')


@app.route('/contactUs')
def contact_Us():
    if 'customer_id' in session:
        return render_template('contactUs.html', loggedin=True)
    else:
        return render_template('contactUs.html')


@app.route('/about')
def about():
    if 'customer_id' in session:
        return render_template('about.html', loggedin=True)
    else:
        return render_template('about.html')


@app.route('/terms_and_condition')
def terms_and_condition():
    if 'customer_id' in session:
        return render_template('terms_and_condition.html', loggedin=True)
    else:
        return render_template('terms_and_condition.html')


@app.route('/privacy_policy')
def privacy_policy():
    if 'customer_id' in session:
        return render_template('privacy_policy.html', loggedin=True)
    else:
        return render_template('privacy_policy.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


'''
START OF MENU/CART
'''
GabMenuCart.init_Gab_MenuCart(app)
'''
END OF MENU/CART
'''

'''
START OF QUEUE
'''
ReneQueue.init_rene_queue(app)
'''
END OF QUEUE
'''

'''
START OF PAYMENT
'''
PaymentEason.init_payment_Eason(app)
'''
END OF PAYMENT

START OF Voucher
'''
WenkaiVoucher.init_Wenkai_Voucher(app)
'''
END OF Voucher
'''


#START OF CONFIRMATION PAGE
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'customer_id' in session:
        if request.method == 'GET':
            bag = CRUD.get_cart(session['customer_id'])
            total = 0
            for item in bag:
                total += item['item_quantity'] * item['item_price']

            try:
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'r')
                CreditCard_dict = db['CreditCard']
                db.close()

                customer = ''
                customer_info = []
                for key in CreditCard_dict:
                    if key == session['customer_id']:
                        customer = CreditCard_dict.get(key)
                        customer_info.append(customer)
                if customer != '':
                    for customer in customer_info:
                        name = customer.get_name()
                        email = customer.get_email()
                        last_four_digit = customer.get_last_four_digit()
                        card_number = '************'+last_four_digit
                        expired_date = customer.get_expired_date()
                        cvv = '***'
                        return render_template('Payment/checkoutform.html', bag=bag, total=total, name=name, email=email, card_number=card_number, expired_date=expired_date, cvv=cvv, loggedin=True)
            except:
                customer_dict = {}
                db = shelve.open('Account_Management_System.db', 'r')
                customer_dict = db['Customer']
                db.close()
                no_customer_info = []
                for key in customer_dict:
                    if key == session['customer_id']:
                        customer = customer_dict.get(key)
                        no_customer_info.append(customer)
                for customer in no_customer_info:
                    name = customer.get_name()
                    print(name)
                    email = customer.get_email()
                
                

                return render_template('Payment/checkoutform.html', name=name, email=email, loggedin=True)
            return render_template('Payment/checkoutform.html', loggedin=True)
        if request.method == 'POST':
            bag = CRUD.get_cart(session['customer_id'])
            total = 0
            for item in bag:
                total += item['item_quantity'] * item['item_price']
            if bag:
                email = request.form['email']
                name = request.form['name']
                cardnumber = request.form['cardnumber']
                cvv = request.form['cvv']
                expiry_date = request.form['expdate']
                CRUD.delete_cart(session['customer_id'])
                return render_template('confirmation_page.html', total=total, bag=bag, email=email, name=name, cardnumber=cardnumber, cvv=cvv, expiry_date=expiry_date, loggedin=True)
            else:
                print('testing')
                return redirect(url_for('retrieve_cart'))
    else:
        return render_template('noSessCheckout.html')

'''
SQLITE3 DATABASE
'''
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'Arrata.sqlite'),
    SHELVE_DATABASE=os.path.join(app.instance_path, 'MenuAndCart.db'),
)

database.init_app(app)
'''
END SQLITE3 DATABASE
'''

if __name__ == "__main__":
    app.run(debug=True)
