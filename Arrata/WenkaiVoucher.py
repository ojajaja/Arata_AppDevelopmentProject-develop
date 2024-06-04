from flask import Flask, session, redirect, url_for, render_template, request
import shelve
import datetime
import random
from . import Summon
from .Forms import CreateVoucherForm


# def create_voucher_database():


def init_Wenkai_Voucher(app: Flask):
    @app.route('/my_voucher')
    def my_voucher():
        if 'customer_id' in session:
            my_voucher_dict = {}
            with shelve.open('my_voucher.db', 'c') as db:
                try:
                    my_voucher_dict = db['my_voucher']
                except:
                    print("Error")

            voucher_dict = {}
            with shelve.open('voucher.db', 'c') as ab:
                try:
                   voucher_dict = ab['Vouchers']
                except:
                    print("Error")

            voucher_list = 0
            tday = datetime.date.today()
            print(my_voucher_dict)
            for voucher in my_voucher_dict:
                print(session['customer_id'])

                key_list = list(my_voucher_dict.keys())
                print(key_list)


                if session['customer_id'] in key_list:
                    print('customer_id in session')
                    voucher = my_voucher_dict.get(session['customer_id'])
                    voucher_list = voucher
                    # print(voucher_list)
                    expired_voucher = []
                    valid_voucher = []
                    detailed_list = []
                    read = []

                    for item in voucher_list:
                        temp = []
                        temp.append(item.get_my_voucher())
                        temp.append(item.get_expiring_date())
                        read.append(temp)

                    for key in voucher_dict:
                        detailed_voucher = voucher_dict.get(key)
                        detailed_list.append(detailed_voucher)

                    x = 0
                    while x < len(read):
                        # print(read[x])
                        y = 0
                        if y < len(detailed_list):
                            for thing in detailed_list:
                                # print(thing.get_voucher(), "", thing.get_Detail())
                                if thing.get_voucher() == read[x][0]:
                                    read[x].append(thing.get_Detail())
                            y += 1
                        else:
                            pass

                        x += 1

                    print(read)

                    for voucher in read:
                        if voucher[1] <= tday:
                            expired_voucher.append(voucher)
                        else:
                            valid_voucher.append(voucher)

                    print(f'\n\n{expired_voucher}\n{valid_voucher}\n\n')

                    for voucher in valid_voucher:
                        print(voucher[0])
                        print(voucher[1])

                    return render_template('my_voucher.html', valid_voucher=valid_voucher,
                                           expired_voucher=expired_voucher, num_of_valid=len(valid_voucher),
                                           num_of_expired=len(expired_voucher), loggedin=True)
                else:
                    print('customer id not in session')
                    return redirect(url_for('menu'))
        else:
            print('returning here?')
            return redirect(url_for('customer_id'))

    @app.route('/summon')
    def summon():
        if 'customer_id' in session:

            return render_template('summon.html', loggedin=True)
        else:
            return redirect(url_for('customer_id'))

    @app.route('/singlesummon')
    def single_summon():
        if 'customer_id' in session:
            x = random.randint(0, 1)
            ab = open('Points.txt', 'r')

            for xy in ab:
                point = xy.split(',')
                point[-1] = point[-1].replace('\n', '')
            ab.close()

            my_voucher_dict = {}
            my_voucher_list = []
            new_voucher_list = []
            db = shelve.open('my_voucher.db', 'c')
            try:
                my_voucher_dict = db['my_voucher']
            except:
                print("Error")

            for voucher in my_voucher_dict:
                print(session['customer_id'])

                key_list = list(my_voucher_dict.keys())
                print(key_list)

                customer_dict = {}
                cb = shelve.open('Account_Management_System.db', 'w')
                customer_dict = cb['Customer']

                customer_list = []
                for key in customer_dict:
                    if session['customer_id'] in key_list:
                        customer = customer_dict.get(session['customer_id'])
                        customer_list.append(customer)

                customer = customer_list[0]
                id = customer.get_customer_id()
                email = customer.get_email()
                password = customer.get_password_type()
                name = customer.get_name()
                gender = customer.get_gender()
                birthday = customer.get_date_of_birth()
                phone = customer.get_phone_number()
                original_point = customer.get_point()
                profile_picture = customer.get_profile_picture()

                if original_point >= 100:
                    original_point -= 100
                    if x == 0:
                        y = len(point) - 1
                        z = random.randint(0, y)

                        result_list = []
                        result_list.append(point[z] + ' points')

                        point_received = point[z]

                        final_point = int(original_point) + int(point_received)
                        customer_info = Summon.Point(email, password, name, gender, birthday, phone, id, profile_picture, final_point)
                        customer_dict[id] = customer_info
                        cb['Customer'] = customer_dict
                        cb.close()
                        return render_template('result-single.html', result_list=result_list)
                    elif x == 1:
                        voucher_dict = {}
                        bb = shelve.open('voucher.db', 'r')
                        voucher_dict = bb['Vouchers']
                        bb.close()

                        voucher_list = []
                        readable_list = []
                        for key in voucher_dict:
                            voucher = voucher_dict.get(key)
                            voucher_list.append(voucher)

                        for The_voucher in voucher_list:
                            if The_voucher.get_voucher() != 'Birthday Voucher':
                                continue
                            else:
                                readable_list.append(The_voucher.get_voucher())

                        y = len(readable_list) - 1
                        z = random.randint(0, y)

                        result_list = []
                        result_list.append(readable_list[z])
                        voucher_received = readable_list[z]

                        tday = datetime.date.today()
                        tdelta = datetime.timedelta(days=31)

                        expiring_date = tday + tdelta

                        if session['customer_id'] in key_list:
                            voucher = my_voucher_dict.get(session['customer_id'])
                            if isinstance(voucher, list):
                                new_voucher = Summon.my_voucher(voucher_received, expiring_date)
                                new_voucher_list.append(new_voucher)
                                final_list = voucher + new_voucher_list

                            else:
                                my_voucher_list.append(voucher)

                                new_voucher = Summon.my_voucher(voucher_received, expiring_date)
                                new_voucher_list.append(new_voucher)
                                final_list = my_voucher_list + new_voucher_list
                                if final_list[0] == '':
                                    final_list.pop(0)
                                else:
                                    pass
                            my_voucher_dict[id] = final_list
                            db['my_voucher'] = my_voucher_dict
                            db.close()

                        return render_template('result-single.html', result_list=result_list)
                    # return render_template('summon.html', loggedin=True)
                else:

                    return render_template('summon.html', loggedin=True)

        else:
            return redirect(url_for('customer_id'))

    @app.route('/MultiSummon')
    def multi_summon():
        if 'customer_id' in session:
            ab = open('Points.txt', 'r')

            for xy in ab:
                point = xy.split(',')
                point[-1] = point[-1].replace('\n', '')
            ab.close()

            my_voucher_dict = {}
            my_voucher_list = []
            new_voucher_list = []
            db = shelve.open('my_voucher.db', 'c')
            try:
                my_voucher_dict = db['my_voucher']
            except:
                print("Error")

            voucher_dict = {}
            bb = shelve.open('voucher.db', 'r')
            voucher_dict = bb['Vouchers']

            voucher_list = []
            readable_list = []
            for key in voucher_dict:
                voucher = voucher_dict.get(key)
                voucher_list.append(voucher)

            for The_voucher in voucher_list:
                if The_voucher.get_voucher() != 'Birthday Voucher':
                    continue
                else:
                    readable_list.append(The_voucher.get_voucher())

            for voucher in my_voucher_dict:
                print(session['customer_id'])

                key_list = list(my_voucher_dict.keys())
                print(key_list)

                customer_dict = {}
                cb = shelve.open('Account_Management_System.db', 'w')
                customer_dict = cb['Customer']

                customer_list = []
                for key in customer_dict:
                    if session['customer_id'] in key_list:
                        customer = customer_dict.get(session['customer_id'])
                        customer_list.append(customer)
                        voucher = my_voucher_dict.get(session['customer_id'])

                customer = customer_list[0]
                id = customer.get_customer_id()
                email = customer.get_email()
                password = customer.get_password_type()
                name = customer.get_name()
                gender = customer.get_gender()
                birthday = customer.get_date_of_birth()
                phone = customer.get_phone_number()
                original_point = customer.get_point()
                profile_picture = customer.get_profile_picture()

                final_list = point + readable_list

                if original_point >= 1000:
                    original_point -= 1000
                    x = random.randint(1, 2)
                    if x > 0:
                        z = 1
                        total_points = 0
                        result_list = []
                        while z <= 10:
                            z += 1
                            t = random.randint(0, len(final_list) - 1)
                            result_list.append(final_list[t])
                            if final_list[t].isnumeric():
                                total_points = int(final_list[t]) + total_points

                            else:
                                continue
                        to_do_list = []
                        for t in result_list:
                            if t[-1].isalpha() == True:
                                to_do_list.append(t)
                            else:
                                pass

                        final_point = int(original_point) + int(total_points)
                        customer_info = Summon.Point(email, password, name, gender, birthday, phone, id, profile_picture, final_point)
                        customer_dict[id] = customer_info
                        cb['Customer'] = customer_dict

                        tday = datetime.date.today()
                        tdelta = datetime.timedelta(days=31)

                        expiring_date = tday + tdelta

                        if isinstance(voucher, list):
                            for a in to_do_list:
                                new_voucher = Summon.my_voucher(a, expiring_date)
                                new_voucher_list.append(new_voucher)
                            final_list = voucher + new_voucher_list

                        else:
                            my_voucher_list.append(voucher)

                            for a in to_do_list:
                                new_voucher = Summon.my_voucher(a, expiring_date)
                                new_voucher_list.append(new_voucher)
                            final_list = my_voucher_list + new_voucher_list
                            if final_list[0] == '':
                                final_list.pop(0)
                            else:
                                pass

                        my_voucher_dict[id] = final_list
                        db['my_voucher'] = my_voucher_dict
                        ab.close()
                        bb.close()
                        cb.close()
                        db.close()
                        return render_template('result-multi.html', total_points=total_points, result_list=result_list)
                else:
                    return render_template('summon.html', loggedin=True)
        else:
            return redirect(url_for('customer_id'))

    @app.route('/exchange_shop')
    def exchange_shop():
        if 'customer_id' in session:
            voucher_dict = {}
            db = shelve.open('voucher.db', 'r')
            voucher_dict = db['Vouchers']
            db.close()

            voucher_list = []
            for key in voucher_dict:
                voucher = voucher_dict.get(key)
                voucher_list.append(voucher)
            for test in voucher_list:
                print(test.get_voucher())
                if test.get_voucher() == 'Birthday Voucher':
                    voucher_list.remove(test)

            for test_two in voucher_list:
                print(test_two.get_voucher())

            

            

            customer_dict = {}
            ab = shelve.open('Account_Management_System.db', 'c')
            try:
                customer_dict = ab['Customer']
            except:
                print("Error in retrieving Customers from Account Management System.db.")
            ab.close()
            customer_list = []
            for key in customer_dict:
                if key == session['customer_id']:
                    customer = customer_dict.get(key)
                    customer_list.append(customer)
            customer = customer_list[0]

            point = customer.get_point()
            print(point)

            return render_template('exchange_shop.html', loggedin=True, voucher_list=voucher_list, point=point)
        else:
            return redirect(url_for('customer_id'))

    @app.route('/voucher_management')
    def voucher_management():
        if 'staff_id' in session:
            voucher_dict = {}
            db = shelve.open('voucher.db', 'c')
            try:
                voucher_dict = db['Vouchers']
            except:
                print("Error")
            db.close()

            voucher_list = []
            for key in voucher_dict:
                voucher = voucher_dict.get(key)
                voucher_list.append(voucher)

            return render_template('voucher_management.html', count=len(voucher_list), voucher_list=voucher_list)
        else:
            return redirect(url_for('staff_signin'))

    @app.route('/createvoucher', methods=['GET', 'POST'])
    def create_voucher():
        create_voucher_form = CreateVoucherForm(request.form)
        if request.method == 'POST' and create_voucher_form.validate():
            voucher_dict = {}
            test_dict = {}
            db = shelve.open('voucher.db', 'c')
            ab = shelve.open('allvoucher.db', 'c')

            try:
                test_dict = ab['Vouchers']
            except:
                print("Error in retrieving Users from allvoucher.db.")

            try:
                voucher_dict = db['Vouchers']
            except:
                print("Error in retrieving Users from voucher.db.")

            print(len(test_dict))

            voucher = Summon.Voucher(create_voucher_form.voucher.data, create_voucher_form.detail.data,
                                     create_voucher_form.value.data, create_voucher_form.Price.data,
                                     int(len(test_dict)))

            count = Summon.Count_all(int(len(test_dict)))

            test_dict[voucher.get_ID()] = count
            ab['Vouchers'] = test_dict
            ab.close()

            voucher_dict[voucher.get_ID()] = voucher
            db['Vouchers'] = voucher_dict
            db.close()

            return redirect(url_for('voucher_management'))
        return render_template('createvoucher.html', form=create_voucher_form)

    @app.route('/deletevoucher/<int:id>', methods=['POST'])
    def delete_Voucher(id):
        voucher_dict = {}
        db = shelve.open("voucher.db", 'w')
        voucher_dict = db['Vouchers']

        voucher_dict.pop(id)

        db["Vouchers"] = voucher_dict
        db.close()

        return redirect(url_for('voucher_management'))

    @app.route('/updatevoucher/<int:id>/', methods=['GET', 'POST'])
    def update_Voucher(id):
        update_voucher_form = CreateVoucherForm(request.form)
        if request.method == 'POST' and update_voucher_form.validate():
            voucher_dict = {}
            db = shelve.open('voucher.db', 'w')
            voucher_dict = db['Vouchers']

            voucher = voucher_dict.get(id)
            voucher.set_voucher(update_voucher_form.voucher.data)
            voucher.set_Detail(update_voucher_form.detail.data)
            voucher.set_Value(update_voucher_form.value.data)
            voucher.set_price_in_points(update_voucher_form.Price.data)

            db['Vouchers'] = voucher_dict
            db.close()

            return redirect(url_for('voucher_management'))
        else:
            voucher_dict = {}
            db = shelve.open('voucher.db', 'r')
            voucher_dict = db['Vouchers']
            db.close()

            voucher = voucher_dict.get(id)
            update_voucher_form.voucher.data = voucher.get_voucher()
            update_voucher_form.detail.data = voucher.get_Detail()
            update_voucher_form.value.data = voucher.get_Value()
            update_voucher_form.Price.data = voucher.get_price_in_points()

            return render_template('updatevoucher.html', form=update_voucher_form)

    @app.route('/purchasevoucher/<int:id>/')
    def Purchase_voucher(id):
        if 'customer_id' in session:
            voucher_dict = {}
            db = shelve.open('voucher.db', 'r')
            voucher_dict = db['Vouchers']
            db.close()

            voucher_list = []
            for key in voucher_dict:
                if key == id:
                    the_voucher = voucher_dict.get(key)
                    voucher_list.append(the_voucher)

            Voucher = voucher_list[0]
            ID = Voucher.get_ID()
            name = Voucher.get_voucher()
            print('check here')
            print(ID)
            print(name)
            return redirect(url_for('my_voucher'))

    