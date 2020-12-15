from warnings import catch_warnings
from flask import Blueprint,render_template
from flask.globals import request
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import UserAgentMixin
from models import User,db
from flask_login import login_user,logout_user,login_required
from Encrypt import Encryt

auth = Blueprint('auth',__name__)


@auth.route('/Etchguard')
def index():
    try:
        logout_user()
    except:
        pass
    return render_template('/Etchguard.html')



@auth.route('/login')
def login():
    try:
        logout_user()
    except:
        pass
    return render_template('Login.html')
   
@auth.route('/login', methods=['POST'])
def login_post():
    email=request.form.get('email')
    fpassword=request.form.get('fpassword')
    
    if email == "" or fpassword == "":
        flash("Please Fill Out All the Feilds")
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first()
    if user != None:
        if check_password_hash(user.password,fpassword):
            login_user(user)
            return redirect(url_for('main.passwords'))
        else:
            flash("Username or Password Incorrect")
            return redirect(url_for('auth.login'))
    else:
        flash("User Does Not Exist. Please Register First.")
        return redirect(url_for('auth.login'))

   
@auth.route('/register')
def register():
    try:
        logout_user()
    except:
        pass
    return render_template('Register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    tpassword=request.form.get('tpassword')
    hint=request.form.get('hint')
    print(email)
    if name==""  or email == "" or password == "" or tpassword =="" or hint=="":
        flash("Please Fill Out All the Feilds")
        return redirect(url_for('auth.register'))
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email Already exists")
        return redirect(url_for('auth.register'))

    if password==tpassword:

        if hint!=password:
            from strength import strong
            if strong(password) == "Strong" or strong(password)  == "Moderate":
                new_user= User(email=email,name=name,hint=hint,password=generate_password_hash(password,method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash(f"This is the only password you might have to remember please make it strong. The Password now is { strong(password).upper() }!!")
                return redirect(url_for('auth.register'))

        else:
            flash("Hint and Password Cannot be Same")
            return redirect(url_for('auth.register'))
    else:
        flash("Passwords Do Not Match")
        return redirect(url_for('auth.register'))




@auth.route('/howitworks')
@auth.route('/Etchguard.html')
@login_required
def howitworks():
    logout_user()
    return render_template('howitworks.html')


@auth.route('/forgotpass',methods=['GET','POST'])
def forgotpass():
    try:
        logout_user()
    except:
        pass
   
    if request.method == "POST":
        try:
            logout_user()
        except:
            pass
       
        from sendemail import send_mail
        email=request.form.get('femail')
        user = User.query.filter_by(email=email).first()
  
        if user != None:
    
            a=send_mail(email,user.hint)
            flash(a)
            return redirect(url_for('auth.index'))
        else:

            flash("Email Does'nt Exist.")
            return redirect(url_for('auth.forgotpass'))   

    return render_template('forgotpass.html')


@auth.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return render_template('Etchguard.html')