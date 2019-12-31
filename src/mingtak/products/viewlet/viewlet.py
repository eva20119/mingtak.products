# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import random
import json
from plone import api
from mingtak.ECBase.browser.views import SqlObj


class JSCode(base.ViewletBase):
    """  """


class ShopCart(base.ViewletBase):
    def update(self):
        request = self.request
        shop_cart = request.cookies.get('shop_cart')
        shop_cart = json.loads(shop_cart) if shop_cart else {}

        data = []
        report = []
        cart_money = 0
        execSql = SqlObj()
        for i in shop_cart.keys():
            try:
                if 'sql_' in i :
                    sqlStr = """SELECT price FROM cart WHERE id = {}""".format(i.split('sql_')[1])
                    price = execSql.execSql(sqlStr)[0][0]
                    cart_money += price
                    report.append(price)
                else:
                    content = api.content.get(UID=i)
                    cart_money += content.salePrice if content.salePrice else content.listPrice
                    data.append(content)
            except:
                continue
        self.data = data
        self.report = report
        self.cart_money = cart_money

