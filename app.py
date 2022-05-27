from flask import Flask, render_template, request, g
from flask import redirect, url_for, abort
import sqlite3
import os

app = Flask(__name__)
gidcount = 0

@app.route("/")
def main():
    return render_template('main.html')

#submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            insert_message(request)

            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id int,
            handle varchar(255),
            message varchar(255)
            );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
#        g.idcount = 0
        return g.message_db

def insert_message(request):
    conn = get_message_db()
    handle = request.form["name"]
    message = request.form["message"]
    global gidcount
    gidcount += 1
    newid = gidcount
    cmd = \
    '''
    INSERT INTO `messages`
    VALUES (?, ?, ?);
    '''
    cursor = conn.cursor()
    cursor.execute(cmd, (newid, handle, message))
    conn.commit()
    conn.close()

@app.route('/view/', methods=['POST', 'GET'])
def view():
    if request.method == 'GET':
        return render_template('view.html')
    else:
#        try:
            msg = random_message(request.form['num'])
            return render_template('view.html', valid=True, msg=msg)
 #       except:
  #          return render_template('view.html', error=True)

def random_message(n):
    conn = get_message_db()
    cmd = \
    '''
    SELECT * FROM messages ORDER BY RANDOM() LIMIT ?;
    '''
    cursor = conn.cursor()
    cursor.execute(cmd, (n,))
    msg = cursor.fetchall()
    conn.close()
    return msg


