## 자비스가 필요해! (음성 녹음 기능 구현)

### 과제 1 : 시스템의 마이크를 인식하고 음성을 녹음하는 부분을 완성한다.
record_audio 함수를 통해 음성을 녹음한다.  
39~44번 줄에서 `sd.InputStream`을 활용해 마이크 입력을 받고, `callback` 함수를 통해 큐(q)에 데이터를 담아 녹음을 수행한다.

```python
with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < duration:
        file.write(q.get())
```

### 과제 2 : 시스템의 마이크를 인식하고 음성을 녹음하는 부분은 외부 라이브러리를 사용하는 것이 가능하다.
오디오 입출력 제어 외부 라이브러리 설치
```
   pip install sounddevice soundfile
```

라이브러리 설치 후 오디오 입출력 라이브러리인 `sounddevice`와 오디오 파일을 읽고 쓸 수 있는 라이브러리인 `soundfile`을 import 한다.

```python
import sounddevice as sd
import soundfile as sf
```

### 과제 3 : 파일들은 파이썬 앱이 실행되고 있는 하위에 records 폴더에 모두 저장된다.
26번 줄에서 현재 실행 경로 하위에 records 폴더를 파일들을 저장할 경로로 지정한다.

```python
record_dir = os.path.join(os.getcwd(), "records")
```

### 과제 4 : 파일의 이름은 녹음 날짜와 시간을 참조해서 ‘년월일-시간분초’와 같은 형태로 저장한다.
31번 줄에서 녹음 시점 기준으로 '년월일-시간분초’와 같은 형태로 파일명이 지정된다.

```python
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
```

### 과제 5 : 작성한 코드는 javis.py로 저장한다.


### 보너스 : 특정 범위의 날짜의 녹음 파일을 보여주는 기능을 추가한다.
   106~109번 줄에서 `list_records_by_date` 함수를 통해 조회할 기간을 입력받아 해당 범위의 날짜의 녹음 파일을 조회한다.
   
   ```python
   print("\n📅 날짜 입력 예시: 20260501")
   start = input("시작 날짜를 입력하세요 (YYYYMMDD): ")
   end = input("종료 날짜를 입력하세요 (YYYYMMDD): ")
   list_records_by_date(start, end)
   ```
