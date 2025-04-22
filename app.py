from flask import Flask, jsonify, request
from flask_cors import CORS
from forcastin_by_state import *
from forcastin_by_state import forecast_medicine
from backend import db
from datetime import datetime
import pandas as pd
# from all_med_forcast import all_forecasts_into_dict


app = Flask(__name__)
CORS(app)

# Sample data
medicines = medication_list
states = state_list

selected_time = None
selected_medicine = None
selected_state = None

@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    return jsonify(medicines)

@app.route('/api/states', methods=['GET'])
def get_states():
    return jsonify(states)

@app.route('/api/selection', methods=['POST'])
def receive_selection():
    global selected_time, selected_medicine, selected_state

    data = request.json
    selected_time = data.get('time')
    selected_medicine = data.get('medicine')
    selected_state = data.get('state')

   


    return jsonify({"message": "Selections received"}), 200


@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    if selected_time and selected_medicine and selected_state:
        forecast_value = forecast_medicine(time_period=selected_time, medicine_code=selected_medicine, state=selected_state)
        forecast_medicine_1 = forecast_value.to_dict()

        new_data = {str(key): value for key, value in forecast_medicine_1.items()}
        return jsonify(new_data), 200
    else:
        return jsonify({"error": "Selections not made"}), 400
    

@app.route('/api/all_forecasts', methods=['GET'])
def get_all_forecasts():

    all_forecast_med = list(db.all_med_forcast.find({}, {'_id': 0}))

    return jsonify(all_forecast_med), 200



@app.route('/api/all_forecast_post/', methods=['GET'])
def all_forecasts_into_dict():
    # Initialize an empty dictionary to store all forecasts
    all_forecasts_dict = {}

    for i in medication_list:
        future_pre = forecast_medicine_weekly(medicine_code=i)
        
        # Create a safer version of the dictionary formatting
        forecast_dict_formatted = {}
        for date, value in future_pre.items():
            if hasattr(date, 'strftime'):
                date_key = date.strftime('%Y-%m-%d')
            else:
                date_key = str(date)
            forecast_dict_formatted[date_key] = value
        
        
        all_forecasts_dict[i] = forecast_dict_formatted

    forecast_document = {
        "timestamp": datetime.now(),
        "forecasts": all_forecasts_dict
    }

    
    try:
        db.all_med_forcast.delete_many({})
        
    except Exception as e:
        print(f"Error clearing forecasts from MongoDB: {str(e)}")

   
    try:
        db.all_med_forcast.insert_one(forecast_document)
        
    except Exception as e:
        print(f"Error storing forecasts in MongoDB: {str(e)}")

    return all_forecasts_dict

@app.route('/api/stock', methods=['GET'])
def get_stock_out():
    
    all_medication_forcast = list(db.all_med_forcast.find({}, {'_id': 0}))
    
    forecasts = all_medication_forcast[0]['forecasts']  
    all_forecasts_df = pd.DataFrame(forecasts)
    
    
    current_stock = list(db.medication_current_stock.find({}, {'_id': 0}))
    current_stock_df = pd.DataFrame(current_stock)

    result = {}

    for medicine_code in medicines:
        mask = current_stock_df['medication_name'] == medicine_code
        current_stock = current_stock_df[mask]['current_stock'].iloc[0]

        week_counter = 0
        for forecast in all_forecasts_df[medicine_code]:
            current_stock -= forecast
            week_counter += 1
            if current_stock < 2:
                break
        if week_counter <= 2:
            result[medicine_code] = f"{medicine_code} medication out of stock in {week_counter} weeks"
    
    

    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True, port=7000)