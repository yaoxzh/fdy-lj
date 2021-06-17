/** !
 *	全局通用js
 *	Created @ 2017/2/28 by blueking
 */

(function() {
    var initMask = function(options) {
        var opts = options || {},
            trigger = opts.el ? $(opts.el) : $(document),
            shown = opts.shown ? opts.shown : function() {},
            closed = opts.closed ? opts.closed : function() {}
        mask = $('#bk_mask'),
            bk_mask_content = mask.children('#bk_mask_content');

        //显示侧边栏
        trigger.on('click', function() {
            mask.show();
            setTimeout(function() {
                bk_mask_content.css('right', 0);
                shown && shown(mask);
            }, 10);
        });

        //遮罩绑定事件
        mask.on('click', function(event) {
            var target = event.target,
                $this = $(this);

            if ($(target).attr('id') == 'bk_mask') {
                bk_mask_content.removeAttr('style');
                setTimeout(function() {
                    $this.hide();
                    closed && closed(mask);
                }, 200);

            }
        });
    }

    //重置侧边栏
    var resetPopup = function(el) {
        var form = $(el);

        form.find('input').val('');
        form.find('select option').removeAttr('selected');
    }

    window.initMask = initMask;
    window.resetPopup = resetPopup;
})();