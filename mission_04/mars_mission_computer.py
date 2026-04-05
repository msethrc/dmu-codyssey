import time
import random # 문제 3 DummySensor 랜덤 데이터 생성
import threading # 보너스 과제 1 

class DummySensor:
    # 범위를 별도로 관리.
    # (최솟값, 최댓값) 튜플 형태로 저장.
    SENSOR_CONFIG = {
        "mars_base_internal_temperature": (18, 30),
        "mars_base_external_temperature": (0, 21),
        "mars_base_internal_humidity": (50, 60),
        "mars_base_external_illuminance": (500, 715),
        "mars_base_internal_co2": (0.02, 0.1),
        "mars_base_internal_oxygen": (4, 7)
    }

    def __init__(self):
        self.env_values = {key: None for key in self.SENSOR_CONFIG.keys()}

    # 랜덤 값 생성 메소드 추가
    def set_env(self):
        for key, (min_val, max_val) in self.SENSOR_CONFIG.items():
            self.env_values[key] = round(random.uniform(min_val, max_val), 2)
        return self.env_values

# 과제 1 : 클래스 생성
class MissionComputer:
    def __init__(self):
        # 과제 2, 3 : 사전 객체 추가
        self.env_values = {}
        self.ds = DummySensor() # 과제 4 : DummySensor 클래스 인스턴스화
        self.is_running = True  # 시스템 가동 상태 플래그
        self.history = {key: [] for key in self.ds.SENSOR_CONFIG.keys()} # 평균 계산용 저장소
        self.start_time = time.time() # 5분 측정을 위한 시작 시간

    def check_stop_signal(self):
        # 보너스 1 : 별도 스레드에서 키 입력을 감시
        while self.is_running:
            user_input = input("").lower()
            if user_input == 'q':
                self.is_running = False
                print("\nSytem stoped...")
                break

    # 과제 5 : get_sensor_data() 메소드 추가
    def get_sensor_data(self):
        # 입력 감지 스레드 시작
        input_thread = threading.Thread(target=self.check_stop_signal)
        input_thread.daemon = True
        input_thread.start()

        try:
            while self.is_running:
                # 과제 6-1 : 센서 값 가져와와서 env_values에 담기
                sensor_data = self.ds.set_env()
                self.env_values.update(sensor_data)

                # 평균 계산을 위해 리스트에 추가
                for k, v in sensor_data.items():
                    self.history[k].append(v)

                # 과제 6-2 : env_values 값을 json 형태로 출력
                print(json_format(self.env_values))

                # 보너스 2 : 5분(300초)에 한번씩 평균 값 출력
                current_time = time.time()
                if current_time - self.start_time >= 300:
                    self.print_average()
                    self.start_time = current_time # 시간 리셋

                # 과제 6-3 : 위 두 가지 동작을 5초에 한번씩 반복
                time.sleep(5)
        except KeyboardInterrupt:
            print("반복 출력 종료")

    # 5분 평균 값 출력 메소드
    def print_average(self):
        avg_values = {}
        for key, values in self.history.items():
            if values:
                avg_values[key] = round(sum(values) / len(values), 2)
                self.history[key] = [] # 다음 5분을 위해 비우기

        print("\n" + "="*50)
        print(" 5분 주기 환경 데이터 평균 값")
        print(json_format(avg_values))
        print("="*50 + "\n")

# json 형태로 출력하는 메소드
def json_format(data_dict):
    json_str = "{\n"
    
    items = list(data_dict.items())
    
    for i, (key, value) in enumerate(items):
        line = f'    "{key}": {value}'
        
        if i < len(items) - 1:
            line += ","
        
        json_str += line + "\n"
    
    # 끝 중괄호
    json_str += "}"
    return json_str

# 과제 7 : MissionComputer 클래스 인스턴스화
RunComputer = MissionComputer()

if __name__ == "__main__":
    RunComputer.get_sensor_data()