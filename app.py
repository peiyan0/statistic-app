from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3 
import json

from blueprints.anova import anova_views
from blueprints.confidence import confidence_views
from blueprints.descriptive import descriptive_views
from blueprints.linear import linear_views

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with a strong secret key for production

app.register_blueprint(anova_views, url_prefix='/calculations')
app.register_blueprint(confidence_views, url_prefix='/calculations')
app.register_blueprint(descriptive_views, url_prefix='/calculations')
app.register_blueprint(linear_views, url_prefix='/calculations')

# initialize history
@app.before_request
def before_request(): 
    if 'history' not in session:
        session['history'] = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculations')
def calculations():
    return render_template('calculations.html')

@app.route('/datasets')
def datasets():
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    datasets = cursor.fetchall()
    cursor.execute("SELECT * FROM two_pops")
    two_pops = cursor.fetchall()
    conn.close()
    return render_template('datasets.html',
        datasets=datasets,
        two_pops=two_pops
    )           

@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/history')
def history():
    return render_template('history.html', history=session.get('history',[]))

if __name__ == '__main__':
    app.run(debug=True)