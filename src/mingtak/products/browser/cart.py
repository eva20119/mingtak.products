# -*- coding: utf-8 -*-
from mingtak.products import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
import logging
from mingtak.ECBase.browser.views import SqlObj


class CartUpdate(BrowserView):
    logger = logging.getLogger('Update Item to Cart.')
    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()
        logger = self.logger

        uid = request.form.get('uid')
        action = request.form.get('action')

        if not (uid and action):
            return
        try:
            content = api.content.get(UID=uid)
        except:
            import pdb;pdb.set_trace()
            return

        # shop_cart's format: {UID:amount, ...}
        shop_cart = request.cookies.get('shop_cart')
        shop_cart = json.loads(shop_cart) if shop_cart else {}

        msg = ''

        if action == 'add':
            if shop_cart.__contains__(uid):
                msg = '商品已在購物車內'
            else:
                shop_cart[uid] = 1
                msg = '新增成功'
        elif action == 'plus':
            if shop_cart.__contains__(uid):
                shop_cart[uid] += 1
            else:
                shop_cart[uid] = 1
        elif action == 'less':
            item = shop_cart.__contains__(uid)
            if item > 1:
                shop_cart[uid] -= 1
            else:
                del shop_cart[uid]
        elif action == 'del':
            if 'sql_' in uid:
                execSql = SqlObj()
                mysqlId = uid.split('sql_')[1]
                sqlStr = """SELECT price FROM cart WHERE id = {}""".format(mysqlId)
                price = execSql.execSql(sqlStr)[0][0]
                sqlStr = """DELETE FROM cart WHERE id = {}""".format(mysqlId)
                execSql.execSql(sqlStr)
            
            del shop_cart[uid]
            msg = '刪除成功'
        else:
            return

        shop_cart = json.dumps(shop_cart)
        request.response.setCookie('shop_cart', shop_cart, path='/OppToday')
        if action in ['add', 'get'] and msg not in ['商品已在購物車內']:
            data = {
                'abs_url': content.absolute_url(),
                'title': content.title,
                'listPrice': content.listPrice,
                'salePrice': content.salePrice
            }
        elif action == 'del':
            if 'sql_' in uid:
                data = {'price': price}
            else:
                data = {'price': content.salePrice or content.listPrice}
        else:
            data = {}

        return json.dumps({'action': action, 'msg': msg, 'data': data})
