(function() {
    var initPage = function() {
        //保存新增管理员按钮函数
        $('#save').on('click', function() {
            alert('auth');
        });

        //点击新增显示侧边栏
        initMask({
            el: '#add_auth',
            closed: function(element) {
                resetPopup('#add_auth_form');
            }
        });
        //点击修改显示侧边栏
        initMask({
            el: '[data-type="modify"]',
            shown: function() {
                //显示侧边栏之后的回调函数
            },
            closed: function() {
                resetPopup('#add_auth_form');
            }
        });
    };

    initPage();
})();