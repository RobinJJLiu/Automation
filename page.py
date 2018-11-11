import os, random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from appium.webdriver.common.touch_action import TouchAction
from time import sleep
from appium import webdriver

class BasePage(object):
    
    def __init__(self, application):
        self.application = application

    def swipe_page(self, start_x, start_y, end_x, end_y, timer):
        self.application.swipe(start_x, start_y, end_x, end_y, timer)

    def is_content_exist(self, search_keywords, check_point):
        try:
            wording = self.application.find_element_by_xpath(check_point).text
            print(wording)
            if search_keywords in wording:
                return True
            else:
                return False
        except:
            return False

    def is_element_exist(self, element_locator):
        try:
            WebDriverWait(self.application, 20).until(EC.presence_of_element_located(element_locator))
            return True
        except:
            return False
    
    def click_element(self, element_locator):
        try:
            element = WebDriverWait(self.application, 20).until(EC.element_to_be_clickable(element_locator))
            element.click()
            return True
        except:
            return False
    
    def take_screenshot(self):
        SCREENSHOT_DIR = os.path.abspath(os.path.join(__file__, '../screenshots/'))
        filename = 'Result excluding keywords_' + str(random.randint(1, 100000)) + '.png'
        fullPath = os.path.join(SCREENSHOT_DIR, filename)
        self.application.get_screenshot_as_file(fullPath)

class LogOnPage(BasePage):
    #ID locator
    ID_LogOn            = (By.ID, "com.thecarousell.Carousell:id/welcome_page_login_button")
    ID_SelectAccount    = (By.ID, "com.google.android.gms:id/credential_picker_options")

    #xpath locator
    xpath_SelectAccount = (By.XPATH, '//android.widget.LinearLayout[@content-desc="team dp"]/android.widget.LinearLayout')

    def check_log_on_element(self):
        return self.is_element_exist(self.ID_LogOn)
    
    def click_log_on_element(self):
        return self.click_element(self.ID_LogOn)

    def check_account_element(self):
        return self.is_element_exist(self.ID_SelectAccount)
    
    def click_account_element(self):
        return self.click_element(self.ID_SelectAccount)

class MainPage(BasePage):
    #xpath locator
    xpath_SeeAllGroup   = (By.XPATH, '//*/android.widget.TextView[@class="android.widget.TextView"][@text="See All"]')

    def check_see_all_Category(self):
        return self.is_element_exist(self.xpath_SeeAllGroup)

    def click_see_all_Category(self):
        return self.click_element(self.xpath_SeeAllGroup)

class CategoryPage(BasePage):
    #xpath locator
    xpath_Following     = (By.XPATH, '//*/android.widget.LinearLayout/android.widget.TextView[@text="Following"]')
    xpath_Cars          = (By.XPATH, '//*/android.widget.LinearLayout/android.widget.TextView[@text="Cars"]')

    def check_following_Category(self):
        return self.is_element_exist(self.xpath_Following)
    
    def check_cars_Category(self):
        return self.is_element_exist(self.xpath_Cars)
    
    def click_cars_Category(self):
        return self.click_element(self.xpath_Cars)

class SearchPage(BasePage):
    #Search keyword
    search_keywords     = "Porsche"

    #ID locator
    ID_Search           = (By.ID, "header_page_search_text_field")
    ID_Search_Input     = (By.ID, "input_search_bar")
    ID_Feature_Button_OK= (By.ID, "feature_button")

    #xpath locator
    xpath_FirstResult   = (By.XPATH, '//*/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]')
    xpath_ResultContent = (By.XPATH, '//*/android.view.ViewGroup[@resource-id="com.thecarousell.Carousell:id/view_coordinated"]')
    xpath_FirstGoods    = (By.XPATH, '//*/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]')
    xpath_Title         = (By.XPATH, '//*/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[@resource-id="com.thecarousell.Carousell:id/tvInfo"]')
    xpath_Description   = (By.XPATH, '//*/android.widget.RelativeLayout[7]/android.widget.LinearLayout/android.widget.TextView[@resource-id="com.thecarousell.Carousell:id/tvInfo"]')
    
    def check_ok_button(self):
        return self.is_element_exist(self.ID_Feature_Button_OK)
    
    def click_ok_button(self):
        return self.click_element(self.ID_Feature_Button_OK)

    def check_search_bar(self):
        return self.is_element_exist(self.ID_Search)
    
    def click_search_bar(self):
        return self.click_element(self.ID_Search)

    def input_keywords(self, search_keywods):
        self.application.find_element_by_id(self.ID_Search_Input[1]).send_keys(self.search_keywords)

    def check_any_results(self):
        return self.is_element_exist(self.xpath_FirstResult)
    
    def click_first_result(self):
        return self.click_element(self.xpath_FirstResult)
    
    def check_any_result_contents(self):
        return self.is_element_exist(self.xpath_ResultContent)
    
    def is_keywords_in_title(self, search_keywords):
        return self.is_content_exist(search_keywords, self.xpath_Title[1])
        
    def is_keywords_in_description(self, search_keywords):
        return self.is_content_exist(search_keywords, self.xpath_Description[1])

    def click_goods(self):
        self.click_element(self.xpath_FirstGoods)