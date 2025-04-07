from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3 

from statisticss.descriptive import mean, median, mode, variance, std_dev


app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with a strong secret key for production

# initialize history
@app.before_request
def before_request(): 
    if 'history' not in session:
        session['history'] = []

# add new entry to history
def add_to_history(calculation_type, input_data, result_data):
    history_entry = {
        'type': calculation_type,
        'input_data': input_data,
        'result_data': result_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    session['history'].append(history_entry)
    session.modified = True # save session

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

@app.route('/calculations/descriptive', methods=['GET','POST'])
def descriptive_stats(): 
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    datasets = cursor.fetchall()
    conn.close()
    if request.method == 'POST':
        data_input = request.form.get('data')
        try:
            data = [float(x.strip()) for x in data_input.split(',')]
            result = {}
            result['mean'] = mean(data)
            result['median'] = median(data)
            result['mode'] = mode(data)
            result['range'] = max(data) - min(data)
            result['variance'] = variance(data)
            result['std_dev'] = std_dev(data)

            # Quartiles and outliers calculation
            sorted_data = sorted(data)
            q1 = sorted_data[int(len(sorted_data)*0.25)]
            q3 = sorted_data[int(len(sorted_data)*0.75)]
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            outliers = [x for x in data if x < lower_bound or x > upper_bound]
            
            result['quartiles'] = {
                'q1': q1,
                'q2': median(data),
                'q3': q3,
                'iqr': iqr,
                'outliers': outliers
            }
            
            add_to_history('Descriptive Statistics', data, result)
            return render_template('calculations/descriptive.html', 
                                 result=result, 
                                 sample_data=datasets,
                                 input_data=data_input)
        except ValueError:
            error = "Invalid input. Please enter numbers separated by commas."
            return render_template('calculations/descriptive.html', 
                                 error=error,
                                 sample_data=datasets)
    
    return render_template('calculations/descriptive.html', sample_data=datasets)


if __name__ == '__main__':
    app.run(debug=True)