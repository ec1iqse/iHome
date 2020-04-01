function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
    });
    $(".form-login").submit(function (e) {
        // 阻止默认行为
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        // 将表单的数据存放到对象data中
        let data={
            mobile:mobile,
            password:passwd,
        };

        // 将data转换为json字符串

        let jsonData=JSON.stringify(data);
        $.ajax({
            url:"/api/v1.0/sessions",
            type:"post",
            data:jsonData,
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token"),
                // "X-CSRFToken":getCookie("csrf_token"),
            },
            success:function (data) {
                if(data.errno=="0"){
                    // 登录成功，跳转到主页
                    location.href="/";
                }else {
                    $("#password-err span").html(data.errmsg);
                    $("password-err span").show();
                }

            }
        })

    });
})