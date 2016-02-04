$(document).ready(function(){
	startClock(DEADLINE);
});

function getTimeRemaining(endtime){
	var time = Date.parse(endtime) - Date.parse(new Date());
	var seconds = Math.floor( (time/1000) % 60 );
	var minutes = Math.floor( (time/(1000*60)) % 60 );
	var hours = Math.floor( (time/(1000*60*60)) );
	return {
		'total': time,
		'hours': hours,
		'minutes': minutes,
		'seconds': seconds
	};
}

function startClock(endtime){
	var clock = $('.clock');
	function updateClock(){
		var time = getTimeRemaining(endtime);
		if (!(clock.hasClass("clock-small"))){
			if (time.seconds <= 0 && time.minutes !== 0){
				clock.find('.seconds').hide();
				clock.find('.clock-label:nth-of-type(4)').hide();
			} else {
				clock.find('.seconds').show();
				clock.find('.clock-label:nth-of-type(4)').show();
			}
			if (time.minutes <= 0 && time.seconds !== 0){
				clock.find('.minutes').hide();
				clock.find('.clock-label').first().hide();
			} else {
				clock.find('.minutes').show();
				clock.find('.clock-label').first().show();
			}
			if (time.minutes === 1){
				clock.find('.clock-label').first().text('minute')
			} else {
				clock.find('.clock-label').first().text('minutes')
			}
			if (time.seconds === 1){
				clock.find('.clock-label:nth-of-type(4)').text('second')
			} else {
				clock.find('.clock-label:nth-of-type(4)').text('seconds')
			}
		} else {
			clock.find('span').show();
		}
		clock.find('.minutes').text(time.minutes);
		if (clock.hasClass("clock-small")){
			clock.find('.seconds').text(('0' + time.seconds).slice(-2));
		} else {
			clock.find('.seconds').text(time.seconds);
		}		
		if (time.total <= 0){
			clock.find('.minutes').text(0);
			if (clock.hasClass("clock-small")){
				clock.find('.seconds').text('00');
			} else {
				clock.find('.seconds').text(0);
			}
			clearInterval(timeinterval);
			var ajaxQuery = setInterval(function(){
				$.ajax({
				type:"GET",
				url:"/check_status",
				dataType:"json"
				}).done(function(result) {
					if (result.state == "ordered"){
						clearInterval(ajaxQuery);
						location.reload(true);
					}
				});
			}, 1000);
		}		
	}	
	if (STATE == "ordering"){
		updateClock();	
		var timeinterval = setInterval(updateClock, 1000);
	}
}
