# Test class for testing the boot process of a Linux kernel
#
# This work is licensed under the terms of the GNU GPL, version 2 or
# later.  See the COPYING file in the top-level directory.

import os

from .testcase import QemuSystemTest
from .cmd import wait_for_console_pattern
from .archive import deb_extract


class LinuxKernelTest(QemuSystemTest):
    KERNEL_COMMON_COMMAND_LINE = 'printk.time=0 '

    def wait_for_console_pattern(self, success_message, vm=None):
        wait_for_console_pattern(self, success_message,
                                 failure_message='Kernel panic - not syncing',
                                 vm=vm)

    def launch_kernel(self, kernel, initrd=None, dtb=None, console_index=0,
                      wait_for=None):
        self.vm.set_console(console_index=console_index)
        self.vm.add_args('-kernel', kernel)
        if initrd:
                self.vm.add_args('-initrd', initrd)
        if dtb:
                self.vm.add_args('-dtb', dtb)
        self.vm.launch()
        if wait_for:
                self.wait_for_console_pattern(wait_for)

    def extract_from_deb(self, deb_path, path):
        """
        Extracts a file from a deb package into the test workdir

        :param deb_path: path to the deb archive
        :param path: path within the deb archive of the file to be extracted
        :returns: path of the extracted file
        """
        deb_extract(deb_path, self.workdir, member="." + path)
        # Return complete path to extracted file.  Because callers to
        # extract_from_deb() specify 'path' with a leading slash, it is
        # necessary to use os.path.relpath() as otherwise scratch_file()
        # interprets it as an absolute path and drops the required prefix
        return os.path.normpath(self.scratch_file(os.path.relpath(path, '/')))

