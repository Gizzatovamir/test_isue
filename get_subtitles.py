import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
import json
from utils import blank_remove, youtube_link_convert, load_audio, video_download
import speechbrain as sb
from pydub import AudioSegment
from pydub.playback import play

MIN_TO_MILSEC = 60*1000
SEC_TO_MILSEC = 1000
videos = [
    "https://www.youtube.com/watch?v=zIwLWfaAg-8&t=35s&ab_channel=TED"
    #"https://www.youtube.com/watch?v=ESIjxVudERY&t=10s&ab_channel=TeslaIntelligenceUK"

]
voice_sample = "../sample.mp3"
dir = "../audios"
fragments_dir = "../fragments"
audience_noices = ["[Laughter]", "[Music]", "[Applause]","(Laughter)"]


def remove_ambient_noices(script):
    """Removing ambient noices like: [Music],[Laughter],[Applause]"""
    clear_script = []
    for line in script:
        if line['text'] in audience_noices:
            pass
        else:
            clear_script.append(line)
    return clear_script


def get_text_timing(script,audio):
    """returning start and end time from script json"""
    start = script['start']*SEC_TO_MILSEC
    end = start+script['duration']*SEC_TO_MILSEC
    return audio[start:end]


def generate_transcript(link):
    return remove_ambient_noices(YouTubeTranscriptApi.get_transcript(link))


def generate_data(id, audio_path, sample_path):
    """verification if speaker is Elon Musk or an interviewer and creating array like
    {
    'questions':
    [
        <question_1>,
        ...
    ],
    'answers':
    [
        <answer_1>,
        ...
    ]

    }
    """
    subtitles = generate_transcript(youtube_link_convert(id))
    audio_file = AudioSegment.from_file(audio_path,"mp4")
    questions = []
    answers = []
    verification = sb.pretrained.SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                                                 savedir="pretrained_models/spkrec-ecapa-voxceleb")
    for line, i in zip(subtitles, range(len(subtitles))):
        fragment = get_text_timing(line, audio_file)
        fragments_path = fragments_dir+"/fragment-{}.mp3".format(i)
        fragment.export(fragments_path, format="mp3")
        waveform_x = verification.load_audio(fragments_path)
        waveform_y = verification.load_audio(sample_path)
        score, prediction = verification.verify_files(waveform_x,
                                                      waveform_y)
        print(score.item())
        print(prediction.item())
        answers.append(line['text']) if prediction.item() else questions.append(line['text'])

    return {
        "questions_and_answers" : {
            "questions": questions,
            "answers": answers
        }
    }


if __name__ == "__main__":
    for video,i in zip(videos,range(len(videos))):
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(fragments_dir):
            os.makedirs(fragments_dir)
        audio_path = dir + "/{}.mp4".format(i)
        print(audio_path)
        video_download(video, audio_path)
        json = generate_data(video, audio_path, voice_sample)
    print(json)
