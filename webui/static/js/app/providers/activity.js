
define(['jquery'], function($){

    function DataProvider(){ };

    DataProvider.prototype = {
        requestData: function(){
            var self = this;
            $.get('/stats_data', function(result){
                self.donecallback(result)
            });
            return this;
        },

        done: function(callback){
            this.donecallback = callback;
        }
    };

    return DataProvider;
});
