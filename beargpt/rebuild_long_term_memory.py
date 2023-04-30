from assistant import open_ai, chat_history, config, memory

# memory.forget_everything()

# fetch all sessions
chat_sessions = chat_history.get_chat_sessions()
print("Found {} chat sessions".format(len(chat_sessions)))
for session in chat_sessions:
    print("Processing session {}".format(session['name']))
    # fetch all messages for this session
    history = chat_history.get_chat_history(session['id'], raw=True)
    print("Found {} messages".format(len(history)))
    # check if there are any messages with remembered = 1
    remembered_messages = [message for message in history if message["remembered"] == 1]
    # rebuild remembered_messages so it only contains role and content
    print("Found {} remembered messages".format(len(remembered_messages)))
    if len(remembered_messages) > 0:
        remembered_messages = [{"role": message["role"], "content": message["content"]} for message in remembered_messages]
        print(remembered_messages[0])
        print("Rebuilding memory")
        # remember this chat history
        memory.remember(history=remembered_messages)
        
        