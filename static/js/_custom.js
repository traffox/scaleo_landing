



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





document.addEventListener("DOMContentLoaded", function () {

	let inputRepass = $('[name=repassword]').parent();
	let inputSocial = $('[name=telegram]').parent();

	$('.auth__choice-item').on('click.smoothscroll', function () {
		$('.auth__choice-item').not($(this)).removeClass('auth__choice-item_active');
		$(this).addClass('auth__choice-item_active');
	});

	let $authChoiceThumb = $('.auth__choice-thumb');

	let $authChoiceItemActiveWidth = $('.auth__choice-item_active').width(),
		$loginWidth = $('#login-btn').width();

	$registerWidth = $('#register-btn').width();

	$authChoiceThumb.css({
		'transform': `translateX(${$loginWidth + 1}px)`,
		'width': `${$registerWidth}px`
	});

	$(window).on("hashchange", function (e) {

		if (location.hash.slice(1) == "register") {
			inputsValueReset($('.auth__form-main').find('input'));
			$('.auth__form-main').append(inputRepass);
			$('.auth__form-main').append(inputSocial);
			// inputSocial
			$('.auth__form-title').html('Регистрация');
			$('.auth__form-button').html('Зарегистрироваться');
			$('.auth__forgot-password').fadeOut(0);

			$authChoiceThumb.css('width', `${$authChoiceItemActiveWidth}px`);
			$('#register-btn').addClass('auth__choice-item_active');
			$('#login-btn').removeClass('auth__choice-item_active');


			$authChoiceThumb.css('transform', `translateX(${$loginWidth + 1}px)`);
			e.preventDefault();
		}

		if (location.hash.slice(1) == "login") {
			inputsValueReset($('.auth__form-main').find('input'));
			hiddenInputs();
			$('.auth__form-title').html('Войти');
			$('.auth__form-button').html('Войти');
			$('.auth__forgot-password').fadeIn(0);
			

			$('#login-btn').addClass('auth__choice-item_active');
			$('#register-btn').removeClass('auth__choice-item_active');

			$authChoiceThumb.css({
				'transform': 'translateX(0px)',
				'width': `${$loginWidth}px`
			});

		}

	});

	$(window).trigger("hashchange");



	if( $('.form-input').val() != '' ){
		let $placeholder = $(this).next();

		if ($(this).val().length > 0)
			$placeholder.addClass('active');
		else
			$placeholder.removeClass('active');
	}

	$('.form-input').on('input', function () {
		let $placeholder = $(this).next();

		if ($(this).val().length > 0)
			$placeholder.addClass('active');
		else
			$placeholder.removeClass('active');
	});

	$(".modal").each(function () {
		$(this).hasClass("modal_forgot") && $(this).iziModal({
			width: 360,
			radius: 15,
			transitionIn: "fadeInDown",
			bodyOverflow: !0,
			overlayColor: 'rgba(0, 0, 0, 0.8)',
			onOpening: function () {
				$('.modal__close').removeClass('modal__close_hidden');
			}
		});
		$(this).hasClass("modal_political") && $(this).iziModal({
			width: 800,
			radius: 15,
			transitionIn: "fadeInDown",
			bodyOverflow: !0,
			overlayColor: 'rgba(0, 0, 0, 0.8)',
			onOpening: function () {
				$('.modal__close').removeClass('modal__close_hidden');
			}
		});
	});
	

	function inputsValueReset(input) {
		input.each(function() {
			$(this).val('');
			$(this).next().removeClass('active');
		});
	}

	function hiddenInputs() {
		inputRepass.detach();
		inputSocial.detach();
	}

});