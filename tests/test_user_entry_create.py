from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.expected_conditions import visibility_of
from webdriver_manager.chrome import ChromeDriverManager

from housewars.models import House, Activity, UserEntry


class UserEntryCreatePageTest(StaticLiveServerTestCase):
    def setUp(self):
        # Headless chrome driver test setup
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        self.browser = Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        self.url = self.live_server_url + reverse('housewars:signup')

        # Initial data setup
        self.house = House.objects.create(name='Hawk')
        self.activity30 = Activity.objects.create(
            name='Dodgeball', time=30, default_quota=5)
        self.activity60 = Activity.objects.create(
            name='Volleyball', time=60, default_quota=5)
        self.hidden = Activity.objects.create(
            name='Hidden', time=30, default_quota=1)

    def tearDown(self):
        self.browser.close()

    def test_valid_form_submission(self):
        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@slps.org')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        self.browser.find_element(By.ID, 'submit').click()

        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'activity1')))

        Select(self.browser.find_element(By.ID, 'activity1')
               ).select_by_visible_text('Dodgeball - 30 min')
        Select(self.browser.find_element(By.ID, 'activity2')
               ).select_by_visible_text('Dodgeball - 30 min')

        self.browser.find_element(By.ID, 'submit').click()

        # Verify signup is successful
        success_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-success').text

        self.assertEquals(success_text, 'Your signup has been submitted.')

        # Verify that activity detail cards are present
        activity_confirm = self.browser.find_elements(
            By.CSS_SELECTOR, 'div.alert.alert-success')

        self.assertEquals(len(activity_confirm), 3)

    def test_invalid_email(self):
        self.browser.get(self.live_server_url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs except email
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@gmail.com')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        self.browser.find_element(By.ID, 'submit').click()

        # Verify that there is a domain error on submit
        error_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-danger').text
        self.assertEquals(error_text, 'Please use your school email.')

    def test_used_email(self):
        UserEntry.objects.create(first_name='Test', last_name='User', email='test.user@slps.org', grade=9, house=self.house,
                                 activity1=self.activity30, activity2=self.activity30)

        self.browser.get(self.live_server_url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs and duplicate email
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@slps.org')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        self.browser.find_element(By.ID, 'submit').click()

        # Verify that duplicate error shows up on submit
        error_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-danger').text
        self.assertEquals(
            error_text, 'A signup with this email already exists, if you want to change your signups, please email cpatino8605@slps.org.')

    def test_invalid_activities_are_not_visible(self):
        UserEntry.objects.create(first_name='Test', last_name='User', email='user.exist@slps.org', grade=9, house=self.house,
                                 activity1=self.hidden, activity2=self.activity30)

        self.browser.get(self.live_server_url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@slps.org')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        self.browser.find_element(By.ID, 'submit').click()

        # Wait until browser loads next step of form before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'activity1')))

        activity1 = Select(self.browser.find_element(By.ID, 'activity1'))
        activity2 = Select(self.browser.find_element(By.ID, 'activity2'))

        # Assert that full activity is not shown
        self.assertRaises(NoSuchElementException,
                          activity1.select_by_visible_text, 'Hidden - 30 min')
        # Asser that 60 minute activity is not shown in second slot
        self.assertRaises(NoSuchElementException,
                          activity2.select_by_visible_text, 'Volleyball - 60 min')

        # Assert that valid activities are still shown in slot
        activity1.select_by_visible_text('Volleyball - 60 min')
        activity2.select_by_visible_text('Hidden - 30 min')

    def test_full_activity_shows_for_other_houses(self):
        House.objects.create(name='Snowy')
        UserEntry.objects.create(first_name='Test', last_name='User', email='user.exist@slps.org', grade=9, house=self.house,
                                 activity1=self.hidden, activity2=self.hidden)

        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs and separate house
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@slps.org')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Snowy')
        self.browser.find_element(By.ID, 'submit').click()

        # Wait until browser loads next form step before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'activity1')))

        # Verify that full activity is still showing for other house
        activity1 = Select(self.browser.find_element(By.ID, 'activity1'))
        activity2 = Select(self.browser.find_element(By.ID, 'activity2'))
        activity1.select_by_visible_text('Hidden - 30 min')
        activity2.select_by_visible_text('Hidden - 30 min')

    def test_activities_gt_allowed_time(self):
        self.browser.get(self.url)

        # Wait until browser loads page before continuing
        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'header')))

        # Fill in form with valid inputs
        self.browser.find_element(By.ID, 'first-name').send_keys('Test')
        self.browser.find_element(By.ID, 'last-name').send_keys('User')
        self.browser.find_element(
            By.ID, 'email').send_keys('test.user@slps.org')
        Select(self.browser.find_element(By.ID, 'grade')
               ).select_by_visible_text('9th/Freshman')
        Select(self.browser.find_element(By.ID, 'house')
               ).select_by_visible_text('Hawk')
        self.browser.find_element(By.ID, 'submit').click()

        WebDriverWait(self.browser, timeout=5).until(
            visibility_of(self.browser.find_element(By.ID, 'activity1')))

        Select(self.browser.find_element(By.ID, 'activity1')
               ).select_by_visible_text('Volleyball - 60 min')
        Select(self.browser.find_element(By.ID, 'activity2')
               ).select_by_visible_text('Dodgeball - 30 min')

        self.browser.find_element(By.ID, 'submit').click()

        # Verify error
        error_text = self.browser.find_element(
            By.CSS_SELECTOR, 'div.alert.alert-danger').text
        self.assertEquals(
            error_text, 'Please pick activities adding up to one hour.')
