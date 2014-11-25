/**
 * Created by pdiazv on 11/9/14.
 */

(function(){

    $('body').on('click', '.js-addride', function(){

        var sid = $('[name="csrfmiddlewaretoken"]').val();

        var source = {
                name: 'test1',
                description: 'My required descr',
                date: '11/25/2014',
                start_coord: '5.234, 12.5234',
                distance: 60,
                difficulty: 6
        };

        $.ajax({
            url: '/api/ride/add',
            dataType: 'json',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: sid, 
                sourceStr: JSON.stringify(source)
            },
            success: function(d,s,e){
                console.log('Ajax result status: ' + s);
            }
        })

    });


}())
