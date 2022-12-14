import sqlite3
from datetime import datetime

cnt = sqlite3.connect('store.db')

islogin = False
isadmin = False
userid = ""

##print("open")

##################################################### TABLE users

##sql=''' CREATE TABLE users
##     (id INTEGER PRIMARY KEY,
##     fname CHAR(20) NOT NULL,
##     lname CHAR(30) NOT NULL,
##     addr CHAR(20) NOT NULL,
##     grade INT(10) NOT NULL,
##     username CHAR(15) NOT NULL,
##     password CHAR(15) NOT NULL,
##     cpassword CHAR(15) NOT NULL,
##     edate CHAR(10) NOT NULL,
##     ncode CHAR(15) NOT NULL,
##     reserve1 CHAR(15) NOT NULL)'''
##cnt.execute(sql)
##print("Table created succssefully")
##cnt.close()

##################################################### TABLE products

##sql=''' CREATE TABLE products
##     (id INTEGER PRIMARY KEY,
##     pname CHAR(30) NOT NULL,
##     quantity CHAR(20) NOT NULL,
##     bprice INT(20) NOT NULL,
##     sprice INT(20) NOT NULL,
##     edate CHAR(15) NOT NULL,
##     exdate CHAR(15) NOT NULL,
##     brand CHAR(40) NOT NULL,
##     reserve1 CHAR(20) NOT NULL)'''
##cnt.execute(sql)
##print("Table created succssefully")
##cnt.close()

##################################################### TABLE transactions

##sql=''' CREATE TABLE transactions
##     (id INTEGER PRIMARY KEY,
##     uid INT(15) NOT NULL,
##     pid INT(15) NOT NULL,
##     bdate CHAR(15) NOT NULL,
##     qnt INT(5) NOT NULL,
##     comment CHAR(50) NOT NULL,
##     reserve1 CHAR(30) NOT NULL)'''
##
##cnt.execute(sql)
##print("Table created succssefully")
##cnt.close()

#################################### main program ######################################################

class valid():
    def validation(self,fname, lname, addr, username, password, cpassword, ncode):
        errorlist = []
        if fname == "" or lname == "" or addr == "" or username == "" or password == "" or cpassword == "" or ncode == "":
            msg = "please fill all the blanks"
            errorlist.append(msg)
        if len(password) < 8:
            msg = "pass length must be at least 8"
            errorlist.append(msg)
        if password != cpassword:
            msg = "pass and confirm mismatch"
            errorlist.append(msg)
        if not ncode.isnumeric():
            msg = "national code shold be numeric"
            errorlist.append(msg)
        sql = 'select *from users where username=?'
        cursor = cnt.execute(sql, (username,))
        rows = cursor.fetchall()
        if len(rows) != 0:
            msg = 'username already exist'
            errorlist.append(msg)
        return errorlist

class shop():

    def submit(self):
        fname = input("please enter your name? ")
        lname = input("please enter your lname? ")
        addr = input("please enter your addr? ")
        grade = 0
        reserve = ""
        edate = datetime.today().strftime('%Y-%m-%d')
        username = input("please enter your username? ")
        password = input("please enter your password? ")
        cpassword = input("please enter your password confirmation? ")
        ncode = input("please enter your natinal code? ")
        result = valid.validation(fname, lname, addr, username, password, cpassword, ncode)
        if len(result) > 0:
            for err_msg in result:
                print(err_msg)
            return

        sql = '''INSERT INTO users(fname,lname,addr,grade,username,password,cpassword,edate,ncode,reserve1)\
            VALUES(?,?,?,?,?,?,?,?,?,?)'''
        cnt.execute(sql, (fname, lname, addr, grade, username, password, cpassword, edate, ncode, reserve))
        cnt.commit()
        print("submit done successfully!")

    def login(self):
        global islogin, isadmin, userid
        if islogin:  # if(islogin==True)
            print("you are already logged in")
            return

        user = input("please enter your username: ")
        passw = input("please enter your password: ")
        sql = ''' SELECT username,id FROM users where username=? AND password=?'''
        cursor = cnt.execute(sql, (user, passw))
        rows = cursor.fetchone()
        if not rows:
            print("wrong user or pass ")
            return
        print("welcome to your account")
        userid = rows[1]
        islogin = True
        if user == "admin":
            isadmin = True

    def logout(self):
        global islogin, isadmin, userid
        islogin = False
        isadmin = False
        userid = ""
        print("you are logged out now!")

    def mproducts(self):
        global islogin, isadmin

        if islogin == False and isadmin == False:
            print("you are not allowed for this action")
            return
        print("ok !")
        pname = input("enter your name: ")
        quantity = input("enter your quant: ")
        bprice = input("enter your price: ")
        sprice = input("enter your price for sell: ")
        edate = datetime.today().strftime('%Y-%m-%d')
        exdate = ""
        brand = input("brand: ")
        reserve1 = ""
        #######################################
        sql = '''SELECT pname FROM products  WHERE pname=?'''
        corsur = cnt.execute(sql, (pname,))
        row = corsur.fetchall()
        if len(row) > 0:
            print("products name is already exist!")
            return
        ####################################
        sql = ''' INSERT INTO products(pname,quantity,bprice,sprice,edate,exdate,brand,reserve1)
            VALUES(?,?,?,?,?,?,?,?)'''
        cnt.execute(sql, (pname, quantity, bprice, sprice, edate, exdate, brand, reserve1))
        cnt.commit()
        print("data inserted !")

    def buy(self):
        global islogin, userid
        if islogin == False:
            print('first you must login')
            return
        bdate = datetime.today().strftime('%Y-%m-%d')
        pname = input('enter a product name you want to buy:  ')
        sql = " SELECT * FROM products WHERE pname=? "
        cursor = cnt.execute(sql, (pname,))
        row = cursor.fetchone()
        if not row:
            print('wrong product name')
            return
        print('product:', row[1], 'Q:', row[2], ' brand:', row[7], ' price:', row[4])
        num = int(input('number of products? '))
        if num <= 0:
            print('wrong number')
            return
        if num > int(row[2]):
            print('not enough number of products')
            return
        print('total cost ', num * row[4])
        confirm = input('are you sure? yes/no ')
        if confirm != 'yes':
            print('canceled by user')
            return
        newquant = int(row[2]) - num
        sql = "UPDATE products SET quantity=? WHERE pname=?"
        cnt.execute(sql, (newquant, pname))
        print('thanks for your shopping')
        cnt.commit()

        comment = ""
        reserve1 = ""

        sql = '''INSERT INTO transactions (uid,pid,bdate,qnt,comment,reserve1)
                   VALUES(?,?,?,?,?,?)'''
        cnt.execute(sql, (userid, row[0], bdate, num, comment, reserve1))
        cnt.commit()

    def plist(self):
        sql = "SELECT pname,quantity FROM products WHERE quantity > 0 "
        cursor = cnt.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row[0], 'Q: ', row[1])

    def alltranc(self):
        # global islogin,isadmin
        # if not isadmin:
        # print("you are not admin")
        # return
        # if not islogin:
        # print("you are not login !")
        # return
        sql = "SELECT users.lname,transactions.bdate FROM transactions INNER JOIN users ON transactions.uid=users.id"
        # INNER JOIN products ON transactions.pid=products.id bada bezar
        cursor = cnt.execute(sql)
        for row in cursor:
            print('user: ', row[0], ', date ', row[1])
            # products: ',row[1],'Q:',row[2],'date: ',row[3]
        print("############################################")

    def forget(self):
        print("password forget !")
        ncode = input("enter your code meli: ")
        sql = "SELECT * FROM users WHERE ncode=? "
        cursor = cnt.execute(sql,(ncode,))
        row = cursor.fetchone()
        if row is not None:
            print("your password: ", row[6])
        else:
            print("wrong !")
        print("############################################")


    def updatepass(self):
        #global islogin
        #if islogin == False:
            #print('first you must login')
            #return
        username = input("enter your username: ")
        newpass = input("enter your password for change: ")
        sql=" UPDATE users SET password=? WHERE username=?"
        cnt.execute(sql,(newpass,username,))
        cnt.commit()
        print("your password changed and its ok !")
        print("############################################")

    def showme(self):
        sql='''SELECT * FROM transactions'''
        cursor = cnt.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("wrong")
        else:
            print("date: ",row[3] ,"mojod kala: ",row[4])

        print("############################################")



#############################
ok=shop()
while True:
    plan = input('''please enter your plan ??
submit = 1 || login = 2 || logout = 3
manage = 4 || buy = 5 || list = 6 
all tranc = 7 || forget pass = 8 || change password = 9 ||  show me order and date = 10  || exit = 0 
here : ''')
    if plan == "1":
        ok.submit()
    elif plan == "2":
        ok.login()
    elif plan == "3":
        ok.logout()
    elif plan == "4":
        ok.mproducts()
    elif plan=="5":
        ok.buy()
    elif plan=="6":
        ok.plist()
    elif plan=="7":
        ok.alltranc()
    elif plan=="8":
        ok.forget()
    elif plan=="9":
        ok.updatepass()
    elif plan=="10":
        ok.showme()
    elif plan == "0":
        print('''thanks for shop !
good luck !''')
        break
    else:
        print("wrong input!!")

cnt.close()
