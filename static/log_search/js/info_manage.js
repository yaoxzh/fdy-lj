(function() {
    var initPage = function() {
        $('#close').on('click', function() {
            $('#bk_mask').trigger('click');
        });
    };

    initPage();
})();