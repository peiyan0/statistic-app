# File: blueprints/confidence.py
from flask import Blueprint, request, render_template
import sqlite3

from statisticss.confidence_intervals import two_pop_CI, dep_data, two_samp_prop
from statisticss.utils import add_to_history

confidence_views = Blueprint("confidence", __name__)

@confidence_views.route('/confidence', methods=['GET','POST'])
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
        cursor.execute("SELECT * FROM dataset WHERE num_elements = 2")
        sample_data = cursor.fetchall()  
    
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
                n1 = float(request.form.get('n1'))
                p1 = float(request.form.get('p1'))
                n2 = float(request.form.get('n2'))
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
