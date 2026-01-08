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


if __name__ == "__main__":

    model_size = "large-v3"
    video_fpath = r"C:\Users\Biel\Documents\translator\video_sample.mp4"
    caption_fpath = r"C:\Users\Biel\Documents\translator\video_sample_caption.srt"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    segments, info = model.transcribe(video_fpath, beam_size=3)
    print(f"Detected language {info.language} with probability {info.language_probability}")

    with open(caption_fpath, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{segment.text.strip()}\n\n")

    print(f"legenda salva em: {caption_fpath}")