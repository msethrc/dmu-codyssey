import time
import random
import threading
import json
import platform
import psutil
import os
from multiprocessing import Process

DEFAULT_SETTING_FILE = 'setting.txt'

class DummySensor:
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

    def set_env(self):
        for key, (min_val, max_val) in self.SENSOR_CONFIG.items():
            self.env_values[key] = round(random.uniform(min_val, max_val), 2)
        return self.env_values

class MissionComputer:
    def __init__(self, setting_file=DEFAULT_SETTING_FILE):
        self.env_values = {}
        self.ds = DummySensor()
        self.is_running = True
        self.history = {key: [] for key in self.ds.SENSOR_CONFIG.keys()}
        self.start_time = time.time()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setting_file = os.path.join(current_dir, setting_file)
        self.settings = self._load_settings()

    def _load_settings(self):
        if not os.path.exists(self.setting_file):
            print(f'경고: {self.setting_file} 파일이 없습니다. 모든 항목을 출력합니다.')
            return None
        
        with open(self.setting_file, "r", encoding="utf-8") as f:
            return [line.split('#')[0].strip() for line in f if line.split('#')[0].strip()]

    def _filter_dict(self, data_dict):
        if self.settings is None:
            return data_dict
        return {k: v for k, v in data_dict.items() if k in self.settings}

    # 과제 1: 20초에 한번씩 결과 출력
    def get_mission_computer_info(self):
        # 20초에 한번씩 결과 출력
        while self.is_running:
            try:
                total_memory_gb = round(psutil.virtual_memory().total / (1024**3), 2)

                info_dict = {
                    '운영체계': platform.system(),
                    '운영체계 버전': platform.version(),
                    'CPU의 타입': platform.processor(),
                    'CPU의 코어 수': psutil.cpu_count(logical=False),
                    '메모리의 크기': f'{total_memory_gb} GB'
                }
                filtered_info = self._filter_dict(info_dict)
                print(f"\n[System Info]\n{json.dumps(filtered_info, indent=4, ensure_ascii=False)}")
            except Exception as e:
                print(f"Info Error: {e}")
            
            # 20초 대기 (1초씩 끊어서 종료 체크)
            for _ in range(20):
                if not self.is_running: break
                time.sleep(1)

    def get_mission_computer_load(self):
        # 20초에 한번씩 결과 출력
        while self.is_running:
            try:
                cpu_usage = psutil.cpu_percent(interval=0.5)
                memory_usage = psutil.virtual_memory().percent

                load_dict = {
                    'CPU 실시간 사용량': f'{cpu_usage}%',
                    '메모리 실시간 사용량': f'{memory_usage}%'
                }
                filtered_load = self._filter_dict(load_dict)
                print(f"\n[System Load]\n{json.dumps(filtered_load, indent=4, ensure_ascii=False)}")
            except Exception as e:
                print(f"Load Error: {e}")

            # 20초 대기 (1초씩 끊어서 종료 체크)
            for _ in range(20):
                if not self.is_running: break
                time.sleep(1)

    def get_sensor_data(self):
        # env_values에 값을 담고 json 형태로 출력하는 동작을 5초에 한번씩 반복
        try:
            while self.is_running:
                sensor_data = self.ds.set_env()
                self.env_values.update(sensor_data)

                for k, v in sensor_data.items():
                    self.history[k].append(v)

                print(f"\n[Sensor Data]\n{json.dumps(self.env_values, indent=4, ensure_ascii=False)}")

                current_time = time.time()
                if current_time - self.start_time >= 300:
                    self.print_average()
                    self.start_time = current_time

                time.sleep(5)
        except KeyboardInterrupt:
            self.is_running = False

    def print_average(self):
        avg_values = {}
        for key, values in self.history.items():
            if values:
                avg_values[key] = round(sum(values) / len(values), 2)
                self.history[key] = []

        print("\n" + "="*50)
        print(" 5분 주기 환경 데이터 평균 값")
        print(json.dumps(avg_values, indent=4, ensure_ascii=False))
        print("="*50 + "\n")

    def run_all_tasks(self):
        # 과제 3: 인스턴스의 3개 메소드를 각각 멀티 쓰레드로 실행
        threads = [
            threading.Thread(target=self.get_mission_computer_info, daemon=True),
            threading.Thread(target=self.get_mission_computer_load, daemon=True),
            threading.Thread(target=self.get_sensor_data, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        # 보너스: 'q' 입력 시 종료 제어
        while self.is_running:
            user_input = input("").lower()
            if user_input == 'q':
                self.is_running = False
                print("\nSytem stoped...")
                break

def start_instance():
    # 과제 2: MissionComputer 인스턴스화 
    runComputer = MissionComputer()
    runComputer.run_all_tasks()

if __name__ == "__main__":
    print("입력창에 'q'를 입력하면 해당 인스턴스가 종료됩니다.\n")

    # 과제 4: 3개의 인스턴스 생성
    runComputer1 = Process(target=start_instance)
    runComputer2 = Process(target=start_instance)
    runComputer3 = Process(target=start_instance)

    # 과제 5: 3개의 인스턴스를 멀티 프로세스로 실행
    runComputer1.start()
    runComputer2.start()
    runComputer3.start()

    # 프로세스 대기
    runComputer1.join()
    runComputer2.join()
    runComputer3.join()

    print("모든 시스템 종료.")