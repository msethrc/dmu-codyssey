import string

def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 해독하는 함수
    # param  : target_text(해독할 문자열)
    # return : (해독 결과 딕셔너리, 자동감지된 shift 번호)
    """
    results = {}
    alphabet = string.ascii_lowercase
    num_alphabet = len(alphabet)
    
    # 텍스트 사전 생성
    dictionary = ["emergency", "secret", "password", "access", "key", "door", "open", "hello", "mars"]
    detected_shift = None

    print(f"\n--- 암호 해독 시작 (대상: {target_text}) ---")

    # 과제 4 : 알파벳 수(26번)만큼 반복하며 자리수 변경
    for shift in range(num_alphabet):
        decoded_text = ""
        for char in target_text:
            if char.lower() in alphabet:
                idx = alphabet.find(char.lower())
                # 복호화: 현재 위치에서 shift만큼 뒤로 이동
                new_idx = (idx - shift) % num_alphabet
                
                # 대소문자 구분 유지
                if char.isupper():
                    decoded_text += alphabet[new_idx].upper()
                else:
                    decoded_text += alphabet[new_idx]
            else:
                # 알파벳이 아닌 경우(공백, 특수문자 등) 그대로 유지
                decoded_text += char
        
        results[shift] = decoded_text
        # 과제 5 : 해독된 결과 출력
        print(f"Shift {shift:2d}: {decoded_text}")

        # 보너스 : 사전에 있는 단어와 일치하는 키워드가 발견될 경우 반복 중단
        found_keyword = False
        for word in dictionary:
            if word in decoded_text.lower():
                print(f"\n[자동 감지] '{word}' 키워드를 발견하여 해독을 중단합니다. (Shift: {shift})")
                detected_shift = shift
                found_keyword = True
                break # 사전 탐색 루프 중단
        
        if found_keyword:
            break # 전체 shift 반복 루프 중단

    return results, detected_shift

def main():
    # 과제 1 : password.txt 파일 읽기
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            target_text = f.read().strip()
    except FileNotFoundError:
        print("Error: password.txt 파일을 찾을 수 없습니다.")
        return

    # 과제 2,3 : 카이사르 해독 수행 (함수 호출 및 파라메터 전달)
    all_results, auto_shift = caesar_cipher_decode(target_text)

    # 해독 결과 확인 및 선택
    final_text = ""
    
    if auto_shift is not None:
        # 자동 감지된 경우
        print(f"\n자동 해독된 결과: {all_results[auto_shift]}")
        confirm = input("이 결과가 맞습니까? (y/n): ").lower()
        if confirm == 'y':
            final_text = all_results[auto_shift]
        else:
            choice = int(input("눈으로 확인 후 올바른 Shift 번호를 직접 입력하세요: "))
            final_text = all_results.get(choice, "")
    else:
        # 자동 감지되지 않은 경우 사용자가 직접 선택
        choice = int(input("\n사전에서 일치하는 단어를 찾지 못했습니다. 해독 번호를 입력하세요: "))
        final_text = all_results.get(choice, "")

    # 과제 6 : 선택한 결과를 result.txt로 저장
    if final_text:
        with open("result.txt", "w", encoding="utf-8") as f_res:
            f_res.write(final_text)
        print(f"\n[성공] 최종 결과가 'result.txt'에 저장되었습니다.")
        print(f"내용: {final_text}")
    else:
        print("\n[오류] 저장할 결과가 없습니다.")

if __name__ == "__main__":
    main()