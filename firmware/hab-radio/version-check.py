# Returns Python version

import sys

# Check minimum requirement version
if sys.version_info < (3,6):
    print("Python version 3.6 or higher is required", file=sys.stderr)
    sys.exit(1)

# Print version number
print("python{}.{}".format(sys.version_info.major, sys.version_info.minor))
