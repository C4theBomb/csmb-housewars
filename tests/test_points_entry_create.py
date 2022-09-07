from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import visibility_of

from housewars.models import House, Activity, Award


class UserEntryCreatePageTest(StaticLiveServerTestCase):
    def setUp(self):
        # Headless chrome driver test setup
        options = Options()
        options.add_argument('--headless')
        self.browser = Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.url = self.live_server_url + reverse('housewars:add_points')

        # Initial data setup
        self.house = House.objects.create(name='Hawk')
        self.activity = Activity.objects.create(name='Dodgeball', time=30)
        self.award = Award.objects.create(name='1st', activity=self.activity)

    def tearDown(self):
        self.browser.close()

    def test_user_form_submission(self):
        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs
        Select(self.browser.find_element(By.ID, 'id_activity')
               ).select_by_visible_text('Dodgeball (30)')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        Select(self.browser.find_element(By.ID, 'id_award')
               ).select_by_visible_text('1st')
        self.browser.find_element(By.ID, 'submit').click()

        # Verify that success message is shown
        success_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-success').text
        self.assertEquals(
            success_text, 'Your points entry has been submitted.')

    def test_no_awards_on_default(self):
        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Verify that only null option is in options
        award_select = Select(self.browser.find_element(By.ID, 'id_award'))
        self.assertEquals(len(award_select.options), 1)
