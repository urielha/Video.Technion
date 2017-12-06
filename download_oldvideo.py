import getpass
import os
import traceback
from collections import namedtuple

def ImportSelenium():
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait as Wait
    except ImportError:
        pass

ImportSelenium()

Selectors = namedtuple("Selectors", ["links", "video_button"])
InputsIds = namedtuple("InputsIds", ["name", "password", "server", "submit"])
InjectorDetails = namedtuple("InjectorDetails", ["fileName", "fromElmId", "toElmId", "doneElmId", "doneLink"])


class Downloader(object):
    _optionTagName = "option"

    _selectors = Selectors(
        links="table td a.iframe:not(.vidlink)",
        video_button="a.closebox[title='Play Video']")
    _inputsIds = InputsIds(
        name="LogiN",
        password="PasswD",
        server="ServeR",
        submit="idenT_conT")
    _injectorDetails = InjectorDetails(
        fileName="oldvideo_inject_script.js",
        fromElmId="_from_vid",
        toElmId="_to_vid",
        doneElmId="_done_button",
        doneLink="#done")

    timeout = 100

    def __init__(self):
        inject_script = open(
            self._injectorDetails.fileName).read().split("// - split code -")
        self._prompt_script = ''.join([
            inject_script[0],
            inject_script[1].format(
                self._injectorDetails.fromElmId,
                self._injectorDetails.toElmId,
                self._injectorDetails.doneLink,
                self._injectorDetails.doneElmId
            )
        ])

    def start(self):
        self.browser = webdriver.Chrome()
        return self

    def end(self):
        self.browser.close()

    def navigate(self, url):
        self.browser.get(url)
        return self

    def _find_id(self, id):
        return self.browser.find_element_by_id(id)

    def _get_input_fields(self):
        return self.browser.find_element_by_id(self._inputsIds.name), \
               self.browser.find_element_by_id(self._inputsIds.password)

    def login(self, username='', password=''):
        self.browser \
            .find_element_by_id(self._inputsIds.server) \
            .find_elements_by_tag_name(self._optionTagName)[-1].click()

        usr_input, pass_input = self._get_input_fields()
        if username: usr_input.send_keys(username)
        if password: pass_input.send_keys(password)
        if username and password:
            self._find_id(self._submitId).click()

        self._wait_for_video_page()

        return self

    def _wait_for_video_page(self):
        Wait(self.browser, self.timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "videolist"))
        )
        return self

    def load_links(self):
        links = self.browser.find_elements_by_css_selector(self._selectors.links)
        self.links = list(map(lambda l: l.get_attribute("href"), links))
        return self

    def _prompt_download(self):
        start, end = 0, len(self.links)

        self.browser.execute_script(
            self._prompt_script.format(start, end))

        Wait(self.browser, self.timeout).until(
            EC.url_contains(self._doneLink)
        )

        start = min(end, max(start,
                             int(self._find_id(self._selectFromId).get_attribute("value"))
                             ))
        end = min(end, max(start,
                           int(self._find_id(self._selectToId).get_attribute("value")) + 1
                           ))
        return start, end

    def download(self):
        start, end = self._prompt_download()
        self.browser.set_window_size(0, 0)
        for link in self.links[start:end]:
            filename = link.split("/")[-1]
            self.navigate(link)
            rtsp_link = self.browser \
                .find_element_by_css_selector(self._selectors.video_button) \
                .get_attribute("href")
            self.browser.back()
            os.system("msdl.exe -s2 {} -o {}".format(rtsp_link, filename))


def main():
    url = input("Please enter the url of the lecture: ")
    username = input("username: ")
    password = getpass.getpass()

    # TODO: save password?
    # save = input("save password (y/n) ?") == "y"

    downloader = Downloader()
    try:
        downloader.start() \
            .navigate(url) \
            .login(username, password) \
            .load_links() \
            .download()
    except TimeoutError:
        print("timeout on browser, please try again")
    except:
        traceback.print_exc()
    finally:
        try:
            downloader.end()
        except:
            pass
        input("Press Enter to quit...")


if __name__ == '__main__':
    main()
