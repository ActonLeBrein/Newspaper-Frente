$(document).ready(function(){
	$(".menu_option").click(function() {
		$(".menu_option").removeClass("activate");
		$(this).addClass("activate");
	});
	$('.pagers').click(function() {
		value_page = $(this).attr("id").replace('nextpage','');
		$("input[name=page]").val(value_page);
		$("#main_form").submit();
		return false;
	});
});
