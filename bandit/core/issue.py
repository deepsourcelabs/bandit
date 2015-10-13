# -*- coding:utf-8 -*-
#
# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from bandit.core import constants

from six.moves import xrange

import linecache


class Issue(object):
    def __init__(self, severity, confidence=constants.CONFIDENCE_DEFAULT,
                 text="", ident=None):
        self.severity = severity
        self.confidence = confidence
        self.text = text
        self.ident = ident
        self.fname = ""
        self.test = ""
        self.lineno = -1
        self.linerange = []

    def __str__(self):
        return "Issue: '%s' from %s: Severity: %s Confidence: %s at %s:%i" % (
            self.text, (self.ident or self.test), self.severity,
            self.confidence, self.fname, self.lineno)

    def filter(self, severity, confidence):
        '''Used to filter on confidence and severity.

        This wil return false if either the confidence or severity of the issue
        are lower then the given threashold values.

        :param severity: Severity threashold
        :param confidence: Confidence threashold
        '''
        rank = constants.RANKING
        return (rank.index(self.severity) >= rank.index(severity) and
                rank.index(self.confidence) >= rank.index(confidence))

    def get_code(self, max_lines=3, tabbed=False):
        '''Gets lines of code from a file the generated this issue.

        :param max_lines: Max lines of context to return
        :param tabbed: Use tabbing in the output
        :return: strings of code
        '''
        lines = []
        max_lines = max(max_lines, 1)
        lmin = max(1, self.lineno - max_lines / 2)
        lmax = lmin + len(self.linerange) + max_lines - 1

        tmplt = "%i\t%s" if tabbed else "%i %s"
        for line in xrange(int(lmin), int(lmax)):
            text = linecache.getline(self.fname, line)
            if not len(text):
                break
            lines.append(tmplt % (line, text))
        return ''.join(lines)

    def as_dict(self, with_code=True):
        '''Convert the issue to a dict of values for outputting.'''
        out = {
            'filename': self.fname,
            'test_name': self.test,
            'issue_severity': self.severity,
            'issue_confidence': self.confidence,
            'issue_text': self.text,
            'line_number': self.lineno,
            'line_range': self.linerange,
            }

        if with_code:
            out['code'] = self.get_code()
        return out