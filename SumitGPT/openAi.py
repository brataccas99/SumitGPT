import openai

def get_api_key(file_path:str):
    """
    This funtion gets the api key for open ai from a file in the memory
    @param file_path the file path where the key is stored
    @return key the string containig the key
    """
    file = open(file_path, 'r')
    Lines = file.readlines()
    return Lines[0].replace("\n", "")

def openAiCallSummary(text):
    # Set your API key
    openai.api_key = get_api_key("/home/dario/api_key_GPT.txt")
    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-003"

    for section, value in text.items():
        if not text[section]:
            continue
        prompt = f"riassumi il seguente testo in meno di {len(value[0])} parole in utf-8, il testo è il seguente: \n {value[0]}"
        completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=len(value[0]), n=1,
                                               stop=None, temperature=0.5)
        text[section] = completions.choices[0].text
        return text
