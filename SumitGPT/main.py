from SumitGPT.openAi import openAIService
from Utilities import verifyValueLength, makeSingleValuePerKey, removeUselessKeys, stringedDiz, removeSpaces
from pdfManipulation import write_text_to_pdf, extractFromInput


# questa func elimina le chiavi con value vuoti senza perdere informazioni
def reformatDiz(d: dict):
    prev_key, prev_value = next(iter(d.items()))  # Get the first key in the dictionary
    keys_to_remove = []
    for key, value in d.items():
        if (not value and not key) or (key == ' ' and value == '') or (key == ' ' and value == []):
            prev_key, prev_value = next(iter(d.items()))
            keys_to_remove.append(key)
        if key != prev_key:
            if (key != ' ' and value == ' ') or (key != ' ' and value == []):
                prev_value = f"{prev_value} {key}"  # concatenate key to previous value
                d[prev_key] = prev_value.replace("[", "").replace("]", "").replace("'", "")
                keys_to_remove.append(key)
        prev_key, prev_value = key, value
    d = removeSpaces(stringedDiz(removeUselessKeys(d, keys_to_remove)))
    return d


def SummarizeTexts(text: dict):
    text = verifyValueLength(reformatDiz(text))
    count = 0
    for section, value in text.items():
        if not value or not section:
            continue
        text[section] = openAIService(value)
    return text


def summaryGPT(filepath: str):
    write_text_to_pdf(SummarizeTexts(verifyValueLength(makeSingleValuePerKey(extractFromInput(filepath)))))


def main():
    summaryGPT("C:/Users/roach/Desktop/Storia_contemporanea.pdf")


if __name__ == '__main__':
    main()
