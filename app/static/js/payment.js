function make_payment(venmo_access_token) {
	$.ajax({
		type: "POST",
		url: "/make_payment",
		data: JSON.stringify({
			access_token:venmo_access_token
		}),
		contentType: "application/json",
		dataType: "json"
	}).done(function(response) {
		$(".homepage-button").hide();
		$(".payment-complete").show();
	}).fail(function() {
		$(".homepage-button").text("Server Error");
	});
}