CITIZENLENS is a sentiment analysis project. It allows users to view the sentiments of a constituency based on the completion of CDF projects. After receiving input from users through a USSD code: * 789 *9085635#
This input is taken through a sentiment analysis model that processes the text data and outputs the result of the analyzed sentiment into a webpage. 

The authors are: 
Rachael Kibicho   
rachaelkibicho@gmail.com 

George Karanja
gkkaranja2@gmail.com

Angela Kinoro
angela.kinoro@riarauniversity.ac.keq

CitizenLens: CDF Project Feedback System   
Project structure from the ussd ->  model -> webpage

PROJECT STRUCTURE 
project/
│
├── app.py                  # The main file to run your Flask app
├── config.py               # Configuration for the project (e.g., database config)
├── models/                 # Directory for machine learning models
│   └── sentiment_model.py   # Sentiment prediction logic
├── database/               # Directory for database-related operations
│   └── db_operations.py     # Database connection and queries
│   └── db_script.sql     # Database connection and queries
├── routes/                 # Directory for Flask route handlers
│   └── ussd_routes.py       # USSD routes
└── utils/                  # Utility functions
    └── helpers.py   
    
Features
USSD Integration: Allows users to share feedback via USSD.
Database: Uses PostgreSQL to store project details and user feedback.
Sentiment Analysis: Leverages a fine-tuned DistilBERT model to analyze the sentiment of feedback.
Dynamic Menus: Provides a USSD menu where users select constituency, project, project state, and urgency.

Getting Started
Prerequisites
Make sure you have the following installed:

Python 3.8+
PostgreSQL
Ngrok (for exposing your local server to the internet, used for USSD callbacks)
A virtual environment (recommended)


Installation
Clone the Repository

First, clone this repository to your local machine: git clone -b george https://github.com/your-repo.git

Navigate into the project directory: cd project
Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate

Install the Required Dependencies: pip install -r requirements.txt


Database Setup
Set Up PostgreSQL: Ensure you have PostgreSQL running and properly configured with the necessary databases and tables. 
Create the required tables (Find the schema in the folder database/ db_script.sql):

Running the Application
Start the Flask App: python app.py
The app should now be running on http://127.0.0.1:5000.

Expose to the Internet (for USSD):
Use Ngrok to expose the local server: ngrok http 5000
Take note of the Ngrok URL (e.g., http://<ngrok-id>.ngrok.io) and update your USSD service provider's callback URL to point to http://<ngrok-id>.ngrok.io/ussd.

Interacting with the Application
USSD Menu: Dial the USSD code to interact with the system. You will be prompted to provide feedback about CDF projects in your constituency.
Feedback Storage: User feedback will be saved in the PostgreSQL database, and the system will perform sentiment analysis using the pre-trained DistilBERT model.

Model Information
This project uses a fine-tuned DistilBERT model to predict the sentiment of feedback messages. The model is loaded from the models/sentiment_model.py file.

Contributing
If you'd like to contribute to this project, please open a pull request or contact us.

License



FOR THE MODEL IN FineTuning1.ipynb:

FOR THE WEBPAGE IN app.py: 


KNOWN ISSUES: 


