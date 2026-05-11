import zipfile
import time
import string
import multiprocessing
from datetime import datetime
import zlib

# 1. 자식 프로세스들이 공유할 전역 변수 선언
shared_counter = None

def init_worker(counter):
    """각 프로세스가 시작될 때 실행되어 공유 변수를 전역으로 설정"""
    global shared_counter
    shared_counter = counter

def get_password_by_index(index, characters, length):
    base = len(characters)
    pwd = []
    for _ in range(length):
        index, rem = divmod(index, base)
        pwd.append(characters[rem])
    return ''.join(reversed(pwd))

def attempt_unlock_chunk(zip_path, start_idx, end_idx, characters, length):
    """더 이상 counter를 인자로 받지 않고 전역 변수 shared_counter를 사용"""
    global shared_counter
    local_count = 0
    with zipfile.ZipFile(zip_path) as z_file:
        for i in range(start_idx, end_idx):
            password = get_password_by_index(i, characters, length)
            local_count += 1
            
            if local_count % 1000 == 0:
                with shared_counter.get_lock():
                    shared_counter.value += 1000
                local_count = 0

            try:
                # 패스워드 검증 (가장 가벼운 파일 하나만 시도)
                z_file.read(z_file.namelist()[0], pwd=password.encode('utf-8'))
                with shared_counter.get_lock():
                    shared_counter.value += local_count
                return password
            except (RuntimeError, zipfile.BadZipFile, zlib.error):
                continue
    return None

def unlock_zip(zip_path, password_length=6):
    characters = string.ascii_lowercase + string.digits
    total_combinations = len(characters) ** password_length
    start_time = time.time()
    
    # 실시간 반복 횟수를 저장할 공유 변수 생성
    counter = multiprocessing.Value('i', 0)
    
    print(f"--- 작업 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"--- 총 시도 예정 조합: {total_combinations:,} 개 ---")

    num_cores = multiprocessing.cpu_count()
    chunk_size = total_combinations // num_cores
    
    found_password = None
    
    # 2. Pool 생성 시 initializer와 initargs를 통해 공유 변수 전달
    with multiprocessing.Pool(processes=num_cores, initializer=init_worker, initargs=(counter,)) as pool:
        results = []
        for i in range(num_cores):
            s_idx = i * chunk_size
            e_idx = (i + 1) * chunk_size if i < num_cores - 1 else total_combinations
            # 인자에서 counter를 제거함
            res = pool.apply_async(attempt_unlock_chunk, (zip_path, s_idx, e_idx, characters, password_length))
            results.append(res)

        try:
            while not found_password:
                elapsed = time.time() - start_time
                current_attempts = counter.value
                print(f"\r[탐색 중] 시도 횟수: {current_attempts:,} / {total_combinations:,} | 경과 시간: {elapsed:.2f}초", end="")
                
                for r in results:
                    if r.ready():
                        res_val = r.get()
                        if res_val:
                            found_password = res_val
                            pool.terminate()
                            break
                if all(r.ready() for r in results): break
                time.sleep(0.1) 
        except KeyboardInterrupt:
            pool.terminate()
            print("\n사용자에 의해 중단되었습니다.")
            return

    total_duration = time.time() - start_time
    if found_password:
        print(f"\n\n[성공] 암호: {found_password}")
        print(f"최종 반복 횟수: {counter.value:,}회")
        print(f"총 소요 시간: {total_duration:.2f}초")
        
        with open("password.txt", "w") as f:
            f.write(found_password)
    else:
        print(f"\n\n[실패] 모든 조합 시도 완료.")

if __name__ == "__main__":
    target_zip = 'emergency_storage_key.zip'
    # Windows 환경을 위한 필수 안전장치
    multiprocessing.freeze_support()
    unlock_zip(target_zip)