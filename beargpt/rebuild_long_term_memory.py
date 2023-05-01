from assistant import open_ai, chat_history, config, memory

print("   ___                  ___   ___  _____ ")
print("  / __\ ___  __ _ _ __ / _ \ / _ \/__   \\")
print(" /__\/// _ \/ _` | '__/ /_\// /_)/  / /\/")
print("/ \/  \  __/ (_| | | / /_\\\\/ ___/  / /   ")
print("\_____/\___|\__,_|_| \____/\/      \/    ")
print("")                                      
print("")                                      
print("Welcome to the long-term memory rebuild tool")
print("==========================================")
print("This tool will rebuild your Pinecone index.")
print("First, it will check the summaries table for stored summaries.")
print("If not found it will use your chat history.")
print("The pinecone index will only contain summaries xor remembered messages.")
print("If summaries are not found, we will generate and store them.")
print("Generating the summaries uses GPT-4, so that will take a LOT of time.")
print("\033[91mWARNING\033[0m: ", end="")
print("This will delete your existing Pinecone index, effectively BearGPT will forget everything.")
print("==========================================")
# prompt the user if they want to continue
answer = input("Do you want to continue? Type 'yes' to proceed: ")
if answer != "yes":
    print("Aborting")
    exit()
print("Removing all memories from Pinecone...")

memory.forget_everything()

# fetch summaries
print("Fetching summaries from database...")
summaries = chat_history.get_summaries()
print("Found {} summaries".format(len(summaries)))
# if no summaries found, generate them
if len(summaries) == 0:
    print("No summaries found, generating...")
    # fetch all sessions
    chat_sessions = chat_history.get_chat_sessions()
    print("Found {} chat sessions".format(len(chat_sessions)))
    for session in chat_sessions:
        print("Processing session {}".format(session['name']))
        # fetch all messages for this session
        history = chat_history.get_chat_history(session['id'], raw=True)
        remembered_messages = [message for message in history if message["remembered"] == 1]
        print("Found {} remembered messages".format(len(history)))
        # if no remembered messages found, skip
        if len(remembered_messages) == 0:
            print("No remembered messages found, skipping")
            continue
        # rebuild remembered_messages so it only contains role and content
        remembered_messages = [{"role": message["role"], "content": message["content"]} for message in remembered_messages]

        # generate a summary
        summary = open_ai.generate_long_summary(remembered_messages)
        print("Storing summary")
        chat_history.store_summary(session['id'], summary)
    # fetch summaries again
    print("Fetching summaries from database...")
    summaries = chat_history.get_summaries()
    print("Found {} summaries".format(len(summaries)))

# store summaries in memory
print("Storing summaries in memory...")
for summary in summaries:
    memory.remember(summary=summary['summary'])

# # fetch all sessions
# chat_sessions = chat_history.get_chat_sessions()
# print("Found {} chat sessions".format(len(chat_sessions)))
# for session in chat_sessions:
#     print("Processing session {}".format(session['name']))
#     # fetch all messages for this session
#     history = chat_history.get_chat_history(session['id'], raw=True)
#     print("Found {} messages".format(len(history)))
#     # check if there are any messages with remembered = 1
#     remembered_messages = [message for message in history if message["remembered"] == 1]
#     # rebuild remembered_messages so it only contains role and content
#     print("Found {} remembered messages".format(len(remembered_messages)))
#     if len(remembered_messages) > 0:
#         remembered_messages = [{"role": message["role"], "content": message["content"]} for message in remembered_messages]
#         print(remembered_messages[0])
#         print("Rebuilding memory")
#         # remember this chat history
#         memory.remember(history=remembered_messages)
        
        