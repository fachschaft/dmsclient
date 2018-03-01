import os

from configparser import ConfigParser
from enum import Enum

__all__ = ['ReadStatus', 'Sec', 'DmsConfig']


class ReadStatus(Enum):
    NOT_FOUND = 0
    OUTDATED = 1
    LATEST = 2


class Sec(Enum):
    ALIASES = 'ALIASES'
    GENERAL = 'GENERAL'


class DmsConfig(ConfigParser):

    def __init__(self):
        """Create a config with default values"""
        super().__init__()

        self.add_section(Sec.GENERAL)
        self.set(Sec.GENERAL, 'api', 'https://dms.fachschaft.tf/api')
        self.set(Sec.GENERAL, 'token', '')
        self.set(Sec.GENERAL, 'version', '1')

        self.add_section(Sec.ALIASES)
        self.set(Sec.ALIASES, 'wasser', 'Prinzen Perle')

    def read(self, path):
        """Read given config. If config is an older config version it is migrated
        and can later be updated with write()
        """
        found = super().read(path)
        if not found:
            return ReadStatus.NOT_FOUND

        res = ReadStatus.LATEST

        # Update config to new version
        if 'token' in self.defaults():
            res = ReadStatus.OUTDATED
            self.set(Sec.GENERAL, 'version', '1')
            self.set(Sec.GENERAL, 'token', self.defaults()['token'])
            del self.defaults()['token']

        # Future breaking config change can use:
        # if self._p.getint(Sec.GENERAL, 'version') == 1:
        #     res = ReadStatus.OUTDATED
        #     self._p.set(Sec.GENERAL, 'version', 2)

        return res

    def write(self, path):
        """Write the current state of the config into a file"""
        with open(path, 'w') as f:
            super().write(f)

    @property
    def api(self):
        """Api endpoint of the drink management system"""
        return self.get(Sec.GENERAL, 'api')

    @property
    def token(self):
        """Access token for the drink management system"""
        return self.get(Sec.GENERAL, 'token')

    @property
    def aliases(self):
        """List of aliases. Alias = (lowercase alias, mapped drink)"""
        return [(x.lowercase(), y) for (x, y) in self.items(Sec.ALIASES)]

    def add_section(self, sec, *args, **kwargs):
        """Wrapper for Configparser.add_section allowing Enum Sec as "sec"."""
        name = sec.name if isinstance(sec, Sec) else sec
        return super().add_section(name, *args, **kwargs)

    def items(self, sec, *args, **kwargs):
        """Wrapper for Configparser.items allowing Enum Sec as "sec"."""
        name = sec.name if isinstance(sec, Sec) else sec
        return super().items(name, *args, **kwargs)

    def get(self, sec, key, *args, **kwargs):
        """Wrapper for Configparser.get allowing Enum Sec as "sec"."""
        name = sec.name if isinstance(sec, Sec) else sec
        return super().get(name, key, *args, **kwargs)

    def set(self, sec, key, value, *args, **kwargs):
        """Wrapper for Configparser.set allowing Enum Sec as "sec"."""
        name = sec.name if isinstance(sec, Sec) else sec
        return super().set(name, key, value, *args, **kwargs)
