from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, make_response
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
import pdfkit

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flask1'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

class RegisterForm(Form):
	panid = StringField('panid', [validators.Length(min=1, max=10)])
	firstname = StringField('firstname', [validators.Length(min=4, max=25)])
	adhaar = StringField('adhaar',[validators.Length(min=1, max= 12)])
	email = StringField('email', [validators.Length(min=6, max=50)])
	password = PasswordField('password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

'''@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
       login()
       render_template('home.html')
    return render_template('index.html')'''


@app.route('/index2.html',methods=['GET','POST'])
def index2():
    render_template('index2.html')
    form = RegisterForm(request.form)
    register()
    return render_template('index2.html',form = form)


@app.route('/invoice.html',methods=['GET','POST'])
def invoice():
    cur  = mysql.connection.cursor()
    #cur.execute("SELECT * FROM user WHERE panid = %s", panid)
    result = cur.execute("SELECT * FROM user WHERE panid = %s", [rc_panid])
    print(rc_panid)
    if(result > 0):
        #data = cur.fetchone
        cur.execute("SELECT * FROM salary_details WHERE rc_panid = %s",[rc_panid])
        data = cur.fetchone()
        rc_a_basic_salary = data['rc_a_basic_salary']
        rc_hra = data['rc_hra']
        rc_rent_paid  = data['rc_rent_paid']
        rc_spa = data['rc_spa']
        rc_LTA = data['rc_LTA']
        rc_expense = data['rc_expense']
        rc_taxable_hra = data['rc_taxable_hra']
        rc_gross_income_sal  = data['rc_gross_income_sal']
        #return render_template('invoice.html', )
        cur.execute("SELECT * FROM interest WHERE rc_panid = %s", [rc_panid])
        data = cur.fetchone()
        rc_interest = data['rc_interest']
        rc_fda = data['rc_fda']

        #cur.execute("SELECT * FROM deductions WHERE rc_panid = %s", [rc_panid])
        #data = cur.fetchone()
        #rc_fda = data['fda']
        cur.execute("SELECT * FROM other_sources WHERE rc_panid =%s",[rc_panid])
        data = cur.fetchone()
        rc_agr = data['rc_agr']
        rc_gifts = data['rc_gifts']
        #rc_other_sources = other_sources
        #rc_gross_income = gross_income
        cur.execute("SELECT * FROM deductions WHERE rc_panid = %s", [rc_panid])
        data = cur.fetchone()
        rc_ppf = data['rc_ppf']
        rc_epf = data['rc_epf'] 
        rc_elss = data['rc_elss']
        rc_lip = data['rc_lip']
        rc_mip1 = data['rc_mip1']
        rc_mip2 = data['rc_mip2']
        rc_fees = data['rc_fees']
        rc_nps = data['rc_nps']
        rc_don = data['rc_don']

        cur.execute("SELECT * FROM tax_details WHERE rc_panid = %s", [rc_panid])
        data = cur.fetchone()
        rc_gross_income = data['rc_gross_income']
        rc_total_deductions = data['rc_total_deductions']
        rc_taxable_income = data['rc_taxable_income']
        rc_tax_liable = data['rc_tax_liable']

        cur.close()




    
    if request.method == 'POST':
        rendered = render_template('invoice.html',rc_a_basic_salary = rc_a_basic_salary, rc_hra = rc_hra, rc_rent_paid = rc_rent_paid, rc_spa = rc_spa, rc_LTA= rc_LTA, rc_expense= rc_expense, rc_taxable_hra=rc_taxable_hra, rc_gross_income_sal=rc_gross_income_sal, rc_interest=rc_interest, rc_fda=rc_fda, rc_agr= rc_agr, rc_gifts= rc_gifts, rc_gross_income=rc_gross_income, rc_ppf=rc_ppf, rc_epf=rc_epf, rc_elss=rc_elss, rc_lip=rc_lip, rc_mip1=rc_mip1, rc_mip2=rc_mip2, rc_fees=rc_fees, rc_nps=rc_nps, rc_don=rc_don, rc_total_deductions= rc_total_deductions, rc_taxable_income=rc_taxable_income, rc_tax_liable=rc_tax_liable)
        pdf = pdfkit.from_string(rendered,False) 
        response = make_response(pdf)
        response.headers['Content-Type'] = 'applcation/pdf'
        response.headers['Content-Disposition'] = 'inline; filename = invoice.pdf'
        return response
    return render_template('invoice.html',rc_a_basic_salary = rc_a_basic_salary, rc_hra = rc_hra, rc_rent_paid = rc_rent_paid, rc_spa = rc_spa, rc_LTA= rc_LTA, rc_expense= rc_expense, rc_taxable_hra=rc_taxable_hra, rc_gross_income_sal=rc_gross_income_sal, rc_interest=rc_interest, rc_fda=rc_fda, rc_agr= rc_agr, rc_gifts= rc_gifts, rc_gross_income=rc_gross_income, rc_ppf=rc_ppf, rc_epf=rc_epf, rc_elss=rc_elss, rc_lip=rc_lip, rc_mip1=rc_mip1, rc_mip2=rc_mip2, rc_fees=rc_fees, rc_nps=rc_nps, rc_don=rc_don, rc_total_deductions= rc_total_deductions, rc_taxable_income=rc_taxable_income, rc_tax_liable=rc_tax_liable)


@app.route('/',methods=['GET','POST'])
def home_start():
    if request.method =='POST':
        return redirect(url_for('index'))
    return render_template('home_start.html')

@app.route('/home.html',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('home_start.html',dt_string = dt_string)
    return render_template('home.html')

# User Register
@app.route('/index2.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        panid = form.panid.data
        email = form.email.data
        name = form.firstname.data
        adhaar = form.adhaar.data
        password = form.password.data

		# Create cursor
        cur = mysql.connection.cursor()

		# Execute query
        cur.execute("INSERT INTO user(panid,  password) VALUES(%s, %s)", (panid, password))
        cur.execute("INSERT INTO user_inform(adhaar,panid,name,email) VALUES(%s, %s, %s, %s)", (adhaar, panid, name, email))
		# Commit to DB
        mysql.connection.commit()

		# Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        #login()
        #flag = 1;
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

def summary(city, sex, age, a_basic_salary, hra, rent_paid, spa, LTA, expense, taxable_hra, gross_income_sal, interest, fda, agr, gifts, other_sources, gross_income, ppf, epf, elss, lip, mip1, mip2,fees, nps, don, total_deductions, taxable_income, tax_liable):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM salary_details");
    cur.execute("DELETE FROM interest")
    cur.execute("DELETE FROM deductions")
    cur.execute("DELETE FROM tax_details")
    #cur.close()
    global rc_a_basic_salary, rc_hra, rc_rent_paid, rc_spa, rc_LTA, rc_expense, rc_taxable_hra, rc_gross_income_sal, rc_interest, rc_fda, rc_agr, rc_gifts, rc_other_sources, rc_gross_income, rc_ppf, rc_epf, rc_elss, rc_lip, rc_mip1, rc_mip2, rc_fees, rc_fees, rc_nps, rc_don, rc_total_deductions, rc_taxable_income, rc_tax_liable
    rc_a_basic_salary = a_basic_salary
    rc_hra = hra
    rc_rent_paid = rent_paid
    rc_spa = spa
    rc_LTA = LTA
    rc_expense = expense
    rc_taxable_hra = taxable_hra
    rc_gross_income_sal = gross_income_sal
    cur.execute("INSERT INTO salary_details(rc_panid, rc_a_basic_salary,rc_hra, rc_rent_paid, rc_spa, rc_LTA, rc_expense, rc_taxable_hra, rc_gross_income_sal) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(rc_panid, rc_a_basic_salary,rc_hra, rc_rent_paid, rc_spa, rc_LTA, rc_expense, rc_taxable_hra,rc_gross_income_sal))
    rc_interest =interest
    rc_fda = fda
    cur.execute("INSERT INTO interest(rc_panid, rc_interest, rc_fda) VALUES (%s, %s, %s)", (rc_panid, rc_interest, rc_fda))
    rc_agr = agr
    rc_gifts = gifts
    rc_other_sources =other_sources
    cur.execute("INSERT INTO other_sources(rc_panid, rc_agr, rc_gifts) VALUES (%s, %s, %s)", (rc_panid, rc_agr, rc_gifts))
    rc_gross_income = gross_income
    rc_ppf = ppf
    rc_epf =epf 
    rc_elss = elss
    rc_lip = lip
    rc_mip1 = mip1
    rc_mip2 = mip2
    rc_fees = fees
    rc_nps = nps
    rc_don = don
    cur.execute("INSERT INTO deductions(rc_panid, rc_ppf, rc_epf, rc_elss, rc_lip, rc_mip1, rc_mip2, rc_fees, rc_nps, rc_don) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (rc_panid, rc_ppf, rc_epf, rc_elss, rc_lip, rc_mip1, rc_mip2, rc_fees, rc_nps, rc_don))
    rc_total_deductions = total_deductions
    rc_taxable_income = taxable_income
    rc_tax_liable = tax_liable
    cur.execute("INSERT INTO tax_details(rc_panid, rc_total_deductions, rc_taxable_income, rc_tax_liable) VALUES(%s, %s, %s, %s)", (rc_panid, rc_total_deductions, rc_taxable_income, rc_tax_liable))
    mysql.connection.commit()
    cur.close()
    #render_template('invoice.html',rc_a_basic_salary = rc_a_basic_salary, rc_hra = rc_hra, rc_rent_paid = rc_rent_paid, rc_spa = rc_spa, rc_LTA= rc_LTA, rc_expense= rc_expense, rc_taxable_hra=rc_taxable_hra, rc_gross_income_sal=rc_gross_income_sal, rc_interest=rc_interest, rc_fda=rc_fda, rc_agr= rc_agr, rc_gifts= rc_gifts, rc_other_sources = rc_other_sources, rc_gross_income=rc_gross_income, rc_ppf=rc_ppf, rc_epf=rc_epf, rc_elss=rc_elss, rc_lip=rc_lip, rc_mip1=rc_mip1, rc_mip2=rc_mip2, rc_fees=rc_fees, rc_nps=rc_nps, rc_don=rc_don, rc_total_deductions= rc_total_deductions, rc_taxable_income=rc_taxable_income, rc_tax_liable=rc_tax_liable)

def tax_calculator(taxable_income):
	temp_income = taxable_income
	liable = 0;
	slab_range = 250000;
	n = int(temp_income / slab_range)
	if(n <= 0):
		return 0
	percentage = 0;
	for i in range(n):
		liable += slab_range * (percentage / 100)
		temp_income = temp_income - slab_range;
		percentage = percentage + 5;
		if(temp_income < slab_range):
			break;
	liable += temp_income * (percentage / 100)
	liable = liable + (liable * 0.04)
	return liable 

def gross_income_calculator(gross_income_sal, interest, other_sources):
	return gross_income_sal + interest + other_sources

def  total_deduction_calculator(ppf,epf,elss,lip,mip1,mip2,fees,nps,don,interest,fda):
	self_health = mip1;
	parents = mip2;
	d_80c = ppf+epf+elss
	d_80tta = interest
	d_80u = fees
	if(mip1 > 25000):
		self_health = 25000
	if(mip2 > 50000):
		parents = 50000
	if(d_80c > 150000):
		d_80c = 150000
	if(d_80tta > 10000):
		d_80tta = 10000
	if(fees > 150000):
		d_80u = 150000
	return d_80tta + d_80c + parents + self_health + d_80u + don + nps + fda

def gross_income_from_sal(a_basic_salary, LTA, expense, spa, std_deduction,taxable_hra):
	taxable_lta = (LTA - expense)
	if(taxable_lta < 0):
		taxable_lta = 0             #if bill amount is exceding LTA then taxable LTA should be 0
	return a_basic_salary + taxable_hra + spa + taxable_lta - std_deduction;


def taxable_hra_calc(city,a_basic_salary, hra, rent_paid):
	result = hra;   
	if(city == "Metro" or city == "metro"):     
		half_ab = a_basic_salary * 0.5
	else:
		half_ab = a_basic_salary * 0.4
	ten_ab = a_basic_salary * 0.1
	excess_rent = rent_paid - ten_ab
	if(excess_rent < half_ab):
		result = hra - excess_rent
	else:
		result = hra - half_ab
	if(result > 0):
		return result
	else:   
		return 0 

#ButtonPressed = 0
@app.route('/main.html',methods=['GET','POST'])
def dashboard():
	std_deduction = float("50000")
	if request.method == 'POST':
		city = request.form['city']
		sex = request.form['sex']
		age = request.form['age']
		#INCOME FROM SALARY
		a_basic_salary = float(request.form['salary'])
		hra = float(request.form['hra'])
		rent_paid = float(request.form['rent'])
		spa = float(request.form['spa'])
		LTA = float(request.form['lta'])
		expense = float(request.form['exp'])
		taxable_hra=taxable_hra_calc(city,a_basic_salary,hra,rent_paid)
		gross_income_sal = gross_income_from_sal(a_basic_salary, LTA, expense, spa, std_deduction,taxable_hra)
		#INCOME FROM OTHER SOURCES
		interest = float(request.form['interest']) #interest from savings account
		fda = float(request.form['fda']) #interest on FD Account 
		agr = float(request.form['agr'])
		gifts = float(request.form['gifts'])
		other_sources = fda + agr + gifts
		gross_income = gross_income_calculator(gross_income_sal,interest,other_sources)


		#DEDUCTIONS
		ppf = float(request.form['ppf']) 
		epf = float(request.form['epf']) 
		elss = float(request.form['elss'])
		lip = float(request.form['lip']) #life insurance premium
		mip1 = float(request.form['mip1']) #medical insurance premium for self and family
		mip2 = float(request.form['mip2']) #medical insurance premium for parents
		fees = float(request.form['fees'])
		nps = float(request.form['nps'])
		don = float(request.form['don'])
		total_deductions = total_deduction_calculator(ppf,epf,elss,lip,mip1,mip2,fees,nps,don,interest,fda)

		taxable_income = gross_income - total_deductions

		tax_liable = tax_calculator(taxable_income)

		#atd = float(request.form['atd'])
		#tds = float(request.form['tds'])
		#tcs = float(request.form['tcs'])
		#sat = float(request.form['sat'])

		#tax_already_paid = atd + tds + tcs + sat

		#income_tax_payable = tax_liable - tax_already_paid
        #summary(city, sex, age, a_basic_salary, hra, rent_paid, spa, LTA, expense, taxable_hra, gross_income_sal, interest, fda, agr, gifts, other_sources, gross_income, ppf, epf, elss, lip, mip1, mip2,fees, nps, don, total_deductions, taxable_income, tax_liable)

		return render_template('final1.html',taxable_hra = taxable_hra, gross_income_sal = gross_income_sal, gross_income = gross_income, total_deductions = total_deductions, taxable_income = taxable_income, tax_liable = tax_liable)

		# I think you want to increment, that case ButtonPressed will be plus 1
	return render_template('main.html')

@app.route('/main2.html', methods=['GET','POST'])
def main2():
    global now, dt_string,taxable_hra, gross_income_sal,gross_income,total_deductions,taxable_income,tax_liable
    std_deduction = float("50000")
    if request.method == 'POST':
        city = request.form['city']
        sex = request.form['sex']
        age = request.form['age']
        #INCOME FROM SALARY
        a_basic_salary = float(request.form['salary'])
        hra = float(request.form['hra'])
        rent_paid = float(request.form['rent'])
        spa = float(request.form['spa'])
        LTA = float(request.form['lta'])
        expense = float(request.form['exp'])
        taxable_hra=taxable_hra_calc(city,a_basic_salary,hra,rent_paid)
        gross_income_sal = gross_income_from_sal(a_basic_salary, LTA, expense, spa, std_deduction,taxable_hra)
        #INCOME FROM OTHER SOURCES
        interest = float(request.form['interest']) #interest from savings account
        fda = float(request.form['fda']) #interest on FD Account 
        agr = float(request.form['agr'])
        gifts = float(request.form['gifts'])
        other_sources = fda + agr + gifts
        gross_income = gross_income_calculator(gross_income_sal,interest,other_sources)


        #DEDUCTIONS
        ppf = float(request.form['ppf']) 
        epf = float(request.form['epf']) 
        elss = float(request.form['elss'])
        lip = float(request.form['lip']) #life insurance premium
        mip1 = float(request.form['mip1']) #medical insurance premium for self and family
        mip2 = float(request.form['mip2']) #medical insurance premium for parents
        fees = float(request.form['fees'])
        nps = float(request.form['nps'])
        don = float(request.form['don'])
        total_deductions = total_deduction_calculator(ppf,epf,elss,lip,mip1,mip2,fees,nps,don,interest,fda)

        taxable_income = gross_income - total_deductions

        tax_liable = tax_calculator(taxable_income)

        #atd = float(request.form['atd'])
        #tds = float(request.form['tds'])
        #tcs = float(request.form['tcs'])
        #sat = float(request.form['sat'])

        #tax_already_paid = atd + tds + tcs + sat

        #income_tax_payable = tax_liable - tax_already_paid
        summary(city, sex, age, a_basic_salary, hra, rent_paid, spa, LTA, expense, taxable_hra, gross_income_sal, interest, fda, agr, gifts, other_sources, gross_income, ppf, epf, elss, lip, mip1, mip2,fees, nps, don, total_deductions, taxable_income, tax_liable)
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #render_template('invoice.html',rc_a_basic_salary = rc_a_basic_salary, rc_hra = rc_hra, rc_rent_paid = rc_rent_paid, rc_spa = rc_spa, rc_LTA= rc_LTA, rc_expense= rc_expense, rc_taxable_hra=rc_taxable_hra, rc_gross_income_sal=rc_gross_income_sal, rc_interest=rc_interest, rc_fda=rc_fda, rc_agr= rc_agr, rc_gifts= rc_gifts, rc_other_sources = rc_other_sources, rc_gross_income=rc_gross_income, rc_ppf=rc_ppf, rc_epf=rc_epf, rc_elss=rc_elss, rc_lip=rc_lip, rc_mip1=rc_mip1, rc_mip2=rc_mip2, rc_fees=rc_fees, rc_nps=rc_nps, rc_don=rc_don, rc_total_deductions= rc_total_deductions, rc_taxable_income=rc_taxable_income, rc_tax_liable=rc_tax_liable)
        
        #render_template('final2.html',taxable_hra = taxable_hra, gross_income_sal = gross_income_sal, gross_income = gross_income, total_deductions = total_deductions, taxable_income = taxable_income, tax_liable = tax_liable)
        return redirect((url_for('final2')))
        # I think you want to increment, that case ButtonPressed will be plus 1
    return render_template('main2.html')

@app.route('/final2.html', methods = ['GET','POST'])
def final2():
    if request.method == 'POST':
        return render_template('home.html') 
    return render_template('final2.html',taxable_hra = taxable_hra, gross_income_sal = gross_income_sal, gross_income = gross_income, total_deductions = total_deductions, taxable_income = taxable_income, tax_liable = tax_liable)


# User login
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    global rc_panid;
    if request.method == 'POST':
		# Get Form Fields
        panid = request.form['login-panid']
        password_candidate = request.form['login-password']
        print("Candidate Passsword")
        print(password_candidate)

		# Create cursor
        cur = mysql.connection.cursor()

		# Get user by username
        result = cur.execute("SELECT * FROM user WHERE panid = %s", [panid])
        print(result)
        if result > 0:
            rc_panid = panid
			# Get stored hash
            data = cur.fetchone()
            password = data['password']
            panid = data['panid']
            print(password)
			# Compare Passwords
            if (password_candidate == password) and request.method == 'POST':
                print("passwords matched")
				# Passed
                session['logged_in'] = True
                session['panid'] = panid

                flash('You are now logged in', 'success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid login'
                return render_template('index.html', error=error)
			# Close connection
            cur.close()
        else:
            error = 'PAN ID not registered'
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)


    from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string) 
