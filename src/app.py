from flask import Flask, render_template, request
import numpy as np
import joblib
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Load the trained model
model_path = 'random_forest_model.pkl'
clf = joblib.load(model_path)

geolocator = Nominatim(user_agent="crime-probability-app")

def predict_crime_probability(new_locations):
    if hasattr(clf, "predict_proba"):
        probabilities = clf.predict_proba(new_locations)
        if probabilities.shape[1] == 2:
            cluster_probability = probabilities[:, 1].mean()
            return probabilities[:, 1], cluster_probability
        else:
            raise ValueError("Unexpected shape of probabilities array: expected 2 columns, got {}".format(probabilities.shape[1]))
    else:
        raise ValueError("The classifier does not support probability prediction.")

def address_to_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    probabilities = None
    cluster_probability = None
    address = None
    lat_value = None
    lon_value = None
    location_names = None
    
    if request.method == 'POST':
        input_address = request.form.get('address')
        if input_address:
            lat_value, lon_value = address_to_coordinates(input_address)
            address = input_address
            
            if lat_value and lon_value:
                new_locations = np.array([[lat_value, lon_value]])
                probabilities, cluster_probability = predict_crime_probability(new_locations)
                probabilities = probabilities.tolist()
                location_names = ["Location"] * len(probabilities)
            else:
                address = "Could not find coordinates for the provided address"

    return render_template('index.html', 
                         probabilities=probabilities,
                         cluster_probability=cluster_probability,
                         address=address,
                         latitude=lat_value,
                         longitude=lon_value,
                         location_names=location_names,
                         zip=zip)

if __name__ == '__main__':
    app.run(debug=True)