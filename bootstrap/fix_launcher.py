# -*- coding: utf-8; mode: python -*-
u"""fix python's *Scripts* launchers"""

# pylint: disable=invalid-name, too-many-branches

import sys
import os
import io
import platform

import pkg_resources

from fspath import FSPath
from dm.cdbtools import CDBTOOLS_PY27, CDBTOOLS_HOME

def log(msg):
    u"""log to stderr"""
    sys.stderr.write(str(msg) + "\n")

python_ep_template = r"""#!%(interpreter)s
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

powerscript_ep_template = r"""#!%(interpreter)s
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

powerscript_prefix = r"""#!%(interpreter)s
# -*- coding: utf-8; -*-

# FIXME: this hack to build up powerscripts RTE is not very well tested

import os
os.environ['CADDOK_TOOL'] = '%(cmd)s'

from cdb import rte
import cdbwrapc

rte._set_mainmodule(cdbwrapc)
rte.run_level1('%(project_name)s')
rte.run_level2()
rte.run_level3()
rte.run_level4()
rte.run_level5(os.environ.get("CADDOK_AUTH_PERSNO", "caddok"))

"""

run_ptpython = r"""
from dm.cdbtools.run_ptpython import main
main()
"""

launcher_map = {
    'pip2.7'       : None
    , 'pip2'         : None
    , 'ptipython2'   : None
    , 'ptipython'    : None
    , 'ptpython'     : {
        'cdbtools-python'        : ('python.exe',      python_ep_template)
        , 'cdbtools-powerscript' : ('powerscript.exe', powerscript_prefix + run_ptpython )
        , }
    , 'ptpython2'    : None
}


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

def create_launchers(scripts_folder, path_item):
    u"""create launchers in ``scripts_folder`` for entry points of ``path_item``"""
    def_py = 'python.exe'

    for (distro, group, cmd, entry_point) in find_entry_points(path_item):

        launchers = launcher_map.get(cmd, def_py)
        if not isinstance(launchers, dict):
            if not isinstance(launchers, tuple):
                launchers = (launchers, python_ep_template)
            launchers = {cmd : launchers}

        for out_name, (interpreter, my_template) in launchers.items():
            # pylint: disable=protected-access, no-member
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

            ctx = dict(
                project_name  = distro.project_name
                , version     = distro.version
                , group       = group
                , cmd         = cmd
                , interpreter = interpreter )

            script = None

            if group == 'console_scripts':
                script = my_template % ctx

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
                os.chmod(py_out, 0o755)
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


def fix_pth_files(path_item):
    u"""fix *.pth files located in folder ``path_item``.

    Replaces all absolute pathname in *.pth files with the relative pathname.
    """
    path_item = FSPath(path_item)
    if platform.system() == 'Windows':
        path_item = FSPath(path_item.lower())

    scan_files = list(path_item.glob('*.pth')) + list(path_item.glob('*.egg-link'))
    intro_flag = False
    for pth_file in scan_files:
        old_lines = pth_file.readFile().splitlines()
        new_lines = []
        for line in old_lines:
            x = FSPath(line)
            if not x.ISABSPATH:
                new_lines.append(line)
                continue
            if platform.system() == 'Windows':
                x = FSPath(line.lower())
                prefix = CDBTOOLS_HOME.lower()
            else:
                prefix = CDBTOOLS_HOME

            if x.startswith(prefix):
                intro_flag or log("  %s .." % pth_file) # pylint: disable=expression-not-assigned
                intro_flag = True
                log("  -- %s" % line )
                new_l = x.relpath(path_item)
                if platform.system() == 'Windows':
                    new_l = new_l.replace('\\', '/')
                log("  ++ %s" % new_l )
                new_lines.append(new_l)
            else:
                new_lines.append(line)

        old_lines = "\n".join(old_lines)
        new_lines = "\n".join(new_lines)
        if new_lines != old_lines:
            with pth_file.openTextFile(mode='w') as f:
                f.write(new_lines)
            #log(new_lines)
        else:
            pass
            #log("  %s .." % pth_file)
            #log("  --> nothing to do.")


if __name__ == '__main__':
    _scripts_folder = CDBTOOLS_PY27/'Scripts'
    _path_item      = CDBTOOLS_PY27/'Python27/site-packages'
    log("fix pathnames in *.pth files located at: %s" % _path_item)
    fix_pth_files(_path_item)
    log("fix script wrappers in: %s" % _scripts_folder)
    create_launchers(_scripts_folder, _path_item)
