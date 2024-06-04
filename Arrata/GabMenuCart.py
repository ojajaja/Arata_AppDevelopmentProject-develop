from flask import Flask, session, redirect, url_for, render_template, g
import functools
import shelve
import json
from . import database
from . import CRUD

def with_customer_id(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        customer_id = session['customer_id'] if 'customer_id' in session else -1
        return view(customer_id, **kwargs)
    return wrapped_view


def init_Gab_MenuCart(app: Flask):
    @with_customer_id
    @app.route('/<string:type>')
    def menu(type: str):
        """
        Args:
            type: don, drinks or sashimi
        Returns: menu.html
        """
        items = CRUD.get_menu(type)

        if type in ['don', 'sashimi', 'drinks']:
            title = f'{type.capitalize()}'
        else:
            title = ''

        loggedin = 'customer_id' in session
        
        return render_template(f'menu.html', items=items, title=title, loggedin=loggedin)


    def get_overview(cart: list, customer_id) -> dict:
        subtotal = 0
        
        for b in cart:
            subtotal += b['item_price'] * b['item_quantity']

        if customer_id > 0:
            subtotal = round(subtotal, 2)
            gst = round(0.07 * subtotal, 2)
            service_charge = round(0.10 * subtotal, 2)
            discount = 0
            total = round(subtotal + gst + service_charge, 2)
            if 'active_voucher' in session:
                discount = round(((1 - session['active_voucher']) * subtotal), 2)
                total = total - discount


            # print(f'subtotal = {subtotal}\n gst = {gst}\n service_charge = {service_charge}\n total = {total}')

            overview = {
                'subtotal': subtotal,
                'gst': gst,
                'service_charge': service_charge,
                'discount': discount,
                'total': round(total, 2)
            }

            return overview

        else:
            subtotal = round(subtotal, 2)
            gst = round(0.07 * subtotal, 2)
            service_charge = round(0.10 * subtotal, 2)
            
            total = round(subtotal + gst + service_charge, 2)
            


            # print(f'subtotal = {subtotal}\n gst = {gst}\n service_charge = {service_charge}\n total = {total}')

            overview = {
                'subtotal': subtotal,
                'gst': gst,
                'service_charge': service_charge,
                
                'total': round(total, 2)
            }

            return overview



    @app.route('/cart/update', methods=['GET'])
    @with_customer_id
    def get_updated_cart(customer_id):
        bag = CRUD.get_cart(customer_id)
        overview = get_overview(bag, customer_id)
        return overview

    @app.route('/add_voucher/<float(signed=True):discount>', methods=['POST'])
    def add_voucher(discount):
        print(f'discount is {discount}')
        session['active_voucher'] = discount
        return 'nothing'

    @app.route('/cart')
    @with_customer_id
    def retrieve_cart(customer_id):
        """ Note: In the future add customer id as arg """
        bag = CRUD.get_cart(customer_id)
        overview = get_overview(bag, customer_id)

        voucher_dict = {}
        ab = shelve.open('voucher.db', 'r')
        voucher_dict = ab['Vouchers']
        ab.close()

        voucher_list = []
        for key in voucher_dict:
            voucher = voucher_dict.get(key)
            voucher_list.append(voucher)

        my_voucher_dict={}
        cb = shelve.open('my_voucher.db', 'r')
        my_voucher_dict = cb['my_voucher']
        cb.close()

        print(customer_id)

       

        if customer_id > 0:
            for voucher in my_voucher_dict:
                print(session['customer_id'])

                key_list = list(my_voucher_dict.keys())
                print(key_list)


                if session['customer_id'] in key_list:
                    
                    print('customer_id in session')
                    voucher = my_voucher_dict.get(session['customer_id'])
                    print(voucher)
                    using_list = []
                    for x in voucher:
                        print(x)
                        name = x.get_my_voucher()
                        using_list.append(name)
                    print(voucher_list)
                    father = []
                    y = 0
                    while y < len(voucher_list):
                        detail_list = []
                        name = voucher_list[y].get_voucher()
                        print(name)
                        detail = voucher_list[y].get_Detail()
                        value = voucher_list[y].get_Value()
                        detail_list.append(name)
                        detail_list.append(detail)
                        detail_list.append(value)
                        father.append(detail_list)
                        y += 1
                    print(father)
                    print(using_list)

                    print('')
                    final = []

                    for z in using_list:
                        for a in father:
                            if z == a[0]:
                                temp = []
                                temp.append(z)
                                temp.append(a[1])
                                temp.append(a[2])
                                final.append(temp)
                            else:
                                pass
                    
                    print(final)

            loggedin = 'customer_id' in session
            return render_template('cart.html', cart=bag, overview=overview, loggedin=loggedin, final=final, customer_id=customer_id)

        else: 
            pass   
            return render_template('cart.html', cart=bag, overview=overview, customer_id=customer_id)

    @app.route('/updateQuantity/<int:item_id>/<int:quantity>', methods=['POST'])
    @with_customer_id
    def update_quantity(customer_id, item_id, quantity):
        db = database.get_db()
        find_item = CRUD.find_cart(item_id, customer_id)

        if find_item:
            if quantity > 0:
                CRUD.update_cart(item_id, quantity, customer_id)
            else:
                CRUD.delete_item(item_id, customer_id)
        else:
            print(f'Item with id {item_id} not in the cart')

        new_total = {
            'total': round(find_item['item_price'] * quantity, 2)
        }

        return json.dumps(new_total)

    @app.route('/add/<int:item_id>', methods=['POST'])
    @with_customer_id
    def add_to_cart(customer_id, item_id):
        db = database.get_db()

        item_quantity = 1
        is_item_random = 0

        if item_id == 1:
            is_item_random = 1
            import random
            item_id = random.randint(2, 6)

        find_item = CRUD.find_cart(item_id, customer_id)

        if not find_item:
            CRUD.add_cart(item_id, item_quantity, customer_id)
        else:
            item_quantity = find_item['item_quantity']
            item_quantity += 1
            CRUD.update_cart(item_id, item_quantity, customer_id)

        return (f'{item_quantity}')

    @app.route('/remove/<int:item_id>', methods=['POST'])
    @with_customer_id
    def remove_from_cart(customer_id, item_id):
        db = database.get_db()

        item_quantity = 0
        find_item = CRUD.find_cart(item_id, customer_id)

        if find_item:
            item_quantity = find_item['item_quantity']
            item_quantity -= 1
            if item_quantity > 0:
                CRUD.update_cart(item_id, item_quantity, customer_id)
            else:
                CRUD.delete_item(item_id, customer_id)
        else:
            print(f'Item with id {item_id} not in the cart')

        return (f'{item_quantity}')


