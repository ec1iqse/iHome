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

    }, "json")

})