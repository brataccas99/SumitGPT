import time
import chardet
import unicodedata


# this func counts how many times a function is called (made to avoid openAI free account max requests/min error)
def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(f"{wrapper.num_calls}a chiamata ad openAI")
        if wrapper.num_calls == 58:  # actually the limit is 60/min requests
            time.sleep(70)
            wrapper.num_calls = 0
        return func(*args, **kwargs)

    wrapper.num_calls = 0
    return wrapper


def singleLetterConversion(letter):
    if unicodedata.category(letter) == "Cc":
        # Get the Unicode code point of the letter
        code_point = ord(letter)
        # Get the UTF-8 byte representation of the code point
        utf8_bytes = code_point.to_bytes(4, byteorder='big')
        # Decode the byte string as UTF-8 to get the converted string
        return utf8_bytes.decode('utf-8')
    return letter


def multipleLetterConversion(letter):
    for char in letter:
        # Check if the character is composed or not
        if unicodedata.combining(char) == 0:
            # Normalize the letter using NFKD decomposition
            normalized = unicodedata.normalize('NFKD', letter)
            # Replace combining diacritical mark with empty string
            return normalized.replace('\u0302', '')
    return letter


def convertLatinToUTF8(letter):
    print(letter)
    if not unicodedata.combining(letter):
        return singleLetterConversion(letter)
    else:
        return multipleLetterConversion(letter)


def makeSingkeValuePerKey(diz):
    return {k: " ".join(v) for k, v in diz.items()}


def verifyValueLength(dictionary):
    result = {}
    for k, v in dictionary.items():
        result[k] = [v[i:i + 4097] for i in range(0, len(v), 4097)]
    return result


def detectEncoding(s):
    if ord(s) > 127:
        byte_str = s.encode()
        result = chardet.detect(byte_str)
        if result['encoding'] != 'ascii':
            return True
    return False


def reduceString(text):
    substrings = []
    for word in text:
        word_substrings = [word[i:i + 85] for i in range(0, len(word), 85)]
        substrings.extend(word_substrings)
        substrings.append(' ')
    if substrings:  # Check if substrings is not empty before removing last item
        substrings.pop()  # Remove the last space character
    return substrings
