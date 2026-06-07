import os
import queue
import sys
import csv
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

RECORD_DIR = os.path.join(os.getcwd(), "records")

# ──────────────────────────────────────────────
# 내부 유틸
# ──────────────────────────────────────────────

# [과제 4] 음성 파일의 이름과 같은 이름으로 csv 저장 (CSV 파일명)
def _wav_to_csv_path(wav_path):
    base, _ = os.path.splitext(wav_path)
    return base + ".csv"

# ──────────────────────────────────────────────
# 녹음 + 자동 STT
# ──────────────────────────────────────────────

def record_audio(duration = 5, samplerate = 16000, channels = 1):
    # records 폴더가 없으면 생성
    if not os.path.exists(RECORD_DIR):
        os.makedirs(RECORD_DIR)

    filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".wav"
    filepath = os.path.join(RECORD_DIR, filename)

    print(f"\n🎙️  녹음을 시작합니다... ({duration}초 동안 말씀해 주세요)")

    # 매 녹음마다 새 큐 생성 → 이전 잔류 데이터 오염 방지
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    try:
        # mode="x" 대신 "w"를 사용하여 동일 초 내 실행 시 충돌 방지
        with sf.SoundFile(filepath, mode="w", samplerate=samplerate, channels=channels) as f:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                start = datetime.now()
                while (datetime.now() - start).total_seconds() < duration:
                    f.write(q.get())
                
                # 루프 종료 후 큐에 남아있는 마지막 데이터까지 모두 기록 (잘림 방지)
                while not q.empty():
                    f.write(q.get())

        print(f"💾 녹음 완료! 저장 경로: {filepath}")
        run_stt_on_file(filepath)

    except Exception as e:
        print(f"❌ 녹음 중 오류: {e}")


# ──────────────────────────────────────────────
# STT 실행 (단일 파일)
# ──────────────────────────────────────────────

def run_stt_on_file(wav_path):
    csv_path = _wav_to_csv_path(wav_path)

    # 이미 CSV가 있으면 덮어쓰기 확인
    if os.path.exists(csv_path):
        ans = input(
            f"⚠️  이미 CSV 파일이 존재합니다 ({os.path.basename(csv_path)}). "
            "덮어쓰시겠습니까? (y/n): "
        )
        if ans.strip().lower() != "y":
            print("STT 변환을 건너뜁니다.")
            return

    print("\n🤖 STT 변환 중... 잠시만 기다려 주세요.")

    recognizer = sr.Recognizer()
    rows = []
    chunk_sec = 30  # 청크 단위(초)

    try:
        # soundfile 로 전체 길이만 빠르게 읽기
        total_sec = sf.info(wav_path).duration

        with sr.AudioFile(wav_path) as source:
            offset = 0.0

            while offset < total_sec:
                # 남은 길이가 chunk_sec 보다 작을 수 있으므로 실제 읽을 길이를 계산
                remaining = total_sec - offset
                read_sec = min(chunk_sec, remaining)

                # sr.AudioFile 은 with 블록 내에서 포인터가 자동 전진하므로
                # duration 만 지정하면 이어서 읽힘
                chunk_audio = recognizer.record(source, duration=read_sec)

                # 빈 청크(파일 끝 초과 등) 안전 처리
                if not chunk_audio.frame_data:
                    break

                # 초(float) → MM:SS 문자열 (CSV 내용)
                m, s = divmod(int(offset), 60)
                time_label = f"{m:02d}:{s:02d}"

                try:
                    text = recognizer.recognize_google(chunk_audio, language="ko-KR")
                    print(f"  [{time_label}] {text}")
                except sr.UnknownValueError:
                    text = "(인식 실패 또는 음성 없음)"
                    print(f"  [{time_label}] ❌ 음성 인식 실패")
                except sr.RequestError as e:
                    text = f"(API 오류: {e})"
                    print(f"  [{time_label}] ❌ API 오류: {e}")

                rows.append((time_label, text))
                offset += read_sec   # 실제 읽은 만큼만 전진

    except Exception as e:
        print(f"❌ STT 처리 중 오류: {e}")
        return

    # [과제 3] STT로 구현된 텍스트 인식 정보를 CSV 저장 (CSV 내용)
    try:
        with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["시간", "인식된 텍스트"])
            writer.writerows(rows)
        print(f"📊 CSV 저장 완료: {csv_path}")
    except Exception as e:
        print(f"❌ CSV 저장 오류: {e}")


# ──────────────────────────────────────────────
# [과제 1] 전체 녹음 파일 목록
# ──────────────────────────────────────────────

def list_all_records():
    if not os.path.exists(RECORD_DIR):
        print("📁 저장된 녹음 파일이 없습니다.")
        return []

    wav_files = sorted(f for f in os.listdir(RECORD_DIR) if f.endswith(".wav"))

    if not wav_files:
        print("📁 저장된 녹음(.wav) 파일이 없습니다.")
        return []

    print("\n📋 전체 녹음 파일 목록:")
    for idx, name in enumerate(wav_files, start=1):
        csv_exists = "📝" if os.path.exists(
            _wav_to_csv_path(os.path.join(RECORD_DIR, name))
        ) else "  "
        print(f"  {idx:>3}. {csv_exists} {name}")

    print("\n  (📝 = STT 변환 완료된 파일)")
    return wav_files


# ──────────────────────────────────────────────
# 날짜 범위 조회
# ──────────────────────────────────────────────

def list_records_by_date(start_date_str, end_date_str):
    if not os.path.exists(RECORD_DIR):
        print("📁 records 폴더가 없습니다.")
        return

    try:
        start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date   = datetime.strptime(end_date_str,   "%Y%m%d").date()
    except ValueError:
        print("❌ 날짜 형식이 올바르지 않습니다. YYYYMMDD 형태로 입력해주세요.")
        return

    if start_date > end_date:
        print("❌ 시작 날짜가 종료 날짜보다 늦습니다.")
        return

    print(f"\n🔍 {start_date_str} ~ {end_date_str} 녹음 파일 목록:")
    found = False

    for name in sorted(os.listdir(RECORD_DIR)):
        if not name.endswith(".wav"):
            continue
        date_part = name.split("-")[0]
        try:
            file_date = datetime.strptime(date_part, "%Y%m%d").date()
            if start_date <= file_date <= end_date:
                print(f"  📄 {name}")
                found = True
        except ValueError:
            continue

    if not found:
        print("  해당 기간에 저장된 녹음 파일이 없습니다.")


# ──────────────────────────────────────────────
# [보너스] 키워드 검색
# ──────────────────────────────────────────────

def search_keyword_in_csv(keyword):
    if not keyword.strip():
        print("❌ 공백만으로는 검색할 수 없습니다.")
        return

    if not os.path.exists(RECORD_DIR):
        print("📁 records 폴더가 존재하지 않습니다.")
        return

    keyword_lower = keyword.strip().lower()
    print(f"\n🔍 키워드 '{keyword}' 검색 결과:")
    found = False

    for name in sorted(os.listdir(RECORD_DIR)):
        if not name.endswith(".csv"):
            continue
        csv_path = os.path.join(RECORD_DIR, name)
        try:
            with open(csv_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 건너뜀
                for row in reader:
                    if len(row) < 2:
                        continue
                    time_info, text_content = row[0], row[1]
                    if keyword_lower in text_content.lower():
                        print(
                            f"  📄 [파일] {name}  "
                            f"[시간] {time_info}  "
                            f"[내용] {text_content}"
                        )
                        found = True
        except Exception as e:
            print(f"  ❌ 파일 읽기 오류 ({name}): {e}")

    if not found:
        print(f"  '{keyword}'가 포함된 기록을 찾지 못했습니다.")


# ──────────────────────────────────────────────
# [과제 2] 기존 WAV 파일 선택 후 STT 재실행
# ──────────────────────────────────────────────

def stt_from_existing():
    wav_files = list_all_records()
    if not wav_files:
        return

    choice = input("\n변환할 파일 번호를 입력하세요 (취소: 0): ").strip()
    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if not (0 <= idx < len(wav_files)):
            raise ValueError
    except ValueError:
        print("❌ 올바른 번호를 입력해주세요.")
        return

    wav_path = os.path.join(RECORD_DIR, wav_files[idx])
    run_stt_on_file(wav_path)


# ──────────────────────────────────────────────
# 메인 루프
# ──────────────────────────────────────────────

def main():
    menu = """
=== JAVIS 음성 시스템 ===
  1. 음성 녹음하기 (5초) & STT 자동 변환
  2. 전체 녹음 파일 목록 보기
  3. 특정 기간 녹음 파일 조회하기
  4. 키워드로 텍스트 검색하기
  5. 기존 녹음 파일 STT 변환하기
  6. 종료
"""
    while True:
        print(menu)
        choice = input("원하는 기능의 번호를 입력하세요: ").strip()

        if choice == "1":
            record_audio(duration=5)

        elif choice == "2":
            list_all_records()

        elif choice == "3":
            print("\n📅 날짜 입력 예시: 20260501")
            start = input("시작 날짜 (YYYYMMDD): ").strip()
            end   = input("종료 날짜 (YYYYMMDD): ").strip()
            list_records_by_date(start, end)

        elif choice == "4":
            keyword = input("\n🔍 검색할 키워드를 입력하세요: ")
            search_keyword_in_csv(keyword)

        elif choice == "5":
            stt_from_existing()

        elif choice == "6":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()