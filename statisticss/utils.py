from flask import session
from datetime import datetime
import json

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
