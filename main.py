from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy     # SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime       # datetime
from datetime import date
import pymysql                      # For MySQL
pymysql.install_as_MySQLdb()        # Installing MySQLdb
import json                         # JSON
import math




''' -------------------- Defining json ---------------------- '''
with open("config.json", 'r') as c:
    params = json.load(c)["params"]


''' App '''
app = Flask(__name__)
app.secret_key = "secret-key"               #secret key for flask app
app.config['UPLOAD_FOLDER'] = params['upload_location']



''' ----------------- Database Settings ------------------------ '''
local_server = True
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


''' ----------------- Class for Contact Page ------------------- '''
class Contacts(db.Model):
    # sno, name phone_num, msg, date, email
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


''' ----------------- Class for Posts Page ------------------- '''
class Posts(db.Model):
    # sno, title, slug, content, tagline, date, img_file, time
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


''' ----------------- Main Page ------------------- '''
@app.route("/")
def home():
        posts = Posts.query.filter_by().all()
        last = math.ceil(len(posts) / int(params['no_of_posts']))
        '''
        request.args.get() returns the value after url. 
        #1. Default is none. So for that we have defined as 1.
        '''

        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]

        if page == 1:
            prev = "#"
            next = "/?page=" + str(page + 1)
        elif page == last:
            prev = "/?page=" + str(page - 1)
            next = "#"
        else:
            prev = "/?page=" + str(page - 1)
            next = "/?page=" + str(page + 1)

        return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


''' ----------------- Log in Page ----------------- '''
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username==params['admin_user'] and userpass==params['admin_password']):
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template('login.html', params=params)


''' ----------------- Logout ----------------- '''
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")


''' ----------------- Add A New Post ----------------- '''
@app.route("/add/<string:sno>",  methods=['GET', 'POST'])
def add_post(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            new_title = request.form.get('title')
            new_tagline = request.form.get('tagline')
            new_slug = request.form.get('slug')
            new_imgfile = request.form.get('img_file')
            new_content = request.form.get('content')
            new_date = date.today()
            # new_time = datetime.now().strftime("%H:%M:%S")

            # If a new or first post is added
            if sno=='0':
                # sno, title, slug, content, tagline, date, img_file, time
                post = Posts(title = new_title, tagline=new_tagline, slug=new_slug, img_file=new_imgfile, content=new_content, date=new_date)
                db.session.add(post)
                db.session.commit()

        return render_template('add_post.html', params=params, sno=sno)


''' ----------------- Edit Previous Posts ----------------- '''
@app.route("/edit/<string:sno>",  methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            new_title = request.form.get('title')
            new_tagline = request.form.get('tagline')
            new_slug = request.form.get('slug')
            new_imgfile = request.form.get('img_file')
            new_content = request.form.get('content')
            new_date = date.today()
            # new_time = datetime.now().strftime("%H:%M:%S")


            post = Posts.query.filter_by(sno=sno).first()       # Fetch the first post with serial no. = sno
            post.title = new_title
            post.tagline = new_tagline
            post.slug = new_slug
            post.img_file = new_imgfile
            post.content = new_content
            post.date = new_date
            # post.time = new_time
            db.session.commit()

            # return redirect('/edit/'+ sno)
            return redirect('/dashboard')

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post)


''' ----------------- Delete Post ----------------- '''
@app.route("/delete/<string:sno>", methods=['GET', "POST"])
def delete_post(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


''' ----------------- About Page ----------------- '''
@app.route("/about")
def about():
    return render_template('about.html', params=params)


''' ----------------- Post Page ------------------- '''
@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)


''' ----------------- Contact Page ---------------- '''
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        # Add entry to the database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html', params=params)

if __name__ == "__main__":
    app.run(debug=True)


