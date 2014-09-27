from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    pass

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

def generate_token_and_confirm():
    # Generate CSRF tokens.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state

    response = make_response(
            render_template(
                'index.html',
                CLIENT_ID=CLIENT_ID,
                STATE=state,
                APPLICATION_NAME=APPLICATION_NAME
            ))
            
    # Confirm CSRF token
    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps("Invalid state parameters"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

def start_gplus_service():
    gplus_id = request.args.get('gplus_id')
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session['credentials'] = credentials
    session['gplus_id'] = gplus_id
    response = make_response(json.dumps("Successfully connected user.", 200))
    return response

if __name__ == "__main__":
    app.run(debug=True)
