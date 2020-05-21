import os
import re
import sys

from chaostoolkit.__main__ import cli


def _get_variable_or_throw(var: str):
    if var in os.environ and os.environ[var]:
        return os.environ[var]
    raise Exception("Environment variable %s does not exist" % var)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    orginal_argv = sys.argv.copy()

    # Custom stuff
    sys.argv = orginal_argv.copy()
    sys.argv.extend([
        "run", "chaosexp/experiment.yml"
    ])
    result = cli(standalone_mode=False)
