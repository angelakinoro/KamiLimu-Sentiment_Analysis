from flask import Flask, request, Response
import psycopg2
import datetime

app = Flask(__name__)

# Database connection function
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Function to get ongoing or stalled projects from the database
def get_projects():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM projects WHERE status = 'stalled' OR status = 'ongoing'")
            projects = cur.fetchall()
            cur.close()
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return None
        finally:
            conn.close()
    return None

# Default route for testing
@app.route('/')
def index():
    return "USSD API is running. Please use the /ussd endpoint for USSD requests."

# testing database connection
@app.route('/test_db')
def test_db():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM projects;")
            projects = cur.fetchall()
            cur.close()
            return f"Projects: {projects}"
        except Exception as e:
            return f"Error: {e}"
        finally:
            conn.close()
    return "Failed to connect to the database."


# USSD endpoint for Africa's Talking callback
@app.route('/ussd', methods=['POST'])
def ussd_callback():
    # Get parameters from Africa's Talking
    session_id   = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text         = request.values.get("text", "")

    # Initialize response
    response = ""

    if text == '':
        # Serve the main menu
        response = "CON Welcome to the Project Feedback Service\n"
        response += "1. Provide Feedback\n"
        response += "2. Exit"
    
    elif text == '1':
        # Display available projects from the database
        projects = get_projects()
        if projects:
            response = "CON Select a Project to Provide Feedback:\n"
            for project in projects:
                response += f"{project[0]}. {project[1]}\n"
        else:
            response = "END No projects available at the moment. Please try again later."
    
    elif text.startswith('1*'):
        # Extract the project ID and prompt for feedback
        project_id = text.split('*')[-1]
        response = f"CON Please enter your feedback for Project {project_id}:"
    
    elif text.count('*') == 2 and text.startswith('1*'):
        # Extract project ID and feedback message
        parts = text.split('*')
        project_id = parts[1]
        message = parts[2]

        # Save feedback to database
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO ussd_messages (user_phone, message, project_id, timestamp, status)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(insert_query, (phone_number, message, int(project_id), datetime.datetime.now(), 'pending'))
                conn.commit()
                cur.close()
                response = "END Thank you for your feedback!"
            except Exception as e:
                print(f"Database error: {e}")
                response = "END Sorry, an error occurred. Please try again later."
            finally:
                conn.close()
        else:
            response = "END Sorry, unable to connect to the database."
    
    elif text == '2':
        response = "END Thank you for using our service."
    
    else:
        response = "END Invalid input. Please try again."

    return Response(response, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
