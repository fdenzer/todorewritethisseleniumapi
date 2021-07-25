"""
bgg.loginpage
~~~~~~~~~~~~

Selenium Page Object to bind the login page and perform authentication

"""
from urllib.parse import quote


from selenium.common.exceptions import NoSuchElementException

from bggcli import BGG_BASE_URL
from bggcli.ui import BasePage
from bggcli.util.logger import Logger


class LoginPage(BasePage):
    def authenticate(self, login, password):
        """
        Performs authentication

        :param login: BGG login
        :param password: BGG password
        """
        Logger.info("Authenticating...", break_line=False)

        self.driver.get("%s/login" % BGG_BASE_URL)

        # When user is already authenticated, just skip this task
        # TODO Handle case where another user is logged in
        if self.is_authenticated():
            Logger.info(" (already logged) [done]", append=True)
            return True

        self.update_text(self.driver.find_element_by_id("username"), login)
        self.update_text(self.driver.find_element_by_id("password"), password)
        self.driver.find_element_by_xpath("//tr//td//input[@type='submit']")\
            .click()

        if self.is_authenticated():
            Logger.info(" [done]", append=True)
            return True

        Logger.info(" [error]", append=True)
        Logger.error("Authentication failed, check your credentials!")
        return False

    def is_authenticated(self):
        try:
            from selenium.webdriver.firefox.webelement import FirefoxWebElement
            msgbox: FirefoxWebElement = self.driver.find_element_by_xpath("//div[@class='messagebox']"
                                              )
            txt = msgbox.text

            return 'Login Successful' == txt
        except NoSuchElementException:
            return False
