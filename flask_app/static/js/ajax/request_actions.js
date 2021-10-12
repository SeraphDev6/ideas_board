$(document).ready(function(){
    $(".approve").click(function(){
        data = `idea_id=${$(this).attr("team")}&user_id=${$(this).attr("user")}&approved=1`;
        target=$(this).parent().parent()
        $.ajax({
            method:'POST',
            url:'/ajax/users/manage_request',
            data:data,
        }).done(function(results){
            target.html(results);
            refresh_team(data)
        });
    });
    $(".deny").click(function(){
        data = `idea_id=${$(this).attr("team")}&user_id=${$(this).attr("user")}&approved=0`;
        target=$(this).parent().parent()
        $.ajax({
            method:'POST',
            url:'/ajax/users/manage_request',
            data:data,
        }).done(function(results){
            target.html(results);
        });
    });
});
function refresh_team(data){
    $.ajax({
        method:'POST',
            url:'/ajax/users/update_team',
            data:data,
    }).done(function(results){
        $("#team_members").html(results);
    });
}