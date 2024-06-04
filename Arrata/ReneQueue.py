from flask import Flask, session, redirect, url_for, render_template
import shelve
from . import GenerateQueueNo

def init_rene_queue(app:Flask):
    @app.route('/generate/')
    def generate_queue():
        if 'customer_id' in session:
            customer_id = session['customer_id']
            print('Customer is logged in')
            return redirect(url_for('generate_queue_acc'))
        else:
            print('Customer is not logged in')
            return redirect(url_for('generate_queue_no_acc'))

    @app.route('/queue')
    def queue_queue():
        if 'customer_id' in session:
            print('Customer is logged in')
            return redirect(url_for('get_queue'))
        elif 'staff_id' in session:
            print('Staff is logged in')
            return redirect(url_for('get_staff_queue'))
        else:
            print('Customer is not logged in')

            try:
                your_dict = {}
                db = shelve.open('queue.db' , 'w')
                your_dict = db['Your']
                your_dict.clear()
                your_list = []
                db['Your'] = your_dict
                db.close()
            except:
                print("Error in retrieving Generate from generate.db.")

            return redirect(url_for('get_queue_no_acc'))

    @app.route('/generateQueueAcc')
    def generate_queue_acc():
        generate_dict = {}
        your_dict = {}
        acc_dict = {}
        db = shelve.open('queue.db' , 'c')
        try:
            generate_dict = db['Generate']
            your_dict = db['Your']
            acc_dict = db['Acc']
            customerpid = session['customer_id']
            print(customerpid)
        except:
            print("Error in retrieving Generate from generate.db.")
        # print(your_dict)
        generate_list = []
        your_list = []
        acc_list = []
        if len(generate_dict) >= 1:
            for key in generate_dict:
                generate_list.append(key)
                max_list = max(generate_list)
                your_list.append(max_list + 1)
                generate = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list + 1 , your_queue_no=max_list + 1 ,
                                                           acc_queue_no=max_list + 1 , update_no=1 , serve_no=1 ,
                                                           plus=1)
                your = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list + 1 , your_queue_no=max_list + 1 ,
                                                       acc_queue_no=max_list + 1 , update_no=1 , serve_no=1 , plus=1)
                acc = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list + 1 , your_queue_no=max_list + 1 ,
                                                      acc_queue_no=max_list + 1 , update_no=1 , serve_no=1 , plus=1)
        else:
            your_list.append(1)
            generate = GenerateQueueNo.GenerateQueueNo(generate_queue_no=1 , your_queue_no=1 , acc_queue_no=1 ,
                                                       update_no=1 , serve_no=1 , plus=1)
            your = GenerateQueueNo.GenerateQueueNo(generate_queue_no=1 , your_queue_no=1 , acc_queue_no=1 ,
                                                   update_no=1 , serve_no=1 , plus=1)
            acc = GenerateQueueNo.GenerateQueueNo(generate_queue_no=1 , your_queue_no=1 , acc_queue_no=1 , update_no=1 ,
                                                  serve_no=1 , plus=1)
            max_list = 1
        acc_dict[acc.get_acc_queue_no()] = acc
        your_dict[your.get_your_queue_no()] = your
        generate_dict[generate.get_generate_queue_no()] = generate

        db['Acc'] = acc_dict
        db['Generate'] = generate_dict
        db['Your'] = your_dict
        db.close()
        # time = Chimo.countdown(t=10,i=True)
        return redirect(url_for('get_queue'))

    @app.route('/generate_queue_no_Acc')
    def generate_queue_no_acc():
        generate_dict = {}
        your_dict = {}
        db = shelve.open('queue.db' , 'c')
        try:
            generate_dict = db['Generate']
            your_dict = db['Your']
            your_dict.clear()
        except:
            print("Error in retrieving Generate from generate.db.")
        # print(your_dict)
        generate_list = []
        your_list = []
        if len(generate_dict) >= 1:
            for key in generate_dict:
                generate_list.append(key)
                max_list = max(generate_list)
                your_list.append(max_list + 1)
                generate = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list + 1 , your_queue_no=max_list + 1 ,
                                                           acc_queue_no=0 , update_no=0 , serve_no=1 , plus=1)
                your = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list + 1 , your_queue_no=max_list + 1 ,
                                                       acc_queue_no=0 , update_no=0 , serve_no=1 , plus=1)
        else:
            your_list.append(1)
            generate = GenerateQueueNo.GenerateQueueNo(generate_queue_no=1 , your_queue_no=1 , acc_queue_no=0 ,
                                                       update_no=0 , serve_no=1 , plus=1)
            your = GenerateQueueNo.GenerateQueueNo(generate_queue_no=1 , your_queue_no=1 , acc_queue_no=0 ,
                                                   update_no=0 , serve_no=1 , plus=1)
            max_list = 1
        # print(max_list)
        your_dict[your.get_your_queue_no()] = your
        generate_dict[generate.get_generate_queue_no()] = generate

        db['Generate'] = generate_dict
        db['Your'] = your_dict
        db.close()
        return redirect(url_for('get_queue_no_acc'))

    @app.route('/queueAcc')
    def get_queue():
        queue_dict = {}
        acc_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            queue_dict = db['Generate']
            acc_dict = db['Acc']
            db.close()
        except:
            print('eror1')
        print(queue_dict)
        print(acc_dict)
        queue_list = []
        acc_list = []
        for key in acc_dict:
            acc = acc_dict.get(key)
            acc_list.append(acc)
        for key in queue_dict:
            queue = queue_dict.get(key)
            queue_list.append(queue)
        l = []
        o = []
        for queue in queue_list:
            a = queue.get_generate_queue_no()
            l.append(a)
            print(l)
        for acc in acc_list:
            b = acc.get_acc_queue_no()
            o.append(b)
            print(o)
        queue_list.clear()
        try:
            i = max(o) - 1
        except ValueError:
            i = 0
            print(i)
        z = 0
        for key in queue_dict:
            z += 1
            queue = queue_dict.get(key)
            queue_list.append(queue)
            if z == i:
                break
            else:
                pass
        print(queue_list)
        serve_list = [0]
        return render_template('Queue/queue.html' , queue_list=queue_list , acc_list=acc_list , serve_list=serve_list ,
                               loggedin=True)

    @app.route('/queueNoAcc')
    def get_queue_no_acc():
        your_dict = {}
        queue_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            queue_dict = db['Generate']
            your_dict = db['Your']
            db.close()
        except:
            print('eror2')
        print(queue_dict)
        print(your_dict)
        your_list = []
        queue_list = []
        for key in your_dict:
            your = your_dict.get(key)
            your_list.append(your)
        for key in queue_dict:
            queue = queue_dict.get(key)
            queue_list.append(queue)
        return render_template('Queue/queueNoAcc.html' , queue_list=queue_list , your_list=your_list)

    @app.route('/get_staff_queue')
    def get_staff_queue():
        your_dict = {}
        queue_dict = {}
        acc_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            queue_dict = db['Generate']
            your_dict = db['Your']
            acc_dict = db['Acc']
            db.close()
        except:
            print('eror1')
        print(queue_dict)
        print(your_dict)
        print(acc_dict)
        your_list = []
        queue_list = []
        acc_list = []
        for key in acc_dict:
            acc = acc_dict.get(key)
            acc_list.append(acc)
        for key in your_dict:
            your = your_dict.get(key)
            your_list.append(your)
        for key in queue_dict:
            queue = queue_dict.get(key)
            queue_list.append(queue)
        return render_template('Queue/queueStaffGreen.html' , queue_list=queue_list , your_list=your_list ,
                               acc_list=acc_list) , {"Refresh": "5; url=/queueStaffOrange"}

    @app.route('/queueStaffOrange')
    def queue_staff_orange():
        your_dict = {}
        queue_dict = {}
        acc_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            queue_dict = db['Generate']
            your_dict = db['Your']
            acc_dict = db['Acc']
            db.close()
        except:
            print('eror1')
        print(queue_dict)
        print(your_dict)
        print(acc_dict)
        your_list = []
        queue_list = []
        acc_list = []
        for key in acc_dict:
            acc = acc_dict.get(key)
            acc_list.append(acc)
        for key in your_dict:
            your = your_dict.get(key)
            your_list.append(your)
        for key in queue_dict:
            queue = queue_dict.get(key)
            queue_list.append(queue)
        return render_template('Queue/queueStaffOrange.html' , queue_list=queue_list , your_list=your_list ,
                               acc_list=acc_list) , {"Refresh": "5; url=/queueStaffRed"}

    @app.route('/queueStaffRed')
    def queue_staff_red():
        your_dict = {}
        queue_dict = {}
        acc_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            queue_dict = db['Generate']
            your_dict = db['Your']
            acc_dict = db['Acc']
            db.close()
        except:
            print('eror1')
        print(queue_dict)
        print(your_dict)
        print(acc_dict)
        your_list = []
        queue_list = []
        acc_list = []
        for key in acc_dict:
            acc = acc_dict.get(key)
            acc_list.append(acc)
        for key in your_dict:
            your = your_dict.get(key)
            your_list.append(your)
        for key in queue_dict:
            queue = queue_dict.get(key)
            queue_list.append(queue)
        return render_template('Queue/queueStaffRed.html' , queue_list=queue_list , your_list=your_list ,
                               acc_list=acc_list)

    @app.route('/updateQueue/<int:id>')
    def update_queue(id):
        queue_dict = {}
        db = shelve.open('queue.db' , 'w')
        queue_dict = db['Generate']
        queue_dict.pop(id)
        generate = GenerateQueueNo.GenerateQueueNo(generate_queue_no=id , your_queue_no=id , acc_queue_no=id ,
                                                   update_no=1 , serve_no=1 , plus=1)
        queue_dict[generate.get_generate_queue_no()] = generate

        db['Generate'] = queue_dict
        db.close()

        if 'customer_id' in session:
            return redirect(url_for('get_queue'))
        elif 'staff_id' in session:
            print('Staff is logged in')
            return redirect(url_for('get_staff_queue'))
        else:
            return redirect(url_for('get_queue_no_acc'))

    @app.route('/deleteQueue/<int:id>')
    def delete_queue(id):
        queue_dict = {}
        your_dict = {}
        acc_dict = {}
        db = shelve.open('queue.db' , 'w')
        queue_dict = db['Generate']
        queue_dict.pop(id)
        your_dict = db['Your']
        your_dict.clear()
        acc_dict = db['Acc']
        acc_dict.clear()
        queue_list = []
        for key in queue_dict:
            queue_list.append(key)
            max_list = max(queue_list)
            your = GenerateQueueNo.GenerateQueueNo(generate_queue_no=max_list , your_queue_no=max_list ,
                                                   acc_queue_no=max_list , update_no=0 , plus=1 , serve_no=1)
        try:
            your_dict[your.get_your_queue_no()] = your
        except:
            print('lol')
        db['Your'] = your_dict
        db['Generate'] = queue_dict
        db['Acc'] = acc_dict
        db.close()

        if 'customer_id' in session:
            return redirect(url_for('get_queue'))
        elif 'staff_id' in session:
            print('Staff is logged in')
            return redirect(url_for('get_staff_queue'))
        else:
            return redirect(url_for('get_queue_no_acc'))

    @app.route('/resetQueue/')
    def reset_queue():  # for staff only
        queue_dict = {}
        your_dict = {}
        db = shelve.open('queue.db' , 'w')
        queue_dict = db['Generate']
        queue_dict.clear()
        your_dict = db['Your']
        your_dict.clear()
        db['Your'] = your_dict
        db['Generate'] = queue_dict
        db.close()

        if 'customer_id' in session:
            return redirect(url_for('get_queue'))
        elif 'staff_id' in session:
            print('Staff is logged in')
            return redirect(url_for('get_staff_queue'))
        else:
            return redirect(url_for('get_queue_no_acc'))

    @app.route('/nowServingPlus/')
    def now_serving_plus():
        serve_dict = {}
        plus_dict = {}
        db = shelve.open('queue.db' , 'c')
        try:
            serve_dict = db['Serve']
            plus_dict = db['Plus']
            serve_dict.clear()
        except:
            print("Error in retrieving Generate from generate.db.")
        # print(your_dict)
        serve_list = []
        plus_list = []
        if len(plus_dict) >= 1:
            for key in plus_dict:
                plus_list.append(key)
                max_list = max(plus_list)
                serve_list.append(max_list + 1)
                serve = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                        your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                        acc_queue_no=GenerateQueueNo.GenerateQueueNo , update_no=0 ,
                                                        serve_no=max_list + 1 , plus=max_list + 1)
                plus = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                       your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                       acc_queue_no=GenerateQueueNo.GenerateQueueNo , update_no=0 ,
                                                       serve_no=max_list + 1 , plus=max_list + 1)
        else:
            serve_list.append(1)
            serve = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    acc_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    update_no=0 , serve_no=1 , plus=1)
            plus = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   acc_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   update_no=0 , serve_no=1 , plus=1)
            max_list = 1
        # print(max_list)
        serve_dict[serve.get_serve_no()] = serve
        plus_dict[plus.get_plus()] = plus

        serve_dict.clear()
        plus_dict.clear()

        db['Serve'] = serve_dict
        db['Plus'] = plus_dict

        db.close()
        return redirect(url_for('now_serving_plus_page'))

    @app.route('/nowServingPlusPage/')
    def now_serving_plus_page():
        serve_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            serve_dict = db['Serve']
            db.close()
        except:
            print('eror2')
        serve_list = []
        for key in serve_dict:
            serve = serve_dict.get(key)
            serve_list.append(serve)

        return render_template('Queue/queueStaffGreen.html' , serve_list=serve_list)

    @app.route('/nowServingMinus/')
    def now_serving_minus():
        serve_dict = {}
        plus_dict = {}
        db = shelve.open('queue.db' , 'c')
        try:
            serve_dict = db['Serve']
            plus_dict = db['Plus']
            serve_dict.clear()

        except:
            print("Error in retrieving Generate from generate.db.")
        # print(your_dict)
        serve_list = []
        plus_list = []
        if len(plus_dict) >= 1:
            for key in plus_dict:
                plus_list.append(key)
                max_list = max(plus_list)
                serve_list.append(max_list - 1)
                serve = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                        your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                        acc_queue_no=GenerateQueueNo.GenerateQueueNo , update_no=0 ,
                                                        serve_no=max_list - 1 , plus=max_list - 1)
                plus = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                       your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                       acc_queue_no=GenerateQueueNo.GenerateQueueNo , update_no=0 ,
                                                       serve_no=max_list - 1 , plus=max_list - 1)
        else:
            serve_list.append(1)
            serve = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    acc_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                    update_no=0 , serve_no=1 , plus=1)
            plus = GenerateQueueNo.GenerateQueueNo(generate_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   your_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   acc_queue_no=GenerateQueueNo.GenerateQueueNo ,
                                                   update_no=0 , serve_no=1 , plus=1)
            max_list = 1
        # print(max_list)
        serve_dict[serve.get_serve_no()] = serve
        plus_dict[plus.get_plus()] = plus

        # serve_dict.clear()
        # plus_dict.clear()

        db['Serve'] = serve_dict
        db['Plus'] = plus_dict

        db.close()
        return redirect(url_for('now_serving_minus_page'))

    @app.route('/nowServingMinusPage/')
    def now_serving_minus_page():
        serve_dict = {}
        try:
            db = shelve.open('queue.db' , 'r')
            serve_dict = db['Serve']
            db.close()
        except:
            print('eror2')
        serve_list = []
        for key in serve_dict:
            serve = serve_dict.get(key)
            serve_list.append(serve)

        return render_template('Queue/queueStaffGreen.html' , serve_list=serve_list)

