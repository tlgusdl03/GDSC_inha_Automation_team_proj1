from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


driver = webdriver.Chrome() #브라우저로 아까 다운받은 크롬 드라이버 선택
driver.get("https://plaza.inha.ac.kr/plaza/2091/subview.do?enc=Zm5jdDF8QEB8JTJGcGxhemFCYnMlMkZwbGF6YSUyRjEwMDAxJTJGYXJ0Y2xMaXN0LmRvJTNGYmJzQ2xTZXElM0QlMjZiYnNPcGVuV3JkU2VxJTNEJTI2aXNWaWV3TWluZSUzRGZhbHNlJTI2c3JjaENvbHVtbiUzRGFsbCUyNnNyY2hXcmQlM0QlRUElQjMlQjUlRUIlQUElQTglRUMlQTAlODQlMjY%3D") #이미지 페이지를 연다
elem = driver.find_element_by_name("q") #검색창을 찾는 문장 name이 q이다. 개발자 화면을 열어서 확인하면 된다.
elem.send_keys("강아지") #검색창에 '강이지' 입력
elem.send_keys(Keys.RETURN) #엔터키 입력

#스크롤을 맨 아래까지 내려줘서 이미지를 나오게 한다.
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(1)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(new_height)
    if new_height == last_height:
        try :
            driver.find_element_by_class_name('mye4qd').click()
            time.sleep(3)
        except :
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")#검색 후 나온 모든 이미지를 images에 넣는다. #여러가지를 찾을때는 elements 
count = 1
for image in images :
    try :
        image.click() #모든 이미지들중 하나를 클릭
        time.sleep(1)#위에 코드에서 이미지를 클릭한 후 이미지의 주소를(src)를 가지고와야 하는데 이미지가 불러와지기 전에 다음 코드가 실행되기때문에 일정 시간을 주는 코드이다.
        imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img").get_attribute("src") #클릭한 이미지의 주소를 가지고온다. 기존에 class이름으로 찾는것을 하였지만 같은 이름이 어려개가 있어서 xpath로 수정하였다.
        urllib.request.urlretrieve(imgUrl, str(count)+".jpg") #이미지 저장
        count = count + 1
    except : 
        pass

driver.close()
#
#  assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source