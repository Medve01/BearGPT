import openai
import pinecone
from assistant import chat_history, config

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

def store(session_id):
    batch_size = 32
    history = chat_history.get_chat_history(session_id)
    index = pinecone.Index(config.config("pinecone_index"))
    message_count = len(history)
    for message in history:
        text = message["content"]
        for i in range(0, len(text), batch_size):
            print("handling batch", i)
            i_end = min(i+batch_size, len(text))
            lines_batch = text[i:i+batch_size]
            ids_batch = [str(n) for n in range(i, i_end)]
            print("calculating vectors")
            embeds = calculate_vectors(lines_batch)
            meta = [{'text': line} for line in lines_batch]
            to_upsert = zip(ids_batch, embeds, meta)
            print("upserting vectors")
            index.upsert(vectors=list(to_upsert))
