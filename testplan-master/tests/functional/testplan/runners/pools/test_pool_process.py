"""Process worker pool functional tests."""

import os

import pytest

from testplan.common.utils.testing import log_propagation_disabled
from testplan.report import Status
from testplan.runners.pools import ProcessPool
from testplan.common.utils.logger import TESTPLAN_LOGGER
from testplan.testing import multitest

from tests.functional.testplan.runners.pools.func_pool_base_tasks import (
    schedule_tests_to_pool,
)
from tests.unit.testplan.common.serialization import test_fields


def test_pool_basic(mockplan):
    """Basic test scheduling."""
    schedule_tests_to_pool(
        mockplan, ProcessPool, worker_heartbeat=2, heartbeats_miss_limit=2
    )


def test_kill_one_worker(mockplan):
    """Kill one worker but pass after reassigning task."""
    pool_name = ProcessPool.__name__
    pool_size = 4
    pool = ProcessPool(
        name=pool_name,
        size=pool_size,
        worker_heartbeat=2,
        heartbeats_miss_limit=2,
        max_active_loop_sleep=1,
        restart_count=0,
    )
    pool_uid = mockplan.add_resource(pool)

    dirname = os.path.dirname(os.path.abspath(__file__))

    kill_uid = mockplan.schedule(
        target="multitest_kill_one_worker",
        module="func_pool_base_tasks",
        path=dirname,
        args=("killer", os.getpid(), pool_size),  # kills 4th worker
        resource=pool_name,
    )

    uids = []
    for idx in range(1, 25):
        uids.append(
            mockplan.schedule(
                target="get_mtest",
                module="func_pool_base_tasks",
                path=dirname,
                kwargs=dict(name=idx),
                resource=pool_name,
            )
        )

    with log_propagation_disabled(TESTPLAN_LOGGER):
        res = mockplan.run()

    # Check that the worker killed by test was aborted
    assert (
        len(
            [
                worker
                for worker in mockplan.resources[pool_uid]._workers
                if worker._aborted is True
            ]
        )
        == 1
    )

    assert res.run is True
    assert res.success is True
    assert mockplan.report.status == Status.PASSED

    # All tasks scheduled once except the killed one
    for idx in range(1, 25):
        if uids[idx - 1] == kill_uid:
            assert pool._task_retries_cnt[uids[idx - 1]] == 1


def test_kill_all_workers(mockplan):
    """Kill all workers and create a failed report."""
    pool_name = ProcessPool.__name__
    pool_size = 4
    retries_limit = 3
    pool = ProcessPool(
        name=pool_name,
        size=pool_size,
        worker_heartbeat=2,
        heartbeats_miss_limit=2,
        max_active_loop_sleep=1,
        restart_count=0,
    )
    pool._task_retries_limit = retries_limit
    pool_uid = mockplan.add_resource(pool)

    dirname = os.path.dirname(os.path.abspath(__file__))

    uid = mockplan.schedule(
        target="multitest_kills_worker",
        module="func_pool_base_tasks",
        path=dirname,
        resource=pool_name,
    )

    with log_propagation_disabled(TESTPLAN_LOGGER):
        res = mockplan.run()

    # Check that the worker killed by test was aborted
    assert (
        len(
            [
                worker
                for worker in mockplan.resources[pool_uid]._workers
                if worker._aborted is True
            ]
        )
        == pool_size  # == retries_limit + 1
    )

    assert res.success is False
    # scheduled X times and killed all workers
    assert pool._task_retries_cnt[uid] == retries_limit + 1
    assert mockplan.report.status == Status.ERROR


def test_reassign_times_limit(mockplan):
    """Kill workers and reassign task up to limit times."""
    pool_name = ProcessPool.__name__

    pool_size = 4
    retries_limit = int(pool_size / 2)
    pool = ProcessPool(
        name=pool_name,
        size=pool_size,
        worker_heartbeat=2,
        heartbeats_miss_limit=2,
        max_active_loop_sleep=1,
        restart_count=0,
    )
    pool._task_retries_limit = retries_limit
    pool_uid = mockplan.add_resource(pool)

    dirname = os.path.dirname(os.path.abspath(__file__))

    uid = mockplan.schedule(
        target="multitest_kills_worker",
        module="func_pool_base_tasks",
        path=dirname,
        resource=pool_name,
    )

    with log_propagation_disabled(TESTPLAN_LOGGER):
        res = mockplan.run()

    # Check that the worker killed by test was aborted
    assert (
        len(
            [
                worker
                for worker in mockplan.resources[pool_uid]._workers
                if worker._aborted is True
            ]
        )
        == retries_limit + 1
    )

    assert res.success is False
    assert pool._task_retries_cnt[uid] == retries_limit + 1
    assert mockplan.report.status == Status.ERROR
    assert mockplan.report.counter["error"] == 1


def test_custom_rerun_condition(mockplan):
    """Force reschedule task X times to test logic."""
    pool_name = ProcessPool.__name__
    uid = "custom_task_uid"
    rerun_limit = 2

    def custom_rerun(pool, task_result):
        if task_result.task.reassign_cnt > task_result.task.rerun:
            return False
        return True

    pool_size = 4
    pool = ProcessPool(
        name=pool_name,
        size=pool_size,
        worker_heartbeat=2,
        heartbeats_miss_limit=2,
        max_active_loop_sleep=1,
        restart_count=0,
    )
    pool.set_rerun_check(custom_rerun)
    pool_uid = mockplan.add_resource(pool)

    dirname = os.path.dirname(os.path.abspath(__file__))

    uid = mockplan.schedule(
        target="get_mtest",
        module="func_pool_base_tasks",
        path=dirname,
        kwargs=dict(name="0"),
        resource=pool_name,
        uid=uid,
        rerun=rerun_limit,
    )

    with log_propagation_disabled(TESTPLAN_LOGGER):
        res = mockplan.run()

    assert (
        len(
            [
                worker
                for worker in mockplan.resources[pool_uid]._workers
                if worker._aborted is True
            ]
        )
        == 0
    )

    assert res.success is True
    assert mockplan.report.status == Status.PASSED
    assert pool.added_item(uid).reassign_cnt == rerun_limit


def test_schedule_from_main(mockplan):
    """
    Test scheduling Tasks from __main__ - it should not be allowed for
    ProcessPool.
    """
    # Set up a testplan and add a ProcessPool.
    pool = ProcessPool(name="ProcPool", size=2)
    mockplan.add_resource(pool)

    # First check that scheduling a Task with module string of '__main__'
    # raises the expected ValueError.
    with pytest.raises(ValueError):
        mockplan.schedule(
            target="target", module="__main__", resource="ProcPool"
        )

    # Secondly, check that scheduling a callable target with a __module__ attr
    # of __main__ also raises a ValueError.
    def callable_target():
        raise RuntimeError

    callable_target.__module__ = "__main__"

    with pytest.raises(ValueError):
        mockplan.schedule(target=callable_target, resource="ProcPool")


@multitest.testsuite
class SerializationSuite(object):
    @multitest.testcase
    def test_serialize(self, env, result):
        """Test serialization of test results."""
        # As an edge case, store a deliberately "un-pickleable" type that
        # inherits from int on the result. This should not cause an error
        # since the value should be formatted as a string.
        x = test_fields.UnPickleableInt(42)
        result.equal(
            actual=x, expected=42, description="Compare unpickleable type"
        )


def make_serialization_mtest():
    """
    Callable target to make a MultiTest containing the SerializationSuite
    defined above.
    """
    return multitest.MultiTest(
        name="SerializationMTest", suites=[SerializationSuite()]
    )


def test_serialization(mockplan):
    """Test serialization of test results."""
    pool = ProcessPool(name="ProcPool", size=2)
    mockplan.add_resource(pool)
    mockplan.schedule(
        target="make_serialization_mtest",
        module="test_pool_process",
        path=os.path.dirname(__file__),
        resource="ProcPool",
    )
    res = mockplan.run()
    assert res.success


def test_restart_worker(mockplan):
    pool_name = ProcessPool.__name__
    pool_size = 4
    retries_limit = int(pool_size / 2)

    pool = ProcessPool(
        name=pool_name,
        size=pool_size,
        worker_heartbeat=2,
        heartbeats_miss_limit=3,
        max_active_loop_sleep=1,
    )
    pool._task_retries_limit = retries_limit
    pool_uid = mockplan.add_resource(pool)

    dirname = os.path.dirname(os.path.abspath(__file__))

    mockplan.schedule(
        target="multitest_kills_worker",
        module="func_pool_base_tasks",
        path=dirname,
        resource=pool_name,
    )

    for idx in range(1, 25):
        mockplan.schedule(
            target="get_mtest",
            module="func_pool_base_tasks",
            path=dirname,
            kwargs=dict(name=idx),
            resource=pool_name,
        )

    with log_propagation_disabled(TESTPLAN_LOGGER):
        res = mockplan.run()

    # Check that all workers are restarted
    assert (
        len(
            [
                worker
                for worker in mockplan.resources[pool_uid]._workers
                if worker._aborted is True
            ]
        )
        == 0
    )

    assert res.run is False
    assert res.success is False
    assert mockplan.report.status == Status.ERROR
    assert mockplan.report.counter[Status.ERROR] == 1
