# File: blueprints/descriptive.py
from flask import Blueprint, request, render_template
import sqlite3

from statisticss.descriptive import mean, median, mode, range, variance, std_dev
from statisticss.utils import add_to_history

descriptive_views = Blueprint("descriptive", __name__)

@descriptive_views.route('/descriptive', methods=['GET','POST'])
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
            result['range'] = range(data)
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
