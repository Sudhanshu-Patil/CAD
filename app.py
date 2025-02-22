from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz

app = Flask(__name__)

# In-memory database with pseudo data
onboarding_status = {
    "emp001": {"Complete HR forms": True, "Attend orientation": False, "Set up IT account": False, "Meet team lead": False},
    "emp002": {"Complete HR forms": True, "Attend orientation": True, "Set up IT account": True, "Meet team lead": False},
    "emp003": {"Complete HR forms": False, "Attend orientation": False, "Set up IT account": False, "Meet team lead": False},
    "emp004": {"Complete HR forms": True, "Attend orientation": True, "Set up IT account": False, "Meet team lead": True},
    "emp005": {"Complete HR forms": True, "Attend orientation": True, "Set up IT account": True, "Meet team lead": True},
    "emp006": {"Complete HR forms": False, "Attend orientation": False, "Set up IT account": False, "Meet team lead": False},
    "emp007": {}
}

# Sample onboarding tasks
onboarding_tasks = ["Complete HR forms", "Attend orientation", "Set up IT account", "Meet team lead"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    employee_id = data.get('employee_id')

    response = process_message(message, employee_id)

    return jsonify({'response': response, 'employee_id': employee_id})

def process_message(message, employee_id):
    message = message.lower()

    if "hello" in message or "hi" in message:
        return "Hello! Welcome to the onboarding chatbot. How can I help you today?"

    if not employee_id:
        if message in onboarding_status:
            employee_id = message
            return process_message("status", employee_id)
        else:
            return "Please provide your employee ID to check your onboarding status. (e.g., emp001)"

    if fuzz.ratio(message, "status") >= 80 or fuzz.ratio(message, "progress") >=80: #fuzzy matching.
        return process_message("status", employee_id)
    
def process_message(message, employee_id):
    message = message.lower()

    if "hello" in message or "hi" in message:
        return "Hello! Welcome to the onboarding chatbot. How can I help you today?"

    if not employee_id:
        if message in onboarding_status:
            employee_id = message
            return process_message("status", employee_id)
        else:
            return "Please provide your employee ID to check your onboarding status. (e.g., emp001)"

    if "status" in message or "progress" in message:
        if employee_id not in onboarding_status:
            return "Sorry, incorrect employee ID. Please provide your employee ID to check your onboarding status. (e.g., emp001)"

        status = onboarding_status[employee_id]
        completed_tasks = [task for task, completed in status.items() if completed]
        pending_tasks = [task for task, completed in status.items() if not completed]

        if not status:
            response = "Your onboarding status is empty. Please contact HR."
        elif not pending_tasks:
            response = "Congratulations! You have completed all onboarding tasks."
        else:
            response = "Your onboarding status:\n"
            if completed_tasks:
                response += "<br><b>Completed tasks:</b><br>"
                for task in completed_tasks:
                    response += f"- {task}<br>"
            if pending_tasks:
                response += "<br><b>Pending tasks:</b><br>"
                for task in pending_tasks:
                    response += f"- {task}<br>"

        response += "<br><button onclick='resetConversation()'>Start New Conversation</button>"
        return response

    if "start onboarding" in message:
        try:
            new_employee_id = message.split(' ')[-1]
            if new_employee_id in onboarding_status:
                return "Onboarding for this employee ID has already started."
            onboarding_status[new_employee_id] = {task: False for task in onboarding_tasks}
            return f"Onboarding started for employee ID: {new_employee_id}."
        except:
            return "Please specify the employee ID to start onboarding. (e.g., emp006)"

    if "complete" in message:
        if employee_id not in onboarding_status:
            return "Sorry, incorrect employee ID. Please provide your employee ID to check your onboarding status. (e.g., emp001)"

        try:
            task_to_complete = ' '.join(message.split(' ')[1:])
            if task_to_complete not in onboarding_tasks:
                return "Invalid task. Please specify a valid task."
            onboarding_status[employee_id][task_to_complete] = True
            return f"Task '{task_to_complete}' marked as completed."
        except:
            return "Please specify the task to complete."

    return "I'm sorry, I don't understand. Please ask me about your onboarding status or how to complete tasks."

if __name__ == '__main__':
    app.run(debug=True)