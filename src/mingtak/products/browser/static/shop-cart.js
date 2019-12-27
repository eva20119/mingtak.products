$(function() {
    $('#shop-cart-icon').hover(function(){
        $('#shop-cart').toggle('slow')
    })
    $('.add_to_cart').click(function() {
        shop_cart = $.cookie('shop-cart')
        if(shop_cart){
            shop_cart = JSON.parse(shop_cart)
        }else{
            shop_cart = []
        }
        

    })
})