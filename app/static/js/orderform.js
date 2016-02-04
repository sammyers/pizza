var pizzasize = "half large";

$(document).ready(function (){

	setPrice();

	$("#item-0").click(function(){
		largePizza();
		halfPizza();
	});

	$("#item-1").click(function(){
		largePizza();
		wholePizza();
	});

	$("#item-2").click(function(){
		mediumPizza();
		wholePizza();
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

	$("#location").change(function(){
		setPrice();
	});

	$("#sauce").change(function(){
		setPrice();
	});

});

function wholePizza(){
	$("#left-toppings .section-label").text("Left Toppings");
	$("#right-toppings").show();
	$("#sauce-select").show();
	$("#price").css("right", "5em");
	$(".form-group").css("width", "35em");
	setPrice();
}

function halfPizza(){
	$("#left-toppings .section-label").text("Toppings");
	$("#right-toppings").hide();
	$("#sauce-select").hide();
	$("#price").css("right", "3em");
	$(".form-group").css("width", "24em");
	pizzasize = "half large";
	setPrice();
}

function mediumPizza(){
	$("#topping6").hide();
	$("#topping3").hide();
	pizzasize = "medium";
}

function largePizza(){
	$("#topping6").show();
	$("#topping3").show();
	pizzasize = "large";
}

function setPrice(){
	var price;
	if (pizzasize === "medium"){
		if ($("#sauce").val() === "Tomato"){
			if ($("#location").val() === "Anywhere" || $("#location").val() === "WH"){
				price = MEDIUM_PRICE;
			} else if ($("#location").val() === "EH"){
				price = MEDIUM_PRICE + 0.5;
			} else {
				price = MEDIUM_PRICE + 1.0;
			}
		} else {
			if ($("#location").val() === "Anywhere" || $("#location").val() === "WH"){
				price = MEDIUM_PRICE + 2.0;
			} else if ($("#location").val() === "EH"){
				price = MEDIUM_PRICE + 2.5;
			} else {
				price = MEDIUM_PRICE + 3.0;
			}
		}
	} else if (pizzasize === "large"){
		if ($("#sauce").val() === "Tomato"){
			if ($("#location").val() === "Anywhere" || $("#location").val() === "WH"){
				price = LARGE_PRICE;
			} else if ($("#location").val() === "EH"){
				price = LARGE_PRICE + 0.5;
			} else {
				price = LARGE_PRICE + 1.0;
			}
		} else {
			if ($("#location").val() === "Anywhere" || $("#location").val() === "WH"){
				price = LARGE_PRICE + 2.0;
			} else if ($("#location").val() === "EH"){
				price = LARGE_PRICE + 2.5;
			} else {
				price = LARGE_PRICE + 3.0;
			}
		}
	} else {
		if ($("#location").val() === "Anywhere" || $("#location").val() === "WH"){
			price = LARGE_PRICE / 2;
		} else if ($("#location").val() === "EH"){
			price = LARGE_PRICE / 2 + 0.5;
		} else {
			price = LARGE_PRICE / 2 + 1.0;
		}
	}
	$("#price-total").text("$" + price.toFixed(2));
	$("#price").val(price);
}
