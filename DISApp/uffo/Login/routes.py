from flask import render_template, url_for, flash, redirect, request, Blueprint
from uffo import bcrypt
from uffo.forms import CustomerLoginForm, EmployeeLoginForm
from flask_login import login_user, current_user, logout_user, login_required
from uffo.models import select_Customers, select_Employees
from datetime import datetime


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

@Login.route("/posts")
def posts():
    #202212
    mysession["state"]="posts"
    print(mysession)
    return render_template('posts.html', title='Posts')

@Login.route('/create_post', methods=['POST'])
def create_post():
    from uffo import conn
    cur = conn.cursor()
    # Get data from form
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    comment = request.form.get('comment')
    username = current_user.username  # assuming you are using Flask-Login or a similar extension

    # Add to Posts table
    post_query = """
    INSERT INTO Posts (longitude, latitude, comments, username)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(post_query, (longitude, latitude, comment, username))

    # Add to User_sightings table
    sighting_query = """
    INSERT INTO User_sightings (city, state, country, comments, date_posted, latitude, longitude, username)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    # You'll need to determine how to get city, state, country data.
    # For now, I'll just set them to NULL.
    city = state = country = None
    date_posted = datetime.now().date()  # current date

    cur.execute(sighting_query, (city, state, country, comment, date_posted, latitude, longitude, username))

    # Commit changes and close connection
    conn.commit()
    cur.close()

    flash('Post created successfully!', 'success')
    return redirect(url_for('home'))  # Redirect user to the home page (or wherever you want)

@Login.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"]="login"
    print(mysession)
    role=None
    
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))    
    
    is_employee = True if request.args.get('is_employee') == 'true' else False
    form = EmployeeLoginForm() if is_employee else CustomerLoginForm()
    
    if form.validate_on_submit():
        user = select_Employees(form.username.data) if is_employee else select_Customers(form.username.data)
        
        if user != None and bcrypt.check_password_hash(user.password, form.password.data):
            mysession["role"] = user.role
            mysession["username"] = form.username.data
            print(mysession)
                            
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    role =  mysession.get("role", "")
    print('role: '+ role)

    return render_template('login.html', title='Login', is_employee=is_employee, form=form, role=role)



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
