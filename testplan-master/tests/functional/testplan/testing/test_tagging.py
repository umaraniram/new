import pytest

from testplan.common.utils.testing import (
    check_report,
    log_propagation_disabled,
)

from testplan.report import TestReport, TestGroupReport, TestCaseReport
from testplan.testing.multitest import MultiTest, testsuite, testcase
from testplan.common.utils.logger import TESTPLAN_LOGGER


@testsuite(tags={"color": ["red", "blue"]})
class AlphaSuite(object):
    @testcase
    def test_method_0(self, env, result):
        pass

    @testcase(tags=("foo", "bar"))
    def test_method_1(self, env, result):
        pass

    @testcase(tags={"color": "green"})
    def test_method_2(self, env, result):
        pass


@testsuite(tags={"color": "yellow"})
class BetaSuite(object):
    @testcase
    def test_method_0(self, env, result):
        pass

    @testcase(tags="foo")
    def test_method_1(self, env, result):
        pass

    @testcase(tags={"color": "red"})
    def test_method_2(self, env, result):
        pass


@testsuite
class GammaSuite(object):
    @testcase
    def test_method_0(self, env, result):
        pass

    @testcase(
        parameters=("AAA", "BBB"),
        tag_func=lambda kwargs: {"symbol": kwargs["value"].lower()},
        tags={"speed": "slow"},
    )
    def test_param(self, env, result, value):
        pass

    @testcase(parameters=("XXX", "YYY"), tags={"speed": "fast"})
    def test_param_2(self, env, result, value):
        pass


report_for_multitest_without_tags = TestGroupReport(
    name="MyMultitest",
    category="multitest",
    entries=[
        TestGroupReport(
            name="AlphaSuite",
            category="testsuite",
            tags={"color": {"red", "blue"}},
            entries=[
                TestCaseReport(name="test_method_0"),
                TestCaseReport(
                    name="test_method_1", tags={"simple": {"foo", "bar"}}
                ),
                TestCaseReport(
                    name="test_method_2", tags={"color": {"green"}}
                ),
            ],
        ),
        TestGroupReport(
            name="BetaSuite",
            category="testsuite",
            tags={"color": {"yellow"}},
            entries=[
                TestCaseReport(name="test_method_0"),
                TestCaseReport(name="test_method_1", tags={"simple": {"foo"}}),
                TestCaseReport(name="test_method_2", tags={"color": {"red"}}),
            ],
        ),
        TestGroupReport(
            name="GammaSuite",
            category="testsuite",
            entries=[
                TestCaseReport(name="test_method_0"),
                TestGroupReport(
                    name="test_param",
                    category="parametrization",
                    tags={"speed": {"slow"}},
                    entries=[
                        TestCaseReport(
                            name="test_param <value='AAA'>",
                            tags={"symbol": {"aaa"}},
                        ),
                        TestCaseReport(
                            name="test_param <value='BBB'>",
                            tags={"symbol": {"bbb"}},
                        ),
                    ],
                ),
                TestGroupReport(
                    name="test_param_2",
                    category="parametrization",
                    tags={"speed": {"fast"}},
                    entries=[
                        TestCaseReport(name="test_param_2 <value='XXX'>"),
                        TestCaseReport(name="test_param_2 <value='YYY'>"),
                    ],
                ),
            ],
        ),
    ],
)


report_for_multitest_with_tags = TestGroupReport(
    name="MyMultitest",
    category="multitest",
    tags={"color": {"orange"}, "environment": {"server"}},
    entries=[
        TestGroupReport(
            name="AlphaSuite",
            category="testsuite",
            tags={"color": {"red", "blue"}},
            entries=[
                TestCaseReport(name="test_method_0"),
                TestCaseReport(
                    name="test_method_1", tags={"simple": {"foo", "bar"}}
                ),
                TestCaseReport(
                    name="test_method_2", tags={"color": {"green"}}
                ),
            ],
        ),
        TestGroupReport(
            name="BetaSuite",
            category="testsuite",
            tags={"color": {"yellow"}},
            entries=[
                TestCaseReport(name="test_method_0"),
                TestCaseReport(name="test_method_1", tags={"simple": {"foo"}}),
                TestCaseReport(name="test_method_2", tags={"color": {"red"}}),
            ],
        ),
        TestGroupReport(
            name="GammaSuite",
            category="testsuite",
            entries=[
                TestCaseReport(name="test_method_0"),
                TestGroupReport(
                    name="test_param",
                    category="parametrization",
                    tags={"speed": {"slow"}},
                    entries=[
                        TestCaseReport(
                            name="test_param <value='AAA'>",
                            tags={"symbol": {"aaa"}},
                        ),
                        TestCaseReport(
                            name="test_param <value='BBB'>",
                            tags={"symbol": {"bbb"}},
                        ),
                    ],
                ),
                TestGroupReport(
                    name="test_param_2",
                    category="parametrization",
                    tags={"speed": {"fast"}},
                    entries=[
                        TestCaseReport(name="test_param_2 <value='XXX'>"),
                        TestCaseReport(name="test_param_2 <value='YYY'>"),
                    ],
                ),
            ],
        ),
    ],
)


@pytest.mark.parametrize(
    "multitest_tags,expected_report",
    (
        ({}, report_for_multitest_without_tags),
        (
            {"color": "orange", "environment": "server"},
            report_for_multitest_with_tags,
        ),
    ),
)
def test_multitest_tagging(mockplan, multitest_tags, expected_report):

    multitest = MultiTest(
        name="MyMultitest",
        suites=[AlphaSuite(), BetaSuite(), GammaSuite()],
        tags=multitest_tags,
    )

    mockplan.add(multitest)

    with log_propagation_disabled(TESTPLAN_LOGGER):
        mockplan.run()

    check_report(
        expected=TestReport(name="plan", entries=[expected_report]),
        actual=mockplan.report,
    )
