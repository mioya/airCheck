from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import telegram
import asyncio
import schedule

day1 = 1
day1DeaSte = "프라하"
day2 = 2
day2DeaSte = "비엔나"
day3 = 3
day3DeaSte = "인천"
# 텔레그램 봇 토큰과 채팅 ID 설정
bot_token = '6728446177:AAG7FfqhCVc2dotQUuO-qcZJgDNWOu5Tzyg'
chat_id = '6873525036'


def setDeaste(dayDeaSte, day, driver):
    # 여정 클릭
    destination_input = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'booking-new__code'))
    )
    second_element = destination_input[day]
    second_element.click()

    # 팝업이 나타날 때까지 기다리기
    popup_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auto-search__text"))
    )

    # '프라하' 입력
    popup_input.send_keys(dayDeaSte)

    # 엔터 입력
    popup_input.send_keys(Keys.RETURN)
    # 몇 초간 대기 (프라하에 대한 자동 완성 결과가 나타날 때까지 기다릴 수 있습니다)
    time.sleep(0.3)


def setClass(driver):
    seat_class_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'booking-new__seatclass'))
    )
    seat_class_button.click()
    time.sleep(1)
    # 프레스티지석(label) 클릭
    prestige_label = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'seatclass__label'))
    )
    prestige_label[1].click()
    # 선택(button) 클릭
    select_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'confirm'))
    )
    select_button.click()


def choiceDate(xpath_expression, index, driver):
    date_button = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'booking-new__date'))
    )
    date_button[index].click()
    # XPath로 요소 찾기

    element = driver.find_element(by='xpath', value=xpath_expression)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    cal_confirm = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'dialog__confirm'))
    )
    cal_confirm.click()
    time.sleep(2)

def job():
    try:
        driver = webdriver.Chrome()
        driver.set_window_size(1000, 1000)
        driver.get('https://www.koreanair.com/')
        current_time = datetime.now()
        message = f"현재시간: {current_time} start"
    # 다구간 클릭
        print(message)
        multicity_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'quickbookings__multiple'))
        )
        multicity_button.click()

        setDeaste(day1DeaSte, day1, driver)
        setDeaste(day2DeaSte, day2, driver)
        setDeaste(day3DeaSte, day3, driver)
        setClass(driver)
        xpath_expression107 = "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[1]/div[3]/div[2]/div[11]/div[2]/table/tbody/tr[2]/td[2]/span[1]"
        xpath_expression1020 = "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[4]/td[1]/span[1]"

        choiceDate(xpath_expression107,  0, driver)
        choiceDate(xpath_expression1020, 1, driver)
        time.sleep(2)

        search = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'booking-new__search'))
        )
        search.click()
        time.sleep(8)
        # XPath로 label 요소 찾기
        # 클래스 이름으로 span 요소 찾기
        class_name = "flight-n__cabin-data -prime"
        elements = driver.find_element(By.CLASS_NAME, "flight-n__cabin-data").text
        current_time = datetime.now()
        message = f"현재시간: {current_time}\n정보: {elements}"
        # 텍스트 가져오기
        print(message)
        if elements != '편명 KE969 \n프레스티지 스탠다드\n 매진 ':
            # 텔레그램으로 메시지 보내기
            bot = telegram.Bot(token=bot_token)
            asyncio.run(bot.send_message(chat_id=chat_id, text=message))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 작업이 완료되면 브라우저 닫기
        driver.quit()


# 매 시간 정각에 job 함수 실행
schedule.every().minute.at(":20").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)