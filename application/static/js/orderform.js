$(document).ready(function () {
	$("#item-0").click(function(){
		halfPizza();
		largePizza();
	});

	$("#item-1").click(function(){
		wholePizza();
		largePizza();
	});

	$("#item-2").click(function(){
		wholePizza();
		mediumPizza();
	});

	$("#topping1").change(function(){
		$("#topping4").val(
			$('#topping1 option:selected').val()
		);
	});

	$("#topping2").change(function(){
		$("#topping5").val(
			$('#topping2 option:selected').val()
		);
	});

	$("#topping3").change(function(){
		$("#topping6").val(
			$('#topping3 option:selected').val()
		);
	});

});

function wholePizza() {
	$("#left-toppings .section-label").text("Left Toppings");
	$("#right-toppings").show();
	$(".form-group").css("width", "35em");
}

function halfPizza() {
	$("#left-toppings .section-label").text("Toppings");
	$("#right-toppings").hide();
	$(".form-group").css("width", "24em");
}

function mediumPizza() {
	$("#topping6").hide();
	$("#topping3").hide();
}

function largePizza() {
	$("#topping6").show();
	$("#topping3").show();
}
