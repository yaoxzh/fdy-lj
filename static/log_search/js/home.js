(function() {
    var init = function() {
        $('#all').on('click', function() {
            var $this = $(this),
                status = $this.attr('data-all'),
                type = '',
                text = '',
                next = '';

            $('[data-toggle="collapse"]').each(function(index, item) {
                if (status == 'expand') {
                    type = 'show';
                    text = '全部收起';
                    next = 'collapse';
                } else {
                    type = 'hide';
                    text = '全部展开';
                    next = 'expand';
                }

                $($(this).attr('href')).collapse(type);
            });

            $this.text(text).attr('data-all', next);
        });
    }

    init();
})();