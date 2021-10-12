var validators = {'title':false,'description':false,'explanation':false}
$(document).ready(function(){
    $('#submit').prop('disabled',true);
    Object.keys(validators).forEach(validator => {
        $(`#${validator}`).keyup(function(){checkValid(validator)});
    });
    $('#yes,#no').click(function(){
        var data = $("#ideaform").serialize()
        $.ajax({
            method:'POST',
            url:'/ajax/idea/include_user',
            data:data
        })
        .done(function(results){
            $('#secondary').html(results);
        });
    });
});

function checkValid(id){
    var data = $("#ideaform").serialize()
    console.log(data)
    $.ajax({
            method:'POST',
            url:`/ajax/idea/${id}`,
            data:data
    })
    .done(function(results){
        if(results.length < 3){
            $(`#${id}`).removeClass('is-invalid');
            validators[id]=true;
        }
        else{
            $(`#${id}`).addClass('is-invalid');
            validators[id]=false;
        }
        $(`#${id}_message`).html(results);
        if(Object.values(validators).every(validator => validator === true)){
            $('#submit').prop('disabled',false);
        }else{
            $('#submit').prop('disabled',true);
        }
    });
}