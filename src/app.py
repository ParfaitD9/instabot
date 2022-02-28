import os
import re
from flask import Flask, jsonify, render_template, request
from utils.main import Crawler
import sqlite3

app = Flask(__name__)

c = Crawler(auth= True)

@app.route('/')
def auth():
    if request.method == 'POST':
        pass
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/send', methods= ['GET', 'POST'])
def send_dm():
    if request.method == 'POST':
        username = request.form.get('user')
        msg = request.form.get('message')
        
        r = c.send_message(username, msg)
    
        return jsonify(r)
    return jsonify({'status' : False, 'message':'GET method not allowed for this endpoint'})

@app.route('/followers')
def followers():
    print('Request datas is', request.args)
    user = request.args.get('username')
    r = c.get_followers(user)

    return jsonify(r)

@app.route('/notpinned')
def user_listing():
    con = sqlite3.connect('../datas.db3')
    cur = con.cursor()

    try:
        query = 'SELECT (name, pinned) FROM users WHERE pinned = ?'
        cur.execute(query, (0,))
    except Exception as e:
        print(e)
        return jsonify({
            'status' : False,
            'data' : []
        })
    else:
        return jsonify({
            'status' : True,
            'data' : cur.fetchall()
        })
    finally:
        con.close()



if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=os.environ.get('PORT'))