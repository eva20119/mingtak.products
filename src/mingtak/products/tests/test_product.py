# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from mingtak.products.testing import MINGTAK_PRODUCTS_INTEGRATION_TESTING  # noqa
from mingtak.products.interfaces import IProduct

import unittest2 as unittest


class ProductIntegrationTest(unittest.TestCase):

    layer = MINGTAK_PRODUCTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        schema = fti.lookupSchema()
        self.assertEqual(IProduct, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Product')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IProduct.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Product', 'Product')
        self.assertTrue(
            IProduct.providedBy(self.portal['Product'])
        )
