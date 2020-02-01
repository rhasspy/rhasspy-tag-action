from __future__ import annotations

from dataclasses import dataclass

import re

@dataclass(order=True)
class Version:
    mainVersion: int = 0
    updateVersion: int = 0
    hotfix: int = 0
    releaseType: str = 'release'

    def __str__(self):
        if self.releaseType == 'release':
            return f'{self.mainVersion}.{self.updateVersion}.{self.hotfix}'
        else:
            return f'{self.mainVersion}.{self.updateVersion}.{self.hotfix}-{self.releaseType}'

    @classmethod
    def fromString(cls, versionString: str) -> Version:
        versionMatch = re.search(
            '(?P<mainVersion>\d+)\.(?P<updateVersion>\d+)(?:\.(?P<hotfix>\d+))?(?:-(?P<releaseType>rev|release))?',
            str(versionString))

        # when the string is no version set the version to the lowest possible value
        if not versionMatch:
            return cls(0, 0, 0, '')

        return cls(
            int(versionMatch.group('mainVersion')),
            int(versionMatch.group('updateVersion')),
            int(versionMatch.group('hotfix') or 0),
            versionMatch.group('releaseType') or 'release')
