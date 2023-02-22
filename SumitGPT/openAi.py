import openai
from SumitGPT.Utilities import count_calls


def get_api_key(file_path: str):
    """
    This funtion gets the api key for open ai from a file in the memory
    @param file_path the file path where the key is stored
    @return key the string containig the key
    """
    file = open(file_path, 'r')
    Lines = file.readlines()
    return Lines[0].replace("\n", "")


@count_calls
def openAiCallSummary(text: str,
                      prompt: str = "riassumi il seguente testo in meno caratteri della sua dimensione originale con solo caratteri utf-8. il testo è il seguente:\n"):
    """
    This function makes the call to openAI to execute a custom prompt with the specified text

    @param prompt the prompt used for the call at openAI
    @param text the text to use for the query
    """
    # Set your API key
    openai.api_key = get_api_key("C:/Users/roach/Desktop/openAI_api_key.txt")
    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-003"

    prompt_to_send = f"{prompt} \n {text}"
    completions = openai.Completion.create(engine=model_engine, prompt=prompt_to_send, max_tokens=len(text), n=1, stop=None,
                                           temperature=0.5)
    return completions.choices[0].text
