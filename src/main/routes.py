"""General routes go in this file."""
from flask import render_template, request, Blueprint
from ..models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """Render the index page."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    """Render the about page."""
    return render_template('about.html', title='About')
