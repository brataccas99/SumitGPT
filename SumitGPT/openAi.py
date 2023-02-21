import openai
from SumitGPT.Utilities import count_calls


def getApiKey():
    with open('C:/Users/roach/Desktop/openAI_api_key.txt', 'r') as f:
        contents = f.read()
    return contents


@count_calls
def openAiCallSummary(value):
    # Set your API key
    openai.api_key = getApiKey()
    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-003"

    prompt = f"riassumi il seguente testo in meno di {len(value)} parole in utf-8, il testo è il seguente: \n {value}"
    completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=len(value[0]), n=1, stop=None,
                                           temperature=0.5)
    return completions.choices[0].text
