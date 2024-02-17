from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import visibility_of
from webdriver_manager.chrome import ChromeDriverManager

from housewars.models import Activity


class FacilitatorEntry(StaticLiveServerTestCase):
    def setUp(self):
        # Headless chrome driver test setup
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        self.browser = Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.url = self.live_server_url + reverse('housewars:facilitator')

        # Initial data setup
        self.activity = Activity.objects.create(
            name='Dodgeball', time=30)

    def tearDown(self):
        self.browser.close()

    def test_form_submission(self):
        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        Select(self.browser.find_element(By.ID, 'activity')
               ).select_by_visible_text('Dodgeball - 30 min')
        self.browser.find_element(By.ID, 'submit').click()

        # Assert that signup is successful
        success_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-success').text

        self.assertEquals(
            success_text, 'Your facilitator signup has been submitted.')
