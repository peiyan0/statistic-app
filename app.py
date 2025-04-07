from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3 
import json

from statisticss.descriptive import mean, median, mode, range, variance, std_dev
from statisticss.anova import anova
from statisticss.confidence_intervals import two_pop_CI, dep_data, two_samp_prop
from statisticss.linear_regression import linear_regression


app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with a strong secret key for production

# initialize history
@app.before_request
def before_request(): 
    if 'history' not in session:
        session['history'] = []

# add new entry to history
def add_to_history(calculation_type, input_data, result_data):
    formatted_result = json.loads(json.dumps(result_data, default=lambda x: round(x, 4) if isinstance(x, (int, float)) else x))
    history_entry = {
        'type': calculation_type,
        'input_data': input_data,
        'result_data': formatted_result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    session['history'].insert(0,history_entry) # insert at beginning, show latest on top
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

@app.route('/calculations/anova', methods=['GET', 'POST'])
def anova_calc():
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    datasets = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        groups_input = request.form.get('groups_data')
        try:
            # Process input in format: group1:1,2,3;group2:4,5,6
            groups = {}
            for group_str in groups_input.split(';'):
                if ':' in group_str:
                    group_name, group_data = group_str.split(':', 1)
                    groups[group_name.strip()] = [float(x.strip()) for x in group_data.split(',')]
            
            if len(groups) < 2:
                error = "ANOVA requires at least 2 groups"
                return render_template('calculations/anova.html',
                                    error=error,
                                    sample_data=datasets)
            
            arrays = list(groups.values())
            result = anova(arrays)
            
            add_to_history('ANOVA', groups, result)
            return render_template('calculations/anova.html',
                                result=result,
                                groups=groups,
                                sample_data=datasets,
                                input_data=groups_input)
        except Exception as e:
            error = f"Invalid input format. Please use format: 'group1:1,2,3;group2:4,5,6'. Error: {str(e)}"
            return render_template('calculations/anova.html',
                                 error=error,
                                 sample_data=datasets)
    
    return render_template('calculations/anova.html', sample_data=datasets)

@app.route('/calculations/confidence', methods=['GET', 'POST'])
def confidence_intervals():
    calculation_type = request.args.get('type', 'two_pop')
    conn = sqlite3.connect('dataset/dataset.db')
    cursor = conn.cursor()
    
    if calculation_type == 'two_pop':
        cursor.execute("SELECT * FROM two_pops")
        sample_data = cursor.fetchall()
    elif calculation_type == 'dep_data':
        cursor.execute("SELECT * FROM dataset WHERE num_elements > 5")
        sample_data = cursor.fetchall()
    else:  # two_samp_prop
        sample_data = []  # No specific sample data for proportions
    
    conn.close()
    
    if request.method == 'POST':
        if calculation_type == 'two_pop':
            try:
                n1 = float(request.form.get('n1'))
                x1 = float(request.form.get('x1'))
                s1 = float(request.form.get('s1'))
                n2 = float(request.form.get('n2'))
                x2 = float(request.form.get('x2'))
                s2 = float(request.form.get('s2'))
                t = float(request.form.get('t_value'))
                equal_var = request.form.get('equal_var') == 'true'
                
                args = [[n1, x1, s1], [n2, x2, s2], t, "equal" if equal_var else "unequal"]
                result = two_pop_CI(args)
                
                add_to_history('Two Population CI', 
                             {'n1': n1, 'x1': x1, 's1': s1,
                              'n2': n2, 'x2': x2, 's2': s2,
                              't': t, 'equal_variance': equal_var},
                              result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
            except ValueError:
                error = "Invalid input. Please enter numeric values."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
        
        elif calculation_type == 'dep_data':
            try:
                before = [float(x.strip()) for x in request.form.get('before_data').split(',')]
                after = [float(x.strip()) for x in request.form.get('after_data').split(',')]
                
                if len(before) != len(after):
                    error = "Before and after data must have the same number of values"
                    return render_template('calculations/confidence.html',
                                         error=error,
                                         calculation_type=calculation_type,
                                         sample_data=sample_data)
                
                result = dep_data([before, after])
                
                add_to_history('Dependent Data T-Test',
                             {'before': before, 'after': after},
                             result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
            except ValueError:
                error = "Invalid input. Please enter numbers separated by commas."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
        
        elif calculation_type == 'two_samp_prop':
            try:
                n1 = float(request.form.get('n1_prop'))
                p1 = float(request.form.get('p1'))
                n2 = float(request.form.get('n2_prop'))
                p2 = float(request.form.get('p2'))
                
                result = two_samp_prop([[n1, p1], [n2, p2]])
                
                add_to_history('Two Sample Proportion',
                             {'n1': n1, 'p1': p1, 'n2': n2, 'p2': p2},
                             result)
                
                return render_template('calculations/confidence.html',
                                     result=result,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
            except ValueError:
                error = "Invalid input. Please enter numeric values."
                return render_template('calculations/confidence.html',
                                     error=error,
                                     calculation_type=calculation_type,
                                     sample_data=sample_data)
    
    return render_template('calculations/confidence.html',
                         calculation_type=calculation_type,
                         sample_data=sample_data)

@app.route('/calculations/linear', methods=['GET', 'POST'])
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
            
            equation, r_squared, correlation, predict_func = linear_regression([x_data, y_data])
            
            result = {
                'equation': equation,
                'r_squared': r_squared,
                'correlation': correlation,
                'x_data': x_data,
                'y_data': y_data,
                'predict_func': predict_func
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


if __name__ == '__main__':
    app.run(debug=True)