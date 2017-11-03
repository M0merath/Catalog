from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Recipe, User
from flask import session as login_session
import random
import string
import json
import httplib2
import os

app = Flask(__name__)
app.secret_key = 'nothing special'

engine = create_engine('sqlite:///gastronaut.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print ("access token received %s ") % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
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

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


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
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
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
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
    

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


#decorator functions

@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category)
    #return render_template('categories.html', categories=categories)
    if 'username' not in login_session:
        return render_template('publicCategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)
        

@app.route('/category/JSON')
def categoriesJSON():
	categories = session.query(Category).all()
	return jsonify(categories=[c.serialize for c in categories])

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/recipes')
def showRecipes(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category_id)
    creator = getUserInfo(category.user_id)
    #return render_template('showRecipes.html', category=category, recipes=recipes, category_id=category_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicRecipes.html', category=category, creator=creator, recipes=recipes, category_id=category_id)
    else:
        return render_template('showRecipes.html', category=category, creator=creator, recipes=recipes, category_id=category_id)

@app.route('/category/<int:category_id>/recipe/<int:recipe_id>')
def singleRecipe(category_id, recipe_id):
        category = session.query(Category).filter_by(id=category_id).one()
        recipe = session.query(Recipe).filter_by(id=recipe_id).one()
        ingString = str(recipe.ingredients)
        ingSplit = ingString.split(", ")
        for i in ingSplit:
                print (i)
        ingList = "\n".join(ingSplit)
        if 'username' not in login_session:
            return render_template('publicRecipe.html', category=category, recipe=recipe, category_id=category_id, recipe_id=recipe_id, ingSplit=ingSplit)
        else:
            return render_template('singleRecipe.html', category=category, recipe=recipe, category_id=category_id, recipe_id=recipe_id, ingSplit=ingSplit)

@app.route('/category/<int:category_id>/recipes/JSON')
def recipesJSON(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	recipes = session.query(Recipe).filter_by(category_id=category_id).all()
	return jsonify(Recipes=[r.serialize for r in recipes])

@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    categoryToEdit = session.query(Category).filter_by(id = category_id).one()
    user = login_session['user_id']
    if categoryToEdit.user_id == user:
        if request.method == 'POST':
            category = session.query(Category).filter_by(id=category_id).one()
            category.name = request.form['name']
            session.commit()
            flash("Category Successfully Edited")
            return redirect(url_for('showCategories'))
        else:
            return render_template('editCategory.html', category_id = category_id, categoryToEdit = categoryToEdit)
    else:
        flash("Only the author of this category can edit it.")
        return redirect(url_for('showCategories'))

@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    #flash("category_id: %s" % category_id)
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    user = login_session['user_id']
    if categoryToDelete.user_id == user:
        if request.method == 'POST':
            session.delete(categoryToDelete)
            session.commit()
            flash("Category Successfully Deleted")
            return redirect(url_for('showCategories'))
        else:
            return render_template('deleteCategory.html', category_id = category_id, categoryToDelete = categoryToDelete)
    else:
        flash("Only the author of this category can delete it.")
        return redirect(url_for('showCategories'))

@app.route('/category/<int:category_id>/recipe/new', methods=['GET','POST'])
def newRecipe(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Recipe(name=request.form['name'], summary=request.form['summary'], ingredients=request.form['ingredients'], directions=request.form['directions'], category_id = category_id, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("Recipe Created!")
        return redirect(url_for('showRecipes', category_id=category_id))
    else:
        return render_template('newRecipe.html', category_id = category_id)

@app.route('/category/<int:category_id>/recipe/<int:recipe_id>/edit', methods=['GET','POST'])
def editRecipe(category_id, recipe_id):
    itemToEdit = session.query(Recipe).filter_by(id=recipe_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    user = login_session['user_id']
    if itemToEdit.user_id == user:
        if request.method == 'POST':
            itemToEdit.name = request.form['name']
            itemToEdit.summary = request.form['summary']
            itemToEdit.ingredients = request.form['ingredients']
            itemToEdit.directions = request.form['directions']
            session.add(itemToEdit)
            session.commit()
            if request.form['name']:
                itemToEdit.name = request.form['name']
            if request.form['summary']:
                itemToEdit.description = request.form['summary']
            if request.form['ingredients']:
                itemToEdit.price = request.form['ingredients']
            if request.form['directions']:
                itemToEdit.course = request.form['directions']
                flash("Recipe Successfully Edited")
                return redirect(url_for('showRecipes', category_id=category_id))
            return render_template('editRecipe.html', category_id = category_id, recipe_id = recipe_id, itemToEdit = itemToEdit)
    else:
        flash("You must be the author of this recipe to edit it.")
        return redirect(url_for('singleRecipe', category_id=category_id, recipe_id=recipe_id))

@app.route('/category/<int:category_id>/recipe/<int:recipe_id>/JSON')
def recipeJSON(category_id, recipe_id):
    category = session.query(Category).filter_by(id=category_id).one()
    recipe = session.query(Recipe).filter_by(id=recipe_id)
    return jsonify(recipe=[r.serialize for r in recipe])

@app.route('/category/<int:category_id>/recipe/<int:recipe_id>/delete', methods=['GET','POST'])
def deleteRecipe(category_id, recipe_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
    user = login_session['user_id']
    if itemToDelete.user_id == user:
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            flash("Menu Item Successfully Deleted")
            return redirect(url_for('showRecipes', category_id=category_id))
        else:
            return render_template('deleteRecipe.html', recipe=itemToDelete, category_id=category_id)
    else:
        flash("Only the author of this recipe can delete it.")
        return redirect(url_for('singleRecipe', category_id=category_id, recipe_id=recipe_id))
            

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            #del login_session['gplus_id']
            #del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['user_id']
            del login_session['provider']
            flash("You have successfully been logged out.")
            return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))

if __name__ == '__main__':
    app.debug = True
    myPort = int(os.environ.get('PORT', 8000))
    app.run(host = '0.0.0.0', myPort)
