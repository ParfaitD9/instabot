import json
import os
from flask import Flask, jsonify, render_template, request
from utils.main import Crawler
from utils.orm import add_new_message, all_users, messages_existants \
    , set_message_default, get_default_message, not_pinned_users

#Hello

app = Flask(__name__)

c = Crawler(auth= True)

@app.route('/')
def auth():
    if request.method == 'POST':
        pass
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home-remake.html')

@app.route('/new-message', methods= ['POST'])
def new_message():
    message, default = request.form.get('message'), request.form.get('set-default')
    r = add_new_message(message)
    return jsonify(r)
    
@app.route('/messages')
def messages():
    return render_template('messages-remake.html')

@app.route('/default', methods= ['POST'])
def default_message():
    pk = int(request.form.get('msg'))
    r = set_message_default(pk)

    return jsonify(r)

@app.route('/existants-messages')
def existants_messages():
    r = messages_existants()

    return jsonify(r)

@app.route('/send', methods= ['GET', 'POST'])
def send_dm():
    username = request.args.get('user')
    msg = get_default_message().get('data')
    
    r = c.send_message(username, msg)

    return jsonify(r)
    
@app.route('/sendmass')
def send_mass():
    users = json.loads(request.args.get('users'))
    r = c.send_mass_message(users, message= get_default_message().get('data'))

    return r

@app.route('/followers')
def followers():
    print('Request datas is', request.args)
    user = request.args.get('username')
    r = c.get_followers(user)

    return jsonify(r)

@app.route('/c-logout')
def logout_crawler():
    r = c.logout()
    return jsonify(r)

@app.route('/api/users/all')
def users():
    r = all_users()
    return jsonify(r)

@app.route('/users/all')
def users_html():
    return render_template('users.html')

@app.route('/users/not')
def users_not():
    r = not_pinned_users()

    return jsonify(r)

@app.route('/v1/connected')
def is_connected():
    return jsonify(c.connected)

@app.route('/v1/message')
def provide_default_message():
    r = get_default_message()
    return jsonify(r)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=os.environ.get('PORT'), debug= False)