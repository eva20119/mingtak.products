$(function() {
    offset = $('#shop-cart-icon').offset()
    $('#shop-cart').css('top', offset['top'] + 40)
    $('#shop-cart').css('left', offset['left'] - 120)

    $('.delete_product').click(function(){
        uid = $(this).data()['uid']
        $.ajax({
            type: "post",
            url: location.href  + "/cart_update",
            data: {uid: uid, action: 'del'},
            success: function (rep) {
                rep = JSON.parse(rep)
                alert(rep['msg'])
            }
        })
    })
    $('#shop-cart-icon').click(function(){
        $('#shop-cart').toggle('slow')
    })
    $('.add_to_cart').click(function() {
        uid = $(this).data()['uid']
        $.ajax({
            type: "post",
            url: location.href  + "/cart_update",
            data: {uid: uid, action: 'add'},
            success: function (rep) {
                try {
                    rep = JSON.parse(rep)
                    msg = rep['msg']
                    data = rep['data']
                    salePrice = data['salePrice']
                    listPrice = data['listPrice']
                    abs_url = data['abs_url']
                    cart_money = parseInt($('#cart_money').text())

                    if(msg){
                        $('#global_statusmessage').html('')
                        correct = ['新增成功', '刪除成功']
                        type = correct.includes(msg)?'info':'error'
                        html = `<div class="portalMessage ${type}">
                                    <strong></strong>
                                    ${msg}
                                </div>`
                        $('#global_statusmessage').append(html)
                    }

                    if(abs_url){
                        html = `
                        <div class="single-cart">
                            <div class="cart-img">
                                <a href="${abs_url}">
                                    <img src="${abs_url}/@@images/image_1/thumb">
                                </a>
                            </div>
                            <div class="cart-info">
                                <h5>
                                    <a href="${abs_url}">${data['title']}</a>
                                </h5>
                        `
                        if(salePrice){
                            html += `
                                <span class='discount_price'>NT${salePrice}</span>
                                <del>${listPrice}</del>
                            </div>
                            `
                            cart_money += parseInt(salePrice)
                        }else{
                            html += ` <span>NT${listPrice}</span></div>`
                            cart_money += parseInt(listPrice)
                        }
                        
                        $('#product_area').append(html)
                        $('#cart_money').text(cart_money)
                    }
                } catch{
                        
                }
            }
        });
    })
})