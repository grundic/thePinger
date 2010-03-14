$(document).ready( function(){
    if(!window.console) window.console = {};
    if(!window.console.log) window.console.log = function(){};

    hash=0

    updater.poll();
});


var updater = {
    
    poll: function(){
        var args = {"hash": hash};
        $.ajax({
            url: "/ping", 
            type: "POST", 
		    data: $.param(args), 
            datatype: "json",
            success: updater.onSuccess,
		    error: updater.onError
        });
    },

    onSuccess: function(response){
        try{
            updater.parseRsponse(response)
        } catch(e){
            updater.onError();
            return;
        }
    },

    dotIterator:0,
    onError: function(response){
        if (updater.dotIterator < 10){            
            htmlStr = 'Initializing.'
            dots = Array(updater.dotIterator+1).join('.')
            htmlStr += dots
            $('.PingList').html(htmlStr)
            updater.dotIterator += 1
        } else{
            htmlStr = 'Initializing'
            $('.PingList').html(htmlStr)
            updater.dotIterator = 0
        }
        console.log("Ping error; sleeping for 1 second");
        window.setTimeout(updater.poll, 1000);
    },

    parseRsponse: function(response){
        hash=response[1]
        $('.PingList').text('')
        $.each(response[2], function(i, item){
            item.reply > 0 ? isOnline ='online' : isOnline ='offline'
            $('.PingList').append('<span class=' + isOnline + '>' + item.host + "</span><br>")
        });

        $('.PingList').append('<span class=pingtime>' + response[0] + "</span><br>")
        window.setTimeout(updater.poll, 0)
    },
};
