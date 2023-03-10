import time

import openai
import tiktoken

from SumitGPT.Utilities import count_calls


def get_api_key(file_path: str):
    """
    This funtion gets the api key for open AI from a file in the memory
    @param file_path the file path where the key is stored
    @return key the string containig the key
    """
    file = open(file_path, 'r')
    Lines = file.readlines()
    return Lines[0].replace("\n", "")


@count_calls
def openAiCallSummary(text: str, prompt: str):
    """
    This function makes the call to openAI to execute a custom prompt with the specified text

    @param prompt the prompt used for the call at openAI
    @param text the text to use for the query
    """
    # Set your API key
    openai.api_key = get_api_key("C:/Users/roach/Desktop/openAI_api_key.txt")
    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-002"
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("text-davinci-002")
    prompt_to_send = f"{prompt} {text}"
    encoding.encode(prompt_to_send)
    tokens = 4000 - len(encoding.encode(prompt_to_send)) - int((len(encoding.encode(prompt_to_send)) * 0.3))
    try:
        completions = openai.Completion.create(engine=model_engine, prompt=prompt_to_send,
                                               max_tokens=tokens,
                                               n=1,
                                               stop=None,
                                               temperature=0.5)
        return completions.choices[0].text
    except Exception as e:
        print('Error: ', e)
        time.sleep(180)
        return openAiCallSummary(text, prompt)


def splitString(test):
    # dimezza la stringa test se è più lunga di 4097 caratteri
    mid = len(test) // 2
    strings = [test[:mid], test[mid:]]
    return strings


def checkLength(text, prompt):
    max_tokens = 4000
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("text-davinci-002")
    encoding.encode(text)
    if (max_tokens - len(encoding.encode(text + prompt))) <= 0:
        result = splitString(text)
        return [openAiCallSummary(s, prompt) for s in result]
    else:
        return openAiCallSummary(text, prompt)


def openAIService(text: list,
                  prompt: str = "riassumi il seguente testo usando meno caratteri della sua dimensione originale usando codifica utf-8:\n"):
    listBack = []
    result = ""
    if len(text) > 1:
        for i in text:
            backValue = checkLength(i, prompt)
            if isinstance(backValue, list):
                for b in backValue:
                    listBack.append(b)
            else:
                listBack.append(backValue)
    else:
        backValue = checkLength(text[0], prompt)
        if isinstance(backValue, list):
            for b in backValue:
                listBack.append(b)
        else:
            listBack.append(backValue)

    for i in range(len(listBack)):
        result += ' ' + listBack[i]

    return result
