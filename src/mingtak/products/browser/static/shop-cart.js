$(function() {
    offset = $('#shop-cart-icon').offset()
    $('#shop-cart').css('top', offset['top'] + 40)
    $('#shop-cart').css('left', offset['left'] - 120)

    $(document).on('click', '#shop-cart .delete_product', function(){
        uid = $(this).data()['uid']
        _self = $(this)
        $.ajax({
            type: "post",
            url: location.href  + "/cart_update",
            data: {uid: uid, action: 'del'},
            success: function (rep) {
                rep = JSON.parse(rep)
                msg = rep['msg']
                price = rep['data']['price']
                number = rep['number']
                if(msg == '刪除成功'){
                    _self.parents('.single-cart').remove()
                    cart_money = $('#cart_money').text()
                    $('#cart_money').text(parseInt(cart_money) - (price * number))
                }
                alert(msg)
            }
        })
    })
    $('#shop-cart-icon').click(function(){
        $('#shop-cart').toggle('slow')
    })
    $('.add_to_cart').click(function() {
        uid = $(this).data()['uid']
        number = $('#number').val()
        $.ajax({
            type: "post",
            url: location.href  + "/cart_update",
            data: {uid: uid, action: 'add', number: number},
            success: function (rep) {
                try {
                    rep = JSON.parse(rep)
                    msg = rep['msg']
                    data = rep['data']
                    number = rep['number']
                    salePrice = data['salePrice']
                    listPrice = data['listPrice']
                    abs_url = data['abs_url']
                    uid = data['uid']
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
                            `
                            cart_money += parseInt(salePrice * number)
                        }else{
                            html += ` <span>NT${listPrice}</span>`
                            cart_money += parseInt(listPrice * number)
                        }
                        html += `
                                <span class='cart_number'>X ${number}</span>
                            </div>
                            <img src="${abs_url}/++resource++mingtak.products/trash.png" 
                                class="delete_product" data-uid='${uid}'
                            >
                        `

                        $('#product_area').append(html)
                        $('#cart_money').text(cart_money)
                    }
                } catch{
                    alert('添加失敗, 請在試一次')
                }
            }
        });
    })
})