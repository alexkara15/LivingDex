from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from users import *
from usersession import *
from pokedex import *

app = Flask(__name__)

database = UserDatabase('test.csv')
nationalDex = NationalDex('nationaldex.txt')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<username>')
def user(username):
    if database.userExists(username):
        return render_template('user.html', username=username, dex=database.dexForUsername(username, nationalDex.numberOfPokemon), pokemonNames=nationalDex.pokemonNames)
    else:
        return render_template('baduser.html', username=username)

@app.route('/togglePokemon', methods=['POST'])
def togglePokemon():
    username = request.form['username']
    if username == currentUser():
        toggledPokemon = request.form['toggledPokemon']
        database.togglePokemonForUser(username, int(toggledPokemon))
    return 'OK'

@app.route('/register', methods=['POST'])
def register():
    registerUsername = request.form['registerUsername']
    registerPassword = request.form['registerPassword']

    usernameIsValid, usernameError = database.verifyNewUsername(registerUsername)
    passwordIsValid, passwordError = database.verifyNewPassword(registerPassword)

    if not usernameIsValid:
        return render_template('login.html', error=usernameError)
    elif not passwordIsValid:
        return render_template('login.html', error=passwordError)
    else:
        database.registerUser(registerUsername, registerPassword, 0)
        logInUser(registerUsername)
        return redirect(url_for('user', username=registerUsername))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        if len(loginUsername) > 0:
            if not database.userExists(loginUsername):
                error = 'User {} does not exist'.format(loginUsername)
            elif database.userHasPassword(loginUsername, loginPassword):
                logInUser(loginUsername)
                return redirect(url_for('user', username=loginUsername))
            else:
                error = 'Incorrect username / password'
        else:
            error = 'You need to enter in a username and password to register or log in as.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logoutAndGoHome():
    logout()
    return home()

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # app.run()
    app.run(host='0.0.0.0', debug = True)

