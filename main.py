print("Executing main.py...")

from flask import Flask, request, render_template_string
import numpy as np
import joblib

print("Starting the Flask application...")

app = Flask(__name__)

model_path = 'random_forest_model.pkl'
try:
    clf = joblib.load(model_path)
    print(f"Model successfully loaded from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

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

template = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Route Safety Predictor</title>
  </head>
  <body>
    <h1>Enter Coordinates</h1>
    <form method="post">
      <textarea name="coordinates" rows="10" cols="30" placeholder="Enter one lat,lng per line"></textarea><br>
      <button type="submit">Predict Safety</button>
    </form>
    {% if results %}
      <h2>Results</h2>
      <ul>
        {% for name, prob in results %}
          <li>{{ name }}: {{ prob }} probability of crime</li>
        {% endfor %}
      </ul>
      <p>Overall route risk score: {{ overall }}</p>
    {% endif %}
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Handling request...")
    results = None
    overall = None
    if request.method == 'POST':
        coords_str = request.form.get('coordinates', '')
        print(f"Received coordinates: {coords_str}")
        coords_list = []
        for line in coords_str.strip().splitlines():
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    lat, lng = float(parts[0].strip()), float(parts[1].strip())
                    coords_list.append([lat, lng])
                except ValueError:
                    print(f"Invalid coordinate: {line}")
                    continue
        if coords_list:
            new_locations = np.array(coords_list)
            print(f"Parsed coordinates: {new_locations}")
            try:
                probabilities, cluster_probability = predict_crime_probability(new_locations)
                results = [(f"Location {i+1}", f"{prob:.3f}") for i, prob in enumerate(probabilities)]
                overall = f"{cluster_probability:.3f}"
                print(f"Prediction results: {results}, Overall: {overall}")
            except Exception as e:
                print(f"Error during prediction: {e}")
                results = [("Error", str(e))]
        else:
            results = [("Error", "No valid coordinates provided.")]
    return render_template_string(template, results=results, overall=overall)

if __name__ == '__main__':
    print("Running the Flask app...")
    app.run(debug=True)
