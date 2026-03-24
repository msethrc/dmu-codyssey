import csv
import pickle

CSV_FILE = 'Mars_Base_Inventory_List.csv'
OUTPUT_FILE = 'Mars_Base_Inventory_danger.csv'
BINARY_FILE = 'Mars_Base_Inventory_List.bin'

def task_1():
    print('과제 1. csv 출력')
    try: 
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print('오류: 해당 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'기타 오류 발생: {e}')

def task_2():
    print('과제 2. list 변환')
    try: 
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data_list = list(reader)
        return data_list
    except FileNotFoundError:
        print('오류: 해당 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'기타 오류 발생: {e}')

def task_3(data):
    print('과제 3. list 정렬')
    header = data[0]
    body = data[1:]

    try:
        flammability_index = header.index('Flammability')
    except ValueError:
        print('오류: flammability 컬럼을 찾을 수 없습니다.')
    else:
        sorted_body = sorted(body, key=lambda x: float(x[flammability_index]), reverse=True)
        sorted_data = [header] + sorted_body
        return sorted_data

def task_4(data):
    print('과제 4. list 필터링')
    header = data[0]
    body = data[1:]
    flammability_index = header.index('Flammability')

    filtered_body = [row for row in body if float(row[flammability_index]) > 0.7]
    filtered_data = [header] + filtered_body
    for row in filtered_data:
        print(row)
    return filtered_data

def task_5(data):
    print('과제 5. csv 저장')
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')

def bonus_1(data):
    print('보너스 1. 이진 파일 저장')
    try:
        with open(BINARY_FILE, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f'이진 파일 저장 중 오류 발생: {e}')

def bonus_2():
    print('보너스 2. 이진 파일 출력')
    try:
        with open(BINARY_FILE, 'rb') as f:
            data = pickle.load(f)

            if data:
                for row in data:
                    print(row)
            else:
                print('이진 파일에 데이터가 없습니다.')
            return data
    except FileNotFoundError:
        print('오류: 해당 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'기타 오류 발생: {e}')

if __name__ == '__main__':
    # 과제 1. csv 출력
    task_1()

    # 과제 2. list 변환
    csv_list = task_2()

    if csv_list:
        # 과제 3. list 정렬
        sorted_list = task_3(csv_list)

        # 과제 4. list 필터링
        filtered_list = task_4(sorted_list)

        # 과제 5. csv 저장
        task_5(filtered_list)

        # 보너스 1. 이진 파일 저장
        bonus_1(sorted_list)

        # 보너스 2. 이진 파일 출력
        bonus_2()

        # 보너스 3. 텍스트 파일 vs 이진 파일 차이점 및 장단점
        '''
        * 텍스트 파일
         사람이 읽을 수 있는 문자로 이루어진 파일
         • 장점
           - (가독성O) 사람이 직접 읽고 수정 가능
           - (호환성) 다양한 시스템에서 동일하게 사용 가능
         • 단점
           - (용량↑) 데이터를 문자로 변환하므로 이진 파일보다 용량이 큼
           - (속도↓) 저장 시 인코딩, 읽을 때 디코딩 과정이 필요해 상대적으로 느림

        * 이진 파일
         컴퓨터가 이해하는 0과 1로 이루어진 파일
         • 장점
           - (용량↓) 데이터를 압축하거나 그대로 저장하므로 용량이 작음
           - (속도↑) 컴퓨터가 즉시 읽을 수 있는 형태라 처리 속도가 매우 빠름
         • 단점 
           - (가독성X) 사람이 직접 읽기 어려움
           - (의존성) 특정 프로그램이나 운영체제의 데이터 처리 방식에 종속되는 경우가 많음
        '''
