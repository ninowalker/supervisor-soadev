from threading import Thread
import functools
from collections import defaultdict
from supervisor.supervisorctl import ControllerPluginBase
from supervisorsoadev.unpack import unpack_symbols

class SOADevControllerPlugin(ControllerPluginBase):
    name = 'soadev'

    def __init__(self, controller, **config):
        self.ctl = controller
        self.graph = defaultdict(set)
        self.sets = set(map(str.strip, config['sets'].replace(",", " ").split()))
        g = config['graph'].strip()
        for l in g.split("\n"):
            node, edges = l.replace(" ","").split("->")
            self.graph[node].update(map(str.strip, edges.split(",")))

    def _unpack(self, *keys):
        return unpack_symbols(self.sets, self.graph, *keys)

    def _expand(self, arg, command):
        keys = map(str.strip, arg.split())
        supervisor = self.ctl.get_supervisor()

        procs = self._unpack(*keys)

        #self.ctl.output('SOA Group includes: %s' % ", ".join(procs))
        threads = []
        for process in supervisor.getAllProcessInfo():
            for proc in procs:
                print process
                if (process['group'], process['name']) == proc.split(":",1):
                    t = Thread(target=self.ctl.onecmd, args=('%s %s:%s' % (command, process['group'], process['name']), ))
                    t.start()
                    threads.append(t)
        for t in threads:
            t.join()
        if not threads:
            self.ctl.output('No process matched given expression.')

    def _wrap_help(self, command):
        self.ctl.output('The same as %s, but accepts wildcard expressions to match the process name.' % command)
        self.ctl.output('soa_%s <group> - %ss all processes in the SOA group.' % (command, command))

    def do_soagraph(self, arg):
        a = []
        for s in sorted(self.sets):
            a.append("%s:\n  %s\n" % (s, "\n  ".join(self._unpack(s))))
        self.ctl.output('\n'.join(a))

    def help_soagraph(self):
        return self.ctl.output('Display the SOA graph.')

    def enhanced_status(self, default, args):
        if not args:
            args = 'all'
        a = set()
        for a_ in args.split():
            if a_ in self.sets:
                a.update(self._unpack(a_))
            else:
                a.add(a_)
        return default._do_status(" ".join(a))


def make_soadev_controllerplugin(controller, **config):
    from supervisor.supervisorctl import DefaultControllerPlugin as default
    plugin = SOADevControllerPlugin(controller, **config)

    def wrap(func):
        def _wrapper(self, args):
            a = set()
            for a_ in (args or '').split():
                if a_ in plugin.sets:
                    a.update(plugin._unpack(a_))
                else:
                    a.add(a_)
            return func(self, " ".join(a).strip())
        return _wrapper

    for f in ('do_status', 'do_start', 'do_stop', 'do_restart'):
        setattr(default, f, wrap(getattr(default, f)))

    return plugin

