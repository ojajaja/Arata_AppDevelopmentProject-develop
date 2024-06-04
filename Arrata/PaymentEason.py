import shelve

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash
from . import Creditcard


def init_payment_Eason(app: Flask):
    @app.route('/addCreditcard', methods=['GET', 'POST'])
    def add_credit_card():
        if 'customer_id' in session:
            if request.method == "POST":
                credit_card_number = request.form['Credit Card']
                date = request.form['date']
                cvv = request.form['cvv']
                CreditCard_dict = {}
                customer_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                customer_dict = db['Customer']
                try:
                    if 'CreditCard' in db:
                        CreditCard_dict = db['CreditCard']
                    else:
                        db['CreditCard'] = CreditCard_dict
                except IOError:
                    print("Error in opening Account Management System.db")
                for customer_id in customer_dict:
                    if customer_id == session['customer_id']:
                        email = customer_dict[customer_id].get_email()
                        password_type = customer_dict[customer_id].get_password_type()
                        name = customer_dict[customer_id].get_name()
                        gender = customer_dict[customer_id].get_gender()
                        date_of_birth = customer_dict[customer_id].get_date_of_birth()
                        phone_number = customer_dict[customer_id].get_phone_number()
                        profile_picture = customer_dict[customer_id].get_profile_picture()
                        last_four_digit = credit_card_number[12:]
                        front_digit = credit_card_number[:-4]
                        front_digit_hash = generate_password_hash(front_digit, method='sha256')
                        aratapay_balance = 0
                        cvv_hash = generate_password_hash(cvv, method='sha256')
                        credit_card_info = Creditcard.Creditcard(aratapay_balance, last_four_digit, front_digit_hash, date,
                                                                 cvv_hash, email, password_type, name, gender, date_of_birth,
                                                                 phone_number, customer_id, profile_picture)
                        CreditCard_dict[credit_card_info.get_customer_id()] = credit_card_info
                        db['CreditCard'] = CreditCard_dict
                        db.close()
                        return redirect(url_for('aratapay'))
                return redirect(url_for('aratapay'))

            if request.method == "GET":
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'r')
                try:
                    CreditCard_dict = db['CreditCard']
                except:
                    print("Error in retrieving Customers from Account Management System.db.")
                for customer_id in CreditCard_dict:
                    if customer_id == session['customer_id']:
                        try:
                            find_last_four_digit = CreditCard_dict[customer_id].get_last_four_digit()
                            return redirect(url_for('aratapay'))
                        except:
                            return render_template('Payment/addCreditcard.html', loggedin=True)
                return render_template('Payment/addCreditcard.html', loggedin=True)
                db.close()
        else:
            return render_template('AccountManagement/customer_signin_signup.html')

    @app.route('/topup', methods=['GET', 'POST'])
    def topup():
        if 'customer_id' in session:
            if request.method == "POST":
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'r')
                try:
                    CreditCard_dict = db['CreditCard']
                except:
                    print("Error in retrieving Customers from Account Management System.db.")
                customer_list = []
                for key in CreditCard_dict:
                    if key == session['customer_id']:
                        customer = CreditCard_dict.get(key)
                        customer_list.append(customer)
                    else:
                        continue
                for customer_id in CreditCard_dict:
                    if customer_id == session['customer_id']:
                        try:
                            find_last_four_digit = CreditCard_dict[customer_id].get_last_four_digit()
                            balance = CreditCard_dict[customer_id].get_aratapay_balance()
                            return render_template('Payment/topup.html', find_last_four_digit=find_last_four_digit,
                                                   balance=balance, loggedin=True)


                        except:
                            return render_template('Payment/addCreditcard.html', loggedin=True)
                return render_template('Payment/topup.html')
                db.close()
        else:
            return render_template('AccountManagement/customer_signin_signup.html')


    @app.route('/aratapay', methods=['GET', 'POST'])
    def aratapay():
        if 'customer_id' in session:
            if request.method == 'GET':
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                try:
                    if 'CreditCard' in db:
                        CreditCard_dict = db['CreditCard']
                    else:
                        db['CreditCard'] = CreditCard_dict
                except IOError:
                    print("Error in opening Account Management System.db")
                customer_list = []
                for key in CreditCard_dict:
                    if key == session['customer_id']:
                        customer = CreditCard_dict.get(key)
                        customer_list.append(customer)
                    else:
                        continue
                try:
                    for customer in customer_list:
                        last_four_digit = customer.get_last_four_digit()
                        balance = customer.get_aratapay_balance()
                        if last_four_digit != "":
                            return render_template('Payment/aratapay.html', last_four_digit=last_four_digit,
                                                   balance=balance, loggedin=True)
                except:
                    return render_template('Payment/aratapay_homepage.html', loggedin=True)
                    # print(customer_list())
                    db.close()
                return render_template('Payment/aratapay_homepage.html', loggedin=True)

            if request.method == 'POST':
                amount = request.form['amount']
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                try:
                    CreditCard_dict = db['CreditCard']
                except:
                    print("Error in retrieving Customers from Account Management System.db.")
                for customer_id in CreditCard_dict:
                    if customer_id == session['customer_id']:
                        aratapay_balance = CreditCard_dict[customer_id].get_aratapay_balance()
                        email = CreditCard_dict[customer_id].get_email()
                        password_type = CreditCard_dict[customer_id].get_password_type()
                        name = CreditCard_dict[customer_id].get_email()
                        gender = CreditCard_dict[customer_id].get_gender()
                        date_of_birth = CreditCard_dict[customer_id].get_date_of_birth()
                        phone_number = CreditCard_dict[customer_id].get_phone_number()
                        profile_picture = CreditCard_dict[customer_id].get_profile_picture()
                        last_four_digit = CreditCard_dict[customer_id].get_last_four_digit()
                        front_digit = CreditCard_dict[customer_id].get_front_digit_hash()
                        date = CreditCard_dict[customer_id].get_expired_date()
                        cvv = CreditCard_dict[customer_id].get_cvv()
                        total_aratapay_balance = int(aratapay_balance) + int(amount)
                        credit_card_info = Creditcard.Creditcard(total_aratapay_balance, last_four_digit, front_digit, date,
                                                                 cvv, email, password_type, name, gender, date_of_birth,
                                                                 phone_number, customer_id, profile_picture)
                        CreditCard_dict[credit_card_info.get_customer_id()] = credit_card_info
                        db['CreditCard'] = CreditCard_dict
                        db.close()
                        return redirect(url_for('aratapay'))
        else:
            return render_template('AccountManagemnt/customer_signin_signup.html')

    @app.route('/removecreditcard', methods=['GET', 'POST'])
    def removecreditcard():
        if 'customer_id' in session:
            if request.method == 'POST':
                CreditCard_dict = {}
                db = shelve.open('Account_Management_System.db', 'w')
                try:
                    CreditCard_dict = db['CreditCard']
                except:
                    print("Error in retrieving Customers from Account Management System.db.")
                for customer in CreditCard_dict:
                    if customer == session['customer_id']:
                        CreditCard_dict.pop(customer)
                        db['CreditCard'] = CreditCard_dict
                        db.close()
                        return redirect(url_for('aratapay'))
                    else:
                        break
        else:
            return render_template('AccountManagemnt/customer_signin_signup.html')


    @app.route('/sales')
    def sales():
        if 'staff_id' in session:
            sales_dict = {}
            db = shelve.open('sales.db', 'c')
            try:
                sales_dict = db['Sales']

            except:
                print("Error")
            db.close()

            sales_list = []
            for key in sales_dict:
                sales = sales_dict.get(key)
                sales_list.append(sales) 
            return render_template('Payment/sales.html', count=len(sales_list), sales_list=sales_list)
        else:
            return redirect(url_for('staff_signin'))


