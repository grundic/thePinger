    hash=0

    function waitForData(){
        //hash=13
        console.log(hash)
        jQuery.ajax({
            type:"GET",
            url:"/ping",
            timeout:20000,
            data:'hash='+hash,
            success: function(data){
                if (null == data){
                    jQuery("#output").html("<span class=ConnErr>Data not avaliable!</span>");
                    return
                }
                htmlString = ''
                $.each(data[2], function(key, value){
                    (value.reply > 0) ? htmlString +='<span class=online>' + value.host + '</span><br>' : htmlString +='<span class=offline>' + value.host + '</span><br>' 
                })
                htmlString += '<span class="pingtime">' + data[0] + '</span>'
                htmlString += '<br>'
                htmlString += '<span class="md5">' + data[1] + '</span>'
                hash=data[1]
                jQuery("#output").html(htmlString);
                //jQuery("#output").html(data[0].pingtime);
                setTimeout('waitForData()', 1000)
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                console.log("error:" + textStatus + ", " + errorThrown);
                setTimeout('waitForData()', 2000)
            },
        });
    }



    jQuery('document').ready( function(){ 
        //periodicalUpdate()
        //var holdtheInterval = setInterval(periodicalUpdate, 15000);
        waitForData()
    });
