import sys
from subprocess import Popen, call, PIPE
import re
import tempfile


# known pip check issues
PIP_CHECK_IGNORE = r"(fastdiff)"

# coverage threshold
COV_FAIL_UNDER = 48

with tempfile.TemporaryDirectory() as td:
    pip_check = Popen(["pip", "check"], stdout=PIPE, stderr=PIPE, cwd=td)
    stdout, stderr = pip_check.communicate()

lines = (stdout + stderr).decode("utf-8").strip().splitlines()
failed = []

for line in lines:
    print(line, end="")
    if re.findall("No broken", line):
        print("... ignoring...")
        continue
    if re.findall(PIP_CHECK_IGNORE, line):
        print("... ignoring...")
        continue
    print("!!!!!")
    failed += [line]

if failed:
    sys.exit(len(failed))

rc = call(
    [
        "pytest",
        "-vv",
        "--cov=graphene",
        "--cov-report=term-missing:skip-covered",
        "--no-cov-on-fail",
        f"--cov-fail-under={COV_FAIL_UNDER}",
    ],
    cwd="graphene/tests",
)

sys.exit(rc)
