#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc here.
"""

__docformat__ = 'restructuredtext en'

import os
#import shutil
#import tempfile
from unittest import TestCase


class DummyConfigurator(object):
    def __init__(self,
                 defaults=None,
                 bobbyconfig=None,
                 templateconfig=None,
                 variables=None,
                 quiet=False):
        self.defaults = defaults or {}
        self.bobbyconfig = bobbyconfig or {}
        self.variables = variables or {'physdev': 'em0'}
        self.quiet = quiet
        self.templateconfig = templateconfig or {}


class ToolsTest(TestCase):

    def test_within_intervall(self):
        from mrbobby.bobbyexceptions import ValidationError
        from ..hooks import within_intervall
        self.assertRaises(ValidationError, within_intervall, 'O', 'test')
        self.assertRaises(ValidationError, within_intervall, '256', 'test')
        self.assertEquals(within_intervall('200', 'test'), '200')

    def test_is_a_network_address(self):
        from ..hooks import is_a_network_address
        self.assertTrue(is_a_network_address('192.168.0.1/32'))
        self.assertFalse(is_a_network_address('192.168.0.1/31'))


class Post_ask_q_carp_iface_cidrTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import post_ask_q_carp_iface_cidr
        return post_ask_q_carp_iface_cidr(DummyConfigurator(), question,
                                          answer)

    def test_post_ask_q_carp_iface_cidr(self):
        from mrbobby.bobbyexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'test')
        self.assertRaises(ValidationError, self.call_FUT, 'test/32')
        self.assertRaises(ValidationError, self.call_FUT, '192.168.0.3/30')
        self.assertRaises(ValidationError, self.call_FUT, '192.168.0.0/31')
        self.assertEquals(self.call_FUT('192.168.0.1/30'), '192.168.0.1/30')


class Post_ask_q_carp_iface_advskewTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import post_ask_q_carp_iface_advskew
        return post_ask_q_carp_iface_advskew(DummyConfigurator(), question,
                                             answer)

    def test_post_ask_q_carp_iface_advskew(self):
        from mrbobby.bobbyexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'test')
        self.assertRaises(ValidationError, self.call_FUT, '0')
        self.assertRaises(ValidationError, self.call_FUT, '255')
        self.assertEquals(self.call_FUT('254'), '254')


class Post_ask_q_carp_iface_vlanTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import post_ask_q_carp_iface_vlan
        return post_ask_q_carp_iface_vlan(DummyConfigurator(), question,
                                          answer)

    def test_post_ask_q_carp_iface_vlan(self):
        from mrbobby.bobbyexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, '4095')
        self.assertEquals(self.call_FUT('254'), '254')
        self.assertFalse(self.call_FUT('0'))


class Post_ask_q_carp_iface_descriptionTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import post_ask_q_carp_iface_description
        return post_ask_q_carp_iface_description(DummyConfigurator(), question,
                                                 answer)

    def test_post_ask_q_carp_iface_description(self):
        from string import ascii_letters
        self.assertEquals(len(self.call_FUT(ascii_letters)), 48)
        self.assertEquals(self.call_FUT(' test '), 'test')


class Post_ask_q_carp_iface_vhidTest(TestCase):
    def setUp(self):
        import bobbytemplates.thd
        self.fs_templates = os.path.abspath(
            os.path.join(os.path.dirname(bobbytemplates.thd.__file__),
                         'carp_iface'))

    def call_FUT(self, answer, configurator=None, question=None):
        from mrbobby.configurator import Configurator
        from ..hooks import post_ask_q_carp_iface_vhid
        return post_ask_q_carp_iface_vhid(Configurator(self.fs_templates, '',
                                                       {}), question, answer)

    def test_post_ask_q_carp_iface_vhid(self):
        from mrbobby.bobbyexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'test')
        self.assertRaises(ValidationError, self.call_FUT, '0')
        self.assertEquals(self.call_FUT('255'), '255')

# vim:set et sts=4 ts=4 tw=80:
