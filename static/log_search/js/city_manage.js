(function() {
    var initPage = function() {
        //保存新城市按钮函数
        $('#save').on('click', function() {
            alert('city');
        });

        initMask({
            el: '#add_city',
            shown: function() {

            },
            closed: function() {
                resetPopup('#add_city_form');
            }
        });
    };

    initPage();
})();