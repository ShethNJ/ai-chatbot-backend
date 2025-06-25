import socketio

sio = socketio.Client()
session_id = "session5234"
user_id = "user5234"
waiting_for_response = False

@sio.event
def connect():
    print(" Connected to server")
    ask_question()

@sio.event
def connect_error(data):
    print(" Failed to connect:", data)

@sio.event
def disconnect():
    print(" Disconnected from server")

@sio.event
def bot_response(data):
    global waiting_for_response
    print(" Bot says:", data.get("message", "[No message]"))
    if data.get("escalated"):
        print(" Escalation triggered!")
    waiting_for_response = False
    ask_question()

def ask_question():
    global waiting_for_response
    if waiting_for_response:
        return

    user_msg = input("\n You: ")
    if user_msg.lower() in ["exit", "quit", "bye"]:
        print(" Exiting chat...")
        sio.disconnect()
        return

    waiting_for_response = True
    sio.emit("message", {
        "message": user_msg,
        "user_id": user_id,
        "session_id": session_id
    })

try:
    sio.connect("http://localhost:8000", socketio_path="/socket.io")
    sio.wait()
except Exception as e:
    print(f" Exception during connection: {e}")
