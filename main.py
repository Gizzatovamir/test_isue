from twitter_scraper import search_tweets
from get_subtitles import video_download,generate_data
import os
import json

videos = [
    "https://www.youtube.com/watch?v=zIwLWfaAg-8&t=35s&ab_channel=TED"
    #"https://www.youtube.com/watch?v=ESIjxVudERY&t=10s&ab_channel=TeslaIntelligenceUK"

]
filename = "QnA.json"
voice_sample = "../sample.mp3"
dir = "../audios"
fragments_dir = "../fragments"
audience_noices = ["[Laughter]", "[Music]", "[Applause]","(Laughter)"]
celebrity = "Elon Musk"
words = [" once said", " said"]

if __name__ == "__main__":
    json_file = open(filename, 'w')
    phrases = search_tweets(celebrity,words)
    json.dump(phrases,json_file)
    for video, i in zip(videos, range(len(videos))):
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(fragments_dir):
            os.makedirs(fragments_dir)
        audio_path = dir + "/{}.mp4".format(i)
        print(audio_path)
        video_download(video, audio_path)
        QnA = generate_data(video, audio_path, voice_sample)
        json.dump()
