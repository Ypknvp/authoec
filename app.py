from flask import Flask, redirect, request, session, url_for
from auth0.v3.authentication import AuthenticationClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Used to encrypt session data

# Auth0 configuration
CLIENT_ID = 'FamqhcGsNDTZUArdoLWxsPYpzcblbRDl'
CLIENT_SECRET = 'AqtiIItsUcBMcU7e7aGFl9I0SJp5VpkT96Fz244uFa2bODUuap7pFVijvIGa85wc'
DOMAIN = 'dev-4wlz1bgiyq00hl04.us.auth0.com'
CALLBACK_URL = 'http://localhost:5000/callback'
AUTH0_API = f'https://{DOMAIN}.auth0.com'

# Set up Auth0 Authentication client
auth0 = AuthenticationClient(domain=DOMAIN, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

@app.route('/')
def home():
    return 'Welcome to the simple Auth0 Flask website! <br><a href="/login">Login with Auth0</a>'

@app.route('/login')
def login():
    # Redirect to Auth0 login page
    return redirect(f'{AUTH0_API}/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}')

@app.route('/callback')
def callback():
    # Handle the Auth0 callback and get the user info
    code = request.args.get('code')
    try:
        # Exchange the authorization code for tokens
        tokens = auth0.exchange_code_for_access_token(code, CALLBACK_URL)
        session['access_token'] = tokens['access_token']
        return 'Login successful! You can now access the app.'
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/logout')
def logout():
    # Clear session and logout from Auth0
    session.clear()
    return redirect(f'{AUTH0_API}/v2/logout?client_id={CLIENT_ID}&returnTo=http://localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
