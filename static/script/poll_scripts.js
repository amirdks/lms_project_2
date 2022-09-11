function deleteOption(pk, id) {
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
        method: 'post',
        url: `/poll/${pk}/option/${id}/delete`,
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (res) {
            if (res.status === 'success') {
                $('#poll_options_list').fadeOut(500, function () {
                    $('#poll_options_list').html(res.body).fadeIn(500)
                })
                $('#message-success').empty().append(showMessageError(res.message, 'success', 'موفق'));
            } else {
                $('#message-success').empty().append(showMessageError(res.message, 'danger', 'شکست'));
            }
        },

    })
}

var frm = $('#option_form');
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
    $('#myModal').hide();
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
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
                $('#poll_options_list').fadeOut(500, function () {
                    $('#poll_options_list').html(res.body).fadeIn(500)
                })
                $('#message-success').empty().append(showMessageError(res.message, 'success', 'موفق'));
            } else {
                $('#message-success').empty().append(showMessageError(res.message, 'danger', 'شکست'));
            }
        },
        error: function (request, status, error) {
            console.log(error)
        }
    });
});

function onHideInput(id) {
    $(`#input-${id}`).attr('hidden', false)
}


function submitOptionForm(id) {
    var form = $(`#option-form-${id}`);
    form.submit(function (e) {
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
        $('#myModal').hide();
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $.ajax({
            async: true,
            type: form.attr('method'),
            url: form.attr('action'),
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (res) {
                if (res.status === 'success') {
                    $('#poll_options_list').fadeOut(500, function () {
                        $('#poll_options_list').html(res.body).fadeIn(500)
                    })
                    $('#message-success').empty().append(showMessageError(res.message, 'success', 'موفق'));
                } else {
                    $('#message-success').empty().append(showMessageError(res.message, 'danger', 'شکست'));
                }
            },
            error: function (request, status, error) {
                console.log(error)
            }
        });
    });
}