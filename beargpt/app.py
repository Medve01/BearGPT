from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_bootstrap import Bootstrap
import os, time
from assistant import openai, chat_history, config, memory

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set the secret key for Flask sessions
Bootstrap(app)

def get_default_session_id():
    sessions = chat_history.get_chat_sessions()
    default_session = [session for session in sessions if session['name'] == 'Default session']
    if not default_session:
        default_session_id = chat_history.create_chat_session('Default session')
    else:
        default_session_id = default_session[0]['id']
    return default_session_id

def get_openai_response(message):
    mock_openai = config.config("mock_openai")
    if mock_openai:
        assistant_response = 'testing'
        time.sleep(0.5)
    else:
        assistant_response = openai.generate_response(message)
    return assistant_response

@app.route("/", methods=["GET"])
def index():
    chat_sessions = chat_history.get_chat_sessions()
    return render_template("index.html", empty=True, chat_sessions=chat_sessions)
@app.route("/<session_id>", methods=["GET"])
def chats_get(session_id):
    history = chat_history.get_chat_history(session_id, raw=True)
    chat_sessions = chat_history.get_chat_sessions()
    stream = config.config("openai_stream")
    return render_template("index.html",
                           chat_history=history,
                           chat_sessions=chat_sessions,
                           session_id=session_id)

    # return render_template("index.html", chat_history=history, chat_sessions=chat_sessions)

@app.route("/stream/<session_id>", methods=["GET"])
def chats_get_response_stream(session_id):
    def stream():
        collected_response = ""
        # assistant_response = openai.generate_response_stream(chat_history.get_chat_history(session_id))
        for chunk in openai.generate_response_stream(chat_history.get_chat_history(session_id)):
            if chunk is not None:
                if "\n" in chunk:
                    print("newline found")
                chunk = chunk.replace("\n", "<br/>")
                if chunk != "[[stop]]":
                    collected_response += chunk
                # yield chunk
                yield 'data: %s\n\n' % chunk
        chat_history.store_message(session_id, "assistant", collected_response.replace("<br/>", "\n"))
    print("response_stream")
    return Response(stream(), mimetype='text/event-stream')


@app.route("/<session_id>", methods=["POST"])
def chats_post(session_id):
    user_message = request.form["message"]
    chat_history.store_message(session_id, "user", user_message)
    history = chat_history.get_chat_history(session_id)
    stream = config.config("openai_stream")
    chat_sessions = chat_history.get_chat_sessions()
    if not stream:
        assistant_response = get_openai_response(history)
        chat_history.store_message(session_id, "assistant", assistant_response)
        history = chat_history.get_chat_history(session_id)
        # return redirect(url_for("index") +  session_id)
    return render_template("index.html",
                           chat_history=history,
                           chat_sessions=chat_sessions,
                           streaming=stream,
                           session_id=session_id)

@app.route("/new-session", methods=["POST"])
def create_new_chat_session():
    first_message = request.form["first_message"]
    new_session_id = chat_history.create_chat_session("unnamed session")
    chat_history.store_message(new_session_id, "user", first_message)
    chat_summary = openai.generate_short_summary(chat_history.get_chat_history(new_session_id))
    assistant_response = get_openai_response(chat_history.get_chat_history(new_session_id))
    chat_history.store_message(new_session_id, "assistant", assistant_response)
    chat_history.rename_chat_session(new_session_id, chat_summary)
    return redirect(url_for("chats_get", session_id=new_session_id))

@app.route("/delete_chat_session/<session_id>", methods=["POST"])
def delete_chat_session(session_id):
    chat_history.delete_chat_session(session_id)
    return redirect(url_for("index"))

@app.route("/delete_message/<session_id>/<message_id>", methods=["POST"])
def delete_message(session_id, message_id):
    chat_history.delete_message(session_id, message_id)
    return redirect(url_for("chats_get", session_id=session_id))

@app.route("/remember/<session_id>", methods=["POST"])
def remember(session_id):
    memory.store(session_id)
    return redirect(url_for("chats_get", session_id=session_id))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
