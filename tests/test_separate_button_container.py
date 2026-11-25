
import main

def test_separate_button_container_desk():
    test = main.Methods("desk")
    test.open_page("page_url")
    test.check_log_browser()

def test_separate_button_container_mob():
    test = main.Methods("mob")
    test.open_page("page_url")
    test.check_log_browser()
