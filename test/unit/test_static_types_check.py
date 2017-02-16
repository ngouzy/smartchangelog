import inspect

from mypy import api

import commitmsg


def test_static_type_check_with_mypy():
    current_file = inspect.getfile(commitmsg)
    params = ' '.join(['--ignore-missing-imports', '--fast-parser', '--python-version', ' 3.6 ', current_file])
    result = api.run(params)
    if result[0]:
        # FIXME: begin: There is a bug in mypy version 0.471 about support iteration on enums
        # see https://github.com/python/mypy/issues/2305
        # So, we have to remove irrelevant errors
        check_type_errors = "\n".join(
            (error for error in result[0].strip().split("\n") if error.split("error: ")[1] not in (
                '"CommitType" expects no type arguments, but 1 given',
                'Invalid type "commit_type_str"',
                'Iterable expected',
                '"CommitType" has no attribute "__iter__"'
            )))
        # FIXME: end
        if len(check_type_errors) > 0:
            raise (Exception(check_type_errors))
    if result[1]:
        raise (Exception(result[1]))
