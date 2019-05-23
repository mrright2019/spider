

$('#addProduct').click(function () {
    layer.open({
        type: 1,
        skin: 'layui-layer-rim', //加上边框
        title: '新建爬虫',
        btn: ['确认', '取消'],
        yes: function(index, layero){
            var state = $(".layui-layer-content #addState").val();
            var industry = $(".layui-layer-content #addIndustry").val();
            // alert(state+industry);
            $.ajax({
                type: "POST",
                url: '/createspider/',
                data:{"state":state,'industry':industry},
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
                            window.location.href= "/";
                        }, 2500);                        
                    }
                    else{
                        layer.msg('添加失败!'+data,{icon:6,time:2000});
                    }
                                                
                }
            });
        },
        area: ['420px', '190px'], //宽高
        content: $('#addProductContainer').html()
    });
});

