$(document).ready(function(){

	$(document).on('click', '#create_profile', function(e) {
		$('#create_profile_form').show();
		$('#create_profile').hide();
	});

	$(document).on('click', '#close_profile_form', function(e) {
		$('#create_team').show();
		$('#create_team_form').hide();
	});

	$('#create_shop_form').hide();
	$(document).on('click', '#create_shop', function(e) {
		$('#create_shop_form').show();
		$('#create_shop').hide();
	});

	$(document).on('click', '#close_shop_form', function(e) {
		$('#create_shop').show();
		$('#create_shop_form').hide();
	});

  $('#birth-date').mask('00/00/0000');
  $('#phone-number').mask('0000-0000');
 })
