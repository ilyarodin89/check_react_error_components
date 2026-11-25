
import main

def test_coin_page_item_desk():
    test = main.Methods("desk_cors")
    test.open_page("page_url")
    test.check_log_browser()

def test_coin_page_item_mob():
    test = main.Methods("mob_cors")
    test.open_page("page_url")
    test.check_log_browser()
