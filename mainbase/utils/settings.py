import configparser
import os
import socket
import sys
import requests


class Environments(enumerate):
    JENKINS_TEST = "JENKINS_TEST"
    JENKINS_DEPLOYMENT = "JENKINS_DEPLOYMENT"
    TEST_MACHINE = "TEST"
    TEST_MACHINE_FROM_LOCAL = "TEST_MACHINE_FROM_LOCAL"
    LOCAL = "LOCAL"


class Settings:
    project_name = "releasepy"
    test_env_variable_name = "TEST_ENV"

    def __init__(self):
        self._settings = None
        self.env = self.get_env()
        self.project_dir = self.get_project_dir()

    @property
    def env_variables(self):
        return os.environ

    def reset_env_variables(self, defaults):
        for key in dict(self.env_variables).keys():
            self.env_variables.pop(key)

        for key, val in defaults.items():
            self.env_variables[key] = val

    def get_project_dir(self):
        if "JOB_NAME" in os.environ:
            self.project_name = os.environ["JOB_NAME"]
        else:
            self.project_name = "releasepy"
        curent_path_splitted = os.path.realpath(__file__).split(os.sep)
        last_project_name_index = len(curent_path_splitted) - 1 - curent_path_splitted[::-1].index(self.project_name)
        return os.path.join(os.sep.join(curent_path_splitted[:last_project_name_index + 1]))

    def is_hosts_changed_to_test_machine(self):
        """Checks whether the local host has been replaced by the test machine ip"""
        return False
        try:
            response = requests.get("http://inone.useinsider.com")
            return response.headers["Server"] == 'nginx'
        except Exception:
            return False

    def get_env(self):
        if self.test_env_variable_name not in self.env_variables:
            if self.is_hosts_changed_to_test_machine():
                return Environments.TEST_MACHINE_FROM_LOCAL
            return Environments.LOCAL
        else:
            return self.env_variables[self.test_env_variable_name]

    def read_settings(self):
        """
        Read settings.ini
        """
        if self.env in (Environments.JENKINS_TEST, Environments.JENKINS_DEPLOYMENT, Environments.TEST_MACHINE):
            ini_file_location = "/etc/atlas_settings.ini"
        else:
            ini_file_location = os.path.join(self.project_dir, "base", "utils", "settings.ini")

        if not os.path.isfile(ini_file_location):
            raise Exception("Please make settings.ini copy from settings.example.ini to {}".format(ini_file_location))

        config = configparser.ConfigParser()
        config.read(ini_file_location, encoding='utf-8')

        settings = {}
        for option in config.options("ALL"):
            settings[option] = config.get("ALL", option)
        if self.env in (Environments.JENKINS_DEPLOYMENT, Environments.JENKINS_TEST):
            ini_env = "JENKINS"
        elif self.env == Environments.TEST_MACHINE_FROM_LOCAL:
            ini_env = "TEST"
        else:
            ini_env = self.env
        for option in config.options(ini_env):
            settings[option] = config.get(ini_env, option)

        if self.env == Environments.TEST_MACHINE_FROM_LOCAL:
            test_machine_ip = socket.gethostbyname(settings[SettingKeys.PARTNER_NAME] + ".inone.useinsider.com")
            self.env_variables["TEST_MACHINE_IP"] = test_machine_ip
            settings[SettingKeys.DB_HOST] = test_machine_ip
        elif self.env in (Environments.JENKINS_TEST, Environments.JENKINS_DEPLOYMENT) \
                and "HUB_IP" in self.env_variables:
            settings[SettingKeys.HUB_IP] = self.env_variables["HUB_IP"]

        for setting, value in settings.items():
            if value == "None":
                settings[setting] = None
        return settings

    def get(self, settings_key, is_required=True):
        """
        Get value from settings.ini
        :param str settings_key: a settings.ini config key
        :param is_required: if not required config, it doesnt raise error, returns None
        """
        if self._settings is None:
            self._settings = self.read_settings()

        settings_keys = [getattr(SettingKeys, attr) for attr in dir(SettingKeys)
                         if not callable(getattr(SettingKeys, attr)) and not attr.startswith("__")]
        for setting in {*list(self._settings), *list(settings_keys)}:
            for env_key, env_value in self.env_variables.items():
                if setting.upper() == env_key.upper():
                    self._settings[setting] = env_value

        if settings_key in self._settings:
            if type(self._settings[settings_key]) == str:
                return self._settings[settings_key].replace(
                    "{partner_name}", self._settings[SettingKeys.PARTNER_NAME])
            else:
                return self._settings[settings_key]

        else:
            if not is_required:
                return None
            raise Exception("{} not found in settings.ini".format(settings_key))


def is_xdist_slave():
    """
    Checks pytest parallel test run plugins slave session.
    """
    return "-c" in sys.argv


def get_rerun_limit(pytest_config):
    return pytest_config.cache.get("rerun_limit", 0)


def get_jenkins_console_url():
    settings = Settings()
    return "{}job/{}/{}/execution/node/72/log/?consoleFull".format(
        settings.env_variables["JENKINS_URL"],
        settings.env_variables["JOB_NAME"], settings.env_variables["BUILD_ID"]
    )


def get_grafana_url_test(session_id):
    return "http://52.50.9.174:3000/d/H_pba00Wz/atlas-on-test-machine?orgId=1&var-session_id={}&" \
           "var-base_atlas_branch=master&var-base_dev_branch=SEL-2416&var-compare_with_last_n_runs=3&" \
           "var-compare_offset=0".format(session_id)


class SettingKeys(enumerate):
    PARTNER_ID = "partner_id"
    PANEL_USER = "panel_user"
    PANEL_PASSWORD = "panel_password"
    PARTNER_NAME = "partner_name"
    PARTNER_PANEL_URL = "partner_panel_url"
    PARTNER_SITE_URL = "partner_site_url"
    GACHAPON_PARTNER = "gachapon_partner"
    GACHAPON_URL = "gachapon_url"
    COLLABORATE_MAIL = "collaborate_mail"
    COLLABORATE_PASSWORD = "collaborate_password"
    VIEW_ONLY_MAIL = "view_only_mail"
    VIEW_ONLY_PASSWORD = "view_only_password"
    OUTSOURCE_MAIL = "outsource_mail"
    OUTSOURCE_PASSWORD = "outsource_password"
    NOROLE_MAIL = "norole_mail"
    NOROLE_PASSWORD = "norole_password"
    NOROLE_DEACTIVE_MAIL = "norole_deactive_mail"
    NOROLE_DEACTIVE_PASSWORD = "norole_deactive_password"
    HASROLE_DEACTIVE_MAIL = "hasrole_deactive_mail"
    HASROLE_DEACTIVE_PASSWORD = "hasrole_deactive_password"
    SELENIUM_MAIL = "selenium_mail"
    SELENIUM_PASSWORD = "selenium_password"
    LOCK_MAIL = "lock_mail"
    LOCK_PASSWORD = "lock_password"
    THRESHOLD_MAIL = "threshold_mail"
    THRESHOLD_PASSWORD = "threshold_password"
    CONTACT_API_KEY = "contact_api_key"
    GOOGLE_MAP_APIS_KEY = "google_map_apis_key"
    MAIL_API_KEY = "mail_api_key"
    TEST_MAIL = "test_mail"
    TEST_PASSWORD = "test_password"
    TEST_IMAP_SERVER = "test_imap_server"
    QA_GMAIL = "qa_gmail"
    QA_GMAIL_PASSWORD = "qa_gmail_password"
    QA_GMAIL_IMAP_SERVER = "qa_gmail_imap_server"
    RESET_MAIL = "reset_mail"
    RESET_MAIL_PASSWORD = "reset_mail_password"
    FB_EMAIL = "fb_email"
    FB_PASSWORD = "fb_password"
    INSIDER_URL = "insider_url"
    CONFLUENCE_URL = "confluence_url"
    JIRA_URL = "jira_url"
    JIRA_TOKEN = "jira_token"
    MAIL_URL = "mail_url"
    DB_HOST = "db_host"
    DB_USER = "db_user"
    DB_PASSWORD = "db_password"
    TOKEN_DB_HOST = "token_db_host"
    TOKEN_DB_USER = "token_db_user"
    TOKEN_DB_PASSWORD = "token_db_password"
    TOKEN_DB_PORT = "token_db_port"
    QA_DB_HOST = "qa_db_host"
    QA_DB_USER = "qa_db_user"
    QA_DB_PASSWORD = "qa_db_password"
    QA_DB_PORT = "qa_db_port"
    QA_DB_SCHEMA = "qa_db_schema"
    REMOTE_DRIVER = "remote_driver"
    HUB_IP = "hub_ip"
    HEADLESS_MODE = "headless_mode"
    WINDOW_RESOLUTION = "window_resolution"
    GITHUB_TOKEN = "github_token"
    SLACK_WEBHOOK_URL = "slack_webhook_url"
    SLACK_TOKEN = "slack_token"
    CONTACT_API_URL = "contact_api_url"
    LISTENER_API_URL = "listener_api_url"
    PANDORA_ENABLED = "pandora_enabled"
    LOG_DB_HOST = "log_db_host"
    LOG_DB_USER = "log_db_user"
    LOG_DB_PASSWORD = "log_db_password"
    LOG_DB_PORT = "log_db_port"
    UCD_ENDPOINT = "ucd_endpoint"
    MAIL_SERVICE_ENDPOINT = "mail_service_endpoint"
    MAIL_EVENT_KEY = "mail_event_key"
    TRANSACTIONAL_EMAIL_ENDPOINT = "transactional_email_endpoint"
    TRANSACTIONAL_EMAIL_AUTH_KEY = "transactional_email_auth_key"
    CHROMEDRIVER_PATH = "chromedriver_path"
    CONTACT_API_URL_QUERY = "contact_api_url_query"
    TARGETED_PUSH_URL = "targeted_push_url"
    TARGETED_PUSH_KEY = "targeted_push_key"
