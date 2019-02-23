from flask import render_template, url_for, flash, redirect, request, jsonify
from project import app, db
from project.database_setup import Category, Item, User
from project.forms import ItemForm
from sqlalchemy.orm import sessionmaker, relationship, joinedload

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import desc


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"



@app.route("/")
@app.route("/catalog")
def catalog():
    if 'username' not in login_session:
        current_user = False
    else:
        current_user = True
    categories = Category.query.all()
    items = Item.query.all()
    dated_items = Item.query.order_by(desc(Item.date_posted)).limit(5).all()
    return render_template("catalog.html", categories=categories, items=items, dated_items=dated_items, current_user=current_user)


@app.route("/about")
def about():
    categories = Category.query.all()
    items = Item.query.all()
    dated_items = Item.query.order_by(desc(Item.date_posted)).limit(5).all()
    return render_template("about.html", categories=categories, dated_items=dated_items)

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    categories = Category.query.all()
    items = Item.query.all()
    dated_items = Item.query.order_by(desc(Item.date_posted)).limit(5).all()
    return render_template('login.html', STATE=state, categories=categories, items=items, dated_items=dated_items)

@app.route('/logout')
def showLogout():
    return redirect(url_for('gdisconnect'))



@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #See if user exists, if it doesn't create a new user
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'], 'success')
    print ("done!")
    return output


def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = User.query.filter_by(email = login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = User.query.filter_by(id = user_id).one()
    return user


def getUserId(email):
    try:
        user = User.query.filter_by(email = email).one()
        return user.id
    except:
        return None



@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s'), access_token
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out", 'success')
        return redirect(url_for('catalog'))
        
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route("/catalog/new", methods=['GET', 'POST'] )
def new_item():
    if 'username' not in login_session:
        current_user = False
        return redirect(url_for('showLogin'))
    else:
        current_user = True
    form = ItemForm()
    if form.validate_on_submit():
        category_add = Category.query.filter_by(name=form.select.data).first()
        item_add = Item(title=form.title.data, description=form.description.data, cat_id=category_add.id, user_id=login_session['user_id'])
        db.session.add(item_add)
        db.session.commit()
        flash('Your item is added', 'success')
        return redirect(url_for('catalog'))
    return render_template('addNewItem.html', title='Add Item', form=form, legend='Add Item', current_user=current_user)


@app.route("/item/<item_id>/")
def item(item_id):
    if 'username' not in login_session:
        current_user = False
    else:
        current_user = True
    categories = Category.query.all()
    items = Item.query.all()
    dated_items = Item.query.order_by(desc(Item.date_posted)).limit(5).all()
    item = Item.query.get_or_404(item_id)
    category = Category.query.filter_by(id=item.cat_id).first()
    user = User.query.filter_by(id=item.user_id).first()
    return render_template('item.html', title=item.title, item=item, category=category, user=user, current_user=current_user, categories=categories, items=items, dated_items=dated_items)

@app.route("/catalog.json")
def get_catalog():
    category = Category.query.all()
    #category = Category.query.options(joinedload(Category.items)).all()
    items = Item.query.all()
    #return jsonify(Category=[i.serialize for i in category])
    return jsonify(Category=[dict(c.serialize, items=[i.serialize for i in c.items]) for c in category])

@app.route("/item/<item_id>/edit", methods=['GET', 'POST'])
def edit_item(item_id):
    if 'username' not in login_session:
        current_user = False
        return redirect(url_for('showLogin'))
    else:
        current_user = True
    categories = Category.query.all()
    items = Item.query.all()
    dated_items = Item.query.order_by(desc(Item.date_posted)).limit(5).all()
    user = User.query.filter_by(name=login_session['username']).first()
    item = Item.query.get_or_404(item_id)
    category = Category.query.filter_by(id=item.cat_id).first()
    form = ItemForm()
    if user.id == item.user_id:
        if form.validate_on_submit():
            item.title = form.title.data
            item.description = form.description.data
            category = Category.query.filter_by(name=form.select.data).first()
            item.cat_id = category.id
            db.session.commit()
            flash("Item has been edited", 'success')
            return redirect(url_for('item', item_id=item.id))
        elif request.method == 'GET':
            form.title.data = item.title
            form.description.data = item.description
            form.select.data = category.name
            return render_template('addNewItem.html', title='Edit Item', form=form, 
                                legend='Edit Item', current_user=current_user, categories=categories, items=items, dated_items=dated_items)
    else:
        flash("You are not permitted to edit this item. Invalid user!", 'danger')
        return redirect(url_for('showLogin'))


@app.route("/item/<item_id>/delete", methods=['POST'])
def delete_item(item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user = User.query.filter_by(name=login_session['username']).first()
    item = Item.query.get_or_404(item_id)
    if user.id == item.user_id:
        db.session.delete(item)
        db.session.commit()
        flash('Item is deleted', 'success')
        return redirect(url_for('catalog'))
    else:
        flash("You are not permitted to delete this item. Invalid user!", 'danger')
        return redirect(url_for('showLogin'))