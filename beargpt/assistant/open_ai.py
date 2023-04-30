import json
import openai
from assistant import config, memory

# Initialize the OpenAI API key
openai.api_key = config.config("openai_api_key")

def create_system_prompt(assistant, query):
    base_prompt = {"role": "system", "content": config.config("assistant_prompts")[assistant]}
    remember = memory.recall(query)
    base_prompt["content"] += remember
    return base_prompt

def generate_response_stream(chat_history):
    query = chat_history[-1]["content"]
    system_prompt = create_system_prompt("writer_assistant", query)
    messages = [system_prompt] + chat_history
    completion = openai.ChatCompletion.create(
        model = config.config("openai_model"),
        messages = messages,
        stream = True
    )
    for chunk in completion:
        chuck_str = chunk["choices"][0].get("delta", {}).get("content")
        if chuck_str is not None:
    #         yield 'data: %s\n\n' % chuck_str.replace("\n", "<br>")
            yield chuck_str
    # yield 'data: {{stop}}\n\n'
    yield "[[stop]]"

def generate_response(chat_history):
    query = chat_history[-1]["content"]
    system_prompt = create_system_prompt("writer_assistant", query)
    messages = [system_prompt] + chat_history
    completion = openai.ChatCompletion.create(
        model = config.config("openai_model"),
        messages = messages
    )
    response = completion.choices[0].message.content
    return response

def generate_short_summary(chat_history):
    system_prompt = {"role": "system", "content": config.config("assistant_prompts")["titler"]}
    prompt = {"role": "user", "content": "Please summarize this previous message in 5 words or less:\n" + chat_history[-1]["content"]}
    messages = [system_prompt, prompt]
    completion = openai.ChatCompletion.create(
        model = config.config("openai_model_for_summary"),
        messages = messages
    )
    response = completion.choices[0].message.content
    return response

def generate_long_summary(chat_history):
    system_prompt = {"role": "system", "content": config.config("assistant_prompts")["writer_assistant"]}
    messages = [system_prompt] + chat_history + [{"role": "user", "content": config.config("assistant_prompts")["summarizer"]}]
    completion = openai.ChatCompletion.create(
        model = config.config("openai_model"),
        messages = messages
    )
    response = completion.choices[0].message.content
    print("Long summary to store:", response)
    return response
