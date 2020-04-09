function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {

    console.log("页面准备");



    $("#form-avatar").submit(function (e) {
        // 阻止表单的默认行为
        console.log("开始阻止");
        e.preventDefault();


        console.log("阻止表单的默认行为");



        // 利用jquery.form.min.js提供的ajaxSubmit对函数进行异步提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (resp) {
                console.log("返回了值",resp.errno);
                if (resp.errno === "0") {
                    // 上传成功
                    let avatarUrl = resp.data.avatar_url;
                    $("#user-avatar").attr("src", avatarUrl);
                } else {
                    alert(resp.errmsg);
                }
            }
        });
    })
});