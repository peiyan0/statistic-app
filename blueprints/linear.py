# File: blueprins/linear.py
from flask import Blueprint, request, render_template
import sqlite3

from statisticss.linear_regression import linear_regression
from statisticss.utils import add_to_history

linear_views = Blueprint("linear", __name__)

@linear_views.route('/linear', methods=['GET','POST'])
def linear_regression_calc():
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset WHERE num_elements > 5")
    datasets = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        x_input = request.form.get('x_data')
        y_input = request.form.get('y_data')
        try:
            x_data = [float(x.strip()) for x in x_input.split(',')]
            y_data = [float(y.strip()) for y in y_input.split(',')]
            
            if len(x_data) != len(y_data):
                error = "X and Y data must have the same number of values"
                return render_template('calculations/linear.html',
                                     error=error,
                                     sample_data=datasets)
            
            equation, r_squared, correlation = linear_regression([x_data, y_data])
            
            result = {
                'equation': equation,
                'r_squared': r_squared,
                'correlation': correlation,
                'x_data': x_data,
                'y_data': y_data
            }
            
            add_to_history('Linear Regression', 
                          {'x': x_data, 'y': y_data}, 
                          result)
            
            return render_template('calculations/linear.html',
                                 result=result,
                                 sample_data=datasets,
                                 x_data=x_input,
                                 y_data=y_input)
        except ValueError:
            error = "Invalid input. Please enter numbers separated by commas."
            return render_template('calculations/linear.html',
                                 error=error,
                                 sample_data=datasets)
    
    return render_template('calculations/linear.html', sample_data=datasets)
