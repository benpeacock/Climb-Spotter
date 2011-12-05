from flask import Flask
from flask import render_template
from flask import request, session
from flask import abort, redirect, url_for, flash

from functools import wraps

import sqlalchemy
import json
import db

app = Flask(__name__)
app.debug = True

# set the secret key.  keep this really secret:
app.secret_key = 'ADDefA221 -9981 Bdd%kkkll'

# Check for valid login, used as decorator
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session or not session['username']:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function

#@app.context_processor
#def inject_privileges():
#
#    if 'user_id' in session:
#        from model import User
#        user = User.User(session['user_id'])
#        return dict(privilege_ids = user.privilege_ids())

@app.context_processor
def inject_menu():

    menu_items = []
    if 'user_id' in session:

        from model import User
        user = User.User(session['user_id'])
        privilege_ids = user.privilege_ids()
        if 1 in privilege_ids:
            item = {'label': 'Manage Users', 'url': url_for('user_manage'), 'active': False}
            if request.path.find('/u/user') == 0:
                item['active'] = True
            menu_items.append(item)
        if 2 in privilege_ids:
            item = {'label': 'Submit Route', 'url': url_for('route_form'), 'active': False}
            if request.path.find('/u/route/form') == 0:
                item['active'] = True
            menu_items.append(item)
        if 3 in privilege_ids:
            item = {'label': 'View Data', 'url': url_for('route_list'), 'active': False}
            if request.path.find('/u/route/list') == 0:
                item['active'] = True
            menu_items.append(item)
    return dict(menu_items = menu_items)

@app.route('/')
def index(post_id = None, slug = None):

    return render_template('index.html')


@app.route('/register')
def register():

    return render_template('register.html')

@app.route('/doRegister', methods=['POST'])
def doRegister():

    from model import User

    errors = []
    # Validate data
    # Check for required fields
    labels = {'username': 'Username', 'password': 'Password',
        'password2': 'Re-type Password', 'email': 'E-mail',
        'email2': 'Re-type Email', 'display_name': 'Display Name'}
    for el in ['username', 'password', 'password2', 'email', 'email2', 'display_name']:
        if el not in request.form or len(request.form[el]) == 0:
            errors.append("'{0}' is a required field.".format(labels[el]))

    # Make sure username is not currently used
    if User.usernameExists(request.form['username']):
        errors.append("The username '{username}' already exists in our system. Please choose a different one.".format(username = request.form['username']))

    # Compared passwords and emails
    if request.form['password'] != request.form['password2']:
        errors.append('Passwords must match.')
    if request.form['email'] != request.form['email2']:
        errors.append('E-mail addresses must match.')

    # No spaces in username or password
    if ' ' in request.form['username']:
        errors.append('Username may not contain spaces')
    if len(request.form['username']) not in range(4, 31):
        errors.append('Username must be 4-30 characters long.')
    if len(request.form['password']) not in range(6, 21):
        errors.append('Password must be 6-20 characters long.')

    # If errors, display form again
    if len(errors) != 0:

        return render_template(
            'register.html', error = "<br/>\n".join(errors),
            username = request.form['username'],
            password = request.form['password'],
            password2 = request.form['password2'],
            email = request.form['email'],
            email2 = request.form['email2'],
            display_name = request.form['display_name']
        )

    # If no errors, save user as not active and redirect to awaiting approval page
    user = User.User()
    user.username = request.form['username']
    user.set_encrypted_password(request.form['password'])
    user.email = request.form['email']
    user.display_name = request.form['display_name']
    user.save()
    return redirect(url_for('user'))


@app.route('/registerDone')
def registerDone():

    return render_template('registerDone.html')
    

@app.route('/doLogin', methods=['POST'])
def doLogin():
    from model import User

    try:
        user = User.getInstanceFromUsernamePassword(request.form['username'], request.form['password'])
        session['username'] = user.username
        session['user_id'] = user.user_id
        return redirect(url_for('user_manage'))
    except sqlalchemy.orm.exc.NoResultFound:
        return redirect(url_for('index'))

@app.route('/u')
@login_required
def user():

    from model import User
    return render_template('user/index.html', users = User.getData())

@app.route('/u/user')
@login_required
def user_manage():

    from model import User
    return render_template('user/index.html', users = User.getData())


@app.route('/u/user/activate')
@login_required
def user_activate():

    from model import User
    user_id = int(request.args.get('id'))
    user = User.User(user_id)
    user.activate()
    flash('User activated')
    return redirect(url_for('user'))

@app.route('/u/user/form/<username>')
@login_required
def user_form(username):

    from model import User
    user = User.getInstanceFromUsername(username)

    # Do not allow editing administrators
    if user.is_administrator():

        return redirect(url_for('user'))

    return render_template('user/form.html',
                username = user.username,
                original_username = user.username,
                email = user.email,
                display_name = user.display_name,
                active = user.active,
                role_ids = user.role_ids()
    )

@app.route('/u/user/save', methods = ['POST'])
def user_save():

    from model import User

    # Load user id from original username
    user = User.getInstanceFromUsername(request.form['original_username'])

    errors = []
    # Validate data
    # Check for required fields
    labels = {'username': 'Username', 'email': 'E-mail', 'display_name': 'Display Name'}
    for el in ['username', 'email', 'display_name']:
        if el not in request.form or len(request.form[el]) == 0:
            errors.append("'{0}' is a required field.".format(labels[el]))

    # Make sure username is not currently used
    if user.username != request.form['username'] and User.usernameExists(request.form['username'], exclude_user_id = user.user_id):
        errors.append("The username '{username}' already exists in our system. Please choose a different one.".format(username = request.form['username']))

    # No spaces in username or password
    if ' ' in request.form['username']:
        errors.append('Username may not contain spaces')
    if len(request.form['username']) not in range(4, 31):
        errors.append('Username must be 4-30 characters long.')

    # If errors, display form again
    if len(errors) != 0:

        role_id = ''
        if 'role_id' in request.form and len(request.form['role_id']) > 0:
            role_id = int(request.form['role_id'])


        return render_template(
            'user/form.html', error = "<br/>\n".join(errors),
            original_username = request.form['original_username'],
            username = request.form['username'],
            email = request.form['email'],
            display_name = request.form['display_name'],
            active = int(request.form['active']),
            role_ids = [role_id]
        )

    # If no errors, save user as not active and redirect to awaiting approval page
    user.username = request.form['username']
    user.email = request.form['email']
    user.display_name = request.form['display_name']
    user.active = request.form['active']
    user.save()

    user.update_roles([request.form['role_id']])
    return redirect(url_for('user_manage'))

# Route form
@app.route('/u/route/form')
@login_required
def route_form():

    return render_template('route/form.html', area_options = [('1', 'New River Gorge'), ('2', 'Meadow River Gorge')])

# Route save
@app.route('/u/route/save', methods = ['POST'])
@login_required
def route_save():

    from model import RouteWork

    errors = []
    # Validate data
    # Check for required fields
    #labels = {'username': 'Username', 'email': 'E-mail', 'display_name': 'Display Name'}
    #for el in ['username', 'email', 'display_name']:
    #    if el not in request.form or len(request.form[el]) == 0:
    #        errors.append("'{0}' is a required field.".format(labels[el]))

    # If errors, display form again
    if len(errors) != 0:

        return render_template(
            'user/form.html', error = "<br/>\n".join(errors),
            original_username = request.form['original_username'],
            username = request.form['username'],
            email = request.form['email'],
            display_name = request.form['display_name'],
            active = int(request.form['active']),
            role_ids = [role_id]
        )

    # If no errors, save user as not active and redirect to awaiting approval page
    work = RouteWork.RouteWork()
    work.route_id = request.form['route_id']
    work.work_date = request.form['work_date']
    work.who = request.form['who']
    work.bolts_placed = request.form['bolts_placed']
    if 'anchor_replaced' in request.form:
        work.anchor_replaced = 1
    else:
        work.anchor_replaced = 0
    if 'new_anchor' in request.form:
        work.new_anchor = 1
    else:
        work.new_anchor = 0
    work.user_id = session['user_id']
    work.save()

    return redirect(url_for('user_manage'))

# Suggest area
@app.route('/u/area/suggest')
@login_required
def area_suggest():

    from model import Area
    options = []
    for area in Area.search(request.args.get('term')):

       options.append({'label': area['name'], 'value': area['area_id']})

    return json.dumps(options)

# Suggest route
@app.route('/u/route/suggest')
@login_required
def route_suggest():

    from model import Route
    options = []
    for route in Route.search(request.args.get('term'), request.args.get('area_id')):

        options.append({'label': route['name'], 'value': route['route_id']})

    return json.dumps(options)

# View route work data
@app.route('/u/route/list')
@login_required
def route_list():

    from model import RouteWork
    return render_template('route/index.html', routes = RouteWork.getData())

# Logout
@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))











@app.route('/feed/ios/news.json')
def news():

    page = 0
    if request.args.get('page'):
        page = int(request.args.get('page'))

    articles = _get_articles(page, 20)
    return json.dumps(articles)

@app.route('/feed/ios/article')
def article():

    news_id = request.args.get('id')
    return render_template('article.html', article = _get_article(news_id)) 

@app.route('/news/listing')
def newsListing():

    return render_template('newsListing.json')

@app.route('/video/listing')
@app.route('/video/listing/<page>')
def videoListing(page = 1):

    return render_template("videos%s.json" % (page))

@app.route('/video/youtube')
def videoYouTube():

    return render_template('youtube.html')

@app.route('/video/vimeo')
def videoVimeo():
    
    return render_template('vimeo.html')

def _get_db():

    return MySQLdb.connect(
        host='localhost',
        user = 'dpm',
        passwd = 'dpm',
        db = 'dpm',
        cursorclass=MySQLdb.cursors.DictCursor
    )

def _get_articles(page = 0, per_page = 20):

    db = _get_db()
    cursor = db.cursor()
    start = page * per_page
    sql = "SELECT news_id, title, teaser, date_format(posted, '%%m/%%d/%%y') as post, thumb, url FROM dpm.news ORDER BY posted DESC LIMIT %i, %i" % (start, per_page)
    cursor.execute(sql)
    return cursor.fetchall()

def _get_article(news_id):

    db = _get_db()
    cursor = db.cursor()
    sql = "SELECT title, posted, posted_by, detail FROM dpm.news WHERE news_id = %s"
    cursor.execute(sql, (news_id))

    article = cursor.fetchone()
    article['detail'] = _cleanup_detail(article['detail'])
    return article

def _cleanup_detail(detail):

    import re

    # Resolve relative paths
    detail = detail.replace('src="/', 'src="http://www.dpmclimbing.com/')

    # Re-size images
    detail = re.sub(r'width: ([0-9]+)px; height: ([0-9]+)px;?', _resize_img, detail)

    return detail

def _resize_img(m):

    #width = m.group(1)
    #height = m.group(2)
    return 'width: 300px'
        
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)

# set the secret key.  keep this really secret:
#app.secret_key = 'ADDefA221 -9981 Bdd%kkkll'
