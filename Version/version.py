
from collections import namedtuple

Version = namedtuple('semantic_version', ('major', 'minor', 'patch'))


def dotted_version(self):
    return '.'.join(map(str, self))


Version.__str__ = dotted_version
Version.__doc__ = "https://semver.org/"


# version = Version(1, 2, 3)
# print(version)  # 1.2.3
# print((1, 2) < version)  # True
# print((1, 3) > version)  # True
# print(repr(version))  # semantic_version(major=1, minor=2, patch=3)
# print(version.__doc__)  # https://semver.org/
