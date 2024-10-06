

# In[1]:


import sqlite3

conn = sqlite3.connect('CITIZENLENS.db')
cursor = conn.cursor()


# DATABASE IN 3RD NORMALIZATION FORM
#

# In[2]:


cursor.execute('''
CREATE TABLE IF NOT EXISTS Input (
    InputID INTEGER PRIMARY KEY,
    TimeOfInput DATETIME
)
''')

# Create User Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY,
    PhoneNumber TEXT,
    Subscribed INTEGER
)
''')

# Create Year Table (creating this before Project table due to foreign key constraint)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Year (
    YearID INTEGER PRIMARY KEY,
    AllocationInYear INTEGER,
    Unused INTEGER

)
''')

# Create Project Table
cursor.execute("DROP TABLE IF EXISTS Project")

cursor.execute('''
 CREATE TABLE IF NOT EXISTS Project (
     ProjectID VARCHAR(50) PRIMARY KEY,  -- Specify a length, e.g., 50
     YearID INTEGER,
     ProjectName TEXT,
     GovernmentMoneyDisbursed INTEGER,
     FOREIGN KEY (YearID) REFERENCES Year(YearID)
 )
 ''')

# Create Constituency Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Constituency (
    ConstituencyID INTEGER PRIMARY KEY,
    ConstituencyName TEXT
)
''')

# Create AG Report Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS AG_Report (
    AGReportID INTEGER PRIMARY KEY,
    ConstituencyID INTEGER,
    ReportDetails TEXT,
    FOREIGN KEY (ConstituencyID) REFERENCES Constituency(ConstituencyID)
)
''')

# Create Activities Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Activities (
    ActivityID INTEGER PRIMARY KEY,
    ProjectID VARCHAR,
    ActivityDescription TEXT,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
)
''')

# Create Input_User_Constituency_Project Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Input_User_Constituency_Project (
    InputID INTEGER,
    UserID INTEGER,
    ConstituencyID INTEGER,
    ProjectID VARCHAR,
    PRIMARY KEY (InputID, UserID, ConstituencyID, ProjectID),
    FOREIGN KEY (InputID) REFERENCES Input(InputID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ConstituencyID) REFERENCES Constituency(ConstituencyID),
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
)
''')

# Commit the changes
conn.commit()
conn.close


# In[3]:


conn = sqlite3.connect('CITIZENLENS.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables in CITIZENLENS.db:')
for table in tables:
    print(table[0])


conn.close()


import africastalking
username = 'sandbox'
api_key = 'atsk_0a9f05b65c65bed303c62628ed43d1bdcdd988f6ced7645c3a58d203c55e2ccb74e6f7b0'

#initializing sdk
africastalking.initialize(username, api_key)

#getting the ussd service
ussd = africastalking.USSD



from flask import Flask, request, Response
from pyngrok import ngrok
import sqlite3

app = Flask(__name__)

@app.route('/ussd', methods=['GET', 'POST'])
def ussd_callback():
    text = request.values.get("text", "")
    inputs = text.split("*") if text else []  # Handling empty text input

    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)

    with sqlite3.connect('CITIZENLENS.db') as conn:
        cursor = conn.cursor()

        if text == "":
            # Layer 1: Initial menu
            response = "CON Welcome to Citizen Lens\n"
            response += "1. Tell us about a CDF project\n"
            response += "2. View projects\n"

        elif len(inputs) >= 1 and inputs[0] in ["1", "2"]:
            # Layer 2: Select constituency
            if len(inputs) == 1:
                cursor.execute("SELECT ConstituencyID, ConstituencyName FROM Constituency")
                constituencies = cursor.fetchall()
                if constituencies:
                    response = "CON Select your constituency:\n"
                    for i, constituency in enumerate(constituencies, 1):
                        response += f"{i}. {constituency[1]}\n"
                else:
                    response = "END No constituencies available."

            elif len(inputs) == 2:
                constituency_id = int(inputs[1])  # Constituency chosen
                if inputs[0] == "1":
                    # Layer 3A: Talk about a project
                    cursor.execute("SELECT ProjectID, ProjectName FROM Project WHERE ConstituencyID=?", (constituency_id,))
                    projects = cursor.fetchall()
                    if projects:
                        response = "CON Select the project you want to talk about:\n"
                        for i, project in enumerate(projects, 1):
                            response += f"{i}. {project[1]}\n"
                    else:
                        response = "END No projects available for this constituency."
                elif inputs[0] == "2":
                    # Layer 3B: View projects
                    cursor.execute("SELECT ProjectID, ProjectName FROM Project WHERE ConstituencyID=?", (constituency_id,))
                    projects = cursor.fetchall()
                    if projects:
                        response = "CON Select a project to view details:\n"
                        for i, project in enumerate(projects, 1):
                            response += f"{i}. {project[1]}\n"
                    else:
                        response = "END No projects available for this constituency."

        elif len(inputs) == 3 and inputs[0] == "1":
            # Layer 4A: After selecting project for feedback
            response = "CON Please tell us what you think about the project:\n"

        elif len(inputs) == 4 and inputs[0] == "1":
            # Layer 5A: Save feedback and ask if they want updates
            feedback = inputs[3]
            project_id = int(inputs[2])
            constituency_id = int(inputs[1])

            cursor.execute("INSERT INTO Input (PhoneNumber, TimeOfInput) VALUES (?, datetime('now'))", (phone_number,))
            input_id = cursor.lastrowid
            cursor.execute("INSERT INTO Input_User_Constituency_Project (InputID, UserID, ConstituencyID, ProjectID) VALUES (?, ?, ?, ?)",
                           (input_id, 1, constituency_id, project_id))  # Adjust UserID as necessary
            conn.commit()

            response = "CON Would you like to receive updates about this project?\n"
            response += "1. Yes\n"
            response += "2. No\n"

        elif len(inputs) == 5 and inputs[0] == "1":
            # Layer 6A: Handle subscription choice
            subscribed = 1 if inputs[4] == "1" else 0
            cursor.execute("UPDATE User SET subscribed = ? WHERE PhoneNumber = ?", (subscribed, phone_number))
            conn.commit()
            response = "END Thank you! Your feedback has been recorded and your preferences updated."

        elif len(inputs) == 3 and inputs[0] == "2":
            # Layer 4B: View activities and funds
            project_id = int(inputs[2])
            cursor.execute("SELECT ActivityDescription, GovernmentMoneyDisbursed FROM Activities WHERE ProjectID=?", (project_id,))
            activities = cursor.fetchall()
            if activities:
                response = "CON Activities for the project:\n"
                for i, activity in enumerate(activities, 1):
                    response += f"{i}. {activity[0]} - {activity[1]} KES\n"
                response += "END Thank you for using Citizen Lens."
            else:
                response = "END No activities found for the selected project."

        else:
            response = "END Invalid choice."

    return Response(response, mimetype="text/plain")


# Start an ngrok tunnel
public_url = ngrok.connect(5000)
print(f" * ngrok tunnel: {public_url}")

# Just for good practice
if __name__ == "__main__":
    app.run(debug=True)
