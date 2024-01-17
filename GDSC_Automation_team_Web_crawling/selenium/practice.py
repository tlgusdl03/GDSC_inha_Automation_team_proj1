

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from time import sleep
from data import userid, userpassword

id = userid
pw = userpassword

# 엑셀 파일 열기
wb = Workbook()
ws = wb.active
ws.append(['분류', '제목', '좋아요', '싫어요', '조회수', '링크'])

# 웹 드라이버 초기화 
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.implicitly_wait(10)

# 웹사이트 열기
driver.get('https://plaza.inha.ac.kr/plaza/2091/subview.do?enc=Zm5jdDF8QEB8JTJGcGxhemFCYnMlMkZwbGF6YSUyRjEwMDAxJTJGYXJ0Y2xMaXN0LmRvJTNG')

# 로그인 버튼 클릭
# input_element = wait.until(EC.element_to_be_clickable(By.XPATH, '//*[@id="menu2091_obj16"]/form/div/div/div[2]/div/span/input'))
input_element = driver.find_element(By.XPATH, '//*[@id="menu2091_obj16"]/form/div/div/div[2]/div/span/input')
input_element.click()

# 아이디, 비밀번호 입력
# input_id = wait.until(EC.element_to_be_clickable(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[1]/dd/input'))
input_id = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[1]/dd/input')
# input_pw = wait.until(EC.element_to_be_clickable(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[2]/dd/input'))
input_pw = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/article/div/form/div/div[1]/dl[2]/dd/input')

input_id.send_keys(id)

input_pw.send_keys(pw)

input_pw.send_keys(Keys.RETURN)


# 데이터 수집 5페이지까지
for j in range(1, 5):

    # 각 게시물들의 리스트를 얻음
    titles = driver.find_elements(By.CLASS_NAME, '_artclEven')

    for i in titles:

        title_element = i.find_element(By.CSS_SELECTOR, '.artclLinkView')
        title = title_element.text # 제목
        href = title_element.get_attribute('href') # 링크
        category = i.find_element(By.XPATH, './td[2]/span').text # 분류
        up = i.find_element(By.XPATH, './td[6]').text # 좋아요
        down = i.find_element(By.XPATH, './td[7]').text # 싫어요
        access = i.find_element(By.XPATH, './td[8]').text # 조회수
        ws.append([category, title, up, down, access, href])
    next_button = driver.find_element(By.CSS_SELECTOR, '._next')
    next_button.click()
    sleep(1)

wb.save('test.xlsx')
print('완료')