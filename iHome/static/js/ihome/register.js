function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//保存图片验证码ID
let imageCodeId = "";

function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址，设置到页面中，让浏览器请求验证码图片
    // 生成图片验证码编号
    imageCodeId = generateUUID();
    let url = "/api/v1.0/image_codes/" + imageCodeId;
    //设置图片url
    $(".image-code img").attr("src", url);


}

function sendSMSCode() {
    // 点击发送短信验证码后执行的函数
    $(".phonecode-a").removeAttr("onclick");
    let mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    let imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    let req_data = {
        image_code: imageCode,//图片验证码的值
        image_code_id: imageCodeId//图片验证码的编号(全局变量)
    };
    // 向后端发送请求
    $.get("/api/v1.0/sms_codes/" + mobile, req_data, function (resp) {
        // resp是后端返回的相遇值，因为后端返回的是json字符串，所以ajax把json字符串转换为js对象


        console.log("请求被执行");
        console.log("resp代码：",resp.errno);


        if (resp.errno == "0") {



            console.log("==0！");


            let num = 60
            // 发送成功
            let timer = setInterval(function () {

                console.log("开始倒计时");


                if (num > 1) {
                    //修改倒计时文本


                    console.log("修改倒计时 ");
                    console.log("剩余"+num);



                    $(".phonecode-a").html(num + "秒");
                    num--;
                } else {




                    console.log("获取验证码按钮恢复");




                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    clearInterval(timer);
                }
            }, 1000 * 1, 60)
        } else {





            console.log("倒计时结束！");






            alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    });


    $.get("/api/smscode", {mobile: mobile, code: imageCode, codeId: imageCodeId},
        function (data) {
            if (0 != data.errno) {
                $("#image-code-err span").html(data.errmsg);
                $("#image-code-err").show();
                if (2 == data.errno || 3 == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            } else {
                let $time = $(".phonecode-a");
                let duration = 60;
                let intervalid = setInterval(function () {
                    $time.html(duration + "秒");
                    if (duration === 1) {
                        clearInterval(intervalid);
                        $time.html('获取验证码');
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60);
            }
        }, 'json');
}

$(document).ready(function () {
    generateImageCode();
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function () {
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function () {
        $("#phone-code-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function () {
        $("#password2-err").hide();
    });
    $(".form-register").submit(function (e) {
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
    });
})