from src import video_download, generate_data, remove_files, search_tweets
import os
import json

videos = [
    "https://www.youtube.com/watch?v=V59tgbrDkDE&ab_channel=TeslaVision",
    "https://www.youtube.com/watch?v=gV6hP9wpMW8&t=25s&ab_channel=TheLateShowwithStephenColbert",
    "https://www.youtube.com/watch?v=zIwLWfaAg-8&t=35s&ab_channel=TED",
    "https://www.youtube.com/watch?v=ESIjxVudERY&t=10s&ab_channel=TeslaIntelligenceUK",
]
filename = "QnA.json"
voice_sample = "sample.mp3"
dir = "audios"
json_dir = "jsons/"
audience_noices = ["[Laughter]", "[Music]", "[Applause]", "(Laughter)"]
celebrity = "Elon Musk"
words = [" once said", " said"]


def get_subtitles(video, i):
    if not os.path.exists(dir):
        os.makedirs(dir)
    audio_path = dir + "/{}.mp4".format(i)
    print(audio_path)
    video_download(video, audio_path)
    QnA = generate_data(video, audio_path, voice_sample)
    return {"video_{}".format(i): QnA}


if __name__ == "__main__":
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    result = []
    phrases = search_tweets(celebrity, words)
    result.append(phrases)
    for video, i in zip(videos, range(len(videos))):
        result.append(get_subtitles(video, i))
        remove_files()
    with open(json_dir + filename, "w") as json_file:
        json.dump(result, json_file)
