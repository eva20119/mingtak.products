# -*- coding: utf-8 -*-

from mingtak.products import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
#from DateTime import DateTime
#import transaction
#import csv


class ProductView(BrowserView):

    index = ViewPageTemplateFile("template/product_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        return self.index()


# class ProductListing11(BrowserView):
#     index = ViewPageTemplateFile("template/product_listing.pt")
    
#     def __call__(self):
#         context = self.context
#         request = self.request
#         portal = api.portal.get()
        
#         return self.index()


class ProductListing(BrowserView):
    index = ViewPageTemplateFile("template/product_listing.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        self.data = []
        items = api.content.find(context=portal, Type='Product', review_state='published', sort_on='created', sort_order='reverse')
        for item in items:
            self.data.append(item.getObject())
        return self.index()
