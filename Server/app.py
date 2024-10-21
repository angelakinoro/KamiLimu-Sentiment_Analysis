from flask import Flask, jsonify, request
import pandas as pd
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)  # CORS for /api/* routes

# Route to get sentiment data from the CSV file
@app.route('/api/sentiments', methods=['GET'])
def get_sentiments():
    # Load data from the sentiment CSV file
    data = pd.read_csv('project_sentiments.csv')
    response = data.to_dict(orient='records')
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

