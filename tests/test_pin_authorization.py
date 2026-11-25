
import main

def test_pin_authorization_desk():
    test = main.Methods("desk")
    test.open_page("page_url")
    test.check_log_browser()

def test_pin_authorization_mob():
    test = main.Methods("mob")
    test.open_page("page_url")
    test.check_log_browser()