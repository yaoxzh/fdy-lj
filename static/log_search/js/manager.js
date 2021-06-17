var Manager = {

    init: function() {

        this.switch();
    },
    switch: function() {

        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch-small'));
        elems.forEach(function(html) {

            var switchery = new Switchery(html, {
                size: 'small'
            });

        });

    }
};

(function() {
    Manager.init();
})();