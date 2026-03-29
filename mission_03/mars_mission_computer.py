# 과제 3 데이터 랜덤 생성
import random
from datetime import datetime

# 과제 1 클래스 생성
class DummySensor:
    def __init__(self):
        # 과제 2 사전 객체 추가
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    # 과제 4 랜덤 값 생성 메소드 추가
    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.randint(18, 30)
        self.env_values["mars_base_external_temperature"] = random.randint(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.randint(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.randint(500, 715)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 2)
        self.env_values["mars_base_internal_oxygen"] = random.randint(4, 7)

    # 과제 5 get_env() 메소드 추가
    def get_env(self, key=None):
        # 보너스 1 log 파일 생성 추가
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        in_temp = self.env_values["mars_base_internal_temperature"]
        ex_temp = self.env_values["mars_base_external_temperature"]
        in_humid = self.env_values["mars_base_internal_humidity"]
        ex_illum = self.env_values["mars_base_external_illuminance"]
        in_co2 = self.env_values["mars_base_internal_co2"]
        in_o2 = self.env_values["mars_base_internal_oxygen"]

        with open("ds_log.log", "a", encoding="utf-8") as f:
            log_entry = f"[{now}] 내부 온도: {in_temp}도, 외부 온도: {ex_temp}도, 내부 습도: {in_humid}%, 외부 광량: {ex_illum}W/m2, 내부 이산화탄소 농도: {in_co2}%, 내부 산소 농도: {in_o2}%\n"
            f.write(log_entry)

        if key:
            return self.env_values.get(key)
        return self.env_values


# 과제 6 인스턴스 생성
ds = DummySensor()

# 과제 7 set_env()와 get_env() 호출
ds.set_env()
env_datas = ds.get_env()
print(f"로그 저장: {env_datas}")
