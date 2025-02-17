# timer.py
#
# Copyright 2022 Fyodor Sobolev
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.
#
# SPDX-License-Identifier: MIT

from gi.repository import GObject
from .actions import *


class Timer:
    def __init__(self, h, m, s, action, timer_label, desc_label, finish_fn):
        self.h, self.m, self.s = h, m, s
        self.duration = self.h * 3600 + self.m * 60 + self.s
        self.action = action[0]
        self.desc_label = desc_label
        if self.action == 'poweroff':
            self.desc_label.set_text(_('Your device will be powered off in'))
        elif self.action == 'reboot':
            self.desc_label.set_text(_('Your device will be rebooted in'))
        elif self.action == 'suspend':
            self.desc_label.set_text(_('Your device will be suspended in'))
        elif self.action == 'notification':
            self.desc_label.set_text(_('You will receive a notification in'))
            self.notification_text = action[1]
            self.play_sound = action[2]
        self.timer_label = timer_label
        self.finish_fn = finish_fn
        self.stop = False

    def run(self):
        if self.stop: return
        if self.duration > 0:
            self.s = self.duration
            self.h = self.s // 3600
            self.s %= 3600
            self.m = self.s // 60
            self.s %= 60
            self.timer_label.set_text(
                str(self.h) +
                ':{0:0>2}'.format(self.m) +
                ':{0:0>2}'.format(self.s))
            self.duration -= 1
            GObject.timeout_add_seconds(1, self.run)
        else:
            self.act()
            self.finish_fn()

    def act(self):
        if self.action == 'poweroff':
            action_poweroff()
        elif self.action == 'reboot':
            action_reboot()
        elif self.action == 'suspend':
            action_suspend()
        elif self.action == 'notification':
            action_notify(self.notification_text, self.play_sound)
