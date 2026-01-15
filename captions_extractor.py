from typing import Union
from datetime import timedelta
from pathlib import Path

from faster_whisper import WhisperModel, transcribe
from tqdm import tqdm

def format_timestamp_srt(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    millis = int((seconds - total_seconds) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def format_timestamp_vtt(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    millis = int((seconds - total_seconds) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

def load_model_and_transcribe(
    model_size : str,
    video_fpath : str,
    target_language : str
    ) -> Union[WhisperModel, transcribe.TranscriptionInfo]:
    
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    segments, info = model.transcribe(
        video_fpath,
        beam_size=3,
        task="translate",
        language=target_language
    )
    print("Running on CUDA")
    # model = faster_whisper.WhisperModel(model_size, device="cpu", compute_type="int8")
    # print("Running on CPU")
    # segments, info = model.transcribe(
    #     video_fpath,
    #     beam_size=3,
    #     task="translate",
    #     language=target_language
    # )
    return segments, info


def write_captions(segments, caption_fpath):
    with open(caption_fpath, "w", encoding="utf-8") as srt_file:
        srt_file.write("WEBVTT\n\n")
        for i, segment in enumerate(tqdm(segments), start=1):
            start = format_timestamp_vtt(segment.start)
            end = format_timestamp_vtt(segment.end)
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")

def main(video_fpath, caption_dpath, caption_language="pt", model_size = "large-v3") -> None:
    print(f":: Starting processing...")

    caption_fpath = Path(caption_dpath, f"{Path(video_fpath).stem}.vtt")
    segments, info, = load_model_and_transcribe(model_size, video_fpath, caption_language)
    print(f":: Detected language {info.language} with probability {info.language_probability}")

    write_captions(segments, caption_fpath)
    print(f":: Caption saved in: {caption_fpath}")