from datetime import time
from os import name
from typing import get_type_hints
from flask import Blueprint, app,render_template,request,flash
from flask.helpers import url_for
from flask_login import login_required,current_user
import flask_login
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from dbhandler import sqlitedb, writecards ,writetodb,writenote
from Decrypt import Decrypt
from Encrypt import Encryt
from generaterandom import generate_password as r
from pwned import check_leak
main = Blueprint('main',__name__)



@main.route('/')
def index():
    return render_template('Etchguard.html')


@main.route('/passwords')
@login_required
def passwords():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    try:
        d=Decrypt(username,password)
        d.decrypt_vault(nameenc,namedb)
        a=sqlitedb(namedb)
        data=a.readfromdb()
        e = Encryt(username,password)
        e.encrypt_vault(name,namedb)
        return render_template('passwords.html',data=data,random=r())
    except Exception as e:
        print(e)
        flash("No Passwords Currently Present. Add A Password to View!!")
        return redirect(url_for('main.addpass'))


@main.route('/notes')
@login_required
def notes():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    try:
        d=Decrypt(username,password)
        d.decrypt_vault(nameenc,namedb)
        a=sqlitedb(namedb)
        data=a.readfromnotes()
        e = Encryt(username,password)
        e.encrypt_vault(name,namedb)
        return render_template('notes.html',data=data,random=r())
    except:
        flash("No Notes Currently Present. Add A Note to View!!")
        return redirect(url_for('main.addnotes'))

@main.route('/cards')
@login_required
def cards():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    try:
        d=Decrypt(username,password)
        d.decrypt_vault(nameenc,namedb)
        a=sqlitedb(namedb)
        data=a.readfromcards()
        e = Encryt(username,password)
        e.encrypt_vault(name,namedb)
        return render_template('cards.html',data=data,random=r())
    except:
        flash("No Cards Currently Present. Add A Card to View!!")
        return redirect(url_for('main.addcards'))



@main.route('/addpasswords' ,methods=['GET','POST'])
@login_required
def addpass():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    if request.method == "POST":
        appname=request.form.get('add_app-name')
        addemail=request.form.get('add_email')
        addpassword=request.form.get('add_password')
        if appname != "" and addemail != "" and addpassword != "":
            name=gname+hint
            namedb=gname+hint+".db"
            nameenc=gname+hint+".enc"
            try:
                d=Decrypt(username,password)
                d.decrypt_vault(nameenc,namedb)
            except:
                pass
            nname=gname+hint+".db"
            a=writetodb(nname)
            a.newwrite(appname,addemail,addpassword,"0")
            e = Encryt(username,password)
            e.encrypt_vault(name,namedb)
            return redirect (url_for('main.passwords'))
        else:
            flash("Please Fill Out All Feilds.") 
            return redirect(url_for('addpass',random=r()))     
    return render_template('addpasswords.html',random=r())

@main.route('/editpassword',methods=['GET','POST'])
@login_required
def editpassword():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"

    if request.method=="POST":
        oldappname=request.form.get('old_app-name')
        oldemail=request.form.get('old_email')
        appname=request.form.get('add_app-name')
        uemail=request.form.get('add_email')
        upassword=request.form.get('add_password')
        
        if request.form.get('save') != None:
            if oldappname != "" and oldemail != "" and appname != "" and uemail != "" and upassword != "":
                try:
                    d=Decrypt(username,password)
                    d.decrypt_vault(nameenc,namedb)
                except:
                    pass
                a=writetodb(namedb)
                if a.update(appname,uemail,upassword,"0",oldappname,oldemail) == 0:
                    e = Encryt(username,password)
                    e.encrypt_vault(name,namedb)
                    flash("The App Name or UserName Specified Doesnot Exist.")
                    return redirect (url_for('main.editpassword',random=r()))
                e = Encryt(username,password)
                e.encrypt_vault(name,namedb)
                flash("Updated Succesfully.")
                return redirect (url_for('main.passwords'))
            else:
                flash("Please Specify All The Feilds")
                return redirect (url_for('main.editpassword',random =r()))
        elif request.form.get('delete') !=None:
            if oldappname != "" and oldemail != "":
                d=Decrypt(username,password)
                d.decrypt_vault(nameenc,namedb)
                a=writetodb(namedb)
                if a.delete(oldappname,oldemail) == 0:
                    e = Encryt(username,password)
                    e.encrypt_vault(name,namedb)
             
                    flash("The App Name or UserName Specified Does'nt Exist.")
                    return redirect (url_for('main.editpassword',random=r()))

                e = Encryt(username,password)
                e.encrypt_vault(name,namedb)
                flash("Deleted Succesfully.")
                return redirect (url_for('main.passwords'))
            else:
              
                flash("To Delete Please Fill Specify The First Two Feilds.")
                return redirect (url_for('main.editpassword',random=r()))
        else:
            flash("An unknown error occured!.")
            return redirect (url_for('main.passwords'))
    return render_template('editpassword.html',random=r())

@main.route('/addnotes',methods=['GET','POST'])
@login_required
def addnotes():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    if request.method=="POST":
        title=request.form.get('notetitle')
        note=request.form.get('note')
        if title!="" and note!="":
            try:
                d=Decrypt(username,password)
                d.decrypt_vault(nameenc,namedb)
            except:
                pass
            w=writenote(namedb)
            w.newwrite(title,note)
            e = Encryt(username,password)
            e.encrypt_vault(name,namedb)
            flash("Noted Succesfully.")
            return redirect (url_for('main.passwords'))
        else:
            flash("Fill Out All The Feilds.")
            return redirect (url_for('main.addnotes'))
    return render_template('/addnotes.html')

@main.route('/addcards',methods=['GET','POST'])
@login_required
def addcards():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    if request.method=="POST":
        cname=request.form.get('card_name')
        ctype=request.form.get('type')
        cnum=request.form.get('cardnumber')
        ccode=request.form.get('security_code')
        csd=request.form.get('startdate')
        ced=request.form.get('enddate')
        if cname!="" and ctype!="" and cnum!="" and ccode!="" and csd!="" and ced!="":

            try:
                d=Decrypt(username,password)
                d.decrypt_vault(nameenc,namedb)
            except:
                pass
            w=writecards(namedb)
            w.newwrite(cname,ctype,cnum,ccode,csd,ced)
            e = Encryt(username,password)
            
            e.encrypt_vault(name,namedb)
            flash("Card Added Succesfully.")
            return redirect (url_for('main.passwords'))
        else:
            flash("Fill Out All The Feilds.")
            return redirect (url_for('main.addcards'))
    return render_template('/addcards.html')

@main.route('/drkweb',methods=['GET','POST'])
@login_required
def drkweb():
    user=flask_login.current_user
    gname=user.name
    hint=user.hint
    username=user.email
    password=user.password
    name=gname+hint
    namedb=gname+hint+".db"
    nameenc=gname+hint+".enc"
    try:
        d=Decrypt(username,password)
        d.decrypt_vault(nameenc,namedb)
        a=sqlitedb(namedb)
        data=a.readfromdb()
        e = Encryt(username,password)
        e.encrypt_vault(name,namedb)
        x=[]
        for i in data:
            x.append([check_leak(i[2]),i[1],i[0],i[2]])
        return render_template('drkweb.html',data=x)
    except Exception as e:
        print(e)
        flash("No Passwords Currently Present. Add A Password to Check!!")
        return redirect(url_for('main.addpass'))
    




