from Utilities import verifyValueLength, makeSingkeValuePerKey
from openAi import openAiCallSummary
from pdfManipulation import write_text_to_pdf, extractFromInput


def SummarizeTexts(text):
    for section, value in text.items():
        if not text[section]:
            continue
        text[section] = openAiCallSummary(value)
    return text


def summaryGPT(filepath):
    write_text_to_pdf(SummarizeTexts(verifyValueLength(makeSingkeValuePerKey(extractFromInput(filepath)))))


def main():
    summaryGPT("C:/Users/roach/Desktop/Storia_contemporanea.pdf")


if __name__ == '__main__':
    main()
