import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer as stemmer
from speechbrain.pretrained.fetching import fetch
from speechbrain.utils.data_utils import split_path
from speechbrain.utils.distributed import run_on_main
import torchaudio
from pytube import YouTube
import os
from speechbrain.dataio.preprocess import AudioNormalizer

test_string = '@dwad dadadaavhwdvah dwjaidj @dwadk said : "dwaddd"'
test_string1 = "@ddwa dwdhwaudhawuidhiu adhwu@ dwad@ @adawd aidhawuidhawduiah"
test_string2 = 'dhwaudhawuidhawdiu adhwuaidhawuidhawduiah " dwadawdaw"'
test_string3 = "Nicki Minaj once said “~panda…~ ~PANda…~ ~PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAooohhh~”"
test_blank = "dwaud [ __ ] [ __ ] dwadhhdu"
test_link = (
    "https://www.youtube.com/watch?v=ESIjxVudERY&t=10s&ab_channel=TeslaIntelligenceUK"
)

df = pd.DataFrame({"c1": [10, 11, 12], "c2": [test_string, test_string1, test_string2]})


def video_download(link, path):
    try:
        video = YouTube(link)
        audio = video.streams.filter(only_audio=True, file_extension="mp4").first()
        out = audio.download()
        os.rename(out, path)
    except:
        print("Connection Error")


def load_audio(path, savedir="."):
    """Load an audio file with this model"s input spec
    When using a speech model, it is important to use the same type of data,
    as was used to train the model. This means for example using the same
    sampling rate and number of channels. It is, however, possible to
    convert a file from a higher sampling rate to a lower one (downsampling).
    Similarly, it is simple to downmix a stereo file to mono.
    The path can be a local path, a web url, or a link to a huggingface repo.
    """
    source, fl = split_path(path)
    path = fetch(fl, source=source, savedir=savedir)
    signal, sr = torchaudio.load(path, channels_first=False)
    return AudioNormalizer(signal, sr)


def blank_remove(text):
    return re.sub(r"\[ __ ]", "", text)


def youtube_link_convert(link):
    return re.split("watch\?v=", link)[-1]


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
        return text.split("said")[-1]

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
    print(youtube_link_convert(test_link))
    # print(blank_remove(test_blank))
# print(at_sign_remove(test_string3))
# print(remove_extra_infom(df,'c2'))
