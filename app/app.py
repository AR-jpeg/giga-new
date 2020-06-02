"""Main File."""
from flask import Flask, request, redirect, render_template, flash, url_for
from sqlalchemy.types import String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from threading import Thread
from os import name
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model): # work in progress...
    """Base class for users."""

    __tablename__ = "users"

    email = db.Column(String(120), nullable=False)
    is_signed_in = db.Column(String(1)) # Either T/F
    username = db.Column(String(80), nullable=False)
    hashed_password = db.Column(String(400))
    user_id = db.Column(String(1000))
    primary_id = db.Column(Integer, primary_key=True)
    all_posts = db.Column(String(500_000_000), default='') # Takes in some thing like "93;123" which is the id of the post

    def __init__(self, email, is_signed_in, username, hashed_password, user_id):
        """__init__ for User class."""
        super().__init__()
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.user_id = user_id
        self.is_signed_in = is_signed_in

    def __repr__(self):
        """Represent the given user."""
        return f'<User {self.username}>'

    def __eq__(self, other):
        """Is the user eqivelent to an other."""
        return self.email == other.email and self.username == other.username and self.hashed_password == other.hashed_passweord and self.user_id == other.user_id

    @property
    def posts(self):
        """Thing."""
        return ["https://clonebook--adityaru.repl.co/posts/view/" + x for x in self.all_posts.split(';')]

    @posts.setter
    def posts(self, value):
        """Thing."""
        self.posts += ';%s' % value

class BlogPost(db.Model):
    """Base class for BPs."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """How to Represent a BP."""
        return 'Blog post ' + str(self.id)

## Routes
@app.route('/')
def index():
    """Index route (ex) yourdomain.extension/."""
    return render_template('index.html', signedin=False)
            

@app.errorhandler(404)
def error(e):
    """Handle errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(e):
    """Handle errors."""
    return "..."

@app.route('/signup/new', methods=['POST'])
def new_signup():
    """Signup."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, hashed_password=hashed_password, email=email, user_id=hex(random.randint(100_100, 999_999)))
        print(type(new_user.hashed_password))

        db.session.add(new_user)
        db.session.commit()

        return redirect('/signup')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit the current BlogPost."""
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']    
        db.session.commit()
        return redirect('/posts')
        
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/view/<int:id>')
def see_post(id):
    """See any post in 'scope'."""
    post = BlogPost.query.get_or_404(id)

    return render_template('/view.html', post=post)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Login to a given user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = User.query.filter(username=username, email=email)
        if user:
            if bcrypt.check_password_hash(password, password):
                user.is_signed_in = True
                return redirect(f'/user/{user.user_id}')
            else:
                return flash('Oh No! Your account was not found!')
    else:
        return render_template('login.html')

@app.route('/posts/delete/<int:id>')
def delete(id):
    """Delete the post."""
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    """Thingy."""
    all_posts = reversed(BlogPost.query.order_by(BlogPost.date_posted).all())
    return render_template('posts.html', posts=all_posts)

@app.route('/user/<id>')
def user(id_number):
    """Show a user."""
    try:
        user = User.query.filter(user_id=id)
        if user:
            return render_template('view_person.html', user=user, posts=user.all_posts)
    except Exception as e:
        return redirect('/404')

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    """Make a new post."""
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/signup')
def signup():
    """Render template."""
    return render_template('signup.html')



def run():
    """For my own sanity."""
    # for windows 
    if name == 'nt': 
        app.run(host='127.0.0.1', port = 8080, debug=True)
    # for mac and linux(here, os.name is 'posix')
    else: 
        app.run('0.0.0.0', port=8080, debug=False)

def keep_alive():
    """Keep our server alive."""
    server = Thread(target=run)
    server.start()

if __name__ == '__main__':
    run()