import openai
from SumitGPT.Utilities import count_calls


def get_api_key(file_path:str):
    """
    This funtion gets the api key for open ai from a file in the memory
    @param file_path the file path where the key is stored
    @return key the string containig the key
    """
    file = open(file_path, 'r')
    Lines = file.readlines()
    return Lines[0].replace("\n", "")


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
