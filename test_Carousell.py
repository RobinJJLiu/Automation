import unittest, time, os, random
import subprocess
from subprocess import Popen, PIPE
from selenium import webdriver
from appium import webdriver
from page import LogOnPage, MainPage, CategoryPage, SearchPage

android_desired_caps = {
  "platformName": "Android",
  "deviceName": "Pixel 2 API 28",
  "appActivity": "com.thecarousell.Carousell.screens.general.EntryActivity",
  "appPackage": "com.thecarousell.Carousell",
  "automationName": "UiAutomator2",
  "newCommandTimeout": 300
}

class test_Carousell(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        subprocess.Popen("appium --address 127.0.0.1 --port 4723", shell=True)
        self.application = webdriver.Remote('http://localhost:4723/wd/hub', android_desired_caps)
    
    def test_1_check_LogOn(self):
        LogOn = LogOnPage(self.application)
        #Check LogOn Element and Click
        self.assertTrue(LogOn.check_log_on_element(), "Cannot find the LogOn element")
        self.assertTrue(LogOn.click_log_on_element(), "Cannot Click the LogOn element")
        #Check Account Element and Click
        self.assertTrue(LogOn.check_account_element(), "Cannot find the Account element")
        self.assertTrue(LogOn.click_account_element(), "Cannot Click the Account element")

    def test_2_go_to_car_category(self):
        mainPage = MainPage(self.application)
        #Check SeeAll Element of Category and Click
        self.assertTrue(mainPage.check_see_all_Category(), "Cannot find the SeeAll element of Category")
        self.assertTrue(mainPage.click_see_all_Category(), "Cannot Click the SeeAll element of Category")
        
        category = CategoryPage(self.application)
        #Check in the Category
        self.assertTrue(category.check_following_Category(), "May be not in the Category")
        
        #Chck Cars Element in th Category and Click
        while(not category.check_cars_Category()):
            category.swipe_page(540, 1700, 540, 500, 1000)
            #self.application.implicitly_wait(2)
        self.assertTrue(category.click_cars_Category(), "Cannot Click the Cars element in the Category")

    def test_3_check_search_result(self):
        #Check First Time Notification Tips and Click OK
        search = SearchPage(self.application)
        self.assertTrue(search.check_ok_button(), "Cannot find the OK button")
        self.assertTrue(search.click_ok_button(), "Cannot click the OK buuton")

        #Check Search Bar
        self.assertTrue(search.check_search_bar(), "Cannot find the Search Bar")
        self.assertTrue(search.click_search_bar(), "Cannot click the Click Bar")
    
        #Input keywords and Search
        search_keywords = "Porsche"
        search.input_keywords(search_keywords)
        self.assertTrue(search.check_any_results(), "No Results related with keywords show")
        self.assertTrue(search.click_first_result(), "Cannot click the first result")

        #Check Search result
        result = SearchPage(self.application)
        self.assertTrue(result.check_any_result_contents(), "No Result Contents for keywords show")
        #Check first content
        result.click_goods()
        #check toast
        self.assertTrue(result.check_ok_button(), "Cannot find the OK button")
        self.assertTrue(result.click_ok_button(), "Cannot click the OK buuton")
        #check toast
        self.assertTrue(result.check_ok_button(), "Cannot find the OK button")
        self.assertTrue(result.click_ok_button(), "Cannot click the OK buuton")
        #check title and description
        word = self.application.find_element_by_xpath('//*/android.widget.RelativeLayout[1]/*/android.widget.TextView[@resource-id="com.thecarousell.Carousell:id/tvInfo"]').text
        print(word)
        if search_keywords in word:
            print('INININININ')
        self.assertTrue(result.is_keywords_in_title(search_keywords), "Keyword is not in the Title")
        self.assertTrue(result.is_keywords_in_description(search_keywords), "Keyword is not in the Description")

    @classmethod
    def tearDownClass(self):
        #quit app
        self.application.quit()
        #quit appium connection
        os.system("taskkill /F /IM node.exe")

if __name__ == '__main__':
    unittest.main()