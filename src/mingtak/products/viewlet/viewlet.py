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
        for k,v in shop_cart.items():
            try:
                if 'sql_' in k :
                    sqlStr = """SELECT price FROM cart WHERE id = {}""".format(k.split('sql_')[1])
                    price = execSql.execSql(sqlStr)[0][0]
                    report.append(price)
                else:
                    obj = api.content.get(UID=k)
                    price = obj.salePrice if obj.salePrice else obj.listPrice
                    data.append({
                        'obj': obj,
                        'number': v
                    })
                cart_money += price * int(v)
            except:
                continue
        self.data = data
        self.report = report
        self.cart_money = cart_money

