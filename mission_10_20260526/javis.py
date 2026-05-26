import os
import queue
import sys
from datetime import datetime
# 과제 2 : 오디오 입출력 제어
import sounddevice as sd
import soundfile as sf

# 녹음 데이터를 담을 큐 생성
q = queue.Queue()

"""
소리 입력이 들어올 때마다 호출되는 콜백 함수
"""
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


"""
지정된 시간(초) 동안 음성을 녹음하고 records 폴더에 저장하는 함수
"""
def record_audio(duration=5, samplerate=44100, channels=1):
    # 과제 3 : records 폴더 생성 (존재하지 않으면 자동 생성)
    record_dir = os.path.join(os.getcwd(), "records")
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)

    # 과제 4 : 파일 이름 설정 (년월일-시간분초 형태)
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{current_time}.wav"
    filepath = os.path.join(record_dir, filename)

    print(f"\n🎙️ 녹음을 시작합니다... ({duration}초 동안 말씀해 주세요)")

    # 과제 1 : 마이크 인식 및 녹음 진행
    try:
        with sf.SoundFile(filepath, mode="x", samplerate=samplerate, channels=channels) as file:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                # 지정된 시간 동안 큐에 쌓이는 데이터를 파일에 기록
                start_time = datetime.now()
                while (datetime.now() - start_time).total_seconds() < duration:
                    file.write(q.get())

        print(f"💾 녹음 완료! 파일이 저장되었습니다: {filepath}")

    except Exception as e:
        print(f"❌ 녹음 중 오류가 발생했습니다: {e}")

"""
과제 6 : 특정 범위의 날짜의 녹음 파일을 보여주는 기능
"""
def list_records_by_date(start_date_str, end_date_str):
    
    record_dir = os.path.join(os.getcwd(), "records")

    if not os.path.exists(record_dir):
        print("📁 아직 생성된 records 폴더가 없습니다.")
        return

    try:
        # 입력받은 문자열을 datetime 객체로 변환 (날짜 비교용)
        start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date = datetime.strptime(end_date_str, "%Y%m%d").date()
    except ValueError:
        print("❌ 날짜 형식이 올바르지 않습니다. YYYYMMDD 형태로 입력해주세요.")
        return

    print(f"\n🔍 {start_date_str} 부터 {end_date_str} 까지의 녹음 파일 검색 결과:")
    found_any = False

    # records 폴더 내 파일 탐색
    for filename in os.listdir(record_dir):
        if filename.endswith(".wav"):
            # 파일명에서 '년월일' 부분 추출 (예: 20260526-124212.wav -> 20260526)
            date_part = filename.split("-")[0]
            try:
                file_date = datetime.strptime(date_part, "%Y%m%d").date()

                # 날짜가 지정된 범위 내에 있는지 확인
                if start_date <= file_date <= end_date:
                    print(f" 📄 {filename}")
                    found_any = True
            except ValueError:
                # 파일명이 지정된 형식(년월일-시간분초)과 다르면 패스
                continue

    if not found_any:
        print(" 해당 기간에 저장된 녹음 파일이 없습니다.")


if __name__ == "__main__":
    while True:
        print("\n=== JAVIS 음성 시스템 ===")
        print("1. 음성 녹음하기 (5초)")
        print("2. 특정 기간 녹음 파일 조회하기")
        print("3. 종료")
        choice = input("원하는 기능의 번호를 입력하세요: ")

        if choice == "1":
            # 5초 동안 녹음 테스트 (원하는 대로 초 조절 가능)
            record_audio(duration=5)

        elif choice == "2":
            print("\n📅 날짜 입력 예시: 20260501")
            start = input("시작 날짜를 입력하세요 (YYYYMMDD): ")
            end = input("종료 날짜를 입력하세요 (YYYYMMDD): ")
            list_records_by_date(start, end)

        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해 주세요.")