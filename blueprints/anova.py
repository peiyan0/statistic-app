# File: blueprints/anova.py
from flask import Blueprint, request, render_template
import sqlite3

from statisticss.anova import anova
from statisticss.utils import add_to_history

anova_views = Blueprint("anova", __name__)

@anova_views.route('/anova', methods=['GET','POST'])
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
