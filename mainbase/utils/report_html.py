import datetime
import html
import inspect
import json
import os
import pprint
import time
import traceback
from functools import wraps
from pathlib import Path

import jsonpickle
import slack
from pygments import highlight, lexers
from pygments.formatters.html import HtmlFormatter

from mainbase.utils.settings import Environments, get_rerun_limit


def decorator_loader(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def error_logger(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            try:
                tb_text = "".join(traceback.format_exc())
                lexer = lexers.get_lexer_by_name("pytb", stripall=True)
                formatter = HtmlFormatter()
                html_tb_message = highlight(tb_text, lexer, formatter)

                error_log = {
                    'case_name': inspect.getfile(self.__class__).split(os.sep + "test" + os.sep)[-1],
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'error_message': html_tb_message,
                    'img_name': "default_image.png",
                    'html_name': "",
                    'console_log': "Browser log can not be captured.",
                    'context': html.escape(pprint.pformat(get_context(self), indent=4)),
                    'owners': ", ".join([mark.args[0] for mark in self.pytestmark if mark.name == "owner"]),
                    "current_url": ""
                }
                timestamp = str(int(time.time()))
                file_name = timestamp + error_log['case_name'].replace('/', '-').replace('\\', '-').replace('-test-',
                                                                                                            '')
                error_log['html_name'] = file_name + ".html"
                error_log['img_name'] = file_name + ".png"
                # print('*' * 50, '\n', file_name, error_log['html_name'], error_log['img_name'])
                if self.settings.env in (Environments.JENKINS_TEST, Environments.JENKINS_DEPLOYMENT):
                    path = os.path.join(
                        self.settings.env_variables["JENKINS_HOME"],
                        "workspace", "AtlasPipelineWorkspace", self.settings.env_variables["JOB_NAME"],
                        self.settings.env_variables["BUILD_ID"])
                    img_path = os.path.join(path, error_log["img_name"])
                    Path(path).mkdir(parents=True, exist_ok=True)
                else:
                    img_path = os.path.join(self.settings.project_dir, "base", "utils", "error_records",
                                            error_log["img_name"])
                    # print('*' * 50, img_path)
                if self.driver is not None:
                    try:
                        error_log["current_url"] = self.driver.current_url
                        error_log['console_log'] = parse_browser_console_log(self)
                        self.driver.save_screenshot(img_path)
                        # print('*' * 50, img_path)
                    except:
                        error_log['img_name'] = "default_image.png"
                    self.driver.quit()
                    self.driver = None
                create_error_html(self, error_log)
            finally:
                raise e

    return wrap


def get_context(self):
    context = inspect.trace()[-1][0].f_locals
    if "self" in list(context):
        del context["self"]
    context = json.loads(jsonpickle.encode(context, max_depth=4))
    self_variables = {}
    for attr in dir(self):
        attr_value = getattr(self, attr)
        if not inspect.ismethod(attr_value) and not attr.startswith("_") and type(attr_value) in (
                bool, int, float, str, list, dict, tuple, set, type(None)):
            self_variables[attr] = getattr(self, attr)
    context_self = json.loads(jsonpickle.encode(self_variables, max_depth=4))
    context["self"] = context_self
    filter_keys(context, ["settings", "chrome_options", "driver", "py/object", "wait", "base_image"])
    return context


def parse_browser_console_log(self):
    browser_log = self.driver.get_log("browser")
    log_output = ""
    for log in browser_log:
        log_output += log['level'] + " - " + log['message'] + " | Source: " + log['source'] + "<br>"
    return log_output


def create_error_html(self, error_log):
    with open(os.path.join(
            self.settings.project_dir, "base", "utils", "error_records", "error_template.html"), "r") as file:
        data = file.read()
    data = data.replace("{case_name}", error_log['case_name'])
    data = data.replace("{timestamp}", error_log['timestamp'])
    data = data.replace("{error_message}", error_log['error_message'])
    data = data.replace("{img_src}", error_log['img_name'])
    data = data.replace("{case_title}", error_log['case_name'])
    data = data.replace("{console_log}", error_log['console_log'])
    data = data.replace("{context}", error_log['context'])
    data = data.replace("{owners}", error_log['owners'])
    data = data.replace("{current_url}", error_log['current_url'])

    if self.settings.env in (Environments.JENKINS_TEST, Environments.JENKINS_DEPLOYMENT):
        path = os.path.join(self.settings.env_variables["JENKINS_HOME"],
                            "workspace", "AtlasPipelineWorkspace", self.settings.env_variables["JOB_NAME"],
                            self.settings.env_variables["BUILD_ID"])
        html_location = os.path.join(path, error_log['html_name'])
        Path(path).mkdir(parents=True, exist_ok=True)
    else:
        html_location = os.path.join(self.settings.get_project_dir(),
                                     "base", "utils", "error_records", error_log['html_name'])
    with open(html_location, "w") as file:
        file.write(data)
        # if self.settings.env in (Environments.JENKINS_TEST, Environments.JENKINS_DEPLOYMENT, Environments.TEST_MACHINE):
        if "JOB_NAME" in os.environ:
            print_html_dir = (self.settings.env_variables["JENKINS_URL"] +
                              "job/AtlasPipelineWorkspace/ws/{}/{}/" +
                              error_log['html_name']).format(self.settings.env_variables["JOB_NAME"],
                                                             self.settings.env_variables["BUILD_ID"])
        else:
            print_html_dir = "file://" + html_location
        print(print_html_dir)


def filter_keys(obj, bad):
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if k in bad:
                del obj[k]
            else:
                filter_keys(obj[k], bad)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] in bad:
                del obj[i]
            else:
                filter_keys(obj[i], bad)
