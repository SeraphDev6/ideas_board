$(document).ready(function(){
    $('#logform').submit(function(e){
        e.preventDefault();
        var data = $("#logform").serialize()
        $.ajax({
            method:'POST',
            url:`/ajax/user/login`,
            data:data,
        }).done(function(results){
            if(results.length>3){
            $('#login_message').html(results)
            }else{
                window.location.replace('/')
            }
        });
    });
});