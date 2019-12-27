# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import random
import json
from plone import api


class JSCode(base.ViewletBase):
    """  """


class ShopCart(base.ViewletBase):
    def update(self):
        request = self.request
        shop_cart = request.cookies.get('shop_cart')
        shop_cart = json.loads(shop_cart) if shop_cart else {}

        data = []
        cart_money = 0
        for i in shop_cart.keys():
            try:
                content = api.content.get(UID=i)
                cart_money += content.salePrice if content.salePrice else content.listPrice
                data.append(content)
            except:
                continue
        self.data = data
        self.cart_money = cart_money

