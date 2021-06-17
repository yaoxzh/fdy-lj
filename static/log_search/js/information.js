var Information = {

    init: function() {
        this.getFile();
        this.timePicker();
        this.newDate();
    },

    //上传文件
    getFile: function() {
        var bkFileSelector = $('#fileSelector').bkFileSelector({
            accept: ['xls'],
            maxSize: 200
        });
    },

    //启动时间
    timePicker: function() {
        $('.daterangepicker_one').daterangepicker({
            locale: {
                "format": 'YYYY.MM.DD'
            },
            autoApply: true
        });

    },

    //新建启动时间
    newDate: function() {
        var num = 1;


        $('#timeRange-container').on('click', '#add', function() {
            num++;
            var $timerange = $("<div class='bk-form-item'><label class='bk-label' style='width:225px;'>启用时间<span class='num'>" + num + "</span></label><div class='bk-form-content' style='margin-left:225px;position: relative;'><input type='text' class='bk-form-input daterangepicker_one' placeholder='选择日期...'><div class='timePicker-icon' ><i class='fa fa-calculator'></i></div></div><a class='bk-icon-button bk-danger bk-button-mini' title='删除' id='remove'><i class='fa fa-close bk-icon'></i></a><a class='bk-icon-button bk-success bk-button-mini plus-btn' title='添加' id = 'add'><i class='fa fa-plus bk-icon'></i></a></div></div>");
            $('#timeRange-container').append($timerange);
            var timePicker = $('#timeRange-container').find('.daterangepicker_one:last');
            timePicker.daterangepicker({
                locale: {
                    "format": 'YYYY.MM.DD'
                },
                autoApply: true
            });
        });

        $('#timeRange-container').on('click', '#remove', function() {
            $(this).parent().remove();
            --num;
        });
    }

};

(function() {
    Information.init();
})();