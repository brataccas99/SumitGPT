import time
import chardet
import unicodedata


# this func
def count_calls(func):
    """
           This function counts how many times a function is called (made to avoid openAI free account max requests/min error)
           @param func: the function to check
           @return func: the function checked with updated values
           """
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        if wrapper.num_calls == 58:  # actually the limit is 60/min requests
            time.sleep(70)
            print("\naspetto 1 minuto\n")
            wrapper.num_calls = 0
        return func(*args, **kwargs)

    wrapper.num_calls = 0
    return wrapper


def removeTrashList(list: list):
    """
    This function removes any elements of the list made by just ' '
     @param list: the dirty list
    @return list: the modified list
    """
    while ' ' in list:
        list.remove(' ')
    return list


def singleLetterConversion(letter: str):
    """
    This function converts single letters like ò,à,ù,etc... in unicode encoding
    @param letter: the non-unicode letter
    @return letter: the unicode letter
    """
    if unicodedata.category(letter) == "Cc":
        # Get the Unicode code point of the letter
        code_point = ord(letter)
        # Get the UTF-8 byte representation of the code point
        utf8_bytes = code_point.to_bytes(4, byteorder='big')
        # Decode the byte string as UTF-8 to get the converted string
        return utf8_bytes.decode('utf-8')
    return letter


def multipleLetterConversion(letter: str):
    """
        This function converts non-unicode chars made by multiple letters like ff,fi,fa,etc... in single letters unicode encoded
        @param letter: the non-unicoded letters
        @return letter: the unicoded letters
        """
    for char in letter:
        # Normalize the letter using NFKD decomposition
        normalized = unicodedata.normalize('NFKD', char)
        # Replace combining diacritical mark with empty string
        return normalized.replace('\u0302', '')


def convertLatinToUTF8(letter: str):
    """
            This function checks if i got a single letter or a char made by multiple letters non unicoded
            @param letter: the non-unicoded letters
            @return letter: the unicoded letters
            """
    print(letter)
    if not unicodedata.combining(letter):
        return singleLetterConversion(letter)
    else:
        return multipleLetterConversion(letter)


def makeSingleValuePerKey(diz: dict):
    """
               This function takes a dictionary of lists of strings and converts it in a dictionary of strings
               @param diz: the dirty dictionary
               @return diz: the resulting dictionary
               """
    return {k: " ".join(v) for k, v in diz.items()}


def verifyValueLength(dictionary: dict):
    """
       This function takes a dictionary and checks if a value is longer than 4000 tokens, if yes it splits the value in strings of same value but less than 4000
       @param dictionary: the dirty dictionary
       @return result: the resulting dictionary
       """
    result = {}
    for k, v in dictionary.items():
        result[k] = [v[i:i + 4000] for i in range(0, len(v), 4000)]
    return result


def detectEncoding(s: str):
    """
          This function takes a char and detects if it's encoding is non unicode
          @param s: the dirty char
          @return boolean the result of the check
          """
    if ord(s) > 127:
        byte_str = s.encode()
        result = chardet.detect(byte_str)
        if result['encoding'] != 'ascii':
            return True
    return False


def reduceString(text: list):
    """
       This function reduce strings to don't go out of the a4 format width
       @param text: list of string
       @return substrings: the reduced list of strings
       """
    substrings = []
    for word in text:
        word_substrings = [word[i:i + 85] for i in range(0, len(word), 85)]
        substrings.extend(word_substrings)
        substrings.append(' ')
    if substrings:  # Check if substrings is not empty before removing last item
        substrings.pop()  # Remove the last space character
    return substrings


def remove_extra_spaces(string: str):
    """
           This function removes extra spaces from a string
           @param string: the dirty string
           @return string: the modified string
           """
    words = string.split()
    return ' '.join(words)


def removeSpaces(dicti: dict):
    """
             This function removes extra spaces from the values of a dictionary
             @param dicti: the dirty dictionary
             @return string: the modified dictionary
             """
    for key, value in dicti.items():
        dicti[key] = remove_extra_spaces(value)
    return dicti


def removeUselessKeys(diz: dict, keys_to_remove: list):
    """
             This function removes useless keys of a dictionary like '':[]
             @param diz: the dirty dictionary
            @param keys_to_remove: the list of keys to remove
             @return diz: the modified dictionary
             """
    for key in tuple(keys_to_remove):
        del diz[key]
    return diz


def stringedDiz(diz: dict):
    """
    This function takes a diz of lists and converts it in a list of strings
    @param diz: the dirty dictionary
    @return diz: the modified dictionary
    """
    for key, value in diz.items():
        if isinstance(value, list):
            diz[key] = " ".join(value)
        else:
            diz[key] = value
    return diz
