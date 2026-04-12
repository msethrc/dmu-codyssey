import platform
import psutil # psutil 설치 (pip install psutil)
import json
import os

class MissionComputer:
    # 보너스 : setting.txt 에서 출력되는 정보의 항목을 셋팅할 수 있도록 수정.
    def __init__(self, setting_file="setting.txt"):
        # 현재 실행 중인 .py 파일의 디렉토리 경로를 가져옴.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 디렉토리 경로와 파일 이름을 합쳐서 절대 경로를 만듬.
        self.setting_file = os.path.join(current_dir, setting_file)
        self.settings = self._load_settings()

    # setting.txt에서 출력되는 정보 항목 가져오기.
    def _load_settings(self):
        if not os.path.exists(self.setting_file):
            print(f"경고: {self.setting_file} 파일이 없습니다. 모든 항목을 출력합니다.")
            return None
        
        with open(self.setting_file, "r", encoding="utf-8") as f:
            # 주석(#) 제외, 공백 제거 후 유효한 줄만 리스트로 반환
            return [line.split('#')[0].strip() for line in f if line.split('#')[0].strip()]

    def _filter_dict(self, data_dict):
        if self.settings is None:
            return data_dict
        return {k: v for k, v in data_dict.items() if k in self.settings}
    
    # 과제 1 : 미션 컴퓨터의 정보를 알아보는 get_mission_computer_info 메소드 추가.
    def get_mission_computer_info(self):
        total_memory_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        
        info_dict = {
            "운영체계": platform.system(),
            "운영체계 버전": platform.version(),
            "CPU의 타입": platform.processor(),
            "CPU의 코어 수": psutil.cpu_count(logical=False),
            "메모리의 크기": f"{total_memory_gb} GB"
        }
        filtered_info = self._filter_dict(info_dict)
        # 과제 2 : 시스템 정보를 JSON 형식으로 출력.
        return json.dumps(filtered_info, indent=4, ensure_ascii=False)

    # 과제 3, 4 : 미션 컴퓨터의 부하를 가져오는 get_mission_computer_load() 메소드 추가.
    def get_mission_computer_load(self):
        # interval=1은 1초 동안의 평균 사용량을 측정.
        cpu_usage = psutil.cpu_percent(interval=1)
        # 메모리 사용율 (%)
        memory_usage = psutil.virtual_memory().percent
        
        load_dict = {
            "CPU 실시간 사용량": f"{cpu_usage}%",
            "메모리 실시간 사용량": f"{memory_usage}%"
        }
        filtered_load = self._filter_dict(load_dict)
        # 과제 5 : 실시간 사용량 정보를 JSON 형식으로 출력.
        return json.dumps(filtered_load, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # 과제 7 : MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화.
    runComputer = MissionComputer("setting.txt")
    # 과제 6, 8 : get_mission_computer_info(), get_mission_computer_load() 출력.
    print('-- 필터링된 시스템 정보 ---')
    info_result = runComputer.get_mission_computer_info()
    print(info_result)
    
    print('\n--- 필터링된 실시간 사용량 정보 ---')
    load_result = runComputer.get_mission_computer_load()
    print(load_result)