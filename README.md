# my-python-web-app/my-python-web-app/README.md

# My Python Web App

This is a simple web application built with Flask that allows users to input latitude and longitude coordinates for locations in New York City. The application predicts the probability of crime occurrence based on the provided coordinates.

## Features

- User-friendly interface for inputting coordinates.
- Displays the predicted probability of crime occurrence for the entered locations.
- Visually appealing design.

## Requirements

- Python 3.x
- Flask
- NumPy
- Joblib

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd my-python-web-app
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
python src/app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Enter the latitude and longitude coordinates in the provided fields.
3. Click the submit button to see the predicted probability of crime occurrence.

## License

This project is licensed under the MIT License.