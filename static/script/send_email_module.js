var frm = $('#form');
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
let num = 1
$('#add-file-button').click(function () {
    num += 1
    $('#file-div').append(`        <div id="file-div">
            <input style="margin-top: 10px; display: block" class="btn btn-primary" name="file-${num}" type="file"
                   value="انتخاب فایل"
                   id="formFileMultiple">
        </div>`)
})