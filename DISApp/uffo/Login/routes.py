from flask import render_template, url_for, flash, redirect, request, Blueprint, Flask
from uffo import bcrypt
from uffo.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from uffo.models import select_User, get_posts
from datetime import datetime
from uffo import app, login_manager


#202212
from uffo import roles, mysession

Login = Blueprint('Login', __name__)

posts = [{}]


@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)
    
    return render_template('home.html', posts=posts, role=role)


@Login.route("/heatmap")
def heatmap():
    #202212
    mysession["state"]="heatmap"
    print(mysession)
    return render_template('heatmap.html', title='Heatmap')

@Login.route("/posts", methods=['GET'])
@login_required
def posts():
    #202212
    mysession["state"]="posts"
    print(mysession)
    posts = get_posts()
    return render_template('posts.html', title='Posts', posts=posts)

# @Login.route('/posts', methods=['GET'])
# def display_posts():
#     posts = get_posts()
#     return render_template('posts.html', posts=posts)

@Login.route('/create_post', methods=['POST'])
def create_post():
    from uffo import conn
    cur = conn.cursor()
    date_posted = datetime.now().date()  # current date
    # Get data from form
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    comment = request.form.get('comment')
    date = date_posted
    username = current_user.username  # assuming you are using Flask-Login or a similar extension

    # Add to Posts table
    post_query = """
    INSERT INTO Posts (longitude, latitude, comments, date_posted, username)
    VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(post_query, (longitude, latitude, comment, date, username))

    # Add to User_sightings table
    sighting_query = """
    INSERT INTO User_sightings (comments, latitude, longitude, username)
    VALUES (%s, %s, %s, %s)
    """
    # You'll need to determine how to get city, state, country data.
    # For now, I'll just set them to NULL.
    city = state = country = None

    cur.execute(sighting_query, (comment, latitude, longitude, username))

    # Commit changes and close connection
    conn.commit()
    cur.close()

    flash('Post created successfully!', 'success')
    return redirect(url_for('Login.posts'))  # Redirect user to the home page (or wherever you want)

@Login.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"]="login"
    print(mysession)
    
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))    
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = select_User(form.username.data)
        
        # Change the bcrypt.check_password_hash() function to a simple comparison
        if user and user.password == form.password.data:
            mysession["username"] = form.username.data
            print(mysession)
                            
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


@Login.route("/account")
@login_required
def account():
    mysession["state"]="account"
    print(mysession)
    return render_template('account.html', title='Account')
