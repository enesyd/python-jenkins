import operator
import traceback

import pytest

from mainbase.utils.settings import Settings, Environments

settings = Settings()
environment = settings.env

mark = pytest.mark


class Priority:
    """
    Prioritize test cases with pytest marks
        Example: @Priority.LOW
    Add this mark over to your test case function or class
    You can set special priorities with setting numbers instead of using predefined marks.
        Example: @Priority.SET_VALUE(number)
    The default priority for any test case is LOW
    """
    SET_VALUE = mark.priority
    SMOKE = SET_VALUE(1000)
    HIGH = SET_VALUE(500)
    MEDIUM = SET_VALUE(200)
    LOW = SET_VALUE(0)
    LAST = SET_VALUE(-1000)

    class Order:
        """
        Allows to change the order of previously prioritize test cases within themselves with second mark
        If you need your test case to be the first or the end of a priority group use order
            Example:
                @Priority.LAST
                @Priority.Order.HIGH
        """
        SET_VALUE = mark.priority
        FIRST = SET_VALUE(10)
        LAST = SET_VALUE(-10)


def modify_priority_test_cases(test_cases):
    """Modifies order of test cases which marked with priority marks"""
    grouped_test_cases = {}
    for test_case in test_cases:
        priority_values = [marker.args[0] for marker in list(test_case.iter_markers()) if marker.name == "priority"]
        if priority_values:
            priority = sum(priority_values)
        else:
            priority = None
        grouped_test_cases.setdefault(int(priority), []).append(test_case)

    sorted_test_cases = []
    unordered_test_cases = [grouped_test_cases.pop(None, [])]

    start_list = sorted((i for i in grouped_test_cases.items() if i[0] >= 0),
                        key=operator.itemgetter(0), reverse=True)
    end_list = sorted((i for i in grouped_test_cases.items() if i[0] < 0),
                      key=operator.itemgetter(0), reverse=True)

    sorted_test_cases.extend([i[1] for i in start_list])
    sorted_test_cases.extend(unordered_test_cases)
    sorted_test_cases.extend([i[1] for i in end_list])

    return [test_case for sublist in sorted_test_cases for test_case in sublist]


class RunOnly:
    PRODUCTION = mark.production
    TEST_MACHINE = mark.test_machine


def filter_run_only_cases(test_cases):
    if environment == Environments.TEST_MACHINE:

        try:
            jira_env_list = JiraIssueInformation().get_environment(settings.env_variables["DEVELOPMENT_BRANCH"])

            if "Journey Builder" not in jira_env_list:
                test_cases = list(filter(lambda i: "tests/Architect/API/" not in i.nodeid, test_cases))

            if "Email API" not in jira_env_list and "Journey Builder" not in jira_env_list:
                test_cases = list(filter(lambda i: "tests/Newsletter/EmailApi/" not in i.nodeid, test_cases))

            if "Alfred" not in jira_env_list and "Journey Builder" not in jira_env_list:
                test_cases = list(filter(lambda i: "tests/WebPush/API/" not in i.nodeid, test_cases))
        except:
            traceback.print_exc()

        test_cases = list(filter(
            lambda i: "production" not in [marker.name for marker in list(i.iter_markers())], test_cases))
    elif environment in (Environments.JENKINS_DEPLOYMENT, Environments.JENKINS_TEST, Environments.LOCAL):
        test_cases = list(filter(
            lambda i: "test_machine" not in [marker.name for marker in list(i.iter_markers())], test_cases))
    return test_cases


class Owner:
    SET_VALUE = mark.owner
    enes_yenidogan = SET_VALUE("enes.yenidogan@useinsider.com")
