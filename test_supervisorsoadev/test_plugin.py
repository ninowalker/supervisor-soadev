import re
from nose import tools
from os.path import dirname, join
from subprocess import PIPE, Popen
from unittest import TestCase



CONFIG_FILE = join(dirname(__file__), 'supervisord.conf')


class TestPlugin(TestCase):

    def setUp(self):
        self._supervisorctl('start all')

    def _supervisorctl(self, cmd, config_file=CONFIG_FILE):
        c = 'supervisorctl --configuration="%s" %s' % (config_file, cmd)
        out = Popen(c, shell=True, stdout=PIPE).stdout.read().decode("utf-8")
        print(out)
        return out

    def assert_status(self, expected):
        status = dict(
            re.findall('^([^ ]+) +([^ ]+) .*', line)[0]
            for line
            in self._supervisorctl('status').split('\n')
            if line
        )
        tools.assert_equals(
            expected,
            status
        )

    def test_status_1(self):
        self._supervisorctl("stop one")
        self.assert_status({
            'color:red': 'RUNNING',
            'color:blue': 'RUNNING',
            'color:green': 'RUNNING',
            'one': 'STOPPED',
        })

    def test_status_2(self):
        self._supervisorctl("stop g2")
        self.assert_status({
            'color:red': 'RUNNING',
            'color:blue': 'RUNNING',
            'color:green': 'STOPPED',
            'one': 'STOPPED',
        })

    def test_status_3(self):
        self._supervisorctl("stop g1")
        self.assert_status({
            'color:red': 'STOPPED',
            'color:blue': 'RUNNING',
            'color:green': 'STOPPED',
            'one': 'STOPPED',
        })

    def test_status_3(self):
        self._supervisorctl("stop g1 g2 color:blue")
        self.assert_status({
            'color:red': 'STOPPED',
            'color:blue': 'STOPPED',
            'color:green': 'STOPPED',
            'one': 'STOPPED',
        })

    def test_soa(self):
        out = self._supervisorctl("soagraph")
        self.assertEquals("""g0: color:blue
g1: color:green, one, color:red
g2: one, color:green""", out.strip())
