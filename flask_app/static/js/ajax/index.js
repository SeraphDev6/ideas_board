$(document).ready(function(){
    $(".join").click(function(){
        $(this).parent().html(`<input type="text" name="message" id="message${$(this).attr("idea")}${$(this).attr("user")}" class="form-control my-1" placeholder="Enter a message for the team"> <button class="btn btn-sm btn-primary add_request" idea="${$(this).attr("idea")}" user="${$(this).attr("user")}">Submit Request</button>`);
        $(".add_request").click(function(){
            target=$(this).parent();
            message_obj=$(`#message${$(this).attr("idea")}${$(this).attr("user")}`);
            data = `message=${message_obj.val()}&idea_id=${$(this).attr("idea")}&user_id=${$(this).attr("user")}`;
            $.ajax({
                method:'POST',
                url:'/ajax/users/add_request',
                data:data,
            }).done(function(result){
                target.html(result);
            });
        })
    })
});