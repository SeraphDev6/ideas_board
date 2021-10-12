var defaultUN;
$(document).ready(function(){
    defaultUN = $('#username').val();
    $(`#username`).keyup(function(){checkValid('username')});
});
function checkValid(id){
    var data = $("#updform").serialize()
    $.ajax({
            method:'POST',
            url:`/ajax/user/${id}`,
            data:data
    })
    .done(function(results){
        $(`#${id}_message`).html(results);
        if(results.length < 3){
            $(`#${id}`).removeClass('is-invalid');
        }
        else{
            $(`#${id}`).addClass('is-invalid');
            if(defaultUN===$(`#${id}`).val()){
                console.log($(`#${id}`).val())
                $(`#${id}`).removeClass('is-invalid');
                $(`#${id}_message`).html("");
            }
        }
    });
}