from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/comment_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
title = "My First Name"
post = "Prasad"
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    created_at = db.Column(db.TIMESTAMP())

class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    title = db.Column(db.String(11))
    body = db.Column(db.Text(120))
    craeted_at = db.Column(db.TIMESTAMP())

class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    body = db.Column(db.Text(80))
    created_at = db.Column(db.TIMESTAMP())

class replies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    comment_id = db.Column(db.Integer())
    body = db.Column(db.Text(80))
    created_at = db.Column(db.TIMESTAMP())


@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("posts"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['post_text']

        blog_posts = post(title = title, body = body)
        db.session.add(blog_posts)
        db.session.commit()

        return render_template('comment.html',tit =title , po =body)
    return render_template('posts.html')

@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == 'POST':
        comment_body = request.form['blog_comment']

        blog_comment = comments( comment_body = comment_body)
        db.session.add(blog_comment)
        db.session.commit()

        return render_template('comment.html')
    return render_template('comment.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


 


