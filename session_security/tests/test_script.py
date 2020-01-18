import datetime
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from .test_base import BaseLiveServerTestCase, WAIT_TIME


class ScriptTestCase(BaseLiveServerTestCase):


    def test_warning_shows_and_session_expires(self):
        start = datetime.datetime.now()

        for win in self.sel.window_handles:
            self.sel.switch_to_window(win)
            try:
                el = WebDriverWait(self.sel, self.max_warn_after).until(
                expected_conditions.visibility_of_element_located((By.ID, "session_security_warning")))
                assert(el.is_displayed())
            finally:
                pass
        end = datetime.datetime.now()
        delta = end - start

        self.assertGreaterEqual(delta.seconds, self.min_warn_after)
        self.assertLessEqual(delta.seconds, self.max_warn_after)

        for win in self.sel.window_handles:
            self.sel.switch_to_window(win)
            try:
                el = WebDriverWait(self.sel, self.max_expire_after).until(
                expected_conditions.visibility_of_element_located((By.ID, "id_password")))
                assert(el.is_displayed())
            finally:
                pass

        delta = datetime.datetime.now() - start
        self.assertGreaterEqual(delta.seconds, self.min_expire_after)
        self.assertLessEqual(delta.seconds, self.max_expire_after)

    def test_activity_hides_warning(self):
        time.sleep(6 * .7)
        try:
            WebDriverWait(self.sel, self.max_warn_after).until(
            expected_conditions.visibility_of_element_located((By.ID, "session_security_warning")))

            self.press_space()

            for win in self.sel.window_handles:
                self.sel.switch_to_window(win)

            try:
                el = WebDriverWait(self.sel, 20).until(
                expected_conditions.invisibility_of_element_located((By.ID, "session_security_warning")))

                assert(not el.is_displayed())
            finally:
                self.sel.quit()
        finally:
            self.sel.quit()


    def test_activity_prevents_warning(self):
        time.sleep(self.min_warn_after * .7)
        self.press_space()
        start = datetime.datetime.now()
        try:
            el = WebDriverWait(self.sel, self.max_warn_after).until(
            expected_conditions.visibility_of_element_located((By.ID, "session_security_warning")))
            assert(el.is_displayed())

            for win in self.sel.window_handles:
                self.sel.switch_to_window(win)

            delta = datetime.datetime.now() - start
            self.assertGreaterEqual(delta.seconds, self.min_warn_after)
        except:
            assert(False)
