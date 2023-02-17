import openai


def openAiCallSummary(text):
    # Set your API key
    openai.api_key = "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"
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
