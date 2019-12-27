# -*- coding: utf-8 -*-
from mingtak.products import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
import logging


class CartUpdate(BrowserView):
    """ Cart Update
    """

    logger = logging.getLogger('Update Item to Cart.')

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()
        catalog = context.portal_catalog
        logger = self.logger

        # itemInCart's format: {UID:amount, ...}
        itemInCart = request.cookies.get('itemInCart', '{}')
        if itemInCart:
            itemInCart = json.loads(itemInCart)
        else:
            itemInCart = {}

        itemUID = request.form.get('uid')
        action = request.form.get('action')
        if not (itemUID and action):
            response.redirect(portal.absolute_url())
            return
        if not api.content.find(Type='Product', UID=itemUID):
            response.redirect(portal.absolute_url())
            return

        if action == 'plus':
            if itemInCart.get(itemUID):
                itemInCart[itemUID] += 1
            else:
                itemInCart[itemUID] = 1
        elif action == 'less':
            item = itemInCart.get(itemUID)
            if item > 1:
                itemInCart[itemUID] -= 1
            else:
                itemInCart.pop(itemUID)
        elif action == 'del':
            itemInCart.pop(itemUID)
        else:
            response.redirect(portal.absolute_url())
            return

        itemInCart = json.dumps(itemInCart)
        request.response.setCookie('itemInCart', itemInCart)

        return itemInCart
