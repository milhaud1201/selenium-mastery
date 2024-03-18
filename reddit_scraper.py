from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

url = "https://www.reddit.com/r/korea/"

driver.get(url)

driver.implicitly_wait(30)

post_selector = "a[slot='full-post-link']"

posts = driver.find_elements(By.CSS_SELECTOR, post_selector)

# ActionChains 객체 초기화
actions = ActionChains(driver)

# for i in range(len(posts)):
for post in posts:
    actions.move_by_offset(0, 100).perform()

    # 반복문 안에서 예외 처리를 사용하여 스테일 요소 문제를 해결
    try:
        # 페이지가 새로 로드될 때마다 요소를 새로 가져와야 하므로, 매번 find_elements를 호출
        # posts = driver.find_elements(By.CSS_SELECTOR, post_selector)
        # post = posts[i]
        actions.move_to_element(post).click().perform()

        # 필요한 정보 추출
        post_title = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[slot='title']"))
        ).text
        post_class = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "no-decoration"))
        ).text
        text_body_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-post-click-location='text-body']")
            )
        )

        post_body = (
            text_body_element.text
            if text_body_element.is_displayed()
            else "Body not displayed"
        )

        print("Title:", post_title)
        print("Class:", post_class)
        if post_body:
            print("Body:", post_body)

        # 목록 페이지로 돌아가기
        driver.back()
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, post_selector))
        )

        post_title = ""
        post_class = ""
        post_body = ""

    except StaleElementReferenceException:
        print("StaleElementReferenceException 발생, 요소를 다시 찾습니다.")
        continue

# 브라우저 종료
driver.quit()
