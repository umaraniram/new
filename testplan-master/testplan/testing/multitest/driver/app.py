"""Generic application driver."""

import os
import uuid
import shutil
import warnings
import subprocess
import datetime
import platform
import socket

from schema import Or
from past.builtins import basestring

from testplan.common.config import ConfigOption
from testplan.common.utils.path import StdFiles, makedirs
from testplan.common.utils.context import is_context, expand
from testplan.common.utils.process import kill_process

from .base import Driver, DriverConfig

IS_WIN = platform.system() == "Windows"


class AppConfig(DriverConfig):
    """
    Configuration object for
    :py:class:`~testplan.testing.multitest.driver.app.App` resource.
    """

    @classmethod
    def get_options(cls):
        """
        Schema for options validation and assignment of default values.
        """
        return {
            "binary": basestring,
            ConfigOption("pre_args", default=None): Or(None, list),
            ConfigOption("args", default=None): Or(None, list),
            ConfigOption("shell", default=False): bool,
            ConfigOption("env", default=None): Or(None, dict),
            ConfigOption("binary_copy", default=False): bool,
            ConfigOption("app_dir_name", default=None): Or(None, basestring),
            ConfigOption("working_dir", default=None): Or(None, basestring),
        }


class App(Driver):
    """
    Binary application driver.

    :param name: Driver name. Also uid.
    :type name: ``str``
    :param binary: Path the to application binary.
    :type binary: ``str``
    :param pre_args: Arguments to be prepended to binary command. An argument
        can be a :py:class:`~testplan.common.utils.context.ContextValue`
        and will be expanded on runtime.
    :type pre_args: ``list`` or ``str``
    :param args: Arguments to be appended to binary command. An argument
        can be a :py:class:`~testplan.common.utils.context.ContextValue`
        and will be expanded on runtime.
    :type args: ``list`` of ``str``
    :param shell: Invoke shell for command execution.
    :type shell: ``bool``
    :param env: Environmental variables to be made available to child process.
    :type env: ``dict``
    :param binary_copy: Copy binary to a local binary path.
    :type binary_copy: ``bool``
    :param app_dir_name: Application directory name.
    :type app_dir_name: ``str``
    :param working_dir: Application working directory. Default: runpath
    :type working_dir: ``str``

    Also inherits all
    :py:class:`~testplan.testing.multitest.driver.base.DriverConfig` options.
    """

    CONFIG = AppConfig

    def __init__(
        self,
        name,
        binary,
        pre_args=None,
        args=None,
        shell=False,
        env=None,
        binary_copy=False,
        app_dir_name=None,
        working_dir=None,
        **options
    ):
        options.update(self.filter_locals(locals()))
        super(App, self).__init__(**options)
        self.proc = None
        self.std = None
        self.binary = None
        self._binpath = None
        self._etcpath = None
        self._retcode = None

    @property
    def pid(self):
        """
        Return pid of the child process if available, ``None`` otherwise.

        :rtype: ``int`` or ``NoneType``
        """
        if self.proc:
            return self.proc.pid
        else:
            return None

    @property
    def retcode(self):
        """
        Return return code of the app process or ``None``.

        :rtype: ``int`` or ``NoneType``
        """
        if self._retcode is None:
            if self.proc:
                self._retcode = self.proc.poll()
        return self._retcode

    @property
    def cmd(self):
        """Command that starts the application."""
        args = self.cfg.args or []
        pre_args = self.cfg.pre_args or []
        cmd = []
        cmd.extend(pre_args)
        cmd.append(self.binary or self.cfg.binary)
        cmd.extend(args)
        cmd = [
            expand(arg, self.context, str) if is_context(arg) else arg
            for arg in cmd
        ]
        return cmd

    @property
    def env(self):
        """Environment variables."""
        if isinstance(self.cfg.env, dict):
            return {
                key: expand(val, self.context, str) if is_context(val) else val
                for key, val in self.cfg.env.items()
            }
        else:
            return self.cfg.env

    @property
    def logpath(self):
        """Path for log regex matching."""
        if self.cfg.logname:
            return os.path.join(self.app_path, self.cfg.logname)
        return self.outpath

    @property
    def outpath(self):
        """Path for stdout file regex matching."""
        return self.std.out_path

    @property
    def errpath(self):
        """Path for stderr file regex matching."""
        return self.std.err_path

    @property
    def app_path(self):
        """Application directory path."""
        if self.cfg.app_dir_name:
            return os.path.join(self.runpath, self.cfg.app_dir_name)
        return self.runpath

    @property
    def binpath(self):
        """'bin' directory under runpath."""
        return self._binpath

    @property
    def etcpath(self):
        """'etc' directory under runpath."""
        return self._etcpath

    def _prepare_binary(self, path):
        """prepare binary path"""
        return path

    @property
    def hostname(self):
        """
        :return: hostname where the ETSApp is running
        :rtype: ``str``
        """
        return socket.gethostname()

    def pre_start(self):
        """
        Create mandatory directories and install files from given templates
        using the drivers context before starting the application binary.
        """
        super(App, self).pre_start()

        self._make_dirs()

        if self.cfg.path_cleanup is True:
            name = os.path.basename(self.cfg.binary)
        else:
            name = "{}-{}".format(
                os.path.basename(self.cfg.binary), uuid.uuid4()
            )

        self.binary = self._prepare_binary(self.cfg.binary)
        if os.path.isfile(self.binary):
            target = os.path.join(self._binpath, name)
            if self.cfg.binary_copy:
                shutil.copyfile(self.binary, target)
                self.binary = target
            elif not IS_WIN:
                os.symlink(os.path.abspath(self.binary), target)
                self.binary = target

        makedirs(self.app_path)
        self.std = StdFiles(self.app_path)

        if self.cfg.install_files:
            self._install_files()

    def starting(self):
        """Starts the application binary."""
        super(App, self).starting()

        cmd = " ".join(self.cmd) if self.cfg.shell else self.cmd
        cwd = self.cfg.working_dir or self.runpath
        try:
            self.logger.debug(
                "%(driver)s driver command: %(cmd)s,\n"
                "\trunpath: %(runpath)s\n"
                "\tout/err files %(out)s - %(err)s",
                {
                    "driver": self.uid(),
                    "cmd": cmd,
                    "runpath": self.runpath,
                    "out": self.std.out_path,
                    "err": self.std.err_path,
                },
            )
            self.proc = subprocess.Popen(
                cmd,
                shell=self.cfg.shell,
                stdin=subprocess.PIPE,
                stdout=self.std.out,
                stderr=self.std.err,
                cwd=cwd,
                env=self.env,
            )
        except Exception:
            self.logger.error(
                "Error while App[%s] driver executed command: %s",
                self.cfg.name,
                cmd if self.cfg.shell else " ".join(cmd),
            )
            if self.proc is not None:
                if self.proc.poll() is None:
                    kill_process(self.proc)
                assert self.proc.returncode is not None
                self._proc = None
            raise

    def stopping(self):
        """Stops the application binary process."""
        super(App, self).stopping()
        try:
            self._retcode = kill_process(self.proc)
        except Exception as exc:
            warnings.warn(
                "On killing driver {} process - {}".format(self.cfg.name, exc)
            )
            self._retcode = self.proc.poll() if self.proc else 0
        self.proc = None
        if self.std:
            self.std.close()

    def _make_dirs(self):
        bin_dir = os.path.join(self.runpath, "bin")
        etc_dir = os.path.join(self.runpath, "etc")
        for directory in (bin_dir, etc_dir):
            makedirs(directory)
        self._binpath = bin_dir
        self._etcpath = etc_dir

    def _install_target(self):
        return self.etcpath

    def restart(self):
        """
        Stop the driver, archive the app_dir or rename std/log, and then restart
        the driver.
        """
        self.stop()
        self.wait(self.status.STOPPED)

        if self.cfg.app_dir_name:
            self._move_app_path()
        else:
            self._rename_std_and_log()

        path_cleanup = self.cfg.path_cleanup
        self.cfg.path_cleanup = False
        # we don't want to cleanup runpath during restart
        self.start()
        self.wait(self.status.STARTED)
        self.cfg.path_cleanup = path_cleanup

    def _move_app_path(self):
        """
        Move app_path directory to an archive location
        """
        snapshot_path = self.app_path + datetime.datetime.now().strftime(
            "_%Y%m%d_%H%M%S"
        )

        shutil.move(self.app_path, snapshot_path)
        os.makedirs(self.app_path)

    def _rename_std_and_log(self):
        """
        Rename std and log files
        """
        timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

        for file in (self.outpath, self.errpath, self.logpath):
            if os.path.isfile(file):
                os.rename(file, file + timestamp)

    def aborting(self):
        """Abort logic to force kill the child binary."""
        if self.proc:
            self.logger.debug("Killing process id {}".format(self.proc.pid))
            kill_process(self.proc)
        if self.std:
            self.std.close()
