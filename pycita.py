from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select 
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import sender, config, os
driver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)



def create_fast_url(province):
    operation_category = "icpco"
    return "https://icp.administracionelectronica.gob.es/{}/citar?p={}".format(
        operation_category, province
    )

def check_cita_tie_pickup(context: config.Customer):
    # Processing Outline

    browser = webdriver.Chrome(options=options)
    url = create_fast_url(c.province)
    browser.get(url)


    # # Select office
    office_form = browser.find_element(By.XPATH, '//*[@id="sede"]')
    office_dd = Select(office_form)
    office_dd.select_by_visible_text(config.offices["Fuengirola"])

    # # Select  service
    
    service_form = browser.find_element(By.XPATH, '//*[@id="tramiteGrupo[0]"]')
    service_dd = Select(service_form)
    service_dd.select_by_visible_text(config.services["pickup_tie"])
    time.sleep(2)
    submit_button = browser.find_element(By.XPATH, '//*[@id="btnAceptar"]')
    browser.execute_script('arguments[0].scrollIntoView();', submit_button)
    try:
        WebDriverWait(browser, config.WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAceptar"]'))).send_keys(Keys.ENTER)
    except TimeoutException:
        logging.error("Timed out waiting for form to load")
    


    try:
        WebDriverWait(browser, config.WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnEntrar"]'))).send_keys(Keys.ENTER)
    except TimeoutException:
        logging.error("Timed out waiting for form to load")
    
    # Fill credentials

    browser.find_element(By.XPATH, '//*[@id="txtIdCitado"]').send_keys(c.nie)
    browser.find_element(By.XPATH, '//*[@id="txtDesCitado"]').send_keys(c.name)
    try:
        WebDriverWait(browser, config.WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnEnviar"]'))).send_keys(Keys.ENTER)
    except TimeoutException:
        logging.error("Timed out waiting for form to load")
    # Solicitar
    try:
        WebDriverWait(browser, config.WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnEnviar"]'))).send_keys(Keys.ENTER)
    except TimeoutException:
        logging.error("Timed out waiting for form to load")
    
    if "En este momento no hay citas disponibles." in browser.page_source:
        browser.close()
        return False
    else:
        browser.close()
        return True

if __name__ == '__main__':
    c = config.Customer (
        nie = os.getenv('NIE'),
        name = os.getenv('NAME'),
        province = config.Province.MÁLAGA,
        chat_id = os.getenv('CHAT_ID'),
        token =  os.getenv('TELEGRAM_API_KEY'),


    )

    result = check_cita_tie_pickup(c)
    if not result:
        sender.send_message(c, "NO CITA :(")
    else:
        sender.send_message(c, "CITA IS AVALIABLE !!!!")
    