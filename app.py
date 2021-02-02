"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
# connect first
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ghimire@localhost/model_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'learningsql'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
connect_db(app)
db.drop_all()
db.create_all()


@app.route('/')
def index():
    post = Post.query.order_by(Post.created_at).all()
    return render_template('home.html', post=post)


@app.route('/users')
def landing_page():
    user = User.query.all()
    return render_template('user.html', users=user)


@app.route('/users/new')
def user_form():
    return render_template("user_form.html")


@app.route('/users/new', methods=['POST'])
def add_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    imageurl = request.form['imageurl']
    print(firstname, lastname, imageurl)
    new_user = User(first_name=firstname,
                    last_name=lastname, image_url=imageurl)
    db.session.add(new_user)
    db.session.commit()
    flash("New user has been Created!!")
    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_id(user_id):
    """show deatils of user"""
    user_detail = User.query.get_or_404(user_id)
    post_detail = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_detail.html', userd=user_detail, pos=post_detail)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit_post(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstname']
    user.last_name = request.form['lastname']
    user.image_url = request.form['imageurl']
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete')
def user_delete(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


""" second parts of project post routes"""


@app.route('/users/<int:user_id>/post/new')
def new_post(user_id):
    users = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=users)


@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_p = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_p)
    db.session.commit()
    flash("Post is Created")
    return redirect('/')


@app.route('/posts/<int:post_id>')
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", posts=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    print(post)
    return render_template("post_edit.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect("/users")
