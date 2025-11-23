import whisper
from pydub import AudioSegment
from difflib import SequenceMatcher
import json

def load_real_lyrics(path):
    """실제 가사를 음절 단위로 로드"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    syllables = []
    for line in lines:
        line = line.strip()
        if line:
            syllables.extend(list(line))  # 한 글자(음절) 단위로 분리
    return syllables

def align_syllables(whisper_syllables, real_syllables):
    """Whisper 음절과 실제 가사 음절을 간단히 정렬"""
    sm = SequenceMatcher(None, whisper_syllables, real_syllables)
    aligned = []
    for opcode, i1, i2, j1, j2 in sm.get_opcodes():
        if opcode == "equal":
            for w_syl, r_syl in zip(whisper_syllables[i1:i2], real_syllables[j1:j2]):
                aligned.append((w_syl, r_syl))
        elif opcode in ("replace", "insert", "delete"):
            for r_syl in real_syllables[j1:j2]:
                aligned.append(("", r_syl))  # Whisper 음절이 없으면 빈 문자열
    return aligned

def audio_to_lrc_json(audio_path, lyrics_path, output_lrc, output_json):
    model = whisper.load_model("small")

    # 오디오 변환
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")

    # Whisper segment 추출
    result = model.transcribe("temp.wav", language="ko")
    segments = result["segments"]

    all_whisper_syllables = []
    segment_times = []

    # segment -> 음절 단위 균등 분배
    for seg in segments:
        text = seg["text"].strip()
        syllables = list(text)
        duration = seg["end"] - seg["start"]
        if len(syllables) == 0:
            continue
        syl_duration = duration / len(syllables)
        for i, syl in enumerate(syllables):
            start_time = seg["start"] + i * syl_duration
            all_whisper_syllables.append((syl, start_time, syl_duration))
        segment_times.append((seg["start"], seg["end"], len(syllables)))

    # 실제 가사 로드
    real_syllables = load_real_lyrics(lyrics_path)

    # Whisper 음절과 실제 가사 정렬
    whisper_only = [syl for syl, _, _ in all_whisper_syllables]
    aligned = align_syllables(whisper_only, real_syllables)

    # LRC/JSON 생성
    lrc_lines = []
    json_segments = []
    for i, (w_syl, r_syl) in enumerate(aligned):
        start_time = all_whisper_syllables[i][1] if i < len(all_whisper_syllables) else 0
        duration = all_whisper_syllables[i][2] if i < len(all_whisper_syllables) else 0.5
        start_min = int(start_time // 60)
        start_sec = start_time % 60
        timestamp = f"[{start_min:02d}:{start_sec:05.2f}]"
        lrc_lines.append(f"{timestamp}{r_syl}")
        json_segments.append({
            "start": start_time,
            "end": start_time + duration,
            "text": r_syl
        })

    with open(output_lrc, "w", encoding="utf-8") as f:
        for line in lrc_lines:
            f.write(line + "\n")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(json_segments, f, ensure_ascii=False, indent=2)

    print(f"LRC 파일 생성 완료: {output_lrc}")
    print(f"JSON 파일 생성 완료: {output_json}")


if __name__ == "__main__":
    audio_file = "song.mp3"
    lyrics_file = "lyric.txt"
    audio_to_lrc_json(audio_file, lyrics_file, "output_song.lrc", "output_song.json")
