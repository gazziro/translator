from faster_whisper import WhisperModel
from datetime import timedelta

def format_timestamp(seconds: float) -> str:
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

if __name__ == "__main__":
    model_size = "large-v3"
    video_fpath = r"video_sample.mp4"
    caption_fpath = r"video_sample_caption.vtt"

    # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(video_fpath, beam_size=3)
    print(f"Detected language {info.language} with probability {info.language_probability}")

    with open(caption_fpath, "w", encoding="utf-8") as srt_file:
        srt_file.write("WEBVTT\n\n")
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp_vtt(segment.start)
            end = format_timestamp_vtt(segment.end)
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{segment.text.strip()}\n\n")

    print(f"legenda salva em: {caption_fpath}")