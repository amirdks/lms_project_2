$(window).load(function () {
    // Animate loader off screen
    $(".se-pre-con").fadeOut("fast");
    ;
});

function toggleEnable(el1) {
    if (document.getElementById(el1).disabled === true) {
        document.getElementById(el1).disabled = false;
    } else {
        document.getElementById(el1).disabled = true;
    }
}

let lockDiv = document.getElementById('my-lock-div')
lockDiv.addEventListener('click', function () {
    let lockIcon = document.getElementById('my-lock-icon')
    let myPassInput = document.getElementById('my-pass-input')
    if (myPassInput.type == 'password') {
        myPassInput.type = 'text'
        lockIcon.classList.replace('fa-lock', 'fa-lock-open')
    } else {
        myPassInput.type = 'password'
        lockIcon.classList.replace('fa-lock-open', 'fa-lock')
    }
})