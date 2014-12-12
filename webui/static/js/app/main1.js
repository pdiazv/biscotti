define(function (require) {
    var $ = require('jquery'),
        Demo = require('./demo')
        $elt = $('.js-stats');

    new Demo($elt).run();
});
