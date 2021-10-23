import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer as stemmer

test_string = '@dwad dadadaavhwdvah dwjaidj @dwadk said : "dwaddd"'
test_string1 = "@ddwa dwdhwaudhawuidhiu adhwu@ dwad@ @adawd aidhawuidhawduiah"
test_string2 = 'dhwaudhawuidhawdiu adhwuaidhawuidhawduiah " dwadawdaw"'
test_string3 = "Nicki Minaj once said “~panda…~ ~PANda…~ ~PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAooohhh~”"
test_blank = "dwaud [ __ ] [ __ ] dwadhhdu"

df = pd.DataFrame({"c1": [10, 11, 12], "c2": [test_string, test_string1, test_string2]})


def blank_remove(text):
    return re.sub(r"\[ __ ]", "", text)


def celebrity_mention_remove(string):
    citation_pattern = r'"[^>]+"'

    def remove_content(text):
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            "]+",
            re.UNICODE,
        )
        text = re.sub(r"http\S+", "", text)  # remove urls
        text = re.sub(r"\S+\.com\S+", "", text)  # remove urls
        text = re.sub(r"\@\w+", "", text)  # remove mentions
        text = re.sub(r"\#\w+", "", text)  # remove hashtags
        text = re.sub(emoji_pattern, "", text)  # remove emojis and e.t.c
        return text

    try:
        return re.search(citation_pattern, string).group(0)
    except AttributeError:
        return remove_content(string)


def remove_extra_infom(data_frame, celebrity_name):
    return pd.DataFrame(
        [
            celebrity_mention_remove(row[celebrity_name])
            for _, row in data_frame.iterrows()
        ],
        columns=[celebrity_name],
    )


if __name__ == "__main__":
    # print(celebrity_mention_remove(test_string))
    # print(celebrity_mention_remove(test_string1))
    # print(celebrity_mention_remove(test_string2))
    # print(celebrity_mention_remove(test_string3))
    print(blank_remove(test_blank))
# print(at_sign_remove(test_string3))
# print(remove_extra_infom(df,'c2'))
