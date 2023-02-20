import openai
from SumitGPT.Utilities import count_calls


@count_calls
def openAiCallSummary(value):
    # Set your API key
    openai.api_key = "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"
    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-003"

    prompt = f"riassumi il seguente testo in meno di {len(value[0])} parole in utf-8, il testo è il seguente: \n {value[0]}"

    result = value
    try:
        completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=len(value[0]), n=1,
                                               stop=None,
                                               temperature=0.5)
        result = completions.choices[0].text
    except ValueError:
        print(f"token troppo lungo ({len(value)}), ti torno la stringa originale")
        pass
    finally:
        return result
