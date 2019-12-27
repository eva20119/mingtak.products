# -*- coding: utf-8 -*-
#TODO: 整批彙入
"""Module where all interfaces, events and exceptions live."""

from mingtak.products import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective import dexteritytextindexer

from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.textfield import RichText
# from plone.formwidget.contenttree import ObjPathSourceBinder
from datetime import datetime
from plone import api
from plone.autoform import directives
from plone.supermodel.directives import fieldset

class IMingtakProductsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# 紅利點數發放比率，預設為1%(0.01)，基於防笨最高設定不得超過5%(0.05)
MIN_BONUS_RATE = 0.0
MAX_BONUS_RATE = 0.05
DEFAULT_BONUS_RATE = 0.0

# 使用紅利點數可折抵折扣率，以小數點表示百分比, 最小不打折，最多85折(15% off), 預設95折(5% off)
MIN_USED_BONUS_RATE = 0.0
MAX_USED_BONUS_RATE = 0.15
DEFAULT_USED_BONUS_RATE = 0.05


class IProduct(Interface):

    """ 產品 """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Product Name"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    productUrl = schema.URI(
        title=_(u"Pruduct URL"),
        description=_(u"Product introduction web page include http:// or https://"),
        required=False,
    )

    inStock = schema.Bool(
        title=_(u"In Stock?"),
        description=_(u"If In Stock, Please check it."),
        default=True,
        required=False,
    )

    brand = schema.TextLine(
        title=_(u"Brand"),
        description=_(u"Brand name."),
        required=False,
    )

    listPrice = schema.Int(
        title=_(u"List Price"),
        description=_(u"The list price of the product."),
        required=True,
    )

    salePrice = schema.Int(
        title=_(u"Sale price"),
        description=_(u"Sale price for the product if different from the list price, must be <= listPrice."),
        required=True,
    )

    fieldset('images',
            label=u"Product Images",
            fields=['image_1', 'image_2', 'image_3', 'image_4', 'image_5']
        )

    image_1 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image for header."),
        required=True,
    )

    image_2 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_4 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_5 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )


    fieldset('extraInfo',
            label=u"Extra Info",
            fields=['bonusPoint', 'maxUsedBonus', 'promotionalText', 'heroText', 'standardShippingCost', 'lastUpdated']
        )
    # 紅利點數發放比率，以小數點表示百分比
    bonusPoint = schema.Float(
        title=_(u"Bonus Point"),
        description=_(u"Bonus point setting, please filling decimal point. maximum is 0.05 (5%)"),
        default=DEFAULT_BONUS_RATE,
        min=MIN_BONUS_RATE,
        max=MAX_BONUS_RATE,
        required=True,
    )

    # 今日折扣，使用紅利點數可折抵折扣率，以小數點表示百分比
    maxUsedBonus = schema.Float(
        title=_(u"Maximum Used Bonus Points"),
        description=_(u"You can use a maximum bonus points."),
        default=DEFAULT_USED_BONUS_RATE,
        min=MIN_USED_BONUS_RATE,
        max=MAX_USED_BONUS_RATE,
        required=True,
    )

    dexteritytextindexer.searchable('promotionalText')
    promotionalText = RichText(
        title=_(u"Promotional Text"),
        description=_(u"Promotional Text, support html format richtext."),
        required=False,
    )

    # 產品要放在首頁推廣，則本欄必填, 該用 ReviewPortalContent? or ManagePortal? 再考量
    directives.write_permission(heroText='cmf.ReviewPortalContent')
    heroText = schema.Text(
        title=_(u"Hero Text"),
        description=_(u"Promotional Text for Hero page"),
        required=False,
    )

    # 運費，以單品計算, 若一張訂單有多樣商品，須依規則另計
    standardShippingCost = schema.Int(
        title=_(u"Standard shipping cost"),
        description=_(u"Usually is the cost for the typical standard, lowest cost shipping method. This is provided for informational purposes and the actual shipping cost could vary depending on the visitor."),
        required=False,
    )

    lastUpdated = schema.Datetime(
        title=_(u"Last Updated"),
        description=_(u"Date of the most recent update to the product."),
        default=datetime.now(),
        required=True,
    )
