$( document ).ready(function() {
	// $("label[for='id_entregas_0']").hide();	
 	$("label[for='id_nombreEmpresa']").hide();
	$("#id_nombreEmpresa").hide();
	$("label[for='id_puesto']").hide();
	$("#id_puesto").hide();

	//Change de estudia
	$('#id_entregas').on('change', function(){
		var id = $(this).val();
		console.log("esto es id" + id)
		if (id =="oficina") {
			$("label[for='id_nombreEmpresa']").show();
			$("#id_nombreEmpresa").show();
			$("label[for='id_puesto']").show();
			$("#id_puesto").show();
		}else{
			$("label[for='id_nombreEmpresa']").hide();
			$("#id_nombreEmpresa").hide();
			$("label[for='id_puesto']").hide();
			$("#id_puesto").hide();
		};
	});
});