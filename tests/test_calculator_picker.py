
import main

def test_calculator_picker_desk():
    test = main.Methods("desk_cors")
    test.open_page("page_url")
    test.wait_element_for_calc_picker()
    test.check_log_browser()

def test_calculator_picker_mob():
    test = main.Methods("mob_cors")
    test.open_page("page_url")
    test.wait_element_for_calc_picker()
    test.check_log_browser()
