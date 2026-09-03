from playwright.sync_api import sync_playwright, expect
import random

BASE_URL = "https://practicesoftwaretesting.com/"
REGISTER_URL = "https://practicesoftwaretesting.com/auth/register"
LOGIN_URL = "https://practicesoftwaretesting.com/auth/login"

registration_scenarios = [

    {
        "name": "Scenario 1 - Empty First Name",
        "first_name": "",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "testuser01@gmail.com",
        "password": "Volleyball*1303",
        "valid": False
    },

    {
        "name": "Scenario 2 - Empty Last Name",
        "first_name": "arun",
        "last_name": "",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "testuser02@gmail.com",
        "password": "Volleyball*1303",
        "valid": False
    },

    {
        "name": "Scenario 3 - Invalid Email",
        "first_name": "arun",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "invalid-email",
        "password": "Volleyball*1303",
        "valid": False
    },

    {
        "name": "Scenario 4 - Missing Password",
        "first_name": "arun",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "testuser04@gmail.com",
        "password": "",
        "valid": False
    },

    {
        "name": "Scenario 5 - Invalid Password",
        "first_name": "arun",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "email": "testuser05@gmail.com",
        "phone": "8870618311",
        "password": "123",
        "valid": False
    },

    {
        "name": "Scenario 6 - Missing Postal Code",
        "first_name": "arun",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "testuser06@gmail.com",
        "password": "Volleyball*1303",
        "valid": False
    },

    {
        "name": "Scenario 7 - Valid Registration",
        "first_name": "arun",
        "last_name": "deepak",
        "dob": "2003-03-13",
        "country": "IN",
        "postal_code": "630606",
        "house_number": "32-e",
        "street": "pookkara street",
        "city": "manamadurai",
        "state": "tamilnadu",
        "phone": "8870618311",
        "email": "",
        "password": "Volleyball*1303",
        "valid": True
    }
]


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for test_data in registration_scenarios:

        print(test_data["name"])

        # Navigate to registration page
        page.goto(REGISTER_URL)

        # Wait for registration form
        page.locator('[data-test="register-form"]').wait_for(state="visible",timeout=5000)
        print("Registration page opened")

        # Enter registration details
        page.locator('[data-test="first-name"]').fill(test_data["first_name"])

        page.locator('[data-test="last-name"]').fill(test_data["last_name"])

        page.locator('[data-test="dob"]').fill(test_data["dob"])

        page.locator('[data-test="country"]').select_option(test_data["country"])

        # Enter postal code
        page.locator('[data-test="postal_code"]').fill(test_data["postal_code"])

        # Enter house number
        page.locator('[data-test="house_number"]').fill(test_data["house_number"])

        # Wait for address lookup
        if test_data["postal_code"]:
            page.get_by_role("status").wait_for(state="hidden",timeout=5000)


        # Enter address details
        page.locator('[data-test="street"]').fill(test_data["street"])
        page.locator('[data-test="city"]').fill(test_data["city"])
        page.locator('[data-test="state"]').fill(test_data["state"])
        page.locator('[data-test="phone"]').fill(test_data["phone"])



        # Generate unique email for valid registration
        email = test_data["email"]
        if test_data["valid"]:
            email = f"deepak_{random.randint(100000, 999999)}@gmail.com"
            print("Generated email:", email)
        page.locator('[data-test="email"]').fill(email)
        page.locator('[data-test="password"]').fill(test_data["password"])
        print("Registration details entered")


        # Click Register
        page.locator('[data-test="register-submit"]').click()
        print("Register button clicked")



        # Verify result
        if test_data["valid"]:
            # Wait for login page
            expect(page).to_have_url(LOGIN_URL,timeout=5000)
            print("Registration successful")
            print("Redirected to login page")
            print("PASSED:", test_data["name"])
        else:
            # Registration blocked
            expect(page.locator('[data-test="register-form"]')).to_be_visible(timeout=5000)
            print("Registration was blocked")
            print("PASSED:", test_data["name"])

    browser.close()