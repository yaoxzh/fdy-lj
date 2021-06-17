submit = {

    init: function() {

        this.makeList();
    },

    makeList: function() {
        //增加线路
        $('#add_route').on('click', function() {
            var route_tpl = '<div class="line-box">' +
                '<div class="division-box">' +
                '<div class="division-title">新增线路 ' + ($(".line-box").length + 1) + '</div>' +
                '</div>' +
                '<a href="javascript:;" title="删除" class="line-delete-btn" data-type="delete-route">' +
                '<i class="fa fa-remove"></i>' +
                '</a>' +
                '<div class="container-fluid">' +
                '<div class="row">' +
                '<div style="width:45%;float:left;">' +
                '<div class="bk-form-item">' +
                '<label class="bk-label" style="width:225px;">初试官(RTX)</label>' +
                '<div class="bk-form-content" style="margin-left:225px;">' +
                '<input type="text" class="bk-form-input"  data-type="bkMemberSelector">' +
                '</div>' +
                '<div class="bk-form-tip" style="z-index:99;">' +
                '<div class="bk-badge bk-default" data-type="first-round-tips">' +
                '<i class="fa fa-question"></i>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="bk-form-item">' +
                '<label class="bk-label" style="width:225px;">线路</label>' +
                '<div class="bk-form-content" style="margin-left:225px;">' +
                '<select name="" id="" class="bk-form-select">' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '</select>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div style="width:45%;float:left;">' +
                '<div class="bk-form-item">' +
                '<label class="bk-label" style="width:225px;">复试官(RTX)</label>' +
                '<div class="bk-form-content" style="margin-left:225px;">' +
                '<input type="text" class="bk-form-input"  data-type="bkMemberSelector">' +
                '</div>' +
                '<div class="bk-form-tip">' +
                '<div class="bk-badge bk-default" data-type="second-round-tips">' +
                '<i class="fa fa-question"></i>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="bk-form-item">' +
                '<label class="bk-label" style="width:225px;">线路招聘需求</label>' +
                '<div class="bk-form-content" style="margin-left:225px;">' +
                '<select name="" id="" class="bk-form-select">' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '<option value="">请选择</option>' +
                '</select>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="row">' +
                '<div style="width:90%;float:left;">' +
                '<div class="bk-form-content mb20" style="margin-left:225px;">' +
                '<div class="bk-intro bk-default">' +
                '<p class="bk-intro-text">当前线路投递简历总数：<strong>28</strong>，后台开发全公司已申报offer总数：<strong>8</strong>，简历offer数占比：<strong>28/8=3.5；</strong></p>' +
                '<p class="bk-intro-text">参加笔试人数：<strong>20</strong>，优生（前40%）总人数：<strong>15</strong>，优生率：<strong>15/20=75%</strong>，优生简历offer数占比：<strong>15/8=1.88</strong></p>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';

            $('.line-box').last().after(route_tpl);

            //初始化人员选择插件
            var latest_last = $('.line-box').last();

            latest_last.find('[data-type="bkMemberSelector"]').bkMemberSelector({
                maxData: 1
            });

            latest_last.find('[data-type="first-round-tips"]').tooltip({
                title: '初试官tips',
                container: 'body'
            });

            latest_last.find('[data-type="second-round-tips"]').tooltip({
                title: '复试官tips',
                container: 'body'
            });
        });

        //删除线路
        $(document).on('click', '[data-type="delete-route"]', function() {
            var $this = $(this);

            $this.off('click');
            $this.parents('.line-box').remove();
        });

        //显示历史弹窗
        initMask({
            el: '#history',
            shown: function() {

            },
            closed: function() {

            }
        });

        //关闭历史弹窗
        $(document).on('click', '#hide_mask', function() {
            $('#bk_mask').hide();
        });

        //计算线路招聘需求
        $('[data-type="count"]').on('input', function() {
            var $this = $(this),
                val = $this.val(),
                target_amount = $('#target_amount').val(),
                intern_amount = $('#intern_amount').val(),
                advanced_amount = $('#advanced_amount').val(),
                demand_amount = 0;

            if (target_amount.match(/^[0-9]*$/) && intern_amount.match(/^[0-9]*$/) && advanced_amount.match(/^[0-9]*$/)) {
                demand_amount = target_amount - intern_amount - advanced_amount;

                if (demand_amount >= 0) {
                    $('#route_demand').val(demand_amount);
                } else {
                    alert('线路招聘需求应为正数');
                    $this.val('');
                }
            } else {
                alert($this.parent().prev().html() + "应为纯数字");
                $this.val('');
                $('#route_demand').val($('#target_amount').val() - $('#intern_amount').val() - $('#advanced_amount').val());
            }
        });

        //保存草稿
        $('#save').on('click', function() {
            //获取初试官or复试官的rtx时，只需要找到对应有标签data-type="bkMemberSelector"的input框，获取其value即可
        });

        //提交
        $('#submit').on('click', function() {
            //获取初试官or复试官的rtx时，只需要找到对应有标签data-type="bkMemberSelector"的input框，获取其value即可
        });

        //取消
        $('#cancel').on('click', function() {

        });

        $('#advanced_tips').tooltip({
            title: '提前录用offer人数tips',
            container: 'body'
        });

        $('[data-type="first-round-tips"]').tooltip({
            title: '初试官tips',
            container: 'body'
        });

        $('[data-type="second-round-tips"]').tooltip({
            title: '复试官tips',
            container: 'body'
        });

        //初始化人员选择插件
        $('[data-type="bkMemberSelector"]').bkMemberSelector({
            maxData: 1
        });
    }
};

(function() {
    submit.init();
})();