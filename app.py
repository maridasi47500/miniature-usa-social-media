from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,country_id,phone) values (:username,:email,:password,:country_id,:phone)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','country_id','phone']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','country_id','phone']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','country_id','phone']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_influencer_country_identity", methods=["GET","POST"])
def add_one_influencer_country_identity():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into influencer_country_identity (name,identity_type,country_id) values (:name,:identity_type,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from influencer_country_identity')


        return render_template("influencer_country_identityform.html", influencer_country_identitys=user, one_user=one_user, the_title="add new influencer_country_identity", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from influencer_country_identity')
    one_user = query_db("select * from influencer_country_identity limit 1", one=True)
    return render_template("influencer_country_identityform.html", influencer_country_identitys=user, one_user=one_user, the_title="add new influencer_country_identity", touslescountry=touslescountry)

@app.route("/add_one_copy_country_trend", methods=["GET","POST"])
def add_one_copy_country_trend():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        touslesinfluencer_countryentity= query_db("select * from influencer_countryentity")

        one_user = query_db("insert into copy_country_trend (country_id,influencer_country_identity_id) values (:country_id,:influencer_country_identity_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from copy_country_trend')


        return render_template("copy_country_trendform.html", copy_country_trends=user, one_user=one_user, the_title="add new copy_country_trend", touslescountry=touslescountry, touslesinfluencer_countryentity=touslesinfluencer_countryentity)


    touslescountry= query_db("select * from country")

    touslesinfluencer_countryentity= query_db("select * from influencer_countryentity")

    user = query_db('select * from copy_country_trend')
    one_user = query_db("select * from copy_country_trend limit 1", one=True)
    return render_template("copy_country_trendform.html", copy_country_trends=user, one_user=one_user, the_title="add new copy_country_trend", touslescountry=touslescountry, touslesinfluencer_countryentity=touslesinfluencer_countryentity)

@app.route("/add_one_socialmedia", methods=["GET","POST"])
def add_one_socialmedia():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into socialmedia (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from socialmedia')


        return render_template("socialmediaform.html", socialmedias=user, one_user=one_user, the_title="add new socialmedia")


    user = query_db('select * from socialmedia')
    one_user = query_db("select * from socialmedia limit 1", one=True)
    return render_template("socialmediaform.html", socialmedias=user, one_user=one_user, the_title="add new socialmedia")

@app.route("/add_one_carteajouer", methods=["GET","POST"])
def add_one_carteajouer():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslessocialmedia= query_db("select * from socialmedia")

        touslesuser= query_db("select * from user")

        touslescopy_country_trend= query_db("select * from copy_country_trend")

        one_user = query_db("insert into carteajouer (socialmedia_id,title,content,user_id,playingcard_name,pic,copy_country_trend_id) values (:socialmedia_id,:title,:content,:user_id,:playingcard_name,:pic,:copy_country_trend_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from carteajouer')


        return render_template("carteajouerform.html", carteajouers=user, one_user=one_user, the_title="add new carteajouer", touslessocialmedia=touslessocialmedia, touslesuser=touslesuser, touslescopy_country_trend=touslescopy_country_trend)


    touslessocialmedia= query_db("select * from socialmedia")

    touslesuser= query_db("select * from user")

    touslescopy_country_trend= query_db("select * from copy_country_trend")

    user = query_db('select * from carteajouer')
    one_user = query_db("select * from carteajouer limit 1", one=True)
    return render_template("carteajouerform.html", carteajouers=user, one_user=one_user, the_title="add new carteajouer", touslessocialmedia=touslessocialmedia, touslesuser=touslesuser, touslescopy_country_trend=touslescopy_country_trend)

