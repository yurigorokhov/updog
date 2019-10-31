from flask import current_app as app
from . import db
from flask import render_template, request, redirect, url_for, jsonify, Response
from pony.orm import *
from .forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user


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
            message = db.Message(body=body, sender_id=user_id, chat=chat_id)

            return "Message successfully added"
        

@app.route('/api/chats', methods=['GET', 'POST'])
def chats():
    user_id = request.args.get('user_id')


    if request.method == 'GET':
        try:
            user = db.User[user_id]
        except ObjectNotFound:
            return("User Does not Exsist")

        chats = []
        for c in user.chats:
            chats.append({"id": c.id,
                            "last_updated": c.last_updated})

        return jsonify(chats)

    if request.method == 'POST':
        pass


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


@app.route('/chat', methods=['GET'])
def home():
    user_id = request.args.get('user_id')

    try:
        user = db.User[user_id]
    except ObjectNotFound:
        return("User Does not Exsist")

    chats = []
    for c in user.chats:
        chats.append({"id": c.id, 
                      "last_updated": c.last_updated,
                      "last_message": c.messages.select().order_by(lambda m: desc(m.date_created)).limit(1)[0].body,
                      "chat_name": user.first_name})
    
    return render_template('chat.html', chats=chats, user=user)
    




# User log in and log out.  Not yet fully implemented

@db_session
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        possible_user = db.User.get(email=email)
        if possible_user.password == password:
            login_user(possible_user)
            return "It worked!"
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return "You are logged out"