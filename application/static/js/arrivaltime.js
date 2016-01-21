$(document).ready(function(){
	startCountdown(DEADLINE, ARRIVALMIN, ARRIVALMAX);
});

function minutesRemaining(deadline){
	var time = Date.parse(deadline) - Date.parse(new Date());
	var minutes = Math.ceil(time/(1000*60));
	return minutes;
}

function endTime(deadline, arrivaltime){
	var endtime = new Date(Date.parse(deadline));
	endtime.setMinutes(endtime.getMinutes() + arrivaltime);
	return endtime;
}

function startCountdown(start, arrivalmin, arrivalmax){
	var clock = $('.clock');
	var update = $('.arrivaltime');
	function updateTime(){
		$.ajax({
			type:"GET",
			url:"/check_status",
			dataType:"json"
		}).done(function(result){
			if (arrivalmin != result.arrivalmin){
				location.reload(true);
			}
		});
		var finalMin = endTime(start, arrivalmin);
		var finalMax = endTime(start, arrivalmax);
		var minLeft = minutesRemaining(finalMin);
		var maxLeft = minutesRemaining(finalMax);
		if (minLeft < 1){
			minLeft = 1;
		}
		if (maxLeft < 5){
			maxLeft = 5;
		}
		clock.find('.minimum').text(minLeft);
		clock.find('.maximum').text(maxLeft);
		update.find('.minimum input').val(minLeft);
		update.find('.maximum input').val(maxLeft);
	}
	if (STATE == "ordered"){
		updateTime();
		var timeinterval = setInterval(updateTime, (60*1000));
	}
}