import getpass
import os
import traceback
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait


class Downloader(object):
    def __init__(self):
        self.timeout = 100

        sels = self._selectors = namedtuple("Selectors", ["links", "video_button"])
        inputs = self._inputsIds = namedtuple("Inputs", ["name", "password", "server"])

        sels.links = "table td a.iframe:not(.vidlink)"
        sels.video_button = "a.closebox[title='Play Video']"
        inputs.name = "LogiN"
        inputs.password = "PasswD"
        inputs.server = "ServeR"
        self._optionTagName = "option"
        self._submitId = "idenT_conT"
        self._selectFromId = "_from_vid"
        self._selectToId = "_to_vid"
        self._doneButtonId = "_done_button"
        self._doneLink = "#done"

        self._prompt_script = """
            fill = function (s) {{
                for(i = {}; i < {}; i++) {{
                    s.append("<option value=\\"" + i + "\\">" + (i+1) + "</option>");
                }}
            }};
        """
        self._prompt_script += """
            var div = $("<div dir=\\"rtl\\" style=\\"color:red;font-size:24px\\">נא לבחור הרצאות. מ:</div>");
            var select1 = $("<select id=\\"{}\\"></select>");
            fill(select1);
            div.append(select1);
            div.append(" עד ");
            var select2 = $("<select id=\\"{}\\"></select>");
            fill(select2);
            div.append(select2);
            div.append("<a href=\\"{}\\"><button id=\\"{}\\">~ OK ~</button></a>");
            
            div.append("<br />");
            div.append("<hr />");
            div.append("<br />");

            div.insertBefore("center > table");
        """.format(
            self._selectFromId,
            self._selectToId,
            self._doneLink,
            self._doneButtonId)

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
