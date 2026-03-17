# python 정상 설치 여부 확인
print('Hello Mars')


# [수행 과제]
input_file = 'mission_computer_main.log'


# 파일 입출력 및 예외 처리
f = None

try:
    f = open(input_file, 'r', encoding='utf-8')
    for line in f:
        print(line.strip())

except FileNotFoundError:
    print('오류: 해당 파일을 찾을 수 없습니다.')

except Exception as e:
    # 예상치 못한 다른 모든 에러를 처리할 때 사용
    print(f'기타 오류 발생: {e}')

else:
    # try 문에서 오류가 발생하지 않으면 실행
    print('End of log.')

finally:
    # 예외 발생 여부 상관없이 항상 실행
    if f is not None:
        f.close()


# [보너스] 시간의 역순 출력
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        # 모든 라인을 리스트로 읽어와서 역순으로 뒤집음
        lines = f.readlines()
        for line in reversed(lines):
            print(line.strip())

except FileNotFoundError:
    print('오류: 해당 파일을 찾을 수 없습니다.')

except Exception as e:
    print(f'기타 오류 발생: {e}')


# [보너스] 파일 저장
output_file = 'log_extract.log'
limit = 3  # 저장할 줄 수

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        # 모든 라인을 리스트로 읽어와서 역순으로 뒤집음
        lines = f.readlines()

    # 마지막 3줄 추출
    last_3_lines = lines[-3:]

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.writelines(last_3_lines)

except FileNotFoundError:
    print('오류: 해당 파일을 찾을 수 없습니다.')

except Exception as e:
    print(f'기타 오류 발생: {e}')
