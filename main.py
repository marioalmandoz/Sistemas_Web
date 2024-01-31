# -*- coding: UTF-8 -*-

from selenium import webdriver
import time


def geckodriver_test():
    uri = "https://www.ehu.eus"

    # abrir el navegador
    browser = webdriver.Firefox()

    # abrir la pagina
    browser.get(uri)

    time.sleep(5)

    # cerrar el navegador
    browser.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    geckodriver_test()

