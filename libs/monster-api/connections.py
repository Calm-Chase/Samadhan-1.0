from openai import OpenAI
from settings import *
import os


generation_model_name : str


temperature:float= 0.9
top_p=0.9
max_tokens:int= 2048
stream: bool= True
llm_name:str ="Meta-Llama"



monster_client = OpenAI(
            base_url="https://llm.monsterapi.ai/v1/",
            api_key=str(MONSTER_API_KEY))


monster_ai_model_name = {
                "Google-Gemma": "google/gemma-2-9b-it",
                "Mistral": "mistralai/Mistral-7B-Instruct-v0.2",
                "Microsoft-Phi": "microsoft/Phi-3-mini-4k-instruct",
                "Meta-Llama": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            }

message=[
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'\''m quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'\''m cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}]



response  = monster_client.chat.completions.create(
    model=monster_ai_model_name[llm_name],
    messages=message,
    temperature = temperature,
    top_p = top_p,
    max_tokens = max_tokens,
    stream=stream
)


generated_text = ""
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        generated_text += chunk.choices[0].delta.content
        

print(generated_text)

