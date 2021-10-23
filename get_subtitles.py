from youtube_transcript_api import YouTubeTranscriptApi
import json
from utils import blank_remove

path = "QnA.json"
celebrities = [
    "Nicki_Minaj",
    "Taylor_Swift",
    "Billie_Eilish",
    "Ariana_Grande",
    "Donald_Trump",
    "Elon_Musk",
    "Joe_Rogan",
    "Kanye_West",
]
videos = [
    "O0RBngBIKhU&ab_channel=HOT97",
    "ionfV_r8s40&ab_channel=JimmyKimmelLive",
    "IHMb3QHUMmw&ab_channel=JimmyKimmelLive",
    "C0n_aqCcTVk&ab_channel=ZachSangShow",
    "-GwG1_TkhQI&ab_channel=NBCNews",
    "ESIjxVudERY&ab_channel=TeslaIntelligenceUK",
    "ZTJSUR1lbiI&ab_channel=BreakingPoints",
    "qxOeWuAHOiw&t=44s&ab_channel=PowerfulJRE",
]
audience_noices = ["[Laughter]", "[Music]", "[Applause]"]


def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    script = []
    for i in enumerate(transcript):
        if (i[1]["text"] != "[Music]") and (i[1]["text"] != "[Applause]"):
            if i[0] % 2 == 0:
                script.append({"question_{}".format(i[0]): blank_remove(i[1]["text"])})
            else:
                script.append(
                    {"answer_{}".format(i[0] - 1): blank_remove(i[1]["text"])}
                )
    return script


if __name__ == "__main__":
    result_json = []
    for celeb, video_id in zip(celebrities, videos):
        transcript_celbrity = {celeb: generate_transcript(video_id)}
        result_json.append(transcript_celbrity)

    with open(path, "w") as outfile:
        json.dump(result_json, outfile)
