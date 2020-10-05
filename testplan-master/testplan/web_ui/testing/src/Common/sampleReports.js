/**
 * Sample Testplan reports to be used in development & testing.
 */
const TESTPLAN_REPORT = {
  "category": "testplan",
  "name": "Sample Testplan",
  "status": "failed",
  "uid": "520a92e4-325e-4077-93e6-55d7091a3f83",
  "tags_index": {},
  "status_override": null,
  "meta": {},
  "timer": {
    "run": {
      "start": "2018-10-15T14:30:10.998071+00:00",
      "end": "2018-10-15T14:30:11.296158+00:00"
    }
  },
  "entries": [
    {
      "name": "Primary",
      "status": "failed",
      "category": "multitest",
      "description": null,
      "status_override": null,
      "uid": "21739167-b30f-4c13-a315-ef6ae52fd1f7",
      "type": "TestGroupReport",
      "logs": [],
      "tags": {
        "simple": ["server"]
      },
      "timer": {
        "run": {
          "start": "2018-10-15T14:30:11.009705+00:00",
          "end": "2018-10-15T14:30:11.159661+00:00"
        }
      },
      "entries": [
        {
          "status": "failed",
          "category": "testsuite",
          "name": "AlphaSuite",
          "status_override": null,
          "description": null,
          "uid": "cb144b10-bdb0-44d3-9170-d8016dd19ee7",
          "type": "TestGroupReport",
          "logs": [],
          "tags": {
            "simple": ["server"]
          },
          "timer": {
            "run": {
              "start": "2018-10-15T14:30:11.009872+00:00",
              "end": "2018-10-15T14:30:11.158224+00:00"
            }
          },
          "entries": [
            {
              "category": 'testcase',
              "name": "test_equality_passing",
              "status": "passed",
              "status_override": null,
              "description": null,
              "uid": "736706ef-ba65-475d-96c5-f2855f431028",
              "type": "TestCaseReport",
              "logs": [],
              "tags": {
                "colour": ["white"]
              },
              "timer": {
                "run": {
                  "start": "2018-10-15T14:30:11.010072+00:00",
                  "end": "2018-10-15T14:30:11.132214+00:00"
                }
              },
              "entries": [
                {
                  "category": "DEFAULT",
                  "machine_time": "2018-10-15T15:30:11.010098+00:00",
                  "description": "passing equality",
                  "line_no": 24,
                  "label": "==",
                  "second": 1,
                  "meta_type": "assertion",
                  "passed": true,
                  "type": "Equal",
                  "utc_time": "2018-10-15T14:30:11.010094+00:00",
                  "first": 1
                }
              ],
            },
            {
              "category": 'testcase',
              "name": "test_equality_passing2",
              "status": "failed",
              "tags": {},
              "status_override": null,
              "description": null,
              "uid": "78686a4d-7b94-4ae6-ab50-d9960a7fb714",
              "type": "TestCaseReport",
              "logs": [],
              "timer": {
                "run": {
                  "start": "2018-10-15T14:30:11.510072+00:00",
                  "end": "2018-10-15T14:30:11.632214+00:00"
                }
              },
              "entries": [
                {
                  "category": "DEFAULT",
                  "machine_time": "2018-10-15T15:30:11.510098+00:00",
                  "description": "passing equality",
                  "line_no": 24,
                  "label": "==",
                  "second": 1,
                  "meta_type": "assertion",
                  "passed": true,
                  "type": "Equal",
                  "utc_time": "2018-10-15T14:30:11.510094+00:00",
                  "first": 1
                }
              ],
            },
          ],
        },
        {
          "status": "passed",
          "category": "testsuite",
          "name": "BetaSuite",
          "status_override": null,
          "description": null,
          "uid": "6fc5c008-4d1a-454e-80b6-74bdc9bca49e",
          "type": "TestGroupReport",
          "logs": [],
          "tags": {
            "simple": ["client"]
          },
          "timer": {
            "run": {
              "start": "2018-10-15T14:30:11.009872+00:00",
              "end": "2018-10-15T14:30:11.158224+00:00"
            }
          },
          "entries": [
            {
              "category": 'testcase',
              "name": "test_equality_passing",
              "status": "passed",
              "tags": {},
              "status_override": null,
              "description": null,
              "uid": "8865a23d-1823-4c8d-ab37-58d24fc8ac05",
              "type": "TestCaseReport",
              "logs": [],
              "timer": {
                "run": {
                  "start": "2018-10-15T14:30:11.010072+00:00",
                  "end": "2018-10-15T14:30:11.132214+00:00"
                }
              },
              "entries": [
                {
                  "category": "DEFAULT",
                  "machine_time": "2018-10-15T15:30:11.010098+00:00",
                  "description": "passing equality",
                  "line_no": 24,
                  "label": "==",
                  "second": 1,
                  "meta_type": "assertion",
                  "passed": true,
                  "type": "Equal",
                  "utc_time": "2018-10-15T14:30:11.010094+00:00",
                  "first": 1
                }
              ],
            },
          ],
        },
      ],
    },
    {
      "name": "Secondary",
      "status": "passed",
      "category": "multitest",
      "tags": {},
      "description": null,
      "status_override": null,
      "uid": "8c3c7e6b-48e8-40cd-86db-8c8aed2592c8",
      "type": "TestGroupReport",
      "logs": [],
      "timer": {
        "run": {
          "start": "2018-10-15T14:30:12.009705+00:00",
          "end": "2018-10-15T14:30:12.159661+00:00"
        }
      },
      "entries": [
        {
          "status": "passed",
          "category": "testsuite",
          "name": "GammaSuite",
          "tags": {},
          "status_override": null,
          "description": null,
          "uid": "08d4c671-d55d-49d4-96ba-dc654d12be26",
          "type": "TestGroupReport",
          "logs": [],
          "timer": {
            "run": {
              "start": "2018-10-15T14:30:12.009872+00:00",
              "end": "2018-10-15T14:30:12.158224+00:00"
            }
          },
          "entries": [
            {
              "category": 'testcase',
              "name": "test_equality_passing",
              "status": "passed",
              "tags": {},
              "status_override": null,
              "description": null,
              "uid": "f73bd6ea-d378-437b-a5db-00d9e427f36a",
              "type": "TestCaseReport",
              "logs": [],
              "timer": {
                "run": {
                  "start": "2018-10-15T14:30:12.010072+00:00",
                  "end": "2018-10-15T14:30:12.132214+00:00"
                }
              },
              "entries": [
                {
                  "category": "DEFAULT",
                  "machine_time": "2018-10-15T15:30:12.010098+00:00",
                  "description": "passing equality",
                  "line_no": 24,
                  "label": "==",
                  "second": 1,
                  "meta_type": "assertion",
                  "passed": true,
                  "type": "Equal",
                  "utc_time": "2018-10-15T14:30:12.010094+00:00",
                  "first": 1
                }
              ],
            },
          ],
        }
      ],
    },
  ],
};

// Simple report that only contains one MultiTest and one suite.
const SIMPLE_REPORT = {
  "category": "testplan",
  "name": "Sample Testplan",
  "status": "failed",
  "uid": "520a92e4-325e-4077-93e6-55d7091a3f83",
  "tags_index": {},
  "status_override": null,
  "meta": {},
  "timer": {
    "run": {
      "start": "2018-10-15T14:30:10.998071+00:00",
      "end": "2018-10-15T14:30:11.296158+00:00"
    }
  },
  "entries": [{
    "name": "Primary",
    "status": "failed",
    "category": "multitest",
    "description": null,
    "status_override": null,
    "uid": "21739167-b30f-4c13-a315-ef6ae52fd1f7",
    "type": "TestGroupReport",
    "logs": [],
    "tags": {
      "simple": ["server"]
    },
    "timer": {
      "run": {
        "start": "2018-10-15T14:30:11.009705+00:00",
        "end": "2018-10-15T14:30:11.159661+00:00"
      }
    },
    "entries": [{
      "status": "failed",
      "category": "testsuite",
      "name": "AlphaSuite",
      "status_override": null,
      "description": null,
      "uid": "cb144b10-bdb0-44d3-9170-d8016dd19ee7",
      "type": "TestGroupReport",
      "logs": [],
      "tags": {
        "simple": ["server"]
      },
      "timer": {
        "run": {
          "start": "2018-10-15T14:30:11.009872+00:00",
          "end": "2018-10-15T14:30:11.158224+00:00"
        }
      },
      "entries": [{
        "category": 'testcase',
        "name": "test_equality_passing",
        "status": "passed",
        "status_override": null,
        "description": null,
        "uid": "736706ef-ba65-475d-96c5-f2855f431028",
        "type": "TestCaseReport",
        "logs": [],
        "tags": {
          "colour": ["white"]
        },
        "timer": {
          "run": {
            "start": "2018-10-15T14:30:11.010072+00:00",
            "end": "2018-10-15T14:30:11.132214+00:00"
          }
        },
        "entries": [{
          "category": "DEFAULT",
          "machine_time": "2018-10-15T15:30:11.010098+00:00",
          "description": "passing equality",
          "line_no": 24,
          "label": "==",
          "second": 1,
          "meta_type": "assertion",
          "passed": true,
          "type": "Equal",
          "utc_time": "2018-10-15T14:30:11.010094+00:00",
          "first": 1
        }],
      }],
    }],
  }],
};

// Simple report that only contains one MultiTest and one suite.
const ERROR_REPORT = {
  "category": "testplan",
  "name": "Testplan with errors",
  "status": "error",
  "uid": "520a92e4-325e-4077-93e6-55d7091a3f83",
  "tags_index": {},
  "status_override": null,
  "meta": {},
  "timer": {
    "run": {
      "start": "2018-10-15T14:30:10.998071+00:00",
      "end": "2018-10-15T14:30:11.296158+00:00"
    }
  },
  "entries": [],
  "logs": [
    {
      "message": "While starting resource [client]\nTraceback (most recent call last):\n  File \"/d/d1/shared/yitaor/ets.testplan.2/ets/testplan/ets.testplan/src/oss/testplan/common/entity/base.py\", line 143, in start\n    resource.start()\n  File \"/d/d1/shared/yitaor/ets.testplan.2/ets/testplan/ets.testplan/src/oss/testplan/testing/multitest/driver/base.py\", line 148, in start\n    self.starting()\n  File \"/d/d1/shared/yitaor/ets.testplan.2/ets/testplan/ets.testplan/src/oss/testplan/testing/multitest/driver/tcp/client.py\", line 161, in starting\n    1/0\nZeroDivisionError: integer division or modulo by zero\n",
      "created": "2018-10-15T14:30:12.971680+00:00",
      "levelno": 40,
      "levelname": "ERROR",
      "funcName": "post_step_call",
      "lineno": 387,
      "uid": "dbc47190-505b-4153-ab3e-fec460eac78d"
    }
  ]
};

/**
 * Fake interactive report. All entries start with a status of "ready".
 */
const FakeInteractiveReport = {
  counter: {passed: 0, failed: 0},
  entries: [{
    counter: {passed: 0, failed: 0},
    category: "multitest",
    description: null,
    entries: [{
      counter: {passed: 0, failed: 0},
      category: "testsuite",
      description: null,
      entries: [{
        counter: {passed: 0, failed: 0},
        description: null,
        entries: [],
        logs: [],
        name: "test_interactive",
        name_type_index: [],
        status: 'unknown',
        runtime_status: 'ready',
        status_override: null,
        suite_related: false,
        tags: {},
        tags_index: {},
        timer: {},
        type: "TestCaseReport",
        uid: "ddd",
      }],
      logs: [],
      name: "Interactive Suite",
      name_type_index: [],
      part: null,
      status: 'unknown',
      runtime_status: 'ready',
      status_override: null,
      tags: {},
      tags_index: {},
      timer: {},
      type: "TestGroupReport",
      uid: "ccc",
    }],
    logs: [],
    name: "Interactive MTest",
    name_type_index: [],
    part: null,
    status: 'unknown',
    runtime_status: 'ready',
    status_override: null,
    tags: {},
    tags_index: {},
    timer: {},
    type: "TestGroupReport",
    uid: "bbb",
  }],
  meta: {},
  name: "Fake Interactive Report",
  name_type_index: [],
  status: 'unknown',
  runtime_status: 'ready',
  status_override: null,
  tags_index: {},
  timer: null,
  uid: "aaa",
};

export {
  TESTPLAN_REPORT,
  SIMPLE_REPORT,
  ERROR_REPORT,
  FakeInteractiveReport,
}
