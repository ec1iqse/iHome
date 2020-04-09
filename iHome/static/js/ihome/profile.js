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
    $("#form-avatar").submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对函数进行异步提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno === "0") {
                    // 上传成功
                    let avatarUrl = resp.data.avatar_url;
                    $("#user-avatar").attr("src", avatarUrl);
                } else {
                    alert(resp.errmsg);
                }
            }
        });
    });
    $.get("/api/v1.0/user", function (resp) {
// 用户未登录
        if ("4101" === resp.errno) {
            location.href = "/login.html";
        } else if ("0" === resp.errno) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");
    $("#form-name").submit(function (e) {
        e.preventDefault();
//获取参数
        let name = $("#user-name").val();
        if (!name) {
            alert("请输入用户名！");
            return;
        }
        $.ajax({
            url: "/apv/v1.0/users/name",
            type: "PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (data) {
                if ("0" === data.errno) {
                    $(".error-msg").hide();
                } else if ("4001" === data.errno) {
                    $(".error-msg").show();
                } else if ("4101" === data.errno) {
                    location.href = "./login.html"
                }
            }
        });
    });
});

