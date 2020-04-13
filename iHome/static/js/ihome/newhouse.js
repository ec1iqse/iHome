function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    // 获取数据
    // 向后端获取城区信息
    $.get("/api/v1.0/areas", function (resp) {
        if ("0" === resp.errno) {
            let areas = resp.data;
            // for (i = 0; i < areas.length; i++) {
            //     let area = areas[i];
            //     $("#area-id").append('<option value="+ area.aid +">'+ area.aname +'</option>');
            // }
            // 使用js模板
            let html_text = template("areas-tmpl", {areas: areas})
            $("#area-id").html(html_text);
        } else {
            alert(resp.errmsg);
        }

    }, "json");

    $("#form-house-info").submit(function (e) {
        e.preventDefault();
        //处理表单数据
        let data = {};
        $("#form-house-info").serializeArray().map(function (x) {
            data[x.name] = x.value;
        });


        //收集设置id信息
        let facility = [];
        $(":checked[name=facility]").each(function (index, x) {
            facility[index] = $(x).val();
        });
        data.facility = facility;
        //向后端发松请求
        $.ajax({
            url: "api/v1.0/houses/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if ("4101" === resp.errno) {
                    location.href = "./login.html";
                } else if ("0" === resp.errno) {
                    //隐藏基本信息表单
                    $("#form-house-info").hide();
                    //显示图片表单
                    $("#form-house-image").show();
                    //设置图片表单中的house_id
                    $("#house-id").val(resp.data.house_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        });
    });
    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "url/api/v1.0/houses/image",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token"),
            },
            success: function (resp) {
                if ("4101" === resp.errno) {
                    location.href = "./login.html"
                } else if ("0" === resp.errno) {
                    $(".house-image-cons").append('<img src="' + resp.data.image_url + '">');
                } else {
                    alert(resp.errmsg);
                }
            }
        });
    });
});