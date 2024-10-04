from colorama import Cursor
from flask import Flask, abort, jsonify, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from decimal import Decimal
import os
from werkzeug.utils import secure_filename
import time



app = Flask(__name__)
UPLOAD_MATER = 'static/mater/'
if not os.path.exists(UPLOAD_MATER):
    os.makedirs(UPLOAD_MATER)
app.config['UPLOAD_MATER'] = UPLOAD_MATER

UPLOAD_FOLDER = '../static/image/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_BANK = 'static/bank/'
if not os.path.exists(UPLOAD_BANK):
    os.makedirs(UPLOAD_BANK)
app.config['UPLOAD_BANK'] = UPLOAD_BANK

UPLOAD_EMP = '../static/emp/'
if not os.path.exists(UPLOAD_EMP):
    os.makedirs(UPLOAD_EMP)
app.config['UPLOAD_EMP'] = UPLOAD_EMP
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kantavee'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tkmanagement'
 
mysql = MySQL(app)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


 
@app.route('/')
#เข้าสู่ระบบ ****************************************************************************************************************
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['User_ID'] = account['User_ID']
            session['username'] = account['username']
            session['role'] = account['role']
            msg = 'Logged in successfully!'
            if account['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)



@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE User_ID = %s', (session['User_ID'],))
        user_info = cursor.fetchone()

        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT SUM(purchaseseller.total) AS total_revenue, 
                COUNT(payment.Payment_ID) AS total_payments 
            FROM purchaseseller 
            LEFT JOIN payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
            WHERE payment.status = 'ชำระเเล้ว';
        """
        cursor1.execute(query)
        revenue = cursor1.fetchone()

        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT SUM(purchaseorder.total) AS totalunicost, 
                COUNT(purchaseorder.PurchaseOrder_ID) AS PurordId, 
                purchaseorder.CreatedDate as date 
            FROM purchaseorder 
            WHERE purchaseorder.status = 'ซื้อขายสำเร็จ';
        """
        cursor2.execute(query)
        purorder = cursor2.fetchone()

        cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor3.execute('''
            SELECT 
                SUM(detailseller.quantity * productstore.AverageCost) AS cost
            FROM 
                purchaseseller 
            LEFT JOIN
                payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
            LEFT JOIN 
                detailseller ON purchaseseller.Pur_Orderseller_ID = detailseller.Pur_Orderseller_ID
            INNER JOIN 
                customer ON customer.Customer_ID = purchaseseller.Customer_ID
            LEFT JOIN 
                productstore ON productstore.Productstore_ID = detailseller.Productstore_ID
            INNER JOIN 
                user ON user.User_ID = purchaseseller.User_ID
            WHERE
                payment.status = 'ชำระเเล้ว';
        ''')
        costseller = cursor3.fetchone()

        cursor4 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
        SELECT 
            payment.Payment_ID AS payid,
            DATE_FORMAT(payment.paymentDT, '%d/%m/%Y : %H:%i:%s') AS date,
            customer.C_name AS cname,
            customer.C_surname AS csurname,
            user.Name AS uname,
            user.Surname AS usurname,
            payment.status AS status,
            purchaseseller.total as total
        FROM 
            purchaseseller 
        LEFT JOIN
            payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
        INNER JOIN 
            customer ON customer.Customer_ID = purchaseseller.Customer_ID
        INNER JOIN 
            user ON user.User_ID = purchaseseller.User_ID
        WHERE
            payment.status = 'ชำระเเล้ว'
        GROUP BY 
            payment.Payment_ID,
            payment.PaymentDT,
            customer.C_name,
            customer.C_surname,
            user.Name,
            user.Surname,
            payment.Payment_money,
            payment.status;
    """
        cursor4.execute(query)
        payments = cursor4.fetchall()
        
        # Calculate the total number of paid orders
        total_paid_orders = len(payments)

        cursor5 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
        SELECT 
            payment.Payment_ID AS payid,
            DATE_FORMAT(payment.paymentDT, '%d/%m/%Y : %H:%i:%s') AS date,
            customer.C_name AS cname,
            customer.C_surname AS csurname,
            user.Name AS uname,
            user.Surname AS usurname,
            payment.status AS status,
            purchaseseller.total as total
        FROM 
            purchaseseller 
        LEFT JOIN
            payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
        INNER JOIN 
            customer ON customer.Customer_ID = purchaseseller.Customer_ID
        INNER JOIN 
            user ON user.User_ID = purchaseseller.User_ID
        WHERE
            payment.status = 'ยังไม่ชำระ'
        GROUP BY 
            payment.Payment_ID,
            payment.PaymentDT,
            customer.C_name,
            customer.C_surname,
            user.Name,
            user.Surname,
            payment.Payment_money,
            payment.status;
    """
        cursor5.execute(query)
        paymentns = cursor5.fetchall()

        total_paid_orders = len(paymentns)

        cursor6 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor6.execute('''
            SELECT 
                CASE 
                    WHEN MONTH(purchaseseller.CreatedDate) = 1 THEN 'มกราคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 2 THEN 'กุมภาพันธ์'
                    WHEN MONTH(purchaseseller.CreatedDate) = 3 THEN 'มีนาคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 4 THEN 'เมษายน'
                    WHEN MONTH(purchaseseller.CreatedDate) = 5 THEN 'พฤษภาคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 6 THEN 'มิถุนายน'
                    WHEN MONTH(purchaseseller.CreatedDate) = 7 THEN 'กรกฎาคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 8 THEN 'สิงหาคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 9 THEN 'กันยายน'
                    WHEN MONTH(purchaseseller.CreatedDate) = 10 THEN 'ตุลาคม'
                    WHEN MONTH(purchaseseller.CreatedDate) = 11 THEN 'พฤศจิกายน'
                    WHEN MONTH(purchaseseller.CreatedDate) = 12 THEN 'ธันวาคม'
                END as month_thai,
                YEAR(purchaseseller.CreatedDate) as yearth,
                SUM(CASE WHEN payment.status = 'ชำระเเล้ว' THEN purchaseseller.total ELSE 0 END) as paid_money,
                SUM(CASE WHEN payment.status = 'ยังไม่ชำระ' THEN purchaseseller.total ELSE 0 END) as unpaid_money
            FROM purchaseseller
            LEFT JOIN payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
            GROUP BY MONTH(purchaseseller.CreatedDate), YEAR(purchaseseller.CreatedDate)
            ORDER BY YEAR(purchaseseller.CreatedDate), MONTH(purchaseseller.CreatedDate)
        ''')
        chart = cursor6.fetchall()

        cursor7 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT productstore.Type_iron as type, productstore.Pro_name as proname, productstore.Quantity AS quan
            FROM productstore 
            WHERE productstore.Type_iron = 'เหล็กเส้นกลม';
        """
        cursor7.execute(query)
        ironkom = cursor7.fetchall()

        cursor8 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT productstore.Type_iron as type, productstore.Pro_name as proname, productstore.Quantity AS quan
            FROM productstore 
            WHERE productstore.Type_iron = 'เหล็กเส้นเเบน';
        """
        cursor8.execute(query)
        ironban = cursor8.fetchall()

        cursor9 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """
            SELECT productstore.Type_iron as type, productstore.Pro_name as proname, productstore.Quantity AS quan
            FROM productstore 
            WHERE productstore.Type_iron = 'เหล็กข้ออ้อย';
        """
        cursor9.execute(query)
        ironooy = cursor9.fetchall()

        cursor10 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor10.execute('''
            SELECT 
                CASE 
                    WHEN MONTH(purchaseorder.CreatedDate) = 1 THEN 'มกราคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 2 THEN 'กุมภาพันธ์'
                    WHEN MONTH(purchaseorder.CreatedDate) = 3 THEN 'มีนาคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 4 THEN 'เมษายน'
                    WHEN MONTH(purchaseorder.CreatedDate) = 5 THEN 'พฤษภาคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 6 THEN 'มิถุนายน'
                    WHEN MONTH(purchaseorder.CreatedDate) = 7 THEN 'กรกฎาคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 8 THEN 'สิงหาคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 9 THEN 'กันยายน'
                    WHEN MONTH(purchaseorder.CreatedDate) = 10 THEN 'ตุลาคม'
                    WHEN MONTH(purchaseorder.CreatedDate) = 11 THEN 'พฤศจิกายน'
                    WHEN MONTH(purchaseorder.CreatedDate) = 12 THEN 'ธันวาคม'
                END as month_thai,
                YEAR(purchaseorder.CreatedDate) as year_th,
                SUM(purchaseorder.total) as paid
            FROM purchaseorder
            GROUP BY MONTH(purchaseorder.CreatedDate), YEAR(purchaseorder.CreatedDate)
            ORDER BY YEAR(purchaseorder.CreatedDate), MONTH(purchaseorder.CreatedDate);
        ''')
        chartpaid = cursor10.fetchall()
        chart_data_paidpur = []
        for row in chartpaid:
            month_year1 = f"{row['month_thai']}-{row['year_th']}"
            paid_moneypur = float(row['paid']) if row['paid'] is not None else 0.0
            chart_data_paidpur.append({"name":  month_year1, "y": paid_moneypur})

        chart_data_paid = []
        chart_data_unpaid = []

        for row in chart:
            month_year = f"{row['month_thai']}-{row['yearth']}"
            paid_money = float(row['paid_money']) if row['paid_money'] is not None else 0.0
            unpaid_money = float(row['unpaid_money']) if row['unpaid_money'] is not None else 0.0
            chart_data_paid.append({"name": month_year, "y": paid_money})
            chart_data_unpaid.append({"name": month_year, "y": unpaid_money})

        total_revenue = float(revenue['total_revenue']) if revenue['total_revenue'] else 0.0
        total_unicost = float(purorder['totalunicost']) if purorder['totalunicost'] else 0.0
        total = total_revenue - total_unicost
        total_costseller = float(costseller['cost']) if costseller['cost'] else 0.0
        profit = (total_revenue - total_costseller)
        profitper = ((profit / total_costseller) * 100) if total_costseller != 0 else 0

        return render_template('admin_dashboard.html', 
            user_info=user_info, 
            revenue=revenue, 
            purorder=purorder, 
            total=total, 
            costseller=costseller, 
            profit=profit, 
            profitper=profitper, 
            payments=payments, 
            paymentns=paymentns, 
            chart_data_paid=chart_data_paid, 
            chart_data_unpaid=chart_data_unpaid,
            total_paid_orders=total_paid_orders,
            ironooy=ironooy,
            ironkom=ironkom,
            ironban=ironban,
            chart_data_paidpur=chart_data_paidpur
        )
    else:
        return redirect(url_for('login'))


@app.route('/user_dashboard')
def user_dashboard():
    if 'loggedin' in session and session['role'] == 'user':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE User_ID = %s', (session['User_ID'],))
        user_info = cursor.fetchone()
        return render_template('user_dashboard.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

#ออกจากระบบ ****************************************************************************************************************
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#การจัดการข้อมูลพนักงาน *******************************************************************************************************
@app.route('/emp')
def emp():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT User_ID, Name, Surname, Gender, Birthday, Telenumber, Email, Position, userimage, username, password, Status_user, Remark, role,address FROM user')
        data = cur.fetchall()
        cur.close()
        
        if session['role'] == 'admin':
            return render_template('emp.html', data=data)
        elif session['role'] == 'user':
            return render_template('login.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    cursor = mysql.connection.cursor()
    # Perform a search query in your MySQL database based on Name or User_ID
    cursor.execute('SELECT * FROM user WHERE Name LIKE %s OR User_ID = %s', ('%' + search_query + '%', search_query))
    data = cursor.fetchall()
    cursor.close()
    return render_template('emp.html', data=data)

@app.route('/empinsert')
def empinsert():
    return render_template('empinsert.html')

@app.route('/empinsertdb', methods=['POST'])
def empinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        telenumber = request.form['telenumber']
        email = request.form['email']
        position = request.form['position']
        username = request.form['username']
        password = request.form['password']
        remark = request.form['remark']
        role = request.form['role']
        status = request.form['status']
        address = request.form['address']
        # Handle file upload
        if 'userimage' not in request.files:
            return 'No file part'
        file = request.files['userimage']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_EMP'], filename)
            file.save(filepath)
            userimage = filepath

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user (User_ID, Name, Surname, Gender, Birthday, Telenumber, Email, Position, userimage, username, password, Remark, role, Status_user, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, name, surname, gender, birthday, telenumber, email, position, userimage, username, password, remark, role, status, address))
        mysql.connection.commit()
        cur.close()

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/emp" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/login" class="btn btn-primary">กลับหน้ารายการ</a>'


@app.route('/editemp/<id>', methods=['GET'])
def editemp(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE User_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updateemp.html', PD=PD)

@app.route('/updatedbemp', methods=['POST'])
def updateemp():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        telenumber = request.form['telenumber']
        email = request.form['email']
        position = request.form['position']
        username = request.form['username']
        password = request.form['password']
        remark = request.form['remark']
        role = request.form['role']
        status = request.form['status']
        address = request.form['address']
        userimage = None
        if 'userimage' in request.files:
            file = request.files['userimage']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_EMP'], filename)
                file.save(filepath)
                userimage = filepath

        cur = mysql.connection.cursor()
        
        if userimage:
            cur.execute('UPDATE user SET Name = %s, Surname = %s, Gender = %s, Birthday = %s, Telenumber = %s, Email = %s, Position = %s, userimage = %s, username = %s, password = %s, Status_user = %s, Remark = %s, role = %s, address =%s WHERE User_ID = %s', (name, surname, gender, birthday, telenumber, email, position, userimage, username, password, status, remark, role,address, id))
        else:
            cur.execute('UPDATE user SET Name = %s, Surname = %s, Gender = %s, Birthday = %s, Telenumber = %s, Email = %s, Position = %s, username = %s, password = %s, Status_user = %s, Remark = %s, role = %s, address = %s WHERE User_ID = %s', (name, surname, gender, birthday, telenumber, email, position, username, password, status, remark, role,address, id))
        
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/emp" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/deleteemp/<int:id>', methods=['GET', 'POST'])
def deleteemp(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE User_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/emp" class="btn btn-primary">กลับหน้ารายการ</a'





#การจัดการข้อมูลผู้ขาย ผู้ผลิต ********************************************************************************************
@app.route('/vendor')
def vendor():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT Vendor_ID, companyname, Vendorns, Identitynumber, Email, Adress, CreatedDate, Remark, Telenumber FROM vendor')
        data = cur.fetchall()
        cur.close()
        
        if session['role'] == 'admin':
            return render_template('Vend.html', data=data)
        elif session['role'] == 'user':
            return render_template('login.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/searchven', methods=['GET'])
def searchven():
    if 'loggedin' in session:
        search_query = request.args.get('search_query')
        cursor = mysql.connection.cursor()
        # Perform a search query in your MySQL database based on Name, User_ID or Type_iron
        query = '''
            SELECT * FROM vendor 
            WHERE Vendor_ID LIKE %s OR companyname LIKE %s OR Vendorns LIKE %s
        '''
        like_query = '%' + search_query + '%'
        cursor.execute(query, (like_query, like_query, like_query))
        data = cursor.fetchall()
        cursor.close()
        
        if session['role'] == 'admin':
            return render_template('Vend.html', data=data)
        elif session['role'] == 'user':
            return render_template('vendoruser.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/vendorinsert')
def vendorinsert():
    return render_template('vendorinsert.html')

@app.route('/vendorinsertdb', methods=['POST'])
def vendorinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        vdname = request.form['vdname']
        vdsurname = request.form['vdsurname']
        identity = request.form['identity']
        email = request.form['email']
        adress = request.form['adress']
        date = request.form['date']
        remark = request.form['remark']
        Telenumber = request.form['Telenumber']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO vendor (Vendor_ID, companyname, Vendorns, Identitynumber, Email, Adress, CreatedDate, Remark, Telenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, vdname, vdsurname, identity, email, adress, date, remark, Telenumber))
        mysql.connection.commit()
        cur.close()
        
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/login" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/editvd/<id>', methods=['GET'])
def editvd(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vendor WHERE Vendor_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatevendor.html', PD=PD)

@app.route('/updatevendor', methods=['POST'])
def updatevd():
    if request.method == 'POST':
        id = request.form['id']
        vdname = request.form['vdname']
        vdsurname = request.form['vdsurname']
        identity = request.form['identity']
        email = request.form['email']
        adress = request.form['adress']
        date = request.form['date']
        remark = request.form['remark']
        Telenumber = request.form['Telenumber']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE vendor SET companyname = %s, Vendorns = %s, Identitynumber = %s, Email = %s, Adress = %s, CreatedDate = %s, Remark = %s, Telenumber = %s WHERE Vendor_ID = %s', (vdname, vdsurname, identity, email, adress, date, remark, Telenumber, id))
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/deletevd/<int:id>', methods=['GET', 'POST'])
def deletevd(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM vendor WHERE Vendor_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a'

#การจัดการข้อมูลผู้ขายผู้ผลิต user ******************************************************************************************************
@app.route('/vendoruser')
def vendoruser():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT Vendor_ID, companyname, Vendorns, Identitynumber, Email, Adress, CreatedDate, Remark, Telenumber FROM vendor')
        data = cur.fetchall()
        cur.close()

        if session['role'] == 'admin':
            return render_template('Vend.html', data=data)  # Admin sees the same as vendor route
        elif session['role'] == 'user':
            return render_template('vendoruser.html', data=data)  # User sees a different template
    else:
        return redirect(url_for('login'))
    

@app.route('/vendorinsertuser')
def vendorinsertuser():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            return render_template('vendorinsert.html')
        elif session['role'] == 'user':
            return render_template('vendorinsertuser.html')
    else:
        return redirect(url_for('login'))

@app.route('/vendorinsertdbu', methods=['POST'])
def vendorinsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        vdname = request.form['vdname']
        vdsurname = request.form['vdsurname']
        identity = request.form['identity']
        email = request.form['email']
        adress = request.form['adress']
        date = request.form['date']
        remark = request.form['remark']
        Telenumber = request.form['Telenumber']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO vendor (Vendor_ID, companyname, Vendorns, Identitynumber, Email, Adress, CreatedDate, Remark, Telenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, vdname, vdsurname, identity, email, adress, date, remark, Telenumber))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif 'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendoruser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/editvduser/<id>', methods=['GET'])
def editvduser(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM vendor WHERE Vendor_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()
        if session['role'] == 'admin':
            return render_template('updatevendor.html', PD=PD)
        elif session['role'] == 'user':
            return render_template('updatevendoruser.html', PD=PD)
    else:
        return redirect(url_for('login'))
    
@app.route('/updatevendoruser', methods=['POST'])
def updatevendoruser():
    if request.method == 'POST':
        id = request.form['id']
        vdname = request.form['vdname']
        vdsurname = request.form['vdsurname']
        identity = request.form['identity']
        email = request.form['email']
        adress = request.form['adress']
        date = request.form['date']
        remark = request.form['remark']
        Telenumber = request.form['Telenumber']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE vendor SET companyname = %s, Vendorns = %s, Identitynumber = %s, Email = %s, Adress = %s, CreatedDate = %s, Remark = %s, Telenumber = %s WHERE Vendor_ID = %s', (vdname, vdsurname, identity, email, adress, date, remark, Telenumber, id))
        mysql.connection.commit()
        cur.close()

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif 'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendoruser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/deletevduser/<int:id>', methods=['GET', 'POST'])
def deletevduser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM vendor WHERE Vendor_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    if 'loggedin' in session and session['role'] == 'admin':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendor" class="btn btn-primary">กลับหน้ารายการ</a>'
    elif 'loggedin' in session and session['role'] == 'user':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/vendoruser" class="btn btn-primary">กลับหน้ารายการ</a>'



#การจัดการข้อมูลวัสดุอุปกรณ์ admin *******************************************************************************************************
@app.route('/materials1')
def materials1():
    if 'loggedin' in session:
        # Fetch the materials data
        cur = mysql.connection.cursor()
        cur.execute('SELECT Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg FROM materials')
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
        cur.close()

        # Check the status and execute the relevant logic
        status = request.args.get('status')  # Assuming status is passed as a query parameter
        
        if status == 'คืนเเล้ว':
            # First, retrieve all relevant records for materials that need to be updated
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity, dm.Quantity AS dm_qty, dm.Updated
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("Before Update:", row)
            cur.close()
            
            # Update materials quantity
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity + COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'คืนเเล้ว'
                    AND dm.Updated = 1
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'คืนเเล้ว'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 1
                );
            ''')
            mysql.connection.commit()
            
            # Debugging logs after update
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("After Update:", row)
            cur.close()

            # Update detail_materials
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 2
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            mysql.connection.commit()
            cur.close()

        # Render the appropriate template based on the user role
        if session.get('role') == 'admin':
            return render_template('materials.html', data=data)
        elif session.get('role') == 'user':
            return render_template('materialuser.html', data=data)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/searchma', methods=['GET'])
def searchma():
    search_query = request.args.get('search_query')
    cursor = mysql.connection.cursor()
    # Perform a search query in your MySQL database based on Name or User_ID
    cursor.execute('SELECT * FROM materials WHERE Materials_ID LIKE %s OR Materials_name = %s', ('%' + search_query + '%', search_query))
    data = cursor.fetchall()
    cursor.close()
    return render_template('materials.html', data=data)

@app.route('/materialinsert')
def materialinsert():
    return render_template('materialinsert.html')

@app.route('/materialinsertdb', methods=['POST'])
def materialinsertdb():
    if request.method == 'POST':
        if 'loggedin' in session and session['role'] == 'admin':
            id = request.form['id']
            maname = request.form['maname']
            type = request.form['type']
            quantity = request.form['quantity']
            date = request.form['date']

            if 'materialsimg' not in request.files:
                return 'No file part'
            file = request.files['materialsimg']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_MATER'], filename)
                file.save(filepath)
                materialsimg = filepath

                # Insert data into the database
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO materials (Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg) VALUES (%s, %s, %s, %s, %s, %s)', (id, maname, type, quantity, date, materialsimg))
                mysql.connection.commit()
                cur.close()

                return 'Data saved successfully <a href="/materials1" class="btn btn-primary">Back to list</a>'
            else:
                return 'Invalid file type'
        else:
            return redirect(url_for('login'))

@app.route('/editmaterial/<id>', methods=['GET'])
def editmaterial(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materials WHERE Materials_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatematerial.html', PD=PD)

@app.route('/updatematerial', methods=['POST'])
def updatematerial():
    if request.method == 'POST':
        id = request.form['id']
        maname = request.form['maname']
        type = request.form['type']
        quantity = request.form['quantity']
        date = request.form['date']

        # Check if a new file is uploaded
        file = request.files['materialsimg']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            materialsimg = filepath
        else:
            # No new file uploaded, use the existing image from the database
            cur = mysql.connection.cursor()
            cur.execute('SELECT materialsimg FROM materials WHERE Materials_ID = %s', (id,))
            materialsimg = cur.fetchone()[0]  # Get the existing file path
            cur.close()

        # Update the database with the new data
        cur = mysql.connection.cursor()
        cur.execute('UPDATE materials SET Materials_name = %s, Type = %s, Quantity = %s, CreatedDate = %s, materialsimg = %s WHERE Materials_ID = %s', 
                    (maname, type, quantity, date, materialsimg, id))
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/materials1" class="btn btn-primary">กลับหน้ารายการ</a>'


@app.route('/deletematerial/<int:id>', methods=['GET', 'POST'])
def deletematerial(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materials WHERE Materials_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/materials1" class="btn btn-primary">กลับหน้ารายการ</a'

#การจัดการข้อมูลวัสดุอุปกรณ์ user ***************************************************************************************************

@app.route('/materialuser')
def materialuser():
    if 'loggedin' in session:
        # Fetch the materials data
        cur = mysql.connection.cursor()
        cur.execute('SELECT Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg FROM materials')
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
        cur.close()

        # Check the status and execute the relevant logic
        status = request.args.get('status')  # Assuming status is passed as a query parameter

        if status == 'คืนเเล้ว':
            # First, retrieve all relevant records for materials that need to be updated
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity, dm.Quantity AS dm_qty, dm.Updated
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("Before Update:", row)
            cur.close()
            
            # Update materials quantity
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity + COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'คืนเเล้ว'
                    AND dm.Updated = 1
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'คืนเเล้ว'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 1
                );
            ''')
            mysql.connection.commit()
            
            # Debugging logs after update
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("After Update:", row)
            cur.close()

            # Update detail_materials
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 2
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            mysql.connection.commit()
            cur.close()

        # Render the appropriate template based on the user role
        if session.get('role') == 'admin':
            return render_template('materials.html', data=data)
        elif session.get('role') == 'user':
            return render_template('materialuser.html', data=data)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



@app.route('/materialinsertuser')
def materialinsertuser():
    if 'loggedin' in session:
        if session['role'] == 'user':
            return render_template('materialinsertuser.html')
        elif session['role'] == 'admin':
            return render_template('materialinsert.html')
    else:
        return redirect(url_for('login'))

@app.route('/materialinsertdbuser', methods=['POST'])
def materialinsertdbuser():
    if 'loggedin' in session:
        if 'id' in request.form and 'maname' in request.form and 'type' in request.form and 'quantity' in request.form and 'date' in request.form:
            id = request.form['id']
            maname = request.form['maname']
            type = request.form['type']
            quantity = request.form['quantity']
            date = request.form['date']

            if 'materialsimg' not in request.files:
                return 'No file part'
            file = request.files['materialsimg']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                materialsimg = os.path.join('static/image', filename)

                # Insert data into the database after file is successfully saved
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO materials (Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg) VALUES (%s, %s, %s, %s, %s, %s)', (id, maname, type, quantity, date, materialsimg))
                mysql.connection.commit()
                cur.close()

                if session['role'] == 'admin':
                    return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/materials" class="btn btn-primary">กลับหน้ารายการ</a>'
                elif session['role'] == 'user':
                    return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/materialuser" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'Missing form data'
    else:
        return redirect(url_for('login'))


@app.route('/editmaterialuser/<id>', methods=['GET'])
def editmaterialuser(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materials WHERE Materials_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatematerialuser.html', PD=PD)

@app.route('/updatematerialuser', methods=['POST'])
def updatematerialuser():
    if request.method == 'POST':
        id = request.form['id']
        maname = request.form['maname']
        type = request.form['type']
        quantity = request.form['quantity']
        date = request.form['date']

        # Check if the post request has the file part
        file = request.files['materialsimg']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            materialsimg = filepath
        else:
            # No new file uploaded, use the existing image from the database
            cur = mysql.connection.cursor()
            cur.execute('SELECT materialsimg FROM materials WHERE Materials_ID = %s', (id,))
            materialsimg = cur.fetchone()[0]  # Get the existing file path
            cur.close()
        


        # Update the database after file is successfully saved
        cur = mysql.connection.cursor()
        cur.execute('UPDATE materials SET Materials_name = %s, Type = %s, Quantity = %s, CreatedDate = %s, materialsimg = %s WHERE Materials_ID = %s', 
                    (maname, type, quantity, date, materialsimg, id))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/materials" class="btn btn-primary">กลับหน้ารายการ</a>'
            elif session['role'] == 'user':
                return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/materialuser" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return redirect(url_for('login'))
        

@app.route('/deletematerialuser/<int:id>', methods=['GET', 'POST'])
def deletematerialuser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materials WHERE Materials_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/materialuser" class="btn btn-primary">กลับหน้ารายการ</a'

#ตารางข้อมูลลูกค้า ADMIN **************************************************************************************************************
@app.route('/customer')
def customer():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT Customer_ID, C_name, C_surname, Identitynumber, Email, Adress, number FROM customer')
        data = cur.fetchall()
        cur.close()
        if session['role'] == 'admin':
            return render_template('Customer.html', data=data)
        elif session['role'] == 'user':
            return render_template('customeruser.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/searchcus', methods=['GET'])
def searchcus():
    if 'loggedin' in session:
        search_query = request.args.get('search_query')
        cursor = mysql.connection.cursor()
        # Perform a search query in your MySQL database based on Name, User_ID or Type_iron
        query = '''
            SELECT * FROM customer 
            WHERE Customer_ID LIKE %s OR C_name LIKE %s OR C_surname LIKE %s
        '''
        like_query = '%' + search_query + '%'
        cursor.execute(query, (like_query, like_query, like_query))
        data = cursor.fetchall()
        cursor.close()
        
        if session['role'] == 'admin':
            return render_template('Customer.html', data=data)
        elif session['role'] == 'user':
            return render_template('customeruser.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/customerinsert')
def customerinsert():
    return render_template('customerinsert.html')

        
@app.route('/customerinsertdb', methods=['GET', 'POST'])
def customerinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        cname = request.form['cname']
        csurname = request.form['csurname']
        identitynumber = request.form['identitynumber']
        email = request.form['email']
        adress = request.form['adress']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO customer (Customer_ID, C_name, C_surname, Identitynumber, Email, Adress, number) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                    (id, cname, csurname, identitynumber, email, adress, number))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/customer" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/customeruser" class="btn btn-primary">กลับหน้ารายการ</a>'
        

@app.route('/editcustomer/<id>', methods=['GET'])
def editcustomer(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM customer WHERE Customer_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()
        return render_template('updatecustomer.html', PD=PD)

@app.route('/updatecustomer', methods=['POST'])
def updatecustomer():
    if 'loggedin' in session and session['role'] == 'admin':
        id = request.form['id']
        cname = request.form['cname']
        csurname = request.form['csurname']
        identitynumber = request.form['identitynumber']
        email = request.form['email']
        adress = request.form['adress']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE customer SET C_name = %s, C_surname = %s, Identitynumber = %s, Email = %s, Adress = %s, number = %s WHERE Customer_ID = %s', 
                    (cname, csurname, identitynumber, email, adress, number, id))
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/customer" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/deletecustomer/<int:id>', methods=['GET', 'POST'])
def deletecustomer(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM customer WHERE Customer_ID = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/customer" class="btn btn-primary">กลับหน้ารายการ</a>'

#ตารางข้อมูลลูกค้า USER **************************************************************************************************************

@app.route('/customeruser')
def customeruser():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT Customer_ID, C_name, C_surname, Identitynumber, Email, Adress, number FROM customer')
        data = cur.fetchall()
        cur.close()
        if session['role'] == 'admin':
            return render_template('Customer.html', data=data)
        elif session['role'] == 'user':
            return render_template('customeruser.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/searchcususer', methods=['GET'])
def searchcususer():
    if 'loggedin' in session:
        search_query = request.args.get('search_query')
        cursor = mysql.connection.cursor()
        # Perform a search query in your MySQL database based on Name, User_ID or Type_iron
        query = '''
            SELECT * FROM customer 
            WHERE Customer_ID LIKE %s OR C_name LIKE %s OR C_surname LIKE %s
        '''
        like_query = '%' + search_query + '%'
        cursor.execute(query, (like_query, like_query, like_query))
        data = cursor.fetchall()
        cursor.close()
        
        if session['role'] == 'admin':
            return render_template('Customer.html', data=data)
        elif session['role'] == 'user':
            return render_template('customeruser.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/customerinsertuser')
def customerinsertuser():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            return render_template('customerinsert.html')
        elif session['role'] == 'user':
            return render_template('customerinsertuser.html')
    else:
        return redirect(url_for('login'))

@app.route('/customerinsertdbuser', methods=['GET', 'POST'])
def customerinsertdbuser():
    if request.method == 'POST':
        id = request.form['id']
        cname = request.form['cname']
        csurname = request.form['csurname']
        identitynumber = request.form['identitynumber']
        email = request.form['email']
        adress = request.form['adress']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO customer (Customer_ID, C_name, C_surname, Identitynumber, Email, Adress, number) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                    (id, cname, csurname, identitynumber, email, adress, number))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/customer" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/customeruser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/editcustomeruser/<id>', methods=['GET'])
def editcustomeruser(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customer WHERE Customer_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatcustomeruser.html', PD=PD)

@app.route('/updatecustomeruser', methods=['POST'])
def updatecustomeruser():
    if 'loggedin' in session:
        id = request.form['id']
        cname = request.form['cname']
        csurname = request.form['csurname']
        identitynumber = request.form['identitynumber']
        email = request.form['email']
        adress = request.form['adress']
        number = request.form['number']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE customer SET C_name = %s, C_surname = %s, Identitynumber = %s, Email = %s, Adress = %s, number = %s WHERE Customer_ID = %s', 
                    (cname, csurname, identitynumber, email, adress, number, id))
        mysql.connection.commit()
        cur.close()

        # Return to the appropriate page based on the user's role
        if session['role'] == 'admin':
            return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/customer" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif session['role'] == 'user':
            return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/customeruser" class="btn btn-primary">กลับหน้ารายการ</a>'
    else:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login'))
  

@app.route('/deletecustomeruser/<int:id>', methods=['GET', 'POST'])
def deletecustomeruser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM customer WHERE Customer_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/customeruser" class="btn btn-primary">กลับหน้ารายการ</a'


    


#ใบเบิกวัสดุอุปกรณ์ *******************************************************************************************************************************

    
#ส่วนของการจัดการสินค้า admin *****************************************************************************************************************
@app.route('/Store')
def store():
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("START TRANSACTION;")
                
            # Update the total cost in the purchaseseller table
            update_query = '''
            UPDATE productstore
                SET AverageCost = CostAmountVat / Quantity
                WHERE Quantity > 0;
            '''
            cur.execute(update_query)
            
            # Commit the transaction after the update
            mysql.connection.commit()

            # Fetch the updated data
            cur.execute('''
                SELECT productstore.Productstore_ID as proid, productstore.Pro_name as proname, productstore.Quantity as quantity, productstore.CostAmountVat as amountvat, productstore.AverageCost as aaveragecost, productstore.Wight as wight, productstore.Type_iron as type, productstore.Porimage as Porimage, productstore.CreatedDate as date, user.Name as uname, user.Surname as usur, vendor.companyname as company
                FROM productstore
                LEFT JOIN user ON user.User_ID = productstore.User_ID
                LEFT JOIN vendor ON vendor.Vendor_ID = productstore.Vendor_ID;
            ''')
            data = cur.fetchall()
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            data = []
        
        finally:
            cur.close()
        
        if session['role'] == 'admin':
            return render_template('Store.html', data=data)
        elif session['role'] == 'user':
            return render_template('Storeuser.html', data=data)
    else:
        return redirect(url_for('login'))


    
@app.route('/searchemp', methods=['GET'])
def searchemp():
    if 'loggedin' in session:
        search_query = request.args.get('search_query')
        cursor = mysql.connection.cursor()
        # Perform a search query in your MySQL database based on Name, User_ID or Type_iron
        query = '''
            SELECT * FROM productstore 
            WHERE Pro_name LIKE %s OR Productstore_ID LIKE %s OR Type_iron LIKE %s
        '''
        like_query = '%' + search_query + '%'
        cursor.execute(query, (like_query, like_query, like_query))
        data = cursor.fetchall()
        cursor.close()
        
        if session['role'] == 'admin':
            return render_template('Store.html', data=data)
        elif session['role'] == 'user':
            return render_template('Storeuser.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/Storeinsert')
def Storeinsert():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()


        # Debug ข้อมูลผู้ใช้
        print("Users fetched from the database:", users)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('Store'))
    return render_template('Storeinsert.html', users=users, vendors=vendors)

@app.route('/Storeinsertdb', methods=['POST'])
def Storeinsertdb():    
        id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        amountvat = request.form['amountvat']
        wight = request.form['wight']
        type = request.form['type']
        date = request.form['date']
        user = request.form['user']
        vendor = request.form['vendor']

        if 'Porimage' not in request.files:
            return 'ไม่มีไฟล์ที่อัปโหลด'
        file = request.files['Porimage']
        if file.filename == '':
            return 'ไม่ได้เลือกไฟล์'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # บันทึกชื่อไฟล์ภาพในฐานข้อมูล
            Porimage = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # ใช้ชื่อไฟล์ที่ถูกต้องในฐานข้อมูล
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO productstore (Productstore_ID, Pro_name, Quantity, CostAmountVat, Wight, Type_iron, Porimage, CreatedDate, User_id, Vendor_ID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (id, name, quantity, amountvat, wight, type, Porimage, date, user, vendor))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            return f'เกิดข้อผิดพลาดในการแทรกข้อมูล: {e}'

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/Storeuser" class="btn btn-primary">กลับหน้ารายการ</a>'
           
@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productstore")
        product = cur.fetchall()  
        cur.close()


    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('store'))
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productstore WHERE Productstore_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatedb.html', PD=PD ,users=users, vendors=vendors, product=product)

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        amountvat = request.form['amountvat']
        wight = request.form['wight']
        type_iron = request.form['type']
        date = request.form['date']
        user = request.form['user']
        vendor = request.form['vendor']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productstore WHERE Productstore_ID = %s", (id,))
        img = cur.fetchone()  # Use fetchone() to retrieve a single record
        
        # Handle image upload
        if 'Porimage' in request.files and request.files['Porimage'].filename != '':
            file = request.files['Porimage']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                Porimage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                flash('ไม่สามารถอัปโหลดไฟล์รูปภาพได้')
                return redirect(request.url)
        else:
            if img:
                Porimage = img[7]  # Use existing image if no new file is uploaded
            else:
                Porimage = None  # Handle the case where no image exists
        
        if Porimage:
            cur.execute('''UPDATE productstore SET Pro_name = %s, Quantity = %s, CostAmountVat = %s, Wight = %s, Type_iron = %s, Porimage = %s, CreatedDate = %s, User_ID = %s, Vendor_ID = %s WHERE Productstore_ID = %s''', 
                        (name, quantity, amountvat, wight, type_iron, Porimage, date, user, vendor, id))
        else:
            cur.execute('''UPDATE productstore SET Pro_name = %s, Quantity = %s, CostAmountVat = %s, Wight = %s, Type_iron = %s, CreatedDate = %s, User_ID = %s, Vendor_ID = %s WHERE Productstore_ID = %s''',
                        (name, quantity, amountvat, wight, type_iron, date, user, vendor, id))
        
        mysql.connection.commit()
        cur.close()

        flash('อัปเดตข้อมูลเรียบร้อยแล้ว')
        return redirect('/Store')
    

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productstore WHERE Productstore_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a'

#อัพเดทสินค้าฝั่งของ user ************************************************************************************************************
@app.route('/Storeuser')
def Storeuser():
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("START TRANSACTION;")
                
            # Update the total cost in the purchaseseller table
            update_query = '''
            UPDATE productstore
                SET AverageCost = CostAmountVat / Quantity
                WHERE Quantity > 0;
            '''
            cur.execute(update_query)
            
            # Commit the transaction after the update
            mysql.connection.commit()

            # Fetch the updated data
            cur.execute('''
                SELECT productstore.Productstore_ID as proid, productstore.Pro_name as proname, productstore.Quantity as quantity, productstore.CostAmountVat as amountvat, productstore.AverageCost as aaveragecost, productstore.Wight as wight, productstore.Type_iron as type, productstore.Porimage as Porimage, productstore.CreatedDate as date, user.Name as uname, user.Surname as usur, vendor.companyname as company
                FROM productstore
                LEFT JOIN user ON user.User_ID = productstore.User_ID
                LEFT JOIN vendor ON vendor.Vendor_ID = productstore.Vendor_ID;
            ''')
            data = cur.fetchall()
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            data = []
        
        finally:
            cur.close()
        
        if session['role'] == 'admin':
            return render_template('Store.html', data=data)
        elif session['role'] == 'user':
            return render_template('Storeuser.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/Storeinsertuser')
def Storeinsertuser():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()



    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('Storeuser'))
    return render_template('Storeinsertuser.html', users=users, vendors=vendors)

@app.route('/Storeinsertdbu', methods=['POST'])
def Storeinsertdbu():    
        id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        amountvat = request.form['amountvat']
        wight = request.form['wight']
        type = request.form['type']
        date = request.form['date']
        user = request.form['user']
        vendor = request.form['vendor']

        if 'Porimage' not in request.files:
            return 'ไม่มีไฟล์ที่อัปโหลด'
        file = request.files['Porimage']
        if file.filename == '':
            return 'ไม่ได้เลือกไฟล์'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # บันทึกชื่อไฟล์ภาพในฐานข้อมูล
            Porimage = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # ใช้ชื่อไฟล์ที่ถูกต้องในฐานข้อมูล
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO productstore (Productstore_ID, Pro_name, Quantity, CostAmountVat, Wight, Type_iron, Porimage, CreatedDate, User_id, Vendor_ID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (id, name, quantity, amountvat, wight, type, Porimage, date, user, vendor))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            return f'เกิดข้อผิดพลาดในการแทรกข้อมูล: {e}'

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/Storeuser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/edituser/<id>', methods=['GET'])
def edituser(id):
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productstore")
        product = cur.fetchall()  
        cur.close()


    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('Storeuser'))
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productstore WHERE Productstore_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatedbu.html', PD=PD ,users=users, vendors=vendors, product=product)

@app.route('/updatedbu', methods=['GET','POST'])
def updatedbu():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        amountvat = request.form['amountvat']
        wight = request.form['wight']
        type_iron = request.form['type']
        date = request.form['date']
        user = request.form['user']
        vendor = request.form['vendor']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productstore WHERE Productstore_ID = %s", (id,))
        img = cur.fetchone()  # Use fetchone() to retrieve a single record
        
        # Handle image upload
        if 'Porimage' in request.files and request.files['Porimage'].filename != '':
            file = request.files['Porimage']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                Porimage = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                flash('ไม่สามารถอัปโหลดไฟล์รูปภาพได้')
                return redirect(request.url)
        else:
            if img:
                Porimage = img[7]  # Use existing image if no new file is uploaded
            else:
                Porimage = None  # Handle the case where no image exists
        
        if Porimage:
            cur.execute('''UPDATE productstore SET Pro_name = %s, Quantity = %s, CostAmountVat = %s, Wight = %s, Type_iron = %s, Porimage = %s, CreatedDate = %s, User_ID = %s, Vendor_ID = %s WHERE Productstore_ID = %s''', 
                        (name, quantity, amountvat, wight, type_iron, Porimage, date, user, vendor, id))
        else:
            cur.execute('''UPDATE productstore SET Pro_name = %s, Quantity = %s, CostAmountVat = %s, Wight = %s, Type_iron = %s, CreatedDate = %s, User_ID = %s, Vendor_ID = %s WHERE Productstore_ID = %s''',
                        (name, quantity, amountvat, wight, type_iron, date, user, vendor, id))
        
        mysql.connection.commit()
        cur.close()

        if 'role' in session:
            if session['role'] == 'admin':
                return 'อัพเดทข้อมูลเรียบร้อยเเล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a>'
            elif session['role'] == 'user':
                return 'อัพเดทข้อมูลเรียบร้อยเเล้ว <a href="/Storeuser" class="btn btn-primary">กลับหน้ารายการ</a>'
        
        # Default response in case the session role is not set or recognized
        return 'อัพเดทข้อมูลเรียบร้อยเเล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a>' 


@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def deleteuser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productstore WHERE Productstore_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    if 'ลบข้อมูลเรียบร้อยเเล้ว' in session and session['role'] == 'admin':
        return 'ลบข้อมูลเรียบร้อยเเล้ว <a href="/Store" class="btn btn-primary">กลับหน้ารายการ</a>'
    else:
        return 'ลบข้อมูลเรียบร้อยเเล้ว <a href="/Storeuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    
#การจัดการใบเสนอขาย*****************************************************************************************************************************
@app.route('/purchaesSL')
def purchaesSL():
    if 'loggedin' in session:
        if session.get('role') in ['admin', 'user']:
            cur = mysql.connection.cursor()
            try:
                # Start a transaction
                cur.execute("START TRANSACTION;")
                
                # Update the total cost in the purchaseseller table
                update_query = '''
                UPDATE purchaseseller
                SET total = (
                    SELECT SUM(a.Total)
                    FROM (
                        SELECT 
                            detailseller.Pur_Orderseller_ID as Purid, 
                            detailseller.quantity * productstore.AverageCost * (1 + (ps.Persenplus / 100)) * 1.07 as Total
                        FROM productstore
                        INNER JOIN detailseller 
                            ON productstore.Productstore_ID = detailseller.Productstore_ID
                        INNER JOIN purchaseseller ps
                            ON detailseller.Pur_Orderseller_ID = ps.Pur_Orderseller_ID
                    ) as a
                    WHERE a.Purid = purchaseseller.Pur_Orderseller_ID
                );
                '''
                cur.execute(update_query)

                # Select the desired fields with the calculated total amount
                select_query = '''
                SELECT 
                    purchaseseller.Pur_Orderseller_ID as Pur_Orderseller_ID, 
                    purchaseseller.CreatedDate as CreatedDate, 
                    customer.C_name as cname, 
                    user.Name as name,
                    purchaseseller.Persenplus,
                    COALESCE(a.Total, 0) as Total,
                    payment.status,
                    purchaseseller.DocumentDate,
                    user.Surname as suru,
                    customer.C_surname as csur
                FROM purchaseseller
                LEFT JOIN user ON user.User_ID = purchaseseller.User_ID
                LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
                LEFT JOIN payment 
                    ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
                LEFT JOIN (
                    SELECT 
                        detailseller.Pur_Orderseller_ID as Purid, 
                        SUM(detailseller.quantity * ((productstore.AverageCost * (1 + (ps.Persenplus / 100))) * 1.07)) as Total
                    FROM productstore
                    INNER JOIN detailseller 
                        ON productstore.Productstore_ID = detailseller.Productstore_ID
                    INNER JOIN purchaseseller ps 
                        ON detailseller.Pur_Orderseller_ID = ps.Pur_Orderseller_ID
                    GROUP BY detailseller.Pur_Orderseller_ID
                ) as a 
                    ON purchaseseller.Pur_Orderseller_ID = a.Purid;
                '''
                cur.execute(select_query)
                data = cur.fetchall()

                # Commit the transaction
                mysql.connection.commit()

                cur.close()

                if session['role'] == 'admin':
                    return render_template('purchaesSL.html', data=data)
                elif session['role'] == 'user':
                    return render_template('purchaesSLuser.html', data=data)
            except Exception as e:
                # Rollback the transaction in case of an error
                mysql.connection.rollback()
                # Handle exceptions gracefully, e.g., log the error and redirect to an error page
                print(f"Error: {e}")
                return render_template('error.html', error="An error occurred while processing your request.")
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/searchpursell', methods=['GET'])
def searchpursell():
    search_query = request.args.get('query', '')  # ใช้ชื่อพารามิเตอร์ที่ตรงกับฟอร์มค้นหา

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            SELECT 
                purchaseseller.Pur_Orderseller_ID AS Pur_Orderseller_ID, 
                purchaseseller.CreatedDate AS CreatedDate, 
                customer.C_name AS cname, 
                user.Name AS name,
                purchaseseller.Persenplus,
                COALESCE(a.Total, 0) AS Total,
                payment.status,
                purchaseseller.DocumentDate,
                user.Surname AS suru,
                customer.C_surname AS csur
            FROM purchaseseller
            LEFT JOIN user ON user.User_ID = purchaseseller.User_ID
            LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
            LEFT JOIN payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
            LEFT JOIN (
                SELECT 
                    detailseller.Pur_Orderseller_ID AS Purid, 
                    SUM(detailseller.quantity * ((productstore.AverageCost * (1 + (ps.Persenplus / 100))) * 1.07)) AS Total
                FROM productstore
                INNER JOIN detailseller ON productstore.Productstore_ID = detailseller.Productstore_ID
                INNER JOIN purchaseseller ps ON detailseller.Pur_Orderseller_ID = ps.Pur_Orderseller_ID
                GROUP BY detailseller.Pur_Orderseller_ID
            ) AS a ON purchaseseller.Pur_Orderseller_ID = a.Purid
            WHERE purchaseseller.Pur_Orderseller_ID = %s OR customer.C_name LIKE %s OR user.Name LIKE %s
            ''', (search_query, '%' + search_query + '%', '%' + search_query + '%'))
        
        data = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        data = []  # กำหนดค่าเริ่มต้นสำหรับ data
    finally:
        cursor.close()

    # ตรวจสอบสถานะการล็อกอินและส่งคืนผลลัพธ์ตามบทบาทของผู้ใช้
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session['role'] == 'admin':
        return render_template('PurchaesSL.html', data=data)
    elif session['role'] == 'user':
        return render_template('PurchaesSLuser.html', data=data)
    
    # ถ้าไม่มีเงื่อนไขตรงตามที่ระบุ ให้ส่งกลับไปยังหน้าอื่นๆ ตามที่ต้องการ
    return redirect(url_for('login'))

    

@app.route('/purchaesslinsert')
def purchaesslinsert():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Customer_ID, C_name, C_surname FROM customer")
        customer = cur.fetchall()  
        cur.close()


        # Debug ข้อมูลผู้ใช้
        print("Users fetched from the database:", users)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('purchaesSL'))
    return render_template('purchaesslinsert.html', users=users, customer=customer)

@app.route('/purchaesslinsertdb', methods=['POST'])
def purchaesslinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        docdate = request.form['docdate']
        remark = request.form['remark']
        cusid = request.form['cusid']
        userid = request.form['userid']
        persen = request.form['persen']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO purchaseseller (Pur_Orderseller_ID  , CreatedDate, DocumentDate, Remark, Customer_ID, User_ID, Persenplus ) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, date, docdate, remark, cusid,userid,persen))
        mysql.connection.commit()
        id = cur.lastrowid
        print("id", id)
        cur.execute('INSERT INTO payment ( Pur_Orderseller_ID ) VALUES (%s)', [str(id)])
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSLuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/editpurchase/<id>', methods=['GET'])
def editpurchase(id):
    try:
        # ดึงข้อมูลพนักงาน
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        # ดึงข้อมูลลูกค้า
        cur = mysql.connection.cursor()
        cur.execute("SELECT Customer_ID, C_name, C_surname FROM customer")
        customer = cur.fetchall()  
        cur.close()

        # ดึงข้อมูลการซื้อขายตาม Pur_Orderseller_ID
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM purchaseseller WHERE Pur_Orderseller_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        # ตรวจสอบว่ามีข้อมูลใน PD หรือไม่
        if not PD:
            flash(f"ไม่พบข้อมูลการสั่งซื้อที่มี ID {id}", 'warning')
            return redirect(url_for('purchaesSL'))

        # ส่งข้อมูลไปยัง template
        return render_template('updatepurdb.html', PD=PD, users=users, customer=customer)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูล: {e}", 'danger')
        print("Error fetching data:", e)
        return redirect(url_for('purchaesSL'))

@app.route('/updatepurdb', methods=['POST'])
def updatepurdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        docdate = request.form['docdate']
        remark = request.form['remark']
        cusid = request.form['cusid']
        userid = request.form['userid']
        persen = request.form['persen']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE purchaseseller SET CreatedDate = %s, DocumentDate = %s, Remark = %s, Customer_ID = %s, User_ID = %s, Persenplus = %s WHERE Pur_Orderseller_ID = %s', (date, docdate, remark, cusid, userid, persen, id))
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/deletepur/<int:id>', methods=['GET', 'POST'])
def deletepur(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM purchaseseller WHERE Pur_Orderseller_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a'

#*************************************************************************************************************************************
@app.route('/detailseller/<int:Pur_Orderseller_ID>', methods=['GET', 'POST'])
def detailseller(Pur_Orderseller_ID):
    # Initialize variables
    total = 0
    totalvat = 0
    vat = 0.07
    
    if request.method == 'POST':
        id = request.form['id']
        quantity = request.form['quantity']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detailseller SET quantity = %s WHERE Sellerdetail_ID = %s', (quantity, id))
            mysql.connection.commit()
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
            return redirect(url_for('detailseller', Pur_Orderseller_ID=Pur_Orderseller_ID))
        finally:
            cur.close()
    
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            purchaseseller.Pur_Orderseller_ID as PurIDs, 
            purchaseseller.CreatedDate as PurDate,
            purchaseseller.DocumentDate as PurDocdate,
            purchaseseller.Customer_ID as customerid, 
            purchaseseller.User_ID as UserID, 
            purchaseseller.Remark as RemarkPur, 
            detailseller.Sellerdetail_ID as detailsellid, 
            detailseller.CreatedDate as detaildate, 
            detailseller.Productstore_ID as Productid, 
            detailseller.quantity as quantity,
            detailseller.quantity * (productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100))) AS amount,
            customer.C_name as customername, 
            customer.Adress as address, 
            customer.Email as emailcus, 
            user.Name as nameemp,
            productstore.Pro_name as Pro_name, 
            productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100)) as average,
            productstore.Porimage as image,
            payment.status
        FROM 
            purchaseseller 
        LEFT JOIN
        	payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
        LEFT JOIN 
            detailseller ON purchaseseller.Pur_Orderseller_ID = detailseller.Pur_Orderseller_ID
        INNER JOIN 
            customer ON customer.Customer_ID = purchaseseller.Customer_ID
        LEFT JOIN 
            productstore ON productstore.Productstore_ID = detailseller.Productstore_ID
        INNER JOIN 
            user ON user.User_ID = purchaseseller.User_ID
        WHERE
            purchaseseller.Pur_Orderseller_ID = %s;
        '''
        cur.execute(query, (Pur_Orderseller_ID,))
        data = cur.fetchall()
        
        if not data:
            abort(500)  # If no data is found, return a 404 error
        
        for row in data:
            if row[10] is not None:
                total += row[10]
                totalvat += row[10] * (1 + vat)
                print(totalvat)
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []
    finally:
        cur.close()
    
    if session['role'] == 'admin':
        return render_template('detailseller.html', data=data, total=total, totalvat=totalvat)
    elif session['role'] == 'user':
        return render_template('detailselleruser.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))

@app.route('/get_product_info/<int:product_id>', methods=['GET'])
def get_product_info(product_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Pro_name, AverageCost, Porimage, Quantity FROM productstore WHERE Productstore_ID = %s", (product_id,))
        product = cur.fetchone()
        cur.close()

        if product:
            product_info = f"""
            <p><img src="/static/{product[2]}" alt="Product Image" width="100"></p>
            <p>ชื่อสินค้า: {product[0]}</p>
            <p>ราคาเฉลี่ย: {product[1]}</p>
            <p>จำนวนสินค้าคงเหลือ: <span id="available-stock">{ product[3] }</span></p>
            """
            return product_info
        else:
            return '<p>ไม่พบข้อมูลสินค้า</p>'
    except Exception as e:
        return f'<p>เกิดข้อผิดพลาด: {e}</p>'

@app.route('/detailsellerinsert/<int:Pur_Orderseller_ID>', methods=['GET', 'POST'])
def detailsellerinsert(Pur_Orderseller_ID):
    try:

        cur = mysql.connection.cursor()
        cur.execute("SELECT Productstore_ID, Pro_name  FROM productstore")
        product = cur.fetchall()  
        cur.close()
        

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('detailseller/<int:Pur_Orderseller_ID>'))

    return render_template('detailsellerinsert.html', Pur_Orderseller_ID=Pur_Orderseller_ID, product=product)

@app.route('/detailsellerinsertdb', methods=['POST'])
def detailsellerinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        purid = request.form['purid']
        proid = request.form['proid']
        quantity = int(request.form['quantity'])  # Ensure quantity is an integer

        try:
            cur = mysql.connection.cursor()
            
            # Fetch the available stock for the selected product
            cur.execute("SELECT Quantity FROM productstore WHERE Productstore_ID = %s", (proid,))
            stock = cur.fetchone()
            
            if stock and quantity > stock[0]:
                flash('จำนวนสินค้ามากกว่าที่มีอยู่ในคลัง', 'danger')
                cur.close()
                return redirect(url_for('detailsellerinsert', Pur_Orderseller_ID=purid))

            # If quantity is valid, proceed to insert the data
            cur.execute('INSERT INTO detailseller (Sellerdetail_ID, CreatedDate, Pur_Orderseller_ID, Productstore_ID, quantity) VALUES (%s, %s, %s, %s, %s)', (id, date, purid, proid, quantity))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
            
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        
        finally:
            cur.close()
        
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailseller', Pur_Orderseller_ID=purid))
            else:
                return redirect(url_for('detailselleruser', Pur_Orderseller_ID=purid))
    
    return redirect(url_for('login'))

    

@app.route('/editdetailseller/<id>', methods=['GET'])
def editdetailseller(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Productstore_ID, Pro_name FROM productstore")
        products = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        if PD:
            product_id = PD[3]
            print("Selected Productstore_ID:", product_id)
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT Quantity, 
                    COALESCE(Porimage, '') AS Porimage, 
                    COALESCE(AverageCost, 0) AS AverageCost 
                FROM productstore 
                WHERE Productstore_ID = %s
                """, (product_id,))
            stock = cur.fetchone()
            cur.close()
            print("Stock Information:", stock)
            PD = list(PD) + [stock[0], stock[1], stock[2]]  # Add stock information to PD
            print("Updated PD:", PD)
            print(PD)

        return render_template('updatedbdetailseller.html', PD=PD, products=products)
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching details:", e)
        return redirect(url_for('detailseller'))

@app.route('/updatedetailseller', methods=['POST'])
def updatedetailseller():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        purid = request.form['purid']
        proid = request.form['proid']
        quantity = request.form['quantity']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detailseller SET CreatedDate = %s, Pur_Orderseller_ID = %s, Productstore_ID = %s, quantity = %s WHERE Sellerdetail_ID = %s',
                        (date, purid, proid, quantity, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('detailseller', Pur_Orderseller_ID=purid))
    return redirect(url_for('login'))

@app.route('/deletedetailseller/<int:id>', methods=['GET', 'POST'])
def deletedetailseller(id):
    if 'loggedin' in session:
        Pur_Orderseller_ID = None
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Pur_Orderseller_ID ก่อนลบ
            cur.execute('SELECT Pur_Orderseller_ID FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                Pur_Orderseller_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        
        if Pur_Orderseller_ID:
            return redirect(url_for('detailseller', Pur_Orderseller_ID=Pur_Orderseller_ID))
        else:
            return redirect(url_for('detailseller'))
    return redirect(url_for('login'))

    

#ฟอร์มใบเสนอขาย***************************************************************************************************************
@app.route('/detailsellerform/<int:Sellerdetail_ID>')
def detailsellerform(Sellerdetail_ID):
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            query = '''
             SELECT 
                purchaseseller.Pur_Orderseller_ID as PurIDs, 
                purchaseseller.CreatedDate as PurDate,
                purchaseseller.DocumentDate as PurDocdate,
                purchaseseller.Customer_ID as customerid, 
                purchaseseller.User_ID as UserID, 
                purchaseseller.Remark as RemarkPur, 
                detailseller.Sellerdetail_ID as detailsellid, 
                detailseller.CreatedDate as detaildate, 
                detailseller.Productstore_ID as Productid, 
                detailseller.quantity as quantity,
                detailseller.quantity * (productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100))) AS amount,
                customer.C_name as customername, 
                customer.Adress as address, 
                customer.Email as emailcus, 
                user.Name as nameemp,
                productstore.Pro_name as Pro_name, 
                productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100)) as average,
                productstore.Porimage as image,
                payment.status,
                user.Surname as suru,
                customer.C_surname as csur
            FROM 
                purchaseseller 
            LEFT JOIN
                payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
            LEFT JOIN 
                detailseller ON purchaseseller.Pur_Orderseller_ID = detailseller.Pur_Orderseller_ID
            INNER JOIN 
                customer ON customer.Customer_ID = purchaseseller.Customer_ID
            LEFT JOIN 
                productstore ON productstore.Productstore_ID = detailseller.Productstore_ID
            INNER JOIN 
                user ON user.User_ID = purchaseseller.User_ID
            WHERE
                purchaseseller.Pur_Orderseller_ID = %s;
            '''
            cur.execute(query, (Sellerdetail_ID,))
            data = cur.fetchall()
            
            if not data:
                abort(404)  # If no data is found, return a 404 error
            total =0
            totalvat =0
            vat = 0.07
            for row in data:
                total += row[10]
                totalvat += row[10] * (1+vat)
                
        except MySQLdb.Error as e:
            print(f"Database Error: {e}")
            data = []
        finally:
            cur.close()
        
        if session['role'] == 'admin':
            return render_template('detailsellerform.html', data=data, total=total, totalvat=totalvat)
        elif session['role'] == 'user':
            return render_template('detailsellerform.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))
    
#การจัดการข้อมูลใบเสนอขาย user *******************************************************************************************************
@app.route('/purchaesSLuser')
def purchaesSLuser():
    if 'loggedin' in session:
        if session.get('role') in ['admin', 'user']:
            cur = mysql.connection.cursor()
            try:
                # Start a transaction
                cur.execute("START TRANSACTION;")
                
                # Update the total cost in the purchaseseller table
                update_query = '''
                UPDATE purchaseseller
                SET total = (
                    SELECT SUM(a.Total)
                    FROM (
                        SELECT 
                            detailseller.Pur_Orderseller_ID as Purid, 
                            detailseller.quantity * productstore.AverageCost * (1 + (ps.Persenplus / 100)) * 1.07 as Total
                        FROM productstore
                        INNER JOIN detailseller 
                            ON productstore.Productstore_ID = detailseller.Productstore_ID
                        INNER JOIN purchaseseller ps
                            ON detailseller.Pur_Orderseller_ID = ps.Pur_Orderseller_ID
                    ) as a
                    WHERE a.Purid = purchaseseller.Pur_Orderseller_ID
                );
                '''
                cur.execute(update_query)

                # Select the desired fields with the calculated total amount
                select_query = '''
                SELECT 
                    purchaseseller.Pur_Orderseller_ID as Pur_Orderseller_ID, 
                    purchaseseller.CreatedDate as CreatedDate, 
                    customer.C_name as cname, 
                    user.Name as name,
                    purchaseseller.Persenplus,
                    COALESCE(a.Total, 0) as Total,
                    payment.status,
                    purchaseseller.DocumentDate,
                    user.Surname as suru,
                    customer.C_surname as csur
                FROM purchaseseller
                LEFT JOIN user ON user.User_ID = purchaseseller.User_ID
                LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
                LEFT JOIN payment 
                    ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
                LEFT JOIN (
                    SELECT 
                        detailseller.Pur_Orderseller_ID as Purid, 
                        SUM(detailseller.quantity * ((productstore.AverageCost * (1 + (ps.Persenplus / 100))) * 1.07)) as Total
                    FROM productstore
                    INNER JOIN detailseller 
                        ON productstore.Productstore_ID = detailseller.Productstore_ID
                    INNER JOIN purchaseseller ps 
                        ON detailseller.Pur_Orderseller_ID = ps.Pur_Orderseller_ID
                    GROUP BY detailseller.Pur_Orderseller_ID
                ) as a 
                    ON purchaseseller.Pur_Orderseller_ID = a.Purid;
                '''
                cur.execute(select_query)
                data = cur.fetchall()

                # Commit the transaction
                mysql.connection.commit()

                cur.close()

                if session['role'] == 'admin':
                    return render_template('purchaesSL.html', data=data)
                elif session['role'] == 'user':
                    return render_template('purchaesSLuser.html', data=data)
            except Exception as e:
                # Rollback the transaction in case of an error
                mysql.connection.rollback()
                # Handle exceptions gracefully, e.g., log the error and redirect to an error page
                print(f"Error: {e}")
                return render_template('error.html', error="An error occurred while processing your request.")
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login')) 
    
@app.route('/purchaesslinsertuser')
def purchaesslinsertuser():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Customer_ID, C_name, C_surname FROM customer")
        customer = cur.fetchall()  
        cur.close()


        # Debug ข้อมูลผู้ใช้
        print("Users fetched from the database:", users)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('purchaesSLuser'))
    return render_template('purchaesslinsertuser.html', users=users, customer=customer)

@app.route('/purchaesslinsertdbu', methods=['POST'])
def purchaesslinsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        docdate = request.form['docdate']
        remark = request.form['remark']
        cusid = request.form['cusid']
        userid = request.form['userid']
        persen = request.form['persen']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO purchaseseller (Pur_Orderseller_ID  , CreatedDate, DocumentDate, Remark, Customer_ID, User_ID, Persenplus ) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, date, docdate, remark, cusid,userid,persen))
        mysql.connection.commit()
        id = cur.lastrowid
        print("id", id)
        cur.execute('INSERT INTO payment ( Pur_Orderseller_ID ) VALUES (%s)', [str(id)])
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSLuser" class="btn btn-primary">กลับหน้ารายการ</a>'
        
@app.route('/editpurchaseuser/<id>', methods=['GET'])
def editpurchaseuser(id):
    try:
        # ดึงข้อมูลพนักงาน
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        # ดึงข้อมูลลูกค้า
        cur = mysql.connection.cursor()
        cur.execute("SELECT Customer_ID, C_name, C_surname FROM customer")
        customer = cur.fetchall()  
        cur.close()

        # ดึงข้อมูลการซื้อขายตาม Pur_Orderseller_ID
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM purchaseseller WHERE Pur_Orderseller_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        # ตรวจสอบว่ามีข้อมูลใน PD หรือไม่
        if not PD:
            flash(f"ไม่พบข้อมูลการสั่งซื้อที่มี ID {id}", 'warning')
            return redirect(url_for('purchaesSLuser'))

        # ส่งข้อมูลไปยัง template
        return render_template('updatepurdbu.html', PD=PD, users=users, customer=customer)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูล: {e}", 'danger')
        print("Error fetching data:", e)
        return redirect(url_for('purchaesSLuser'))

@app.route('/updatepurdbu', methods=['POST'])
def updatepurdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        docdate = request.form['docdate']
        remark = request.form['remark']
        cusid = request.form['cusid']
        userid = request.form['userid']
        persen = request.form['persen']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE purchaseseller SET CreatedDate = %s, DocumentDate = %s, Remark = %s, Customer_ID = %s, User_ID = %s, Persenplus = %s WHERE Pur_Orderseller_ID = %s', (date, docdate, remark, cusid, userid, persen, id))
        mysql.connection.commit()
        cur.close()

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSLuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

    

@app.route('/deletepuru/<int:id>', methods=['GET', 'POST'])
def deletepuru(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM purchaseseller WHERE Pur_Orderseller_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    if 'loggedin' in session and session['role'] == 'admin':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSL" class="btn btn-primary">กลับหน้ารายการ</a>'
    elif'loggedin' in session and session['role'] == 'user':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaesSLuser" class="btn btn-primary">กลับหน้ารายการ</a>'

#*************************************************************************************************************************************
@app.route('/detailselleruser/<int:Pur_Orderseller_ID>', methods=['GET', 'POST'])
def detailselleruser(Pur_Orderseller_ID):
    # Initialize variables
    total = 0
    totalvat = 0
    vat = 0.07
    
    if request.method == 'POST':
        id = request.form['id']
        quantity = request.form['quantity']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detailseller SET quantity = %s WHERE Sellerdetail_ID = %s', (quantity, id))
            mysql.connection.commit()
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
            return redirect(url_for('detailseller', Pur_Orderseller_ID=Pur_Orderseller_ID))
        finally:
            cur.close()
    
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            purchaseseller.Pur_Orderseller_ID as PurIDs, 
            purchaseseller.CreatedDate as PurDate,
            purchaseseller.DocumentDate as PurDocdate,
            purchaseseller.Customer_ID as customerid, 
            purchaseseller.User_ID as UserID, 
            purchaseseller.Remark as RemarkPur, 
            detailseller.Sellerdetail_ID as detailsellid, 
            detailseller.CreatedDate as detaildate, 
            detailseller.Productstore_ID as Productid, 
            detailseller.quantity as quantity,
            detailseller.quantity * (productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100))) AS amount,
            customer.C_name as customername, 
            customer.Adress as address, 
            customer.Email as emailcus, 
            user.Name as nameemp,
            productstore.Pro_name as Pro_name, 
            productstore.AverageCost * (1 + (purchaseseller.Persenplus / 100)) as average,
            productstore.Porimage as image,
            payment.status
        FROM 
            purchaseseller 
        LEFT JOIN
        	payment ON payment.Payment_ID = purchaseseller.Pur_Orderseller_ID
        LEFT JOIN 
            detailseller ON purchaseseller.Pur_Orderseller_ID = detailseller.Pur_Orderseller_ID
        INNER JOIN 
            customer ON customer.Customer_ID = purchaseseller.Customer_ID
        LEFT JOIN 
            productstore ON productstore.Productstore_ID = detailseller.Productstore_ID
        INNER JOIN 
            user ON user.User_ID = purchaseseller.User_ID
        WHERE
            purchaseseller.Pur_Orderseller_ID = %s;
        '''
        cur.execute(query, (Pur_Orderseller_ID,))
        data = cur.fetchall()
        
        if not data:
            abort(500)  # If no data is found, return a 404 error
        
        for row in data:
            if row[10] is not None:
                total += row[10]
                totalvat += row[10] * (1 + vat)
                print(totalvat)
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []
    finally:
        cur.close()
    
    if session['role'] == 'admin':
        return render_template('detailseller.html', data=data, total=total, totalvat=totalvat)
    elif session['role'] == 'user':
        return render_template('detailselleruser.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))

@app.route('/detailsellerinsertuser/<int:Pur_Orderseller_ID>', methods=['GET', 'POST'])
def detailsellerinsertuser(Pur_Orderseller_ID):
    try:

        cur = mysql.connection.cursor()
        cur.execute("SELECT Productstore_ID, Pro_name  FROM productstore")
        product = cur.fetchall()  
        cur.close()
        

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('detailseller/<int:Pur_Orderseller_ID>'))

    return render_template('detailsellerinsertuser.html', Pur_Orderseller_ID=Pur_Orderseller_ID, product=product)

@app.route('/detailsellerinsertdbu', methods=['POST'])
def detailsellerinsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        purid = request.form['purid']
        proid = request.form['proid']
        quantity = int(request.form['quantity'])  # Ensure quantity is an integer

        try:
            cur = mysql.connection.cursor()
            
            # Fetch the available stock for the selected product
            cur.execute("SELECT Quantity FROM productstore WHERE Productstore_ID = %s", (proid,))
            stock = cur.fetchone()
            
            if stock and quantity > stock[0]:
                flash('จำนวนสินค้ามากกว่าที่มีอยู่ในคลัง', 'danger')
                cur.close()
                return redirect(url_for('detailsellerinsert', Pur_Orderseller_ID=purid))

            # If quantity is valid, proceed to insert the data
            cur.execute('INSERT INTO detailseller (Sellerdetail_ID, CreatedDate, Pur_Orderseller_ID, Productstore_ID, quantity) VALUES (%s, %s, %s, %s, %s)', (id, date, purid, proid, quantity))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
            
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        
        finally:
            cur.close()
        
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailseller', Pur_Orderseller_ID=purid))
            elif session['role'] == 'user':
                return redirect(url_for('detailselleruser', Pur_Orderseller_ID=purid))
    return redirect(url_for('login'))

@app.route('/editdetailselleruser/<id>', methods=['GET'])
def editdetailselleruser(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Productstore_ID, Pro_name FROM productstore")
        products = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        if PD:
            product_id = PD[3]
            print("Selected Productstore_ID:", product_id)
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT Quantity, 
                    COALESCE(Porimage, '') AS Porimage, 
                    COALESCE(AverageCost, 0) AS AverageCost 
                FROM productstore 
                WHERE Productstore_ID = %s
                """, (product_id,))
            stock = cur.fetchone()
            cur.close()
            print("Stock Information:", stock)
            PD = list(PD) + [stock[0], stock[1], stock[2]]  # Add stock information to PD
            print("Updated PD:", PD)
            print(PD)

        return render_template('updatedbdetailselleruser.html', PD=PD, products=products)
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching details:", e)
        return redirect(url_for('updatedbdetailselleruser'))

@app.route('/updatedbdetailselleruser', methods=['POST'])
def updatedbdetailselleruser():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        purid = request.form['purid']
        proid = request.form['proid']
        quantity = request.form['quantity']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detailseller SET CreatedDate = %s, Pur_Orderseller_ID = %s, Productstore_ID = %s, quantity = %s WHERE Sellerdetail_ID = %s',
                        (date, purid, proid, quantity, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        
        # ตรวจสอบ role ของผู้ใช้เพื่อ redirect ไปหน้าที่ถูกต้อง
        if session['role'] == 'admin':
            return redirect(url_for('detailseller', Pur_Orderseller_ID=purid))
        elif session['role'] == 'user':
            return redirect(url_for('detailselleruser', Pur_Orderseller_ID=purid))
    
    return redirect(url_for('login'))


@app.route('/deletedetailselleruser/<int:id>', methods=['GET', 'POST'])
def deletedetailselleruser(id):
    if 'loggedin' in session:
        Pur_Orderseller_ID = None
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Pur_Orderseller_ID ก่อนลบ
            cur.execute('SELECT Pur_Orderseller_ID FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                Pur_Orderseller_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM detailseller WHERE Sellerdetail_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        if Pur_Orderseller_ID:
            if session['role'] == 'admin':
                return redirect(url_for('detailseller', Pur_Orderseller_ID=Pur_Orderseller_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailselleruser', Pur_Orderseller_ID=Pur_Orderseller_ID))
        else:
            return redirect(url_for('detailOrder'))
            
    return redirect(url_for('login'))


#การจัดการข้อมูลใบเสนอซื้อ ************************************************************************************************************  

@app.route('/purchaseOrder')
def purchaseOrder():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['admin', 'user']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    try:
        # Start a transaction
        cur.execute("START TRANSACTION;")
        
        # Update the total cost in the purchaseorder table
        update_query = '''
        UPDATE purchaseorder
        SET total = (
            SELECT SUM(a.Total)
            FROM (
                SELECT 
                    orderdetail.PurchaseOrder_ID as PurodID, 
                    orderdetail.Quantity * orderdetail.UnitCost * 1.07 as Total
                FROM 
                    orderdetail
            ) as a
            WHERE a.PurodID = purchaseorder.PurchaseOrder_ID
        );
        '''
        cur.execute(update_query)

        # Select the desired fields with the calculated total amount
        select_query = '''
        SELECT 
                    purchaseorder.PurchaseOrder_ID as PurodID, 
                    purchaseorder.CreatedDate as CreatedDate, 
                    purchaseorder.Remark as Remark, 
                    user.Name as username,
                    user.Surname as suru,
                    vendor.companyname as company,
                    COALESCE(a.Total, 0) as Total,
                    purchaseorder.status as status
                FROM purchaseorder
                LEFT JOIN (
                    SELECT 
                        orderdetail.PurchaseOrder_ID as PurodID, 
                        SUM(orderdetail.Quantity * orderdetail.UnitCost * 1.07) as Total
                    FROM orderdetail
                    GROUP BY orderdetail.PurchaseOrder_ID
                ) as a ON purchaseorder.PurchaseOrder_ID = a.PurodID
                LEFT JOIN user on purchaseorder.User_ID = user.User_ID
                LEFT JOIN vendor on purchaseorder.Vendor_ID = vendor.Vendor_ID;
        '''
        cur.execute(select_query)
        data = cur.fetchall()

        # Commit the transaction
        mysql.connection.commit()

        cur.close()

        if session['role'] == 'admin':
            return render_template('PurchaseOD.html', data=data)
        elif session['role'] == 'user':
            return render_template('PurchaseODuser.html', data=data)
    except Exception as e:
        # Rollback the transaction in case of an error
        mysql.connection.rollback()
        # Handle exceptions gracefully, e.g., log the error and redirect to an error page
        print(f"Error: {e}")
        return render_template('error.html', error="An error occurred while processing your request.")
    
    # If there's no exception and no redirection happened, redirect to login
    return redirect(url_for('login'))


    
@app.route('/searchpuro', methods=['GET'])
def searchpuro():
    search_query = request.args.get('query', '')  # Set default value to an empty string if no query is found

    cursor = mysql.connection.cursor()
    try:
        query = """
            SELECT 
                purchaseorder.PurchaseOrder_ID as PurodID, 
                purchaseorder.CreatedDate as CreatedDate, 
                purchaseorder.Remark as Remark, 
                user.Name as username,
                user.Surname as suru,
                vendor.companyname as company,
                COALESCE(a.Total, 0) as Total,
                purchaseorder.status as status
            FROM purchaseorder
            LEFT JOIN (
                SELECT 
                    orderdetail.PurchaseOrder_ID as PurodID, 
                    SUM(orderdetail.Quantity * orderdetail.UnitCost * 1.07) as Total
                FROM orderdetail
                GROUP BY orderdetail.PurchaseOrder_ID
            ) as a ON purchaseorder.PurchaseOrder_ID = a.PurodID
            LEFT JOIN user on purchaseorder.User_ID = user.User_ID
            LEFT JOIN vendor on purchaseorder.Vendor_ID = vendor.Vendor_ID
            WHERE vendor.companyname LIKE %s OR purchaseorder.PurchaseOrder_ID = %s
            ORDER BY purchaseorder.PurchaseOrder_ID
        """
        cursor.execute(query, ('%' + search_query + '%', search_query))
        data = cursor.fetchall()
    except Exception as e:
        # Handle errors, such as showing a message or logging the error
        print(f"Error: {e}")
        data = []  # Set default value for data
    finally:
        cursor.close()

    # Check login status and return results based on user role
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'admin':
        return render_template('PurchaseOD.html', data=data)
    elif session['role'] == 'user':
        return render_template('PurchaseODuser.html', data=data)

    # Redirect to login or another page if the conditions above are not met
    return redirect(url_for('login'))

@app.route('/purchaesODinsert')
def purchaesODinsert():
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()


        # Debug ข้อมูลผู้ใช้
        print("Users fetched from the database:", users)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('purchaseOrder'))

    return render_template('purchaesODinsert.html',users=users, vendors=vendors)

@app.route('/purchaesODinsertdb', methods=['POST'])
def purchaesODinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        userid = request.form['userid']
        vendorid = request.form['vendorid']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO purchaseorder (PurchaseOrder_ID  , CreatedDate, Remark, User_ID, Vendor_ID, status ) VALUES (%s, %s, %s, %s, %s,%s)', (id, date,remark, userid,vendorid,status))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaseODuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/editpurchaseOD/<id>', methods=['GET'])
def editpurchaseOD(id):
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname, Vendorns FROM vendor")
        vendors = cur.fetchall()  
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('purchaseOrder'))


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM purchaseorder WHERE PurchaseOrder_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatepurchaseOD.html', PD=PD ,users=users, vendors=vendors)

@app.route('/updatepurchaseOD', methods=['POST'])
def updatepurchaseOD():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        userid = request.form['User_ID']
        vendorid = request.form['Vendor_ID']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE purchaseorder SET CreatedDate = %s, Remark = %s, User_ID = %s, Vendor_ID = %s, status = %s WHERE PurchaseOrder_ID = %s', (date, remark, userid,vendorid ,status, id))
        mysql.connection.commit()
        cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/deletepurchaseOD/<int:id>', methods=['GET', 'POST'])
def deletepurchaseOD(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM purchaseorder WHERE PurchaseOrder_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a'

@app.route('/detailOrder/<int:PurchaseOrder_ID>', methods=['GET', 'POST'])
def detailOrder(PurchaseOrder_ID):
    # Initialize variables
    total = Decimal('0.00')
    totalvat = Decimal('0.00')
    vat = Decimal('0.07')
    
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            purchaseorder.PurchaseOrder_ID as PurodID, 
            purchaseorder.CreatedDate as date,
            purchaseorder.Remark as Remark,
            purchaseorder.Vendor_ID as Vendor_ID, 
            vendor.companyname as company,
            vendor.Adress as address,
            vendor.Email as email,
            purchaseorder.User_ID as UserID, 
            user.Name as username, 
            orderdetail.Orderdetail_ID as orderdetailid, 
            orderdetail.CreatedDate as detaildate, 
            orderdetail.Productname as Productname, 
            orderdetail.UnitCost as unicost,
            orderdetail.Quantity as quantity,
            orderdetail.Quantity * orderdetail.UnitCost AS amount,
            user.Surname as Usur
        FROM 
            purchaseorder 
        LEFT JOIN 
            orderdetail ON purchaseorder.PurchaseOrder_ID = orderdetail.PurchaseOrder_ID
        LEFT JOIN 
            vendor ON vendor.Vendor_ID = purchaseorder.Vendor_ID
        INNER JOIN 
            user ON user.User_ID = purchaseorder.User_ID
        WHERE
            purchaseorder.PurchaseOrder_ID = %s;
        '''
        cur.execute(query, (PurchaseOrder_ID,))
        data = cur.fetchall()
        
        if not data:
            abort(500)  # If no data is found, return a 404 error
        
        for row in data:
            if row[14] is not None:
                total += Decimal(row[14]) * (Decimal('1.00') + vat)
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []
    finally:
        cur.close()
    
    if session['role'] == 'admin':
        return render_template('detailOrder.html', data=data, total=total, totalvat=totalvat)
    elif session['role'] == 'user':
        return render_template('detailOrderuser.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))
    

@app.route('/detailOrderinsert/<int:PurchaseOrder_ID>', methods=['GET', 'POST'])
def detailOrderinsert(PurchaseOrder_ID):
    return render_template('detailOrderinsert.html', PurchaseOrder_ID=PurchaseOrder_ID)

@app.route('/detailOrderinsertdb', methods=['POST'])
def detailOrderinsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        proname = request.form['proname']
        unicost = request.form['unicost']
        quantity = request.form['quantity']
        purodid = request.form['purodid']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO orderdetail (Orderdetail_ID, CreatedDate, Productname, UnitCost, Quantity, PurchaseOrder_ID) VALUES (%s, %s, %s, %s, %s, %s)', (id, date, proname, unicost, quantity, purodid))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
    

        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailOrder', PurchaseOrder_ID=purodid))
            else:
                return redirect(url_for('detailOrderuser', PurchaseOrder_ID=purodid))
    return redirect(url_for('login'))


@app.route('/editdetailOrder/<id>', methods=['GET'])
def editdetailOrder(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatedetailOrder.html', PD=PD)

@app.route('/updatedetailOrder', methods=['POST'])
def updatedetailOrder():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        proname = request.form['proname']
        unicost = request.form['unicost']
        quantity = request.form['quantity']
        purodid = request.form['purodid']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE orderdetail SET CreatedDate = %s, Productname = %s, UnitCost = %s, Quantity = %s, PurchaseOrder_ID = %s WHERE Orderdetail_ID = %s', (date, proname, unicost, quantity,purodid, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('detailOrder', PurchaseOrder_ID=purodid))
    return redirect(url_for('login'))

@app.route('/deletedetailOrder/<int:id>', methods=['GET', 'POST'])
def deletedetailOrder(id):
    if 'loggedin' in session:
        PurchaseOrder_ID = None
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Pur_Orderseller_ID ก่อนลบ
            cur.execute('SELECT PurchaseOrder_ID FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                PurchaseOrder_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        
        if PurchaseOrder_ID:
            return redirect(url_for('detailOrder', PurchaseOrder_ID=PurchaseOrder_ID))
        else:
            return redirect(url_for('detailOrder'))
    return redirect(url_for('login'))



@app.route('/detailOrderform/<int:PurchaseOrder_ID>', methods=['GET', 'POST'])
def detailOrderform(PurchaseOrder_ID):
    # Initialize variables
    total = Decimal('0.00')
    totalvat = Decimal('0.00')
    vat = Decimal('0.07')
    
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            purchaseorder.PurchaseOrder_ID as PurodID, 
            purchaseorder.CreatedDate as date,
            purchaseorder.Remark as Remark,
            purchaseorder.Vendor_ID as Vendor_ID, 
            vendor.companyname as company,
            vendor.Adress as address,
            vendor.Email as email,
            purchaseorder.User_ID as UserID, 
            user.Name as username, 
            orderdetail.Orderdetail_ID as orderdetailid, 
            orderdetail.CreatedDate as detaildate, 
            orderdetail.Productname as Productname, 
            orderdetail.UnitCost as unicost,
            orderdetail.Quantity as quantity,
            orderdetail.Quantity * orderdetail.UnitCost AS amount,
            user.Surname as Usur
        FROM 
            purchaseorder 
        LEFT JOIN 
            orderdetail ON purchaseorder.PurchaseOrder_ID = orderdetail.PurchaseOrder_ID
        LEFT JOIN 
            vendor ON vendor.Vendor_ID = purchaseorder.Vendor_ID
        INNER JOIN 
            user ON user.User_ID = purchaseorder.User_ID
        WHERE
            purchaseorder.PurchaseOrder_ID = %s;
        '''
        cur.execute(query, (PurchaseOrder_ID,))
        data = cur.fetchall()
        
        if not data:
            abort(500)  # If no data is found, return a 404 error
        
        for row in data:
            if row[14] is not None:
                total += Decimal(row[14])
                totalvat += Decimal(row[14]) * (Decimal('1.00') + vat)
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []
    finally:
        cur.close()
    
    if session['role'] == 'admin':
        return render_template('detailOrderform.html', data=data, total=total, totalvat=totalvat)
    elif session['role'] == 'user':
        return render_template('detailOrderform.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))
    
#การจัดการข้อมูลใบเสนอซื้อ user ******************************************************************************************************
@app.route('/PurchaseODuser')
def PurchaseODuser():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['admin', 'user']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    try:
        # Start a transaction
        cur.execute("START TRANSACTION;")
        
        # Update the total cost in the purchaseorder table
        update_query = '''
        UPDATE purchaseorder
        SET total = (
            SELECT SUM(a.Total)
            FROM (
                SELECT 
                    orderdetail.PurchaseOrder_ID as PurodID, 
                    orderdetail.Quantity * orderdetail.UnitCost * 1.07 as Total
                FROM 
                    orderdetail
            ) as a
            WHERE a.PurodID = purchaseorder.PurchaseOrder_ID
        );
        '''
        cur.execute(update_query)

        # Select the desired fields with the calculated total amount
        select_query = '''
        SELECT 
                    purchaseorder.PurchaseOrder_ID as PurodID, 
                    purchaseorder.CreatedDate as CreatedDate, 
                    purchaseorder.Remark as Remark, 
                    user.Name as username,
                    user.Surname as suru,
                    vendor.companyname as company,
                    COALESCE(a.Total, 0) as Total,
                    purchaseorder.status as status
                FROM purchaseorder
                LEFT JOIN (
                    SELECT 
                        orderdetail.PurchaseOrder_ID as PurodID, 
                        SUM(orderdetail.Quantity * orderdetail.UnitCost * 1.07) as Total
                    FROM orderdetail
                    GROUP BY orderdetail.PurchaseOrder_ID
                ) as a ON purchaseorder.PurchaseOrder_ID = a.PurodID
                LEFT JOIN user on purchaseorder.User_ID = user.User_ID
                LEFT JOIN vendor on purchaseorder.Vendor_ID = vendor.Vendor_ID;
        '''
        cur.execute(select_query)
        data = cur.fetchall()

        # Commit the transaction
        mysql.connection.commit()

        cur.close()

        if session['role'] == 'admin':
            return render_template('PurchaseOD.html', data=data)
        elif session['role'] == 'user':
            return render_template('PurchaseODuser.html', data=data)
    except Exception as e:
        # Rollback the transaction in case of an error
        mysql.connection.rollback()
        # Handle exceptions gracefully, e.g., log the error and redirect to an error page
        print(f"Error: {e}")
        return render_template('error.html', error="An error occurred while processing your request.")
    
    # If there's no exception and no redirection happened, redirect to login
    return redirect(url_for('login'))



@app.route('/purchaesODinsertuser')
def purchaesODinsertuser():
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname FROM vendor")
        vendors = cur.fetchall()  
        cur.close()


        # Debug ข้อมูลผู้ใช้
        print("Users fetched from the database:", users)

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('PurchaseODuser'))

    return render_template('purchaesODinsertuser.html',users=users, vendors=vendors)

@app.route('/purchaesODinsertdbu', methods=['POST'])
def purchaesODinsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        userid = request.form['userid']
        vendorid = request.form['vendorid']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO purchaseorder (PurchaseOrder_ID  , CreatedDate, Remark, User_ID, Vendor_ID, status ) VALUES (%s, %s, %s, %s, %s,%s)', (id, date,remark, userid,vendorid,status))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif 'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/PurchaseODuser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/editpurchaseODu/<id>', methods=['GET'])
def editpurchaseODu(id):
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT Vendor_ID, companyname, Vendorns FROM vendor")
        vendors = cur.fetchall()  
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('PurchaseODuser'))


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM purchaseorder WHERE PurchaseOrder_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatepurchaseODu.html', PD=PD ,users=users, vendors=vendors)

@app.route('/updatepurchaseODu', methods=['POST'])
def updatepurchaseODu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        userid = request.form['User_ID']
        vendorid = request.form['Vendor_ID']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE purchaseorder SET CreatedDate = %s, Remark = %s, User_ID = %s, Vendor_ID = %s, status = %s WHERE PurchaseOrder_ID = %s', (date, remark, userid,vendorid ,status, id))
        mysql.connection.commit()
        cur.close()

    if 'loggedin' in session and session['role'] == 'admin':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a>'
    elif 'loggedin' in session and session['role'] == 'user':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/PurchaseODuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/deletepurchaseODu/<int:id>', methods=['GET', 'POST'])
def deletepurchaseODu(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM purchaseorder WHERE PurchaseOrder_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    if 'loggedin' in session and session['role'] == 'admin':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/purchaseOrder" class="btn btn-primary">กลับหน้ารายการ</a>'
    elif 'loggedin' in session and session['role'] == 'user':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/PurchaseODuser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/detailOrderuser/<int:PurchaseOrder_ID>', methods=['GET', 'POST'])
def detailOrderuser(PurchaseOrder_ID):
    # Initialize variables
    total = Decimal('0.00')
    totalvat = Decimal('0.00')
    vat = Decimal('0.07')
    
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            purchaseorder.PurchaseOrder_ID as PurodID, 
            purchaseorder.CreatedDate as date,
            purchaseorder.Remark as Remark,
            purchaseorder.Vendor_ID as Vendor_ID, 
            vendor.companyname as company,
            vendor.Adress as address,
            vendor.Email as email,
            purchaseorder.User_ID as UserID, 
            user.Name as username, 
            orderdetail.Orderdetail_ID as orderdetailid, 
            orderdetail.CreatedDate as detaildate, 
            orderdetail.Productname as Productname, 
            orderdetail.UnitCost as unicost,
            orderdetail.Quantity as quantity,
            orderdetail.Quantity * orderdetail.UnitCost AS amount,
            user.Surname as Usur
        FROM 
            purchaseorder 
        LEFT JOIN 
            orderdetail ON purchaseorder.PurchaseOrder_ID = orderdetail.PurchaseOrder_ID
        LEFT JOIN 
            vendor ON vendor.Vendor_ID = purchaseorder.Vendor_ID
        INNER JOIN 
            user ON user.User_ID = purchaseorder.User_ID
        WHERE
            purchaseorder.PurchaseOrder_ID = %s;
        '''
        cur.execute(query, (PurchaseOrder_ID,))
        data = cur.fetchall()
        
        if not data:
            abort(500)  # If no data is found, return a 404 error
        
        for row in data:
            if row[14] is not None:
                total += Decimal(row[14]) * (Decimal('1.00') + vat)
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []
    finally:
        cur.close()
    
    if session['role'] == 'admin':
        return render_template('detailOrder.html', data=data, total=total, totalvat=totalvat)
    elif session['role'] == 'user':
        return render_template('detailOrderuser.html', data=data, total=total, totalvat=totalvat)
    else:
        return redirect(url_for('login'))
    

@app.route('/detailOrderinsertuser/<int:PurchaseOrder_ID>', methods=['GET', 'POST'])
def detailOrderinsertuser(PurchaseOrder_ID):
    if 'role' in session and session['role'] == 'admin':
        return render_template('detailOrderinsert.html', PurchaseOrder_ID=PurchaseOrder_ID)
    elif 'role' in session and session['role'] == 'user':
        return render_template('detailOrderinsertuser.html',PurchaseOrder_ID=PurchaseOrder_ID)

@app.route('/detailOrderinsertdbu', methods=['POST'])
def detailOrderinsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        proname = request.form['proname']
        unicost = request.form['unicost']
        quantity = request.form['quantity']
        purodid = request.form['purodid']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO orderdetail (Orderdetail_ID, CreatedDate, Productname, UnitCost, Quantity, PurchaseOrder_ID) VALUES (%s, %s, %s, %s, %s, %s)', (id, date, proname, unicost, quantity, purodid))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
    

        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailOrder', PurchaseOrder_ID=purodid))
            else:
                return redirect(url_for('detailOrderuser', PurchaseOrder_ID=purodid))
    return redirect(url_for('login'))


@app.route('/editdetailOrderuser/<id>', methods=['GET'])
def editdetailOrderuser(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updatedetailOrderuser.html', PD=PD)

@app.route('/updatedetailOrderuser', methods=['POST'])
def updatedetailOrderuser():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        proname = request.form['proname']
        unicost = request.form['unicost']
        quantity = request.form['quantity']
        purodid = request.form['purodid']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE orderdetail SET CreatedDate = %s, Productname = %s, UnitCost = %s, Quantity = %s, PurchaseOrder_ID = %s WHERE Orderdetail_ID = %s', (date, proname, unicost, quantity,purodid, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailOrder', PurchaseOrder_ID=purodid))
            elif session['role'] == 'user':
                return redirect(url_for('detailOrderuser', PurchaseOrder_ID=purodid))
    return redirect(url_for('login'))

@app.route('/deletedetailOrderu/<int:id>', methods=['GET', 'POST'])
def deletedetailOrderu(id):
    if 'loggedin' in session:
        PurchaseOrder_ID = None
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Pur_Orderseller_ID ก่อนลบ
            cur.execute('SELECT PurchaseOrder_ID FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                PurchaseOrder_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM orderdetail WHERE Orderdetail_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
        
        if PurchaseOrder_ID:
            if session['role'] == 'admin':
                return redirect(url_for('detailOrder', PurchaseOrder_ID=PurchaseOrder_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailOrderuser', PurchaseOrder_ID=PurchaseOrder_ID))
        else:
            return redirect(url_for('detailOrder'))
            
    return redirect(url_for('login'))



#Requisition materials------------------------------------------------------------------------------------------
@app.route('/requisition')
def requisition():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['admin', 'user']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    try:
        # Check if any materials need updating
        status = 'ยังไม่คืน'
        if status == 'ยังไม่คืน':
            # Update the materials quantity based on the status
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );
            ''')
            mysql.connection.commit()

            # Mark the detail materials as updated
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;
            ''')
            mysql.connection.commit()

        # Select the desired fields with the calculated total amount
        select_query = '''
        SELECT requistion_materials.Req_Materials_ID as reqid, requistion_materials.CreatedDate as date, requistion_materials.Remark as Remark, requistion_materials.status as status, user.User_ID as uid, user.Name as name, user.Surname as surname
        FROM requistion_materials
        LEFT JOIN user ON requistion_materials.User_ID = user.User_ID;
        '''
        cur.execute(select_query)
        data = cur.fetchall()

        cur.close()

        if session['role'] == 'admin':
            return render_template('Requi.html', data=data)
        elif session['role'] == 'user':
            return render_template('Requiuser.html', data=data)
    except Exception as e:
        # Rollback the transaction in case of an error
        mysql.connection.rollback()
        # Handle exceptions gracefully, e.g., log the error and redirect to an error page
        print(f"Error: {e}")
        return render_template('error.html', error="An error occurred while processing your request.")
    
    # If there's no exception and no redirection happened, redirect to login
    return redirect(url_for('login'))

@app.route('/searchreq', methods=['GET'])
def searchreq():
    search_query = request.args.get('query')  # ใช้ชื่อพารามิเตอร์ที่ตรงกับฟอร์มค้นหา
    if search_query is None:
        search_query = ''  # ตั้งค่าเริ่มต้นเป็นสตริงว่างถ้าไม่พบ query

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                requistion_materials.Req_Materials_ID as reqid, 
                requistion_materials.CreatedDate as date, 
                requistion_materials.Remark as Remark, 
                requistion_materials.status as status, 
                user.User_ID as uid, 
                user.Name as name, 
                user.Surname as surname
            FROM requistion_materials
            LEFT JOIN user ON requistion_materials.User_ID = user.User_ID 
            WHERE requistion_materials.status LIKE %s OR requistion_materials.Req_Materials_ID = %s
        """, ('%' + search_query + '%', search_query))
        data = cursor.fetchall()
    except Exception as e:
        # จัดการข้อผิดพลาด เช่น แสดงข้อความหรือบันทึกข้อผิดพลาด
        print(f"Error: {e}")
        data = []  # กำหนดค่าเริ่มต้นสำหรับ data
    finally:
        cursor.close()

    # ตรวจสอบสถานะการล็อกอินและส่งคืนผลลัพธ์ตามบทบาทของผู้ใช้
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session['role'] == 'admin':
        return render_template('Requi.html', data=data)
    elif session['role'] == 'user':
        return render_template('Requiuser.html', data=data)
    
    # ถ้าไม่มีเงื่อนไขตรงตามที่ระบุ ให้ส่งกลับไปยังหน้าอื่นๆ ตามที่ต้องการ
    return redirect(url_for('login'))

@app.route('/requisitioninsert')
def requisitioninsert():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('requisition'))
    return render_template('requisitioninsert.html', users=users)

@app.route('/requisitioninsertdb', methods=['POST'])
def requisitioninsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        status = request.form['status']
        userid = request.form['userid']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO requistion_materials (Req_Materials_ID  , CreatedDate, Remark, status, User_ID ) VALUES (%s, %s, %s, %s, %s)', (id, date,remark,status, userid))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a>'
        else:
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisitionuser" class="btn btn-primary">กลับหน้ารายการ</a>'
    

@app.route('/editrequisition/<id>', methods=['GET'])
def editrequisition(id):
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('requisition'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM requistion_materials WHERE Req_Materials_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updaterequisition.html', PD=PD, users=users)

@app.route('/updaterequisition', methods=['POST'])
def updaterequisition():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        status = request.form['status']
        userid = request.form['User_ID']

        # อัพเดตข้อมูลในตาราง requistion_materials
        cur = mysql.connection.cursor()
        cur.execute('UPDATE requistion_materials SET CreatedDate = %s, Remark = %s, status = %s, User_ID = %s WHERE Req_Materials_ID = %s', 
                    (date, remark, status, userid, id))
        mysql.connection.commit()
        cur.close()

        if status == 'ยังไม่คืน':
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );
            ''')
            mysql.connection.commit()
            cur.close()
            
            # ทำเครื่องหมายว่าอัพเดตแล้ว
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;
            ''')
            mysql.connection.commit()
            cur.close()

        elif status == 'คืนเเล้ว':
            # Debugging logs
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity, dm.Quantity AS dm_qty, dm.Updated
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("Before Update:", row)
            cur.close()
            
            # Update materials quantity
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity + COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'คืนเเล้ว'
                    AND dm.Updated = 1
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'คืนเเล้ว'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 1
                );
            ''')
            mysql.connection.commit()
            
            # Debugging logs after update
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("After Update:", row)
            cur.close()

            # Update detail_materials
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 2
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            mysql.connection.commit()
            cur.close()

        return 'อัปเดตข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a>'


    

@app.route('/deleterequisition/<int:id>', methods=['GET', 'POST'])
def deleterequisition(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM requistion_materials WHERE Req_Materials_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return 'ลบข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a'

#detail requisition-----------------------------------------------------------------------------------------------------------  
@app.route('/detailrequisition/<int:Req_Materials_ID>', methods=['GET', 'POST'])
def detailrequisition(Req_Materials_ID):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # ตรวจสอบสถานะของการเบิกวัสดุ
    status = None
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT status FROM requistion_materials WHERE Req_Materials_ID = %s', (Req_Materials_ID,))
        result = cur.fetchone()
        if result:
            status = result[0]
        cur.close()
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        return redirect(url_for('login'))

    if status == 'ยังไม่คืน':
        try:
            # อัพเดตจำนวนวัสดุ
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );''')
            mysql.connection.commit()
            cur.close()

            # ทำเครื่องหมายว่าอัพเดตแล้ว
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;''')
            mysql.connection.commit()
            cur.close()
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาดในการอัพเดตข้อมูล: {e}", 'danger')
            return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            requistion_materials.Req_Materials_ID as Reqid, 
            detail_materials.Detail_Materials_ID as detaiID, 
            detail_materials.CreatedDate as date, 
            detail_materials.Quantity as Quantity, 
            detail_materials.Materials_ID as materialsid, 
            materials.Materials_name as matename, 
            materials.Type as type, 
            user.Name as name, 
            user.Surname as surname,
            requistion_materials.Remark as remark,
            materials.materialsimg as img
        FROM requistion_materials
        LEFT JOIN detail_materials ON requistion_materials.Req_Materials_ID = detail_materials.Req_Materials_ID
        LEFT JOIN materials ON materials.Materials_ID = detail_materials.Materials_ID
        LEFT JOIN user ON user.User_ID = requistion_materials.User_ID
        WHERE requistion_materials.Req_Materials_ID = %s;
        '''
        cur.execute(query, (Req_Materials_ID,))
        data = cur.fetchall()
        cur.close()
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []

    if session['role'] == 'admin':
        return render_template('detailrequisition.html', data=data)
    elif session['role'] == 'user':
        return render_template('detailrequisitionuser.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/get_materials_info/<int:material_id>', methods=['GET'])
def get_materials_info(material_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Materials_name, materialsimg, Quantity FROM materials WHERE Materials_ID = %s", (material_id,))
        material = cur.fetchone()
        cur.close()

        if material:
            material_info = f"""
            <p><img src="/static/{material[1]}" alt="Materials Image" width="100"></p>
            <p>ชื่อวัสดุ: {material[0]}</p>
            <p>จำนวนวัสดุคงเหลือ: <span id="available-stock">{ material[2] }</span></p>
            """
            return material_info
        else:
            return '<p>ไม่พบข้อมูลวัสดุ</p>'
    except Exception as e:
        return f'<p>เกิดข้อผิดพลาด: {e}</p>'
    
@app.route('/detailrequisitioninsert/<int:Req_Materials_ID>', methods=['GET', 'POST'])
def detailrequisitioninsert(Req_Materials_ID):
    try:

        cur = mysql.connection.cursor()
        cur.execute("SELECT Materials_ID, Materials_name  FROM materials")
        material = cur.fetchall()  
        cur.close()
        
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('detailrequisitioninsert/<int:Req_Materials_ID>'))
    return render_template('detailrequisitioninsert.html', Req_Materials_ID=Req_Materials_ID, material=material)

@app.route('/detailrequisitioninsertdb', methods=['POST'])
def detailrequisitioninsertdb():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        quantity = request.form['quantity']
        Req_Materials_ID = request.form['Req_Materials_ID']
        Materials_ID = request.form['Materials_ID']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO detail_materials (Detail_Materials_ID , CreatedDate, Quantity, Req_Materials_ID, Materials_ID) VALUES (%s, %s, %s, %s, %s)', (id, date, quantity, Req_Materials_ID, Materials_ID))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
    
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
            else:
                return redirect(url_for('detailrequisitionuser', Req_Materials_ID=Req_Materials_ID))
    return redirect(url_for('login'))



@app.route('/editdetailrequisition/<id>', methods=['GET'])
def editdetailrequisition(id):
    try:
        # Fetch materials for the dropdown
        cur = mysql.connection.cursor()
        cur.execute("SELECT Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg FROM materials")
        materials = cur.fetchall()
        cur.close()

        # Fetch the detail for the specific requisition
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        if PD:
            material_id = PD[4]  # Assuming Materials_ID is at index 4 in PD
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT Quantity, 
                    COALESCE(materialsimg, '') AS materialsimg, 
                    Type 
                FROM materials 
                WHERE Materials_ID = %s
            """, (material_id,))
            stock = cur.fetchone()
            cur.close()
            print(stock)
            # Append additional stock information to PD
            PD = list(PD) + [stock[0], stock[1], stock[2]]

        return render_template('updatedetailrequisition.html', PD=PD, materials=materials,stock=stock)
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูล: {e}", 'danger')
        return redirect(url_for('detailrequisition'))

@app.route('/updatedetailrequisition', methods=['POST'])
def updatedetailrequisition():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        quantity = request.form['quantity']
        Req_Materials_ID = request.form['Req_Materials_ID']
        Materials_ID = request.form['Materials_ID']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detail_materials SET CreatedDate = %s, Quantity = %s, Req_Materials_ID = %s, Materials_ID = %s WHERE Detail_Materials_ID = %s', (date, quantity, Req_Materials_ID, Materials_ID, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()

        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailrequisitionuser', Req_Materials_ID=Req_Materials_ID))
    return redirect(url_for('login'))

@app.route('/deletedetailrequisition/<int:id>', methods=['GET', 'POST'])
def deletedetailrequisition(id):
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Req_Materials_ID ก่อนลบ
            cur.execute('SELECT Req_Materials_ID FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                Req_Materials_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
            Req_Materials_ID = None
        finally:
            cur.close()
        
        if Req_Materials_ID:
            return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
        else:
            flash('ไม่พบค่า Req_Materials_ID', 'danger')
            return redirect(url_for('some_other_route'))  # Replace 'some_other_route' with an appropriate route
    return redirect(url_for('login'))


@app.route('/detailrequisitionform/<int:Req_Materials_ID>', methods=['GET', 'POST'])
def detailrequisitionform(Req_Materials_ID):
    if 'role' not in session:
        return redirect(url_for('login'))

    data = []
    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            requistion_materials.Req_Materials_ID as Reqid, 
            detail_materials.Detail_Materials_ID as detaiID, 
            detail_materials.CreatedDate as date, 
            detail_materials.Quantity as Quantity, 
            detail_materials.Materials_ID as materialsid, 
            materials.Materials_name as matename, 
            materials.Type as type, 
            user.Name as name, 
            user.Surname as surname,
            requistion_materials.Remark as remark,
            materials.materialsimg as img,
            user.Gender as gender,
            user.Telenumber as tele,
            user.Position as posi,
            user.address as address
        FROM requistion_materials
        LEFT JOIN detail_materials ON requistion_materials.Req_Materials_ID = detail_materials.Req_Materials_ID
        LEFT JOIN materials ON materials.Materials_ID = detail_materials.Materials_ID
        LEFT JOIN user ON user.User_ID = requistion_materials.User_ID
        WHERE requistion_materials.Req_Materials_ID = %s;
        '''
        cur.execute(query, (Req_Materials_ID,))
        data = cur.fetchall()
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {str(e)}", 'danger')
    finally:
        cur.close()

    if session['role'] == 'admin':
        return render_template('detailrequisitionform.html', data=data)
    elif session['role'] == 'user':
        return render_template('detailrequisitionform.html', data=data)
    else:
        return redirect(url_for('login'))

#การจัดการเบิกวัสดุ user*********************************************************************************************
@app.route('/requisitionuser')
def requisitionuser():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') not in ['admin', 'user']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    try:
        # Check if any materials need updating
        status = 'ยังไม่คืน'
        if status == 'ยังไม่คืน':
            # Update the materials quantity based on the status
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );
            ''')
            mysql.connection.commit()

            # Mark the detail materials as updated
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;
            ''')
            mysql.connection.commit()

        # Select the desired fields with the calculated total amount
        select_query = '''
        SELECT requistion_materials.Req_Materials_ID as reqid, requistion_materials.CreatedDate as date, requistion_materials.Remark as Remark, requistion_materials.status as status, user.User_ID as uid, user.Name as name, user.Surname as surname
        FROM requistion_materials
        LEFT JOIN user ON requistion_materials.User_ID = user.User_ID;
        '''
        cur.execute(select_query)
        data = cur.fetchall()

        cur.close()

        if session['role'] == 'admin':
            return render_template('Requi.html', data=data)
        elif session['role'] == 'user':
            return render_template('Requiuser.html', data=data)
    except Exception as e:
        # Rollback the transaction in case of an error
        mysql.connection.rollback()
        # Handle exceptions gracefully, e.g., log the error and redirect to an error page
        print(f"Error: {e}")
        return render_template('error.html', error="An error occurred while processing your request.")
    
    # If there's no exception and no redirection happened, redirect to login
    return redirect(url_for('login'))

@app.route('/requisitioninsertuser')
def requisitioninsertuser():
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('requisitionuser'))
    return render_template('requisitioninsertuser.html', users=users)

@app.route('/requisitioninsertdbu', methods=['POST'])
def requisitioninsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        status = request.form['status']
        userid = request.form['userid']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO requistion_materials (Req_Materials_ID  , CreatedDate, Remark, status, User_ID ) VALUES (%s, %s, %s, %s, %s)', (id, date,remark,status, userid))
        mysql.connection.commit()
        cur.close()
        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif 'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisitionuser" class="btn btn-primary">กลับหน้ารายการ</a>'

@app.route('/editrequisitionuser/<id>', methods=['GET'])
def editrequisitionuser(id):
    users = []  # เริ่มต้น users เป็นลิสต์ว่าง
    
    try:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT User_ID, Name, Surname FROM user")
        users = cur.fetchall() 
        cur.close()

    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('requisitionuser'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM requistion_materials WHERE Req_Materials_ID = %s', (id,))
    PD = cur.fetchone()
    cur.close()
    return render_template('updaterequisitionuser.html', PD=PD, users=users)

@app.route('/updaterequisitionuser', methods=['POST'])
def updaterequisitionuser():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        remark = request.form['remark']
        status = request.form['status']
        userid = request.form['User_ID']

        # อัพเดตข้อมูลในตาราง requistion_materials
        cur = mysql.connection.cursor()
        cur.execute('UPDATE requistion_materials SET CreatedDate = %s, Remark = %s, status = %s, User_ID = %s WHERE Req_Materials_ID = %s', 
                    (date, remark, status, userid, id))
        mysql.connection.commit()
        cur.close()

        if status == 'ยังไม่คืน':
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );
            ''')
            mysql.connection.commit()
            cur.close()
            
            # ทำเครื่องหมายว่าอัพเดตแล้ว
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;
            ''')
            mysql.connection.commit()
            cur.close()

        elif status == 'คืนเเล้ว':
            # Debugging logs
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity, dm.Quantity AS dm_qty, dm.Updated
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("Before Update:", row)
            cur.close()
            
            # Update materials quantity
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity + COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'คืนเเล้ว'
                    AND dm.Updated = 1
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'คืนเเล้ว'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 1
                );
            ''')
            mysql.connection.commit()
            
            # Debugging logs after update
            cur.execute('''
                SELECT mr.Materials_ID, mr.Quantity
                FROM materials mr
                INNER JOIN detail_materials dm ON dm.Materials_ID = mr.Materials_ID
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print("After Update:", row)
            cur.close()

            # Update detail_materials
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 2
                WHERE reqmater.status = 'คืนเเล้ว'
                AND dm.Updated = 1;
            ''')
            mysql.connection.commit()
            cur.close()

        if 'loggedin' in session and session['role'] == 'admin':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a>'
        elif 'loggedin' in session and session['role'] == 'user':
            return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisitionuser" class="btn btn-primary">กลับหน้ารายการ</a>' 



    

@app.route('/deleterequisitionuser/<int:id>', methods=['GET', 'POST'])
def deleterequisitionuser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM requistion_materials WHERE Req_Materials_ID = %s', (id,))
    mysql.connection.commit()
    cur.close()

    if 'loggedin' in session and session['role'] == 'admin':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisition" class="btn btn-primary">กลับหน้ารายการ</a>'
    elif 'loggedin' in session and session['role'] == 'user':
        return 'บันทึกข้อมูลเรียบร้อยแล้ว <a href="/requisitionuser" class="btn btn-primary">กลับหน้ารายการ</a>'

#detail requisition-----------------------------------------------------------------------------------------------------------
@app.route('/detailrequisitionuser/<int:Req_Materials_ID>', methods=['GET', 'POST'])
def detailrequisitionuser(Req_Materials_ID):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # ตรวจสอบสถานะของการเบิกวัสดุ
    status = None
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT status FROM requistion_materials WHERE Req_Materials_ID = %s', (Req_Materials_ID,))
        result = cur.fetchone()
        if result:
            status = result[0]
        cur.close()
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        return redirect(url_for('login'))

    if status == 'ยังไม่คืน':
        try:
            # อัพเดตจำนวนวัสดุ
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE materials mr
                SET Quantity = (
                    SELECT mr.Quantity - COALESCE(SUM(dm.Quantity), 0)
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE dm.Materials_ID = mr.Materials_ID
                    AND reqmater.status = 'ยังไม่คืน'
                    AND dm.Updated = 0
                )
                WHERE mr.Materials_ID IN (
                    SELECT DISTINCT dm.Materials_ID
                    FROM detail_materials dm
                    INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                    WHERE reqmater.status = 'ยังไม่คืน'
                    AND dm.CreatedDate > (SELECT MAX(CreatedDate) FROM materials WHERE Materials_ID = dm.Materials_ID)
                    AND dm.Updated = 0
                );''')
            mysql.connection.commit()
            cur.close()

            # ทำเครื่องหมายว่าอัพเดตแล้ว
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE detail_materials dm
                INNER JOIN requistion_materials reqmater ON reqmater.Req_Materials_ID = dm.Req_Materials_ID
                SET dm.Updated = 1
                WHERE reqmater.status = 'ยังไม่คืน'
                AND dm.Updated = 0;''')
            mysql.connection.commit()
            cur.close()
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาดในการอัพเดตข้อมูล: {e}", 'danger')
            return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        query = '''
        SELECT 
            requistion_materials.Req_Materials_ID as Reqid, 
            detail_materials.Detail_Materials_ID as detaiID, 
            detail_materials.CreatedDate as date, 
            detail_materials.Quantity as Quantity, 
            detail_materials.Materials_ID as materialsid, 
            materials.Materials_name as matename, 
            materials.Type as type, 
            user.Name as name, 
            user.Surname as surname,
            requistion_materials.Remark as remark,
            materials.materialsimg as img
        FROM requistion_materials
        LEFT JOIN detail_materials ON requistion_materials.Req_Materials_ID = detail_materials.Req_Materials_ID
        LEFT JOIN materials ON materials.Materials_ID = detail_materials.Materials_ID
        LEFT JOIN user ON user.User_ID = requistion_materials.User_ID
        WHERE requistion_materials.Req_Materials_ID = %s;
        '''
        cur.execute(query, (Req_Materials_ID,))
        data = cur.fetchall()
        cur.close()
    except MySQLdb.Error as e:
        flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        data = []

    if session['role'] == 'admin':
        return render_template('detailrequisition.html', data=data)
    elif session['role'] == 'user':
        return render_template('detailrequisitionuser.html', data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/detailrequisitioninsertuser/<int:Req_Materials_ID>', methods=['GET', 'POST'])
def detailrequisitioninsertuser(Req_Materials_ID):
    try:

        cur = mysql.connection.cursor()
        cur.execute("SELECT Materials_ID, Materials_name  FROM materials")
        material = cur.fetchall()  
        cur.close()
        
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูลผู้ใช้: {e}", 'danger')
        print("Error fetching users:", e)
        return redirect(url_for('detailrequisitioninsert/<int:Req_Materials_ID>'))
    return render_template('detailrequisitioninsertuser.html', Req_Materials_ID=Req_Materials_ID, material=material)

@app.route('/detailrequisitioninsertdbu', methods=['POST'])
def detailrequisitioninsertdbu():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        quantity = request.form['quantity']
        Req_Materials_ID = request.form['Req_Materials_ID']
        Materials_ID = request.form['Materials_ID']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO detail_materials (Detail_Materials_ID , CreatedDate, Quantity, Req_Materials_ID, Materials_ID) VALUES (%s, %s, %s, %s, %s)', (id, date, quantity, Req_Materials_ID, Materials_ID))
            mysql.connection.commit()
            flash('บันทึกข้อมูลเรียบร้อยแล้ว!', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()
    
        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailrequisitionuser', Req_Materials_ID=Req_Materials_ID))
    return redirect(url_for('login'))

@app.route('/editdetailrequisitionuser/<id>', methods=['GET'])
def editdetailrequisitionuser(id):
    try:
        # Fetch materials for the dropdown
        cur = mysql.connection.cursor()
        cur.execute("SELECT Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg FROM materials")
        materials = cur.fetchall()
        cur.close()

        # Fetch the detail for the specific requisition
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
        PD = cur.fetchone()
        cur.close()

        if PD:
            material_id = PD[4]  # Assuming Materials_ID is at index 4 in PD
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT Quantity, 
                    COALESCE(materialsimg, '') AS materialsimg, 
                    Type 
                FROM materials 
                WHERE Materials_ID = %s
            """, (material_id,))
            stock = cur.fetchone()
            cur.close()
            print(stock)
            # Append additional stock information to PD
            PD = list(PD) + [stock[0], stock[1], stock[2]]

        return render_template('updatedetailrequisitionuser.html', PD=PD, materials=materials,stock=stock)
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดขณะดึงข้อมูล: {e}", 'danger')
        return render_template('updatedetailrequisitionuser.html', PD=PD)

@app.route('/updatedetailrequisitionuser', methods=['POST'])
def updatedetailrequisitionuser():
    if 'loggedin' in session and request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        quantity = request.form['quantity']
        Req_Materials_ID = request.form['Req_Materials_ID']
        Materials_ID = request.form['Materials_ID']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE detail_materials SET CreatedDate = %s, Quantity = %s, Req_Materials_ID = %s, Materials_ID = %s WHERE Detail_Materials_ID = %s', (date, quantity, Req_Materials_ID, Materials_ID, id))
            mysql.connection.commit()
            flash('อัปเดตข้อมูลเรียบร้อยแล้ว', 'success')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
        finally:
            cur.close()

        if 'loggedin' in session:
            if session['role'] == 'admin':
                return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailrequisitionuser', Req_Materials_ID=Req_Materials_ID))
    return redirect(url_for('login'))


@app.route('/deletedetailrequisitionuser/<int:id>', methods=['GET', 'POST'])
def deletedetailrequisitionuser(id):
    if 'loggedin' in session:
        try:
            cur = mysql.connection.cursor()
            # ดึงค่า Req_Materials_ID ก่อนลบ
            cur.execute('SELECT Req_Materials_ID FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
            result = cur.fetchone()
            if result:
                Req_Materials_ID = result[0]
                # ลบข้อมูล
                cur.execute('DELETE FROM detail_materials WHERE Detail_Materials_ID = %s', (id,))
                mysql.connection.commit()
                flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
            else:
                flash('ไม่พบข้อมูลที่ต้องการลบ', 'danger')
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาด: {e}", 'danger')
            Req_Materials_ID = None
        finally:
            cur.close()
        if Req_Materials_ID:
            if session['role'] == 'admin':
                return redirect(url_for('detailrequisition', Req_Materials_ID=Req_Materials_ID))
            elif session['role'] == 'user':
                return redirect(url_for('detailrequisitionuser', Req_Materials_ID=Req_Materials_ID))
        else:
            return redirect(url_for('detailOrder'))
            
    return redirect(url_for('login'))


#ge#-------------------------------------------------------------------------------------------------------------
def generate_payid(pur_orderseller_id):
    timestamp = int(time.time())
    return f"{pur_orderseller_id}_{timestamp}"
#Geoof#-----------------------------------------------------------------------------------------------------------
#payment admin **************************************************************************************************
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'loggedin' in session:
        if request.method == 'POST':
            try:
                pur_orderseller_id = request.form.get('pur_orderseller_id')
                payid = generate_payid(pur_orderseller_id)
                payment_dt = request.form.get('payment_dt')
                bank = request.form.get('bank')
                payment_money = request.form.get('payment_money')
                payment_image = request.form.get('payment_image')
                status = request.form.get('status')

                # Insert the new payment record with the generated payid
                with mysql.connection.cursor() as cur:
                    insert_query = '''
                    INSERT INTO payment (
                        Payment_ID, PaymentDT, Bank, Payment_money, PaymentImage, Pur_Orderseller_ID, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                    '''
                    cur.execute(insert_query, (payid, payment_dt, bank, payment_money, payment_image, pur_orderseller_id, status))
                    mysql.connection.commit()

                flash('Payment added successfully!', 'success')
                return redirect(url_for('payment'))

            except MySQLdb.Error as e:
                mysql.connection.rollback()
                flash(f"เกิดข้อผิดพลาดในการเพิ่มข้อมูลการชำระเงิน: {e}", 'danger')
                return redirect(url_for('payment'))

        try:
            with mysql.connection.cursor() as cur:
                cur.execute('''
                    SELECT 
                        payment.Payment_ID as payid, 
                        payment.PaymentDT as paydate, 
                        payment.Bank as bank, 
                        payment.Payment_money as money,
                        payment.PaymentImage as payment_image,
                        payment.Pur_Orderseller_ID as purid,
                        payment.status as status,
                        purchaseseller.total as total,
                        customer.C_name as cname,
                        customer.C_surname as surc
                    FROM payment
                    LEFT JOIN purchaseseller ON payment.Pur_Orderseller_ID = purchaseseller.Pur_Orderseller_ID
                    LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
                    ORDER BY payment.Pur_Orderseller_ID;
                ''')
                data = cur.fetchall()

            role = session.get('role')
            if role == 'admin':
                return render_template('payment.html', data=data)
            elif role == 'user':
                return render_template('paymentuser.html', data=data)
            else:
                flash('ไม่พบบทบาทผู้ใช้งาน', 'danger')
                return redirect(url_for('login'))
        
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}", 'danger')
            return redirect(url_for('home'))
    else:
        flash('กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้', 'danger')
        return redirect(url_for('login'))

@app.route('/searchpay', methods=['GET'])
def searchpay():
    search_query = request.args.get('query', '')  # Set default value to an empty string if no query is found

    cursor = mysql.connection.cursor()
    try:
        query = """
        SELECT 
                payment.Payment_ID as payid, 
                payment.PaymentDT as paydate, 
                payment.Bank as bank, 
                payment.Payment_money as money,
                payment.PaymentImage as payment_image,
                payment.Pur_Orderseller_ID as purid,
                payment.status as status,
                purchaseseller.total as total,
                customer.C_name as cname,
                customer.C_surname as surc
            FROM payment
            LEFT JOIN purchaseseller ON payment.Pur_Orderseller_ID = purchaseseller.Pur_Orderseller_ID
            LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
            WHERE payment.Payment_ID LIKE %s OR customer.C_name = %s
            ORDER BY payment.Pur_Orderseller_ID;
        """
        cursor.execute(query, ('%' + search_query + '%', search_query))
        data = cursor.fetchall()
    except Exception as e:
        # Handle errors, such as showing a message or logging the error
        print(f"Error: {e}")
        data = []  # Set default value for data
    finally:
        cursor.close()

    # Check login status and return results based on user role
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'admin':
        return render_template('payment.html', data=data)
    elif session['role'] == 'user':
        return render_template('paymentuser.html', data=data)

    # Redirect to login or another page if the conditions above are not met
    return redirect(url_for('login'))


@app.route('/editpayment/<id>', methods=['GET'])
def editpayment(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute('''
            SELECT payment.Payment_ID, payment.Bank, payment.Payment_money,
                   payment.PaymentDT, payment.Remark, payment.PaymentImage,
                   payment.Pur_Orderseller_ID, purchaseseller.total AS total
            FROM payment
            LEFT JOIN purchaseseller ON purchaseseller.Pur_Orderseller_ID = payment.Pur_Orderseller_ID
            WHERE Payment_ID = %s
        ''', (id,))
        PD = cur.fetchone()
        cur.close()
        print(PD)
        return render_template('updatepayment.html', PD=PD)
    else:
        return redirect('/login')

@app.route('/updatepayment', methods=['POST'])
def updatepayment():
    if 'loggedin' in session:
        role = session.get('role')
        
        # ดึงข้อมูลจากฟอร์ม
        id = request.form.get('id')
        Bank = request.form.get('Bank')
        Payment_money = request.form.get('Payment_money')
        PaymentDT = request.form.get('PaymentDT')
        Remark = request.form.get('Remark')
        Pur_Orderseller_ID = request.form.get('Pur_Orderseller_ID')
        status = request.form.get('status')

        # ตรวจสอบว่ามีไฟล์หรือไม่
        if 'PaymentImage' in request.files:
            file = request.files['PaymentImage']
            if file.filename == '':
                return 'No selected file', 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_BANK'], filename)
                file.save(filepath)
                PaymentImage = filepath
            else:
                return 'Invalid file type', 400
        else:
            # อัปเดตฟิลด์ PaymentImage ในกรณีที่ไม่มีการอัปโหลดไฟล์
            PaymentImage = None

        try:
            cur = mysql.connection.cursor()

            # อัปเดตข้อมูลการชำระเงิน
            cur.execute('''
                UPDATE payment 
                SET Bank = %s, Payment_money = %s, PaymentDT = %s, Remark = %s, PaymentImage = %s, Pur_Orderseller_ID = %s, status = %s 
                WHERE Payment_ID = %s
            ''', (Bank, Payment_money, PaymentDT, Remark, PaymentImage, Pur_Orderseller_ID, status, id))
            mysql.connection.commit()

            if status == 'ชำระเเล้ว':
                # อัปเดตสต็อกสินค้า
                cur.execute('''
                    UPDATE productstore ps
                    SET Quantity = (
                        SELECT ps.Quantity - COALESCE(SUM(ds.quantity), 0)
                        FROM detailseller ds
                        INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                        INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                        WHERE ds.Productstore_ID = ps.Productstore_ID
                        AND p.status = 'ชำระเเล้ว'
                        AND ds.Updated = 0
                    )
                    WHERE ps.Productstore_ID IN (
                        SELECT DISTINCT ds.Productstore_ID
                        FROM detailseller ds
                        INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                        INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                        WHERE p.status = 'ชำระเเล้ว'
                        AND ds.CreatedDate > (SELECT MAX(CreatedDate) FROM productstore WHERE Productstore_ID = ds.Productstore_ID)
                        AND ds.Updated = 0
                    );
                ''')
                mysql.connection.commit()

                # ทำเครื่องหมายว่า details ถูกอัปเดตแล้ว
                cur.execute('''
                    UPDATE detailseller ds
                    INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                    INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                    SET ds.Updated = 1
                    WHERE p.status = 'ชำระเเล้ว'
                    AND ds.Updated = 0;
                ''')
                mysql.connection.commit()

            cur.close()

            # ตรวจสอบบทบาทและกำหนดเส้นทางการกลับ
            if role == 'admin':
                return redirect(url_for('payment'))
            elif role == 'user':
                return redirect(url_for('paymentuser'))

        except Exception as e:
            return str(e), 500
    
    return redirect(url_for('login'))
#payment user ***********************************************************************************************************   
@app.route('/paymentuser', methods=['GET', 'POST'])
def paymentuser():
    if 'loggedin' in session:
        if request.method == 'POST':
            try:
                pur_orderseller_id = request.form.get('pur_orderseller_id')
                payid = generate_payid(pur_orderseller_id)
                payment_dt = request.form.get('payment_dt')
                bank = request.form.get('bank')
                payment_money = request.form.get('payment_money')
                payment_image = request.form.get('payment_image')
                status = request.form.get('status')

                # Insert the new payment record with the generated payid
                with mysql.connection.cursor() as cur:
                    insert_query = '''
                    INSERT INTO payment (
                        Payment_ID, PaymentDT, Bank, Payment_money, PaymentImage, Pur_Orderseller_ID, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                    '''
                    cur.execute(insert_query, (payid, payment_dt, bank, payment_money, payment_image, pur_orderseller_id, status))
                    mysql.connection.commit()

                flash('Payment added successfully!', 'success')
                return redirect(url_for('payment'))

            except MySQLdb.Error as e:
                mysql.connection.rollback()
                flash(f"เกิดข้อผิดพลาดในการเพิ่มข้อมูลการชำระเงิน: {e}", 'danger')
                return redirect(url_for('payment'))

        try:
            with mysql.connection.cursor() as cur:
                cur.execute('''
                    SELECT 
                        payment.Payment_ID as payid, 
                        payment.PaymentDT as paydate, 
                        payment.Bank as bank, 
                        payment.Payment_money as money,
                        payment.PaymentImage as payment_image,
                        payment.Pur_Orderseller_ID as purid,
                        payment.status as status,
                        purchaseseller.total as total,
                        customer.C_name as cname,
                        customer.C_surname as surc
                    FROM payment
                    LEFT JOIN purchaseseller ON payment.Pur_Orderseller_ID = purchaseseller.Pur_Orderseller_ID
                    LEFT JOIN customer ON customer.Customer_ID = purchaseseller.Customer_ID
                    ORDER BY payment.Pur_Orderseller_ID;
                ''')
                data = cur.fetchall()

            role = session.get('role')
            if role == 'admin':
                return render_template('payment.html', data=data)
            elif role == 'user':
                return render_template('paymentuser.html', data=data)
            else:
                flash('ไม่พบบทบาทผู้ใช้งาน', 'danger')
                return redirect(url_for('login'))
        
        except MySQLdb.Error as e:
            flash(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}", 'danger')
            return redirect(url_for('home'))
    else:
        flash('กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้', 'danger')
        return redirect(url_for('login'))



@app.route('/editpaymentuser/<id>', methods=['GET'])
def editpaymentuser(id):
    if 'loggedin' in session and session['role'] == 'user':
        cur = mysql.connection.cursor()
        cur.execute('''
            SELECT payment.Payment_ID, payment.Bank, payment.Payment_money,
                   payment.PaymentDT, payment.Remark, payment.PaymentImage,
                   payment.Pur_Orderseller_ID, purchaseseller.total AS total
            FROM payment
            LEFT JOIN purchaseseller ON purchaseseller.Pur_Orderseller_ID = payment.Pur_Orderseller_ID
            WHERE Payment_ID = %s
        ''', (id,))
        PD = cur.fetchone()
        cur.close()
        print(PD)
        return render_template('updatepaymentuser.html', PD=PD)
    else:
        return redirect('/login')


@app.route('/updatepaymentuser', methods=['POST'])
def updatepaymentuser():
    if 'loggedin' in session:
        role = session.get('role')
        
        # ดึงข้อมูลจากฟอร์ม
        id = request.form.get('id')
        Bank = request.form.get('Bank')
        Payment_money = request.form.get('Payment_money')
        PaymentDT = request.form.get('PaymentDT')
        Remark = request.form.get('Remark')
        Pur_Orderseller_ID = request.form.get('Pur_Orderseller_ID')
        status = request.form.get('status')

        # ตรวจสอบว่ามีไฟล์หรือไม่
        if 'PaymentImage' in request.files:
            file = request.files['PaymentImage']
            if file.filename == '':
                return 'No selected file', 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_BANK'], filename)
                file.save(filepath)
                PaymentImage = filepath
            else:
                return 'Invalid file type', 400
        else:
            # อัปเดตฟิลด์ PaymentImage ในกรณีที่ไม่มีการอัปโหลดไฟล์
            PaymentImage = None

        try:
            cur = mysql.connection.cursor()

            # อัปเดตข้อมูลการชำระเงิน
            cur.execute('''
                UPDATE payment 
                SET Bank = %s, Payment_money = %s, PaymentDT = %s, Remark = %s, PaymentImage = %s, Pur_Orderseller_ID = %s, status = %s 
                WHERE Payment_ID = %s
            ''', (Bank, Payment_money, PaymentDT, Remark, PaymentImage, Pur_Orderseller_ID, status, id))
            mysql.connection.commit()

            if status == 'ชำระเเล้ว':
                # อัปเดตสต็อกสินค้า
                cur.execute('''
                    UPDATE productstore ps
                    SET Quantity = (
                        SELECT ps.Quantity - COALESCE(SUM(ds.quantity), 0)
                        FROM detailseller ds
                        INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                        INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                        WHERE ds.Productstore_ID = ps.Productstore_ID
                        AND p.status = 'ชำระเเล้ว'
                        AND ds.Updated = 0
                    )
                    WHERE ps.Productstore_ID IN (
                        SELECT DISTINCT ds.Productstore_ID
                        FROM detailseller ds
                        INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                        INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                        WHERE p.status = 'ชำระเเล้ว'
                        AND ds.CreatedDate > (SELECT MAX(CreatedDate) FROM productstore WHERE Productstore_ID = ds.Productstore_ID)
                        AND ds.Updated = 0
                    );
                ''')
                mysql.connection.commit()

                # ทำเครื่องหมายว่า details ถูกอัปเดตแล้ว
                cur.execute('''
                    UPDATE detailseller ds
                    INNER JOIN purchaseseller pseller ON pseller.Pur_Orderseller_ID = ds.Pur_Orderseller_ID
                    INNER JOIN payment p ON p.Pur_Orderseller_ID = pseller.Pur_Orderseller_ID
                    SET ds.Updated = 1
                    WHERE p.status = 'ชำระเเล้ว'
                    AND ds.Updated = 0;
                ''')
                mysql.connection.commit()

            cur.close()

            # ตรวจสอบบทบาทและกำหนดเส้นทางการกลับ
            if role == 'admin':
                return redirect(url_for('payment'))
            elif role == 'user':
                return redirect(url_for('paymentuser'))

        except Exception as e:
            return str(e), 500
    
    return redirect(url_for('login'))

#test mater add to cart#
@app.route('/api/materials1', methods=['GET'])
def get_materials1():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT Materials_ID, Materials_name, Type, Quantity, CreatedDate, materialsimg FROM materials')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        cur.close()
        return jsonify(data)
    else:
        return jsonify({"error": "Unauthorized"}), 401


#test mater add to cart#
@app.route('/api/checkout', methods=['POST'])
def checkout():
    if 'loggedin' in session:
        try:
            all_items = request.get_json()
            print("Received items:", all_items)
            
            cur = mysql.connection.cursor()

            # Insert into requistion_materials and get the last inserted Req_Materials_ID
            cur.execute(""" 
                INSERT INTO requistion_materials (CreatedDate, Remark, User_ID, status)
                VALUES (NOW(), %s, %s, 'ยังไม่คืน')
            """, ("Default Remark", session['User_ID']))

            req_materials_id = cur.lastrowid  # Use ID generated by AUTO_INCREMENT

            print("Req_Materials_ID:", req_materials_id)
            print("User_ID:", session['User_ID'])

            # Loop through the items and insert into detail_materials
            for item in all_items:
                material_id = item['product_id']
                quantity = item['quantity']

                print(f"Inserting into detail_materials: Req_Materials_ID: {req_materials_id}, Materials_ID: {material_id}, Quantity: {quantity}")

                cur.execute(""" 
                    INSERT INTO detail_materials (Req_Materials_ID, Materials_ID, Quantity, CreatedDate)
                    VALUES (%s, %s, %s, NOW())
                """, (req_materials_id, material_id, quantity))

                # Update the materials table to deduct the quantity
                print(f"Updating materials: Deduct Quantity - {quantity}, Materials_ID - {material_id}")

            mysql.connection.commit()
            cur.close()

            # Return the ID of the created requisition materials
            return jsonify({"message": "Request and details added successfully", "req_materials_id": req_materials_id}), 200
        except Exception as e:
            mysql.connection.rollback()
            print(f"Error during checkout: {str(e)}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized"}), 401



if (__name__ == "__main__"):
    app.run(debug=True)