from forcastin_by_state import *
from datetime import datetime
from backend import db

def all_forecasts_into_dict():
    
    all_forecasts_dict = {}

    for i in medication_list:
        future_pre = forecast_medicine_weekly(medicine_code=i)
        
       
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

    # Insert into MongoDB collection
    try:
        db.all_med_forcast.insert_one(forecast_document)
        
    except Exception as e:
        print(f"Error storing forecasts in MongoDB: {str(e)}")

    return all_forecasts_dict


