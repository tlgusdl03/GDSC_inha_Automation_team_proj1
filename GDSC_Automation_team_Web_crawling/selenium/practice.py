from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
from datetime import datetime
from time import sleep
from data import userid, userpassword

# 학교 홈페이지 아이디와 비밀번호
id = userid
pw = userpassword

# 현재 시각과 6개월 전의 날짜를 계산함
current_time = datetime.now()
six_months_ago = current_time - relativedelta(months=6)

# 엑셀 파일 열기
wb = Workbook()
ws = wb.active
ws.append(['분류', '제목', '좋아요', '싫어요', '조회수', '링크'])

# 웹 드라이버 초기화 
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.implicitly_wait(10)
print("웹 드라이버 초기화")

# 웹사이트 열기
driver.get('https://plaza.inha.ac.kr/plaza/2091/subview.do?enc=Zm5jdDF8QEB8JTJGcGxhemFCYnMlMkZwbGF6YSUyRjEwMDAxJTJGYXJ0Y2xMaXN0LmRvJTNG')
print("웹사이트 열기")

# 로그인 버튼 클릭
input_element = driver.find_element(By.XPATH, '//*[@id="menu2091_obj16"]/form/div/div/div[2]/div/span/input')
input_element.click()
print("로그인 버튼 클릭")

# 아이디, 비밀번호 입력
input_id = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[1]/dd/input')
input_pw = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[2]/dd/input')

input_id.send_keys(id)
input_pw.send_keys(pw)
input_pw.send_keys(Keys.RETURN)
print("아이디 비밀번호 입력")
sleep(1)

# 제목으로 정렬, 공모전 키워드만 검색
select = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div[2]/div[2]/form[1]/div[2]/div[2]/fieldset/select')
search = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div[2]/div[2]/form[1]/div[2]/div[2]/fieldset/input')
select_object = Select(select)
select_object.select_by_value('sj')
search.send_keys('공모전')
search.send_keys(Keys.RETURN)
print("공모전만 검색")
sleep(1)

# flag 설정
flag = False
# 페이지 설정
page_index = 1
# 데이터 수집 시작
while True:

    # 6개월 이전의 작성된 글일 경우 종료
    if flag:
        break

    # 각 게시물들의 리스트를 얻음
    Eventitles = driver.find_elements(By.CLASS_NAME, '_artclEven')
    Oddtitles = driver.find_elements(By.CLASS_NAME, '_artclOdd')
    print("게시물 리스트 얻음")

    # 게시물 안의 요소에 접근
    for i in Eventitles:
        sleep(1)
        date = i.find_element(By.XPATH, './td[5]').text # 작성일을 확인하여 6개월 이전에 작성된 경우 데이터 수집 종료
        converted_time = datetime.strptime(date, '%Y.%m.%d.')
        print("Eventitles`s date : " , date)
        print("Eventitles`s date : " , converted_time)

        if converted_time < six_months_ago:
            print("6개월 이전 게시물")
            flag = True
            break
        else:
            title_element = i.find_element(By.CSS_SELECTOR, '.artclLinkView')
            title = title_element.text # 제목
            href = title_element.get_attribute('href') # 링크
            category = i.find_element(By.XPATH, './td[2]/span').text # 분류
            up = i.find_element(By.XPATH, './td[6]').text # 좋아요
            down = i.find_element(By.XPATH, './td[7]').text # 싫어요
            access = i.find_element(By.XPATH, './td[8]').text # 조회수
            print(category, title, up, down, access, href)
            ws.append([category, title, up, down, access, href])
            print("추가함")

    for j in Oddtitles:

        sleep(1)
        date = j.find_element(By.XPATH, './td[5]').text # 작성일을 확인하여 6개월 이전에 작성된 경우 데이터 수집 종료
        converted_time = datetime.strptime(date, '%Y.%m.%d.')
        print("Oddtitles`s date : " , date)
        print("Oddtitles`s date : " , converted_time)

        if converted_time < six_months_ago:
            print("6개월 이전 게시물")
            flag = True
            break
        else:
            title_element = j.find_element(By.CSS_SELECTOR, '.artclLinkView')
            title = title_element.text # 제목
            href = title_element.get_attribute('href') # 링크
            category = j.find_element(By.XPATH, './td[2]/span').text # 분류
            up = j.find_element(By.XPATH, './td[6]').text # 좋아요
            down = j.find_element(By.XPATH, './td[7]').text # 싫어요
            access = j.find_element(By.XPATH, './td[8]').text # 조회수
            print(category, title, up, down, access, href)
            ws.append([category, title, up, down, access, href])
            print("추가함")

    # 다음 페이지로 넘어감
    try:
        page_index += 1
        next_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div[2]/div[2]/form[3]/div/div/ul/li[' + str(page_index) + ']')
        
    except:
        next_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div[2]/div[2]/form[3]/div/div/ul/li[' + str(page_index) + ']')
        page_index = 1
        next_button.click()
        print("다음 페이지")
        sleep(1)
    else:
        next_button.click()
        print("다음 페이지")
        sleep(1)

wb.save('test.xlsx')
print('완료')

