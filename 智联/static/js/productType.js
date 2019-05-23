$('#editProductType').click(function () {
    layer.open({
        type: 1,
        skin: 'layui-layer-rim', //加上边框
        title: '编辑商品类型',
        btn: ['确认修改', '取消'],
        yes: function(index, layero){
            var type = $(".layui-layer-content").find("input").val();
            // var url = window.location.href;
            // var id = url.split('/')[4].toString();
            $.ajax({
                type: "POST",
                url: "/ChangeTypeName/",
                data:{"oldtype":typename,'newtype':type },
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                error: function (request) {
                    layer.msg('修改失败!',{icon:6,time:2000});
                },
                success: function (data) {
                    if(data == 'ok')
                    {
                        layer.msg('修改成功!',{icon:6,time:2000});
                        setTimeout("window.location.reload()", 2500);
                        
                    }
                    else{
                        layer.msg(data,{icon:6,time:2000});
                        setTimeout("window.location.reload()", 2500);
                    }
                                                
                }
            });
        },
        area: ['420px', '190px'], //宽高
        content: $('#editProductTypeContainer').html()
    });
});

$('#addProduct').click(function () {
    layer.open({
        type: 1,
        skin: 'layui-layer-rim', //加上边框
        title: '添加商品',
        btn: ['添加', '取消'],
        yes: function(index, layero){
            var productURL = $(".layui-layer-content").find("input").val();
            now_type = typename;
            // alert(productURL);
            // return;
            $.ajax({
                type: "POST",
                url: "/addurl/",
                data:{"url":productURL, 'productType':now_type},
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                error: function (request) {
                    layer.msg('添加失败!',{icon:6,time:2000});
                },
                success: function (data) {
                    if(data == 'ok')
                    {
                        layer.msg('添加成功!立即进行数据更新...',{icon:6,time:2000});
                        setTimeout(function(){
                            window.location.href= window.location.href;
                        }, 2500);                        
                    }
                    else{
                        layer.msg('添加失败!'+data,{icon:6,time:2000});
                    }
                                                
                }
            });
        },
        area: ['420px', '190px'], //宽高
        content: $('#addProductsContainer').html()
    });
});

$('#backHomePage').click(function(){
    window.location.href = '/';
})

function delProduct(productId){
    $.ajax({
        type: "POST",
        url: '/delProduct/',
        data:{"productId":productId},
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (request) {
            layer.msg('删除失败!',{icon:6,time:1500});
        },
        success: function (data) {
            if(data == 'ok')
            {
                layer.msg('删除成功!',{icon:6,time:2000});
                setTimeout("window.location.reload()", 1500);
                
            }
            else{
                layer.msg("删除失败",{icon:6,time:2000});
                setTimeout("window.location.reload()", 1500);
            }
                                        
        }
    });
}

