$(window).load(function() {
		// Animate loader off screen
		$(".se-pre-con").fadeOut("fast");;
	});

function toggleEnable(el1) {
        if (document.getElementById(el1).disabled === true) {
            document.getElementById(el1).disabled = false;
        }
         else {
        document.getElementById(el1).disabled = true;
    }
}