from pydub import AudioSegment

voice = AudioSegment.from_file("output.mp3")
bgm = AudioSegment.from_file("bgm.mp3")

# 调整音量（非常重要）
voice = voice + 0      # 人声
bgm = bgm - 18         # 背景音一般要低 15~25 dB

# 循环 BGM 到和人声一样长
bgm = bgm * (len(voice) // len(bgm) + 1)
bgm = bgm[:len(voice)]

# 混音
final = bgm.overlay(voice)

final.export("meditation.wav", format="wav")
