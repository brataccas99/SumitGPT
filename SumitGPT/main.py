from pdfManipulation import write_text_to_pdf, verifyValueLength, extractFromInput, makeSingkeValuePerKey
from openAi import openAiCallSummary


def SummarizeTexts(text):
    for section, value in text.items():
        if not text[section]:
            continue
        text[section] = openAiCallSummary(value)
    return text


def summaryGPT(filename):
    text = SummarizeTexts(verifyValueLength(makeSingkeValuePerKey(extractFromInput(filename))))
    write_text_to_pdf(openAiCallSummary(text))


def main():
    summaryGPT("Storia_contemporanea_Dalla_Grande_Guerra_a_oggi_Nuova_ediz_Giovanni")


if __name__ == '__main__':
    main()
