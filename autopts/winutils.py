#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation
# Copyright (c) 2023, Codecoup
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

"""Windows utilities"""

import os
import sys
import ctypes

if sys.platform == 'win32':
    import win32gui
    import win32process


class AdminStateUnknownError(Exception):
    pass


def have_admin_rights():
    """"Check if the process has Administrator rights"""
    try:
        return os.getuid() == 0
    except AttributeError:
        pass

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError


def get_pid_by_window_title(title):
    def callback(hwnd, hwnd_list):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)

            if window_title.startswith(title):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    hwnd_list.append(pid)
                except:
                    pass

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)

    if hwnd_list:
        return hwnd_list[0]
    else:
        return None


def exit_if_admin():
    """Exit program if running as Administrator"""
    if have_admin_rights():
        sys.exit("Administrator rights are not required to run this script!")


def main():
    """Main."""

    is_admin = have_admin_rights()

    if is_admin:
        print("Running as administrator")
    else:
        print("Not running as administrator")

    exit_if_admin()


if __name__ == "__main__":
    main()
