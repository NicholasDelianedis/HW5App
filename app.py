# ANACONDA

from flask import Flask, render_template, request
from flask import redirect, url_for, abort

app = Flask(__name__)

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
            # call the database function if successful submission

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
        CREATE TABLE IF NOT EXISTS `messages_db` (
            id int,
            handle varchar(63),
            message TEXT NOT NULL
        );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    conn = get_message_db()
    cmd = \
    f'''
    INSERT INTO 'messages_db'
    VALUES (0, request.name, request.message);
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()
