# -*- coding: utf-8; mode: python -*-
u"""fix python's *Scripts* launchers"""

import sys
import os
import io
import six
import pkg_resources

from fspath import FSPath
from dm.cdbtools import CDBTOOLS_PY27

def log(msg):
    u"""log to stderr"""
    sys.stderr.write(str(msg) + "\n")

launcher_python_template = ur"""#!%(interpreter)s
# -*- coding: utf-8; -*-
# EASY-INSTALL-ENTRY-SCRIPT: '%(project_name)s==%(version)s','%(group)s','%(cmd)s'
__requires__ = '%(project_name)s==%(version)s'
import sys, re
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('%(project_name)s==%(version)s','%(group)s','%(cmd)s')()
    )
"""

launcher_powerscript_template = ur"""#!%(interpreter)s
# -*- coding: utf-8; -*-
# EASY-INSTALL-ENTRY-SCRIPT: '%(project_name)s==%(version)s','%(group)s','%(cmd)s'
__requires__ = '%(project_name)s==%(version)s'
import sys, re, os
from pkg_resources import load_entry_point

# FIXME: this hack to build up powerscripts RTE is not very well tested

os.environ['CADDOK_TOOL'] = '%(cmd)s'

from cdb import rte
import cdbwrapc

rte._set_mainmodule(cdbwrapc)
rte.run_level1('%(project_name)s')
rte.run_level2()
rte.run_level3()
rte.run_level4()
rte.run_level5(os.environ.get("CADDOK_AUTH_PERSNO", "caddok"))

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('%(project_name)s==%(version)s','%(group)s','%(cmd)s')()
    )
"""

def launcher_script(interpreter, distro, group, cmd, entry_point):
    ctx = dict(
        project_name  = distro.project_name
        , version     = distro.version
        , group       = group
        , cmd         = cmd
        , interpreter = interpreter )

    if group == 'console_scripts':
        if interpreter == 'powerscript.exe':
            return launcher_powerscript_template % ctx
        else:
            return launcher_python_template % ctx

    elif group == 'scripts':
        # ToDo
        sys.stderr.write(
            "WARNING: handle group: %s not yet implemented, ignoring"
            " --> distro: %s / cmd: %s / entry_point: %s\n"
            % (group, distro, cmd, entry_point))
    # else:
    #     sys.stderr.write(
    #         "WARNING: handle group: %s is unknown, ignoring"
    #         " --> distro: %s / cmd: %s / entry_point: %s\n"
    #         % (group, distro, cmd, entry_point))

def find_entry_points(path_item):
    """Yield entry_points accessible via `path_item`

    returns tuple with::

        (distro, group, cmd, entry_point)

    types:

    - distro:      class pkg_resources.DistInfoDistribution
    - group:       str
    - cmd:         str
    - entry_point: class pkg_resources.EntryPoint
    """

    for distro in pkg_resources.find_distributions(path_item):
        ep_map = distro.get_entry_map()
        for group, all_eps in ep_map.items():
            for cmd, entry_point in all_eps.items():
                yield (distro, group, cmd, entry_point)

# ==============================================================================
def create_script_exe(script, shebang = u"#!python.exe", exec_out=None):
# ==============================================================================
    u"""Wraps a single script into a MS-Win ``.exe``.

    Only the ``script`` string is wraped into the ``.exe``, not the whole
    python environment!

    This is usefull to create ``.exe`` console scripts for python entry points,
    which can be called directly (``myscript.exe`` instead ``python
    myscript.py``).

    .. caution::

       * This is in an experimental state!
       * This makes use of undocumented pip APIs (ATM pip has no offical API)
       * Use it with care!
       * Shebang default ``#!python.exe``

    """

    from pip._vendor.distlib.scripts import ScriptMaker
    from pip._vendor.distlib.compat import ZipFile

    script   = script.encode('utf-8')
    shebang  = (shebang + u"\n").encode('utf-8')
    exec_out = FSPath(exec_out)
    linesep  = os.linesep.encode('utf-8')

    try:
        shebang.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError(
            'The shebang (%r) is not decodable from utf-8' % shebang)

    maker = ScriptMaker(source_dir   = exec_out.DIRNAME
                        , target_dir = exec_out.DIRNAME )
    launcher = maker._get_launcher('t') # pylint: disable=protected-access
    #if not origin.SUFFIX == '.py':
    #    launcher = maker._get_launcher('w') # pylint: disable=protected-access

    stream = io.BytesIO()
    with ZipFile(stream, 'w') as _f:
        _f.writestr('__main__.py', script)
    zip_data = stream.getvalue()

    with open(exec_out, "wb") as out:
        out.write(launcher + shebang + linesep + zip_data)
    return exec_out


launcher_map = {
    'pip2.7'       : None
    , 'pip2'         : None
    , 'ptipython2'   : None
    , 'ptipython'    : None
    , 'ptpython'     : {'cdbtools-python'        : 'python.exe'
                        , 'cdbtools-powerscript' : 'powerscript.exe'
                        , }
    , 'ptpython2'    : None
}

def create_launchers(scripts_folder, path_item):

    def_py = 'python.exe'

    for (distro, group, cmd, entry_point) in find_entry_points(path_item):
        launchers = launcher_map.get(cmd, def_py)
        if not isinstance(launchers, dict):
            launchers = {cmd : launchers}

        for out_name, interpreter in launchers.items():

            # drop not needed
            drop = [ cmd + "-script.py", out_name + "-script.py" ]
            if os.name == 'posix' or (os.name == 'java' and os._name == 'posix'):
                if out_name != cmd:
                    drop = drop + [ cmd + ".py" ]
                if interpreter is None:
                    drop = drop + [ out_name + ".py"]
            else:
                if out_name != cmd:
                    drop = drop + [ cmd + ".exe" ]
                if interpreter is None:
                    drop = drop + [ out_name + ".exe" ]
            for d in drop:
                d = scripts_folder / d
                if d.EXISTS:
                    log("  delete: %s" % d.BASENAME)
                    d.delete()

            if interpreter is None:
                log("  skip: %s" % out_name)
                continue

            script = launcher_script(interpreter, distro, group, cmd, entry_point)
            if script is None:
                #log("x%s no launcher for:: group: %s / cmd: %s / entry_point: %s"
                #    % (distro, group, cmd, entry_point))
                continue

            if os.name == 'posix' or (os.name == 'java' and os._name == 'posix'):
                py_out = scripts_folder / out_name # + "-script.py"
                log("  create: %s" % py_out.BASENAME)
                with open(py_out, "w") as out:
                    out.write(script)
                # Set the executable bits (owner, group, and world)
                os.chmod(py_ut, 0o755)
            else:
                exec_out = scripts_folder / out_name + ".exe"
                log("  create: %s" % exec_out.BASENAME)
                shebang = u"#!%s" % interpreter
                if interpreter == 'powerscript.exe':
                    shebang = u"#!python.exe"
                create_script_exe(
                    script
                    , shebang  = shebang
                    , exec_out = exec_out )



if __name__ == '__main__':
    scripts_folder = CDBTOOLS_PY27/'Scripts'
    path_item      = CDBTOOLS_PY27/'Python27/site-packages'
    log("fix script wrappers in: %s" % scripts_folder)
    create_launchers(scripts_folder, path_item)

