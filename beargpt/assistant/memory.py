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

def remember(session_id):
    batch_size = 1
    history = chat_history.get_chat_history(session_id)
    index = pinecone.Index(config.config("pinecone_index"))
    # first, call open_ai to summarize the chat history
    long_summary = open_ai.generate_long_summary(history)
    sentences = nltk.sent_tokenize(long_summary)
    for i in range(0, len(sentences), batch_size):
        print("handling batch", i)
        i_end = min(i+batch_size, len(sentences))
        lines_batch = sentences[i:i+batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        print("calculating vectors")
        embeds = calculate_vectors('\n'.join(lines_batch))
        meta = [{'text': line} for line in lines_batch]
        to_upsert = zip(ids_batch, embeds, meta)
        print("upserting vectors")
        index.upsert(vectors=list(to_upsert))

def recall(session_id, query):
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