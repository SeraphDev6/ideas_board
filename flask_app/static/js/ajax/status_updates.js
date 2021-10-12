$(document).ready(function(){
    $('#update').keyup(function(){
        var data = `update=${$("#update").val()}`;
        $.ajax({
            method:'POST',
            url:'/ajax/idea/check_update',
            data:data,
        }).done(function(result){
            $("#update_message").html(result);
        });
    });
    $('#add_update').click(function(){
        if($("#update").val().length >= 3){
            var data = `update=${$("#update").val()}&idea_id=${$(this).attr("idea")}`;
            $.ajax({
                method:'POST',
                url:'/ajax/idea/add_update',
                data:data,
            }).done(function(result){
                $("#update_div").html(result);
                $("#update").val("")
            });
        }
    })
});