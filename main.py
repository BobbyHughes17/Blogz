from flask import redirect,request,render_template,session,flash
from app import db,app
from models import User,Blog,make_pw_hash,check_pw_hash


@app.before_request
def required_login():
    """ if user tries to create a new post, require login """

    allowed_routes = ['index','blog','logout','login','register']

    if 'user' not in session and request.endpoint not in allowed_routes:
        return render_template('login.html')

@app.route('/', methods=['GET'])
def index():
    """ goes to index page where users are listed."""

    users = User.query.all()

    return render_template('index.html', nuser='active',users=users)

@app.route('/login',methods=['GET','POST'])
def login():
    """ goes to login page, to login, if not logged in when doing new_post"""

    if request.method == 'POST':
        #TODO validate user id and password - redirect to new-blog
        user = User.query.filter_by(user_name=request.form['user_name']).first()
        password = request.form['password']
        if user and check_pw_hash(password,user.pw_hash):
            session['user'] = user
            return redirect('/new_blog')
    return render_template('login.html',title='Login',nlogin='active')

@app.route('/register',methods=['GET','POST'])
def register():
    """goes to register page"""
    if request.method == 'POST':

        user_name = request.form['user_name']
        password = request.form['password']
        verify = request.form['verify']
        valid = True

        if len(user_name) > 20:
            flash('User Name is to long.')
            valid = False
        elif len(user_name) < 3:
            flash('User Name is to short.')
            valid = false
        elif User.query.filter_by(user_name=user_name).first():
            flash('user already exists')
            valid = False
        if len(password) > 20:
            flash('Password is to long.')
            valid = False
        elif len(password) < 3:
            flash('Password is to short.')
            valid = false    
        elif password == verify:
            flash("Passwords don't match")
            valid = False
        
        if valid:
            new_user = User(user_name,make_pw_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user        
            return redirect('/new_blog')

        

    return render_template('register.html',nlogin='active')

@app.route('/blog', methods=['GET'])
def blog():
    """ goes to blog page, lists all blogs"""
    blogs = Blog.query.all()

    return render_template('blogz.html',blogs=blogs,)

@app.route('/new_blog',methods=['GET','POST'])
def new_blog():
    """ if posting new blog, add to db and redirect to blogs, else display new post"""

    if request.method == 'POST':
        return redirect('')

    return render_template('new_post.html')

@app.route('/logout',methods=['GET'])
def logout():
    """ logout user, redirect to login"""

    del session['user']
    return redirect('/login')

if __name__ == "__main__":
    app.run()

