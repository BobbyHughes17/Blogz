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
            session['user'] = user.user_name
            flash('You have been successfully logged in '+ session['user'] + '!','info')
            return redirect('/new_blog')
        else:
            if not user:
                flash("User Name doesn't exist.")
            elif not check_pw_hash(password,user.pw_hash):
                flash('Password is incorrect.')
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
            flash('User Name is to long.','error')
            valid = False
        elif len(user_name) < 3:
            flash('User Name is to short.','error')
            valid = False
        elif User.query.filter_by(user_name=user_name).first():
            flash('user already exists','error')
            valid = False
        if len(password) > 20:
            flash('Password is to long.','error')
            valid = False
        elif len(password) < 3:
            flash('Password is to short.','error')
            valid = False  
        elif password != verify:
            flash("Passwords don't match",'error')
            valid = False
        
        if valid:
            new_user = User(user_name,password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user.user_name
            flash('You have been successfully registered '+ session['user'] + '!','info')
            return redirect('/new_blog')

        
    
    return render_template('register.html',nlogin='active')

@app.route('/blog', methods=['GET','POST'])
def blog():
    """ goes to blog page, lists all blogs"""
    blogs = Blog.query.all()
    if request.args.get("user_name") is not None:
        user = User.query.filter_by(user_name = request.args['user_name']).first()
        blogs = Blog.query.filter_by(owner=user).all()
    if request.args.get('blog') is not None:
        blogs = Blog.query.filter_by(title=request.args['blog']).all()
    
    return render_template('blogz.html',blogs=blogs,nblog='active')

@app.route('/new_blog',methods=['GET','POST'])
def new_blog():
    """ if posting new blog, add to db and redirect to blogs, else display new post"""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user = User.query.filter_by(user_name = session['user']).first()
        #check if title exists
        if Blog.query.filter_by(title=title).first():
            flash('blog title already exists.','error')
        #check if body is empty
        if len(body) < 1:
            flash('blog body needs some content.','error')
        #create blog
        if Blog.query.filter_by(title=title).first() is None and len(body) >=1:
            new_blog = Blog(title,body,user)
            #redirect to blog #flash msg blog posted
            db.session.add(new_blog)
            db.session.commit()
            flash('Blog has been posted!','info')
            return redirect('/blog')
        # if error then go to blog with flash
        
    return render_template('new_post.html',nnew_blog='active')

@app.route('/logout',methods=['GET'])
def logout():
    """ logout user, redirect to login"""

    del session['user']
    flash("You have been successfully logged out!",'info')
    return redirect('/')

if __name__ == "__main__":
    app.run()

