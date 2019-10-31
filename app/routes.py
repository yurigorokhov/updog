from flask import current_app as app
from . import db
from flask import render_template, request, redirect, url_for, jsonify, Response
from pony.orm import *
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash


set_sql_debug(True)


@app.route('/api/chats/<int:chat_id>/messages', methods=['GET', 'POST'])
def messages(chat_id):
    

    user_id = int(request.args.get('user_id'))


    # check if user in database

    try:
        chat = db.Chat[chat_id]
        user = db.User[user_id]
    except ObjectNotFound:
        return("User Does Not Exsist")

    # returns json of all chat messages

    if request.method == 'GET':
        if user not in chat.users:
            return "User not in this char group."
        else:  
            return jsonify([
                {
                    'id': m.id,
                    'body': m.body,
                    'sender_first': m.sender_id.first_name,
                    'sender_last': m.sender_id.last_name,
                    'time-stamp': m.date_created

                }
                for m in chat.messages
            ])

    # post message to database

    if request.method == 'POST':

        if not request.content_type == 'application/json':
            return "Invalid request.  Content type must be 'application/json'"
        
        r = request.get_json()
        body = r['body']

        with db_session:
            message = db.Message(body=body, sender_id=user, chat=chat)
            return "Message successfully added"
        

@app.route('/api/chats', methods=['GET', 'POST'])
def chats():
    user_id = request.args.get('user_id')

    if not user_id:
        return "Invalid request.  No user id provided"

    try:
        user = db.User[user_id]
    except ObjectNotFound:
        return("User Does not Exsist")


    if request.method == 'GET':
        chats = []
        for c in user.chats:
            chats.append({"id": c.id,
                            "last_updated": c.last_updated})
        return jsonify(chats)


    if request.method == 'POST':
        with db_session:
            chat = db.Chat(chat_name = user.full_name, creator_id = user.id)
            commit()
            user.chats.add(db.Chat[chat.id])
            return "Success!"


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    user_id = request.args.get('user_id')
    user = db.User[user_id]
    return render_template('index.html', user=user, chats=user.chats)


@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        if not request.content_type == 'application/json':
            return "Invalid request. Content type must be 'application/json'"

        r = request.get_json()
        first_name = r['first_name']
        last_name = r['last_name']
        email = r['email']
        password = r['password']

        with db_session:
            user = db.User(first_name=first_name, last_name=last_name, email=email, password=password)

            return "User successfully added."


@db_session
@app.route('/chat', methods=['GET'])
def home():
    user_id = request.args.get('user_id')

    try:
        user = db.User[user_id]
    except ObjectNotFound:
        return("User Does not Exsist")

    chats = []
    for c in user.chats:
        
        try:
            last_message = c.messages.select().order_by(lambda m: desc(m.date_created)).limit(1)[0].body
        except IndexError:
            last_message = "Tap to send a message"
        chats.append({"id": c.id, 
                      "last_updated": c.last_updated,
                      "last_message": last_message,
                      "chat_name": user.first_name})
    
    return render_template('chat.html', chats=chats, user=user)
    

@db_session
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db.User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, password=generate_password_hash(form.password.data))
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@db_session
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.User.get(email=email)
        print(user.user_id)
        if user.check_password_hash(form.password.data):
            login_user(user)
            return "It worked!"
        else:
            return "Did not work"
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return "You are logged out"