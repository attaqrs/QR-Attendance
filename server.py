from flask import Flask, request, redirect, url_for, render_template, flash
import socket as s
import datetime
import hashlib
import db

app = Flask(__name__)
app.secret_key = str(datetime.datetime.now()).encode()
hash = ''
private_hash = ''

@app.route('/')
def root():
    return 'Webpage still under construction'

@app.route('/start_session')
def start_session():
    global private_hash
    if private_hash:
        return 'A session is already in progress.'
    section = request.args.get('section')
    if not section:
        return 'Section not given.'
    if (len(section) != 1) or section not in 'ABCDEFGHIJKLMNO':
        return 'Invalid section.'
    db.start_session(section)
    private_hash = hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()
    return hash + ' ' + private_hash

@app.route('/end_session')
def end_session():
    global private_hash
    given_private_hash = request.args.get('private_hash')
    if not given_private_hash:
        return 'Private hash not given. Session not ended'
    if given_private_hash != private_hash:
        return 'Invalid private hash provided. Session not ended'
    db.end_session()
    return 'Session ended successfully'

@app.route('/mark_attendance')
def mark_attendance():
    given_hash = request.args.get('hash')
    if not given_hash:
        return 'Hash not given. Attendance not marked.'
    if given_hash != hash:
        return 'Invalid hash provided. Attendance not marked.'
    srn = request.cookies.get('srn')
    if not srn:
        return redirect(url_for('set_srn', hash=given_hash))
    result = db.mark_attendance(srn)
    if not result:
        flash('Invalid SRN. Try again:')
        return redirect(url_for('set_srn', hash=given_hash))
    return result

@app.route('/get_cur_attendance')
def get_cur_attendance():
    return db.get_cur_attendance()

@app.route('/set_srn')
def set_srn():
    return render_template('set_srn.html')

if __name__ == '__main__':
    hash = hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()
    # app.run(host='192.168.1.6', port=8080)
    app.run(host=s.gethostbyname(s.gethostname()), port=8080)
