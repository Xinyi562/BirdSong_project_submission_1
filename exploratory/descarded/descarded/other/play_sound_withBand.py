# Discarded: not flexible enough when trying to adjust progress
import sounddevice as sd
import soundfile as sf
import time
import sys

audio_path = "example.flac"   # 先换成你自己的 flac 路径

data, samplerate = sf.read(audio_path)
duration = len(data) / samplerate

start_time = time.time()

def callback(outdata, frames, time_info, status):
    del outdata, frames, time_info, status # 不用设变量, 占位用
    current_time = time.time() - start_time
    progress = min(current_time, duration) #已播放的时间,但是最多不超过总时长

    bar_len = 30
    filled = int(bar_len * progress / duration)
    bar = "█" * filled + "-" * (bar_len - filled)

    sys.stdout.write(
        f"\r播放进度: |{bar}| {progress:5.1f}s / {duration:5.1f}s"
    )
    sys.stdout.flush()

with sd.OutputStream(
    samplerate=samplerate,
    channels=data.shape[1] if data.ndim > 1 else 1,
    callback=callback
):
    sd.play(data, samplerate)
    sd.wait()

print("\n播放完成")