"""Main File."""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import random


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model): # work in progress...
    """Base class for users."""

    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(400))
    primary_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        """Represent the given user."""
        return f'<User {self.username}>'


class BlogPost(db.Model):
    """Base data base model."""

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author = db.Column(db.String(30), nullable=False, default="N/A")
    title = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    date_posted_fancy = "PLACEHOLDER" 

    def __repr__(self):
        """REPR thing."""
        return 'Blog Post ' + str(self.id)

@app.route('/')
def index():
    """Index route (ex) yourdomain.extension/."""
    return render_template('index.html')

@app.errorhandler(404)
def error(e):
    """Handle errors."""
    return render_template('404.html'), 404

@app.route('/signup/new', methods=['POST'])
def new_signup():
    """Signup."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, hashed_password=hashed_password, email=email, id=hex(random.randint(100_100, 999_999)))
        print(type(new_user.hashed_password))

        db.session.add(new_user)
        db.session.commit()

        return redirect(f'/user/{new_user.id}')
    else:
        return redirect('/signup')

@app.route('/signup')
def signup():
    """Render template."""
    return render_template('signup.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    """Render all posts."""
    all_posts = BlogPost.query.all()
    return render_template('posts.html', posts=all_posts)

@app.route('/user/<id>')
def user(id_number, is_logged_in = False):
    """Show a user."""
    try:
        user = User.query.all()
    except:
        pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Login to a given user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    else:
        return render_template('login.html')

@app.route('/posts/delete/<int:id>')
def delete(id):
    """Delete the post."""
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

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
        return render_template('edit.html/', post=post)

@app.route('/posts/view/<int:id>')
def see_post(id):
    """See any post in 'scope'."""
    post = BlogPost.query.get_or_404(id)

    return render_template('/view.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    """Create a new post."""
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
