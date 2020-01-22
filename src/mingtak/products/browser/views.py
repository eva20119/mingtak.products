# -*- coding: utf-8 -*-

from mingtak.products import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
#from DateTime import DateTime
#import transaction
#import csv
import json
from mingtak.ECBase.browser.views import SqlObj


class ReBuy(BrowserView):
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        id = request.get('id')

        execSql = SqlObj()
        sqlStr = """SELECT * FROM history WHERE id = {}""".format(id)
        data = execSql.execSql(sqlStr)
        
        if data:
            data = data[0]
            cartId = data['cartId']
            uid = data['uid']

            cookie = {}
            if cartId:
                cartId = json.loads(cartId)
                for i in cartId:
                    cookie['sql_' + i] = 1
            if uid:
                uid = json.loads(uid)
                for i in uid:
                    cookie[i] = 1

            sqlStr = """DELETE FROM history WHERE id = {}""".format(id)
            execSql.execSql(sqlStr)
            request.response.setCookie('shop_cart', json.dumps(cookie), path='/OppToday')
            request.response.redirect(self.context.portal_url() + '/pay')
        else:
            request.response.redirect(self.context.portal_url() + '/history_order')
            api.portal.show_message(request=self.request, message='訂單已遺失', type='error')


class OrderHistory(BrowserView):
    template = ViewPageTemplateFile('template/order_history.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()

        userId = api.user.get_current().id
        execSql = SqlObj()
        sqlStr = """SELECT * FROM `history` WHERE cartId is not null or uid is not null
                    or (membership is not null and isPay = 1) AND user = '{}' ORDER BY timestamp DESC
                """.format(userId)
        data = execSql.execSql(sqlStr)

        history = []
        for i in data:
            cartId = i['cartId']
            uid = i['uid']
            membership = i['membership']
            money = i['money']
            timestamp = i['timestamp']
            isPay = i['isPay']
            id = i['id']

            cart = []
            if cartId:
                cartId = json.loads(cartId)
                if len(cartId) == 1:
                    cartId.append('zzzz')
                sqlStr = """SELECT * FROM cart WHERE id in {}""".format(tuple(cartId))
                cart = execSql.execSql(sqlStr)

            productList = []
            if uid:
                uidList = json.loads(uid)
                for i in uidList:
                    productList.append(api.content.get(UID=i))

            history.append({
                'cart': cart,
                'productList': productList,
                'membership': membership,
                'money': money,
                'timestamp': timestamp,
                'isPay': isPay,
                'id': id
            })
        self.history = history
        return self.template()


class CheckOut(BrowserView):
    template = ViewPageTemplateFile('template/check_out.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        abs_url = portal.absolute_url()
        if api.user.is_anonymous():
            request.response.redirect('%s/login' %abs_url)
            api.portal.show_message(request=self.request, message='請先登入', type='error')
            return

        shop_cart = request.cookies.get('shop_cart')
        if shop_cart:
            shop_cart = json.loads(shop_cart)
            if not shop_cart:
                request.response.redirect('%s/products/product_listing' %abs_url)
                api.portal.show_message(request=self.request, message='購物車內尚無商品', type='error')
                return
        else:
            request.response.redirect('%s/products/product_listing' %abs_url)
            api.portal.show_message(request=self.request, message='購物車內尚無商品', type='error')
            return

        data = []
        report = []
        cart_money = 0
        execSql = SqlObj()
        for i in shop_cart.keys():
            try:
                if 'sql_' in i :
                    mysqlId = i.split('sql_')[1]
                    sqlStr = """SELECT price FROM cart WHERE id = {}""".format(mysqlId)
                    price = execSql.execSql(sqlStr)[0][0]
                    cart_money += price
                    report.append({'price': price, 'mysqlId': i})
                else:
                    content = api.content.get(UID=i)
                    cart_money += content.salePrice if content.salePrice else content.listPrice
                    data.append(content)
            except Exception as e:
                continue
        self.data = data
        self.report = report
        self.cart_money = cart_money
        return self.template()


class ProductView(BrowserView):

    index = ViewPageTemplateFile("template/product_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        return self.index()