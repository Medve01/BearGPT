import openai
import pinecone
import nltk
from assistant import chat_history, config, open_ai

openai.api_key = config.config("openai_api_key")
pinecone.init(
    api_key=config.config("pinecone_api_key"),
    environment=config.config("pinecone_environment")
)

def calculate_vectors(text):
    model = "text-embedding-ada-002"
    response = openai.Embedding.create(
        engine=model,
        input=[text]
    )
    embeds = [record['embedding'] for record in response['data']]
    return embeds

def store_in_pinecone(content):
    sentences = nltk.sent_tokenize(content)
    batch_size = 1
    index = pinecone.Index(config.config("pinecone_index"))
    
    # then, calculate the embeddings for each sentence
    print("Calculating and updating embeddings for %d sentences" % len(sentences))
    for i in range(0, len(sentences), batch_size):
        i_end = min(i+batch_size, len(sentences))
        lines_batch = sentences[i:i+batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        embeds = calculate_vectors('\n'.join(lines_batch))
        meta = [{'text': line} for line in lines_batch]
        # then, upsert the embeddings into pinecone
        to_upsert = zip(ids_batch, embeds, meta)
        index.upsert(vectors=list(to_upsert))


def remember(session_id=None, summary=None):
    """

    Args:
        session_id (str, optional): A session id to remember. Defaults to None.
        summary (str, optional): A ready-made summary to remember. Defaults to None.

    This function is used in two places:
        1) when a user presses the "Remember this chat session" button
            In this case, session_id is passed, summary must be None
            We'll fetch the chat history from the database, skip the remembered messages, generate a summary, and upsert the embeddings
        2) when rebuild_long_term_memory.py is run
            In this case, session_id is None, summary is passed
            We use the passed summary to usert the embeddings
    """
    if session_id is None and summary is None:
        raise Exception("Must provide either session_id or chat_history")
    if summary is None:
        history = chat_history.get_chat_history(session_id, skip_remembered=True)

        # first, call open_ai to summarize the chat history
        print("Generating long summary")
        long_summary = open_ai.generate_long_summary(history)
        print(long_summary)
        # let's store the summary in the database for good measure
        chat_history.store_summary(session_id, long_summary)
    else:
        long_summary = summary
    store_in_pinecone(long_summary)
    # finally, update the chat history to mark the messages as remembered
    if session_id is not None:
        chat_history.update_remembered(session_id)

def recall(query):
    index = pinecone.Index(config.config("pinecone_index"))
    embeds = calculate_vectors(query)
    results = index.query(queries=embeds, top_k=5, include_metadata=True)
    print(results)
    for_prompt = '\nSome relevant information from previous conversations:\n'
    for match in results['results'][0]['matches']:
        for t in match['metadata']['text']:
            for_prompt += t
        for_prompt += '\n'
    return for_prompt

def forget_everything():
    index = pinecone.Index(config.config("pinecone_index"))
    index.delete(namespace='', delete_all=True)