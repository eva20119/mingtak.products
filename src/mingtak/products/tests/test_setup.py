# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from mingtak.products.testing import MINGTAK_PRODUCTS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that mingtak.products is properly installed."""

    layer = MINGTAK_PRODUCTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mingtak.products is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mingtak.products'))

    def test_browserlayer(self):
        """Test that IMingtakProductsLayer is registered."""
        from mingtak.products.interfaces import (
            IMingtakProductsLayer)
        from plone.browserlayer import utils
        self.assertIn(IMingtakProductsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MINGTAK_PRODUCTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['mingtak.products'])

    def test_product_uninstalled(self):
        """Test if mingtak.products is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mingtak.products'))

    def test_browserlayer_removed(self):
        """Test that IMingtakProductsLayer is removed."""
        from mingtak.products.interfaces import IMingtakProductsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMingtakProductsLayer, utils.registered_layers())
