
let now = $('#now').val()
var dp = new HaDateTimePicker("#datetime", {
    isSolar: true,
    forceSetTime: true,
    resultFormat: '{year}-{month}-{day} {hour}:{minute}',
    minAllowedDate: now
});
$('#datetime').click(function () {
    dp.show()
})


var frm = $('#my_form');
frm.submit(function (e) {
    e.preventDefault(e);

    var formData = new FormData(this);
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $body = $("body");
    $(document).ajaxStart(function () {
        $body.addClass("loading");
    });
    $(document).ajaxStop(function () {
        $body.removeClass("loading");
    })
    $.ajax({
        async: true,
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (res) {
            if (res.status === 'success') {
                $('#message-success').empty().append(showMessageError(res.message, 'success', 'موفق'));
                setTimeout(function () {
                    window.location.replace(res.redirect);
                }, 5000);
            } else {
                if (res.message === 'این فیلد لازم است.') {
                    res.message = `فیلد ${res.field_name} لازم است`
                }
                $('#message-success').empty().append(showMessageError(res.message, 'danger', 'شکست'));
            }
        },
        error: function (request, status, error) {
            console.log(error)
        }
    });
});
