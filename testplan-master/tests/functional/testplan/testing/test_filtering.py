import pytest

from testplan.testing.multitest import MultiTest, testsuite, testcase

from testplan import TestplanMock
from testplan.common.utils.testing import (
    log_propagation_disabled,
    argv_overridden,
    check_report_context,
)
from testplan.common.utils.logger import TESTPLAN_LOGGER
from testplan.testing import filtering


@testsuite(tags="foo")
class Alpha(object):
    @testcase
    def test_one(self, env, result):
        pass

    @testcase(tags={"color": "blue"})
    def test_two(self, env, result):
        pass

    @testcase(tags={"color": "red"})
    def test_three(self, env, result):
        pass


@testsuite(tags=("foo", "bar"))
class Beta(object):
    @testcase
    def test_one(self, env, result):
        pass

    @testcase(tags={"color": "red"})
    def test_two(self, env, result):
        pass

    @testcase(tags={"color": "green"})
    def test_three(self, env, result):
        pass


@testsuite(tags=("foo", "baz"))
class Gamma(object):
    @testcase
    def test_one(self, env, result):
        pass

    @testcase(tags={"color": ("blue", "yellow")})
    def test_two(self, env, result):
        pass

    @testcase(tags={"color": ("red", "green")})
    def test_three(self, env, result):
        pass


@pytest.mark.parametrize(
    "filter_obj, report_ctx",
    (
        # Case 1
        (
            filtering.Filter(),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_one", "test_two", "test_three"]),
                        ("Beta", ["test_one", "test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_one", "test_two", "test_three"]),)),
            ],
        ),
        # Case 2
        (
            filtering.Pattern("*:*:test_two"),
            [
                ("XXX", [("Alpha", ["test_two"]), ("Beta", ["test_two"])]),
                ("YYY", [("Gamma", ["test_two"])]),
            ],
        ),
        # Case 3
        (
            filtering.Pattern("XXX:Beta:test_two"),
            [("XXX", [("Beta", ["test_two"])])],
        ),
        # Case 4 - testcase name match AND tag match
        (
            filtering.And(
                filtering.Pattern("*:*:test_two"),
                filtering.Tags({"color": "blue"}),
            ),
            [
                ("XXX", [("Alpha", ["test_two"])]),
                ("YYY", [("Gamma", ["test_two"])]),
            ],
        ),
        # Case 5 - testcase name match AND tag match, different syntax
        (
            (
                filtering.Pattern("*:*:test_two")
                and filtering.Tags({"color": "blue"})
            ),
            [
                ("XXX", [("Alpha", ["test_two"])]),
                ("YYY", [("Gamma", ["test_two"])]),
            ],
        ),
        #  Case 6 - Run tests that are:
        # named `test_one` AND tagged with `baz`
        # OR
        # belong to a suite named Alpha OR Beta AND tagged with `color`: `red`
        (
            filtering.Or(
                filtering.And(
                    filtering.Pattern("*:*:test_one"), filtering.Tags("baz")
                ),
                filtering.And(
                    filtering.Pattern.any("*:Alpha:*", "*:Beta:*"),
                    filtering.Tags({"color": "red"}),
                ),
            ),
            [
                ("XXX", [("Alpha", ["test_three"]), ("Beta", ["test_two"])]),
                ("YYY", [("Gamma", ["test_one"])]),
            ],
        ),
        #  Case 7, same as case 6, different syntax
        (
            (
                (filtering.Pattern("*:*:test_one") & filtering.Tags("baz"))
                | (
                    filtering.Pattern.any("*:Alpha:*", "*:Beta:*")
                    & filtering.Tags({"color": "red"})
                )
            ),
            [
                ("XXX", [("Alpha", ["test_three"]), ("Beta", ["test_two"])]),
                ("YYY", [("Gamma", ["test_one"])]),
            ],
        ),
        # Case 8, inverse filter via Not
        (
            filtering.Not(filtering.Pattern("*:*:test_one")),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_two", "test_three"]),
                        ("Beta", ["test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_two", "test_three"]),)),
            ],
        ),
        # Case 9, Same as case 8, different syntax
        (
            ~filtering.Pattern("*:*:test_one"),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_two", "test_three"]),
                        ("Beta", ["test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_two", "test_three"]),)),
            ],
        ),
    ),
)
def test_programmatic_filtering(filter_obj, report_ctx):
    multitest_x = MultiTest(name="XXX", suites=[Alpha(), Beta()])
    multitest_y = MultiTest(name="YYY", suites=[Gamma()])

    plan = TestplanMock(name="plan", test_filter=filter_obj)
    plan.add(multitest_x)
    plan.add(multitest_y)

    with log_propagation_disabled(TESTPLAN_LOGGER):
        plan.run()

    test_report = plan.report
    check_report_context(test_report, report_ctx)


@pytest.mark.parametrize(
    "cmdline_args, report_ctx",
    (
        # Case 1, no filtering args, full report ctx expected
        (
            tuple(),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_one", "test_two", "test_three"]),
                        ("Beta", ["test_one", "test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_one", "test_two", "test_three"]),)),
            ],
        ),
        # Case 2, pattern filtering
        (
            ("--patterns", "XXX:*:test_two"),
            [("XXX", [("Alpha", ["test_two"]), ("Beta", ["test_two"])])],
        ),
        # Case 2, pattern filtering (multiple params)
        (
            ("--patterns", "XXX:*:test_two", "--patterns", "YYY:*:test_three"),
            [
                ("XXX", [("Alpha", ["test_two"]), ("Beta", ["test_two"])]),
                ("YYY", (("Gamma", ["test_three"]),)),
            ],
        ),
        # Case 3, tag filtering
        (
            ("--tags", "bar color=red"),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_three"]),
                        ("Beta", ["test_one", "test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_three"]),)),
            ],
        ),
        # Case 4, tag filtering (multiple params)
        (
            # Run tests that match ANY of these rules
            # as they belong to the same category (tags)
            (
                "--tags",
                "bar color=blue",  # bar OR color=blue
                "--tags-all",
                "baz color=red",  # baz AND color=red
            ),
            [
                (
                    "XXX",
                    [
                        ("Alpha", ["test_two"]),
                        ("Beta", ["test_one", "test_two", "test_three"]),
                    ],
                ),
                ("YYY", (("Gamma", ["test_two", "test_three"]),)),
            ],
        ),
        # Case 5, pattern & tag composite filtering
        # Tag filters will be wrapped by Any
        # Pattern and tag filters will be wrapped by All
        (
            (
                "--pattern",
                "*:*:test_one",
                "*:*:test_three",
                "--tags",
                "bar color=blue",  # bar OR color=blue
                "--tags-all",
                "baz color=red",  # baz AND color=red
            ),
            [
                ("XXX", [("Beta", ["test_one", "test_three"])]),
                ("YYY", (("Gamma", ["test_three"]),)),
            ],
        ),
    ),
)
def test_command_line_filtering(cmdline_args, report_ctx):

    multitest_x = MultiTest(name="XXX", suites=[Alpha(), Beta()])
    multitest_y = MultiTest(name="YYY", suites=[Gamma()])

    with argv_overridden(*cmdline_args):
        plan = TestplanMock(name="plan", parse_cmdline=True)
        plan.add(multitest_x)
        plan.add(multitest_y)

        with log_propagation_disabled(TESTPLAN_LOGGER):
            plan.run()

    test_report = plan.report
    check_report_context(test_report, report_ctx)
