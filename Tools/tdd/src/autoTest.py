"""
Non-interactive test runner used by start.bat when it gets a parameter.

    autoTest.py <Package_Tpkg>  run one package with normal output,
                                exit 0 when all unit tests pass, otherwise 1
    autoTest.py -a              run all packages, print only failed packages,
                                exit with the number of failed packages

Only the unit test result matters, static analysis and complexity are ignored.
Must be started from the test folder.
"""
import contextlib
import os
import sys
import traceback
from pathlib import Path

from TDDConfig import CMainConfig
from testAllPkgs import CTestPkg, CTestPkgThread, setEnvVariable


class NoKeyboard:
    """Replaces KeyboardThread, reports a key press so each package runs only once."""

    def isAnyKeyPressed(self):
        return True


def isPassed(pkg: CTestPkg):
    return "Pass" in pkg.str_testStatus


def listPackages(cfg: CMainConfig):
    suffix = cfg.co_pkg.str_testfldr_suffix
    return sorted(d.name for d in Path(cfg.co_pkg.str_testpath).glob("*" + suffix) if d.is_dir())


def runOne(name: str, cfg: CMainConfig):
    if name not in listPackages(cfg):
        print("Test package '%s' not found." % name)
        return 1

    print(name)
    pkg = CTestPkg(name, cfg, NoKeyboard())
    pkg.b_silent = False
    try:
        pkg.run()
    except Exception:
        traceback.print_exc()
    return 0 if isPassed(pkg) else 1


def runAll(cfg: CMainConfig):
    kpt = NoKeyboard()
    with open(os.devnull, "w") as devnull, \
            contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        pkgs = [CTestPkgThread(name, cfg, kpt) for name in listPackages(cfg)]
        for pkg in pkgs:
            pkg.join()

    failed = [pkg.name for pkg in pkgs if not isPassed(pkg)]
    for name in failed:
        print(name)
    return len(failed)


def main():
    if len(sys.argv) != 2:
        print("Usage: %s <Package_Tpkg> | -a" % Path(sys.argv[0]).name)
        return 1

    cfg = CMainConfig()
    cfg.co_pkg.readFromFile('Tools/TestConfigs/default.tcfg')
    cfg.co_stat.readFromFile('Tools/TestConfigs/default.tcfg')
    cfg.co_env.readFromFile('envPath.ini')
    setEnvVariable(cfg.co_env)

    if sys.argv[1] == "-a":
        return runAll(cfg)
    return runOne(sys.argv[1], cfg)


if __name__ == "__main__":
    exitCode = main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(exitCode)
