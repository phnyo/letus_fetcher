from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from session_id import userid, passwd
import time, requests

def scrape():
    print('[FUNCTION] scrape')
    try:
        options = Options()
        options.add_argument('-headless')
        
        driver = webdriver.Firefox(options=options)
        print('[MIS] driver profile set.')

        driver.get('https://letus.ed.tus.ac.jp/login/index.php')
        print('[GET] https://letus.ed.tus.ac.jp/login/index.php')

        userform = driver.find_element(by=By.ID, value="username").send_keys(userid)
        password = driver.find_element(by=By.ID, value="password").send_keys(passwd)
        driver.find_element(by=By.ID, value="loginbtn").click()
        time.sleep(3)

        print('[GET] https://letus.ed.tus.ac.jp')
        #レタスのメインページ
        driver.find_element(by=By.LINK_TEXT, value="カレンダーへ移動する ...").click()
        time.sleep(3)

        print('[GET] https://letus.ed.tus.ac.jp/calendar/view.php?view=upcoming')
        
        #カレンダーのページ
        driver.find_element(by=By.CLASS_NAME, value="singlebutton").find_element(by=By.TAG_NAME, value="button").click()
        time.sleep(3)

        print('[GET] https://letus.ed.tus.ac.jp/calendar/export.php')

        #エクスポートオプションの指定
        driver.find_element(by=By.ID, value="id_events_exportevents_all").click()
        driver.find_element(by=By.ID, value="id_period_timeperiod_recentupcoming").click()
        #driver.find_element(by=By.ID, value="id_export").click()
        driver.find_element(by=By.ID, value="id_generateurl").click()
        
        calendar_url = driver.find_element(by=By.XPATH, value="//div[@class='generalbox calendarurl']").text.split()[1]
        print(f'[SUC] URL generated. URL:{calendar_url}')
       
        filename = "tmpcalendar.ics"
        urlData = requests.get(calendar_url).content

        with open(filename, mode='wb') as f:
            f.write(urlData)

        print('[SUC] ics file downloaded successfully.')

    finally:
        print('[MIS] cleaning up...')
        driver.quit()
        print('[FUNCTION] scrape end')
