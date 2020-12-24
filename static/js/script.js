

alert("sdad");


setTimeout(function () {
    alert("sdad");
    $('.form-input').click();

}, 1800);

$('.form-input').click(function (){


        alert("sdad");
        let $placeholder = $(this).next();

        if ($('.form-input').val().length > 0){

            $placeholder.addClass('active');
        }
        else

            $placeholder.removeClass('active');

});

if( $('.form-input').val() != '' ){
    let $placeholder = $(this).next();

    if ($('.form-input').val().length > 0)
        $placeholder.addClass('active');
    else
        $placeholder.removeClass('active');
}

$('.form-input').change(function (){
    let $placeholder = $(this).next();

    if ($('.form-input').val().length > 0)
        $placeholder.addClass('active');
    else
        $placeholder.removeClass('active');
});

