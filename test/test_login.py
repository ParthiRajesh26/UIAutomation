import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
USERNAME = 'Admin'
PASSWORD = 'admin123'
USERNAME_XPATH = "//input[@name='username']"
PASSWORD_XPATH = "//input[@name='password']"
LOGIN_BUTTON_XPATH = "//button[@type='submit']"
DASHBOARD_URL_FRAGMENT = '/dashboard'

@pytest.fixture(scope='function')
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

def test_orangehrm_login_valid_user(driver):
    """
    Test Case: Automate login functionality for OrangeHRM
    Jira Key: KAN-15
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Click on Login button
    Expected Result:
        User should be redirected to the dashboard page.
    """
    try:
        driver.get(LOGIN_URL)
        # Wait for username field
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, USERNAME_XPATH))
        )
        username_field = driver.find_element(By.XPATH, USERNAME_XPATH)
        password_field = driver.find_element(By.XPATH, PASSWORD_XPATH)
        login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        username_field.clear()
        username_field.send_keys(USERNAME)
        password_field.clear()
        password_field.send_keys(PASSWORD)
        login_button.click()
        # Wait for dashboard redirect
        WebDriverWait(driver, 15).until(
            EC.url_contains(DASHBOARD_URL_FRAGMENT)
        )
        current_url = driver.current_url
        assert DASHBOARD_URL_FRAGMENT in current_url, (
            f"Login failed: Expected dashboard URL fragment '{DASHBOARD_URL_FRAGMENT}' in '{current_url}'"
        )
        # Additional validation: Check for dashboard element
        try:
            dashboard_header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
            )
            assert dashboard_header.is_displayed(), "Dashboard header not displayed after login."
        except Exception as e:
            pytest.fail(f"Dashboard validation failed: {e}")
    except Exception as e:
        pytest.fail(f"Test failed due to exception: {e}")
