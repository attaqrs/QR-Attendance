from flask import Flask, request, redirect, url_for, render_template
import hashlib
import datetime
import db

app = Flask(__name__)

@app.route('/')
def root():
    return 'Main webpage still under construction :grin:'

@app.route('/start_session')
def start_session():
    hash = hashlib.md5(bytes(str(datetime.date.today()), encoding="utf-8")).hexdigest()
    url =  f'{request.url_root}mark_attendance?hash={hash}'
    db.start_session(hash)
    return url

@app.route('/end_session')
def end_session():
    hash = request.args.get('hash')
    if not hash:
        return '[ERROR]: Hash not provided.'
    present_prns = db.end_session(hash)
    return present_prns

@app.route('/mark_attendance')
def mark_attendance():
    hash = request.args.get('hash')
    if not hash:
        return '[ERROR]: Hash not provided.'
    prn = request.cookies.get('prn')
    if not prn:
        return redirect(url_for('set_prn', hash=hash))
    response = db.mark_attendance(hash, prn)
    return response

@app.route('/set_prn')
def set_prn():
    return render_template('set_prn.html')

