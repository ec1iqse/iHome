function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    let search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

$(document).ready(function(){
    // 判断用户是否登录
    $.get("/api/v1.0/session", function(resp) {
        if ("0" != resp.errno) {
            location.href = "/login.html";
        }
    }, "json");
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        let startDate = $("#start-date").val();
        let endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            let sd = new Date(startDate);
            let ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            let price = $(".house-text>p>span").html();
            let amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    let queryData = decodeQuery();
    let houseId = queryData["hid"];

    // 获取房屋的基本信息
    $.get("/api/v1.0/houses/" + houseId, function(resp){
        if (0 == resp.errno) {
            $(".house-info>img").attr("src", resp.data.house.img_urls[0]);
            $(".house-text>h3").html(resp.data.house.title);
            $(".house-text>p>span").html((resp.data.house.price/100.0).toFixed(0));
        }
    });
    // 订单提交
    $(".submit-btn").on("click", function(e) {
        if ($(".order-amount>span").html()) {
            $(this).prop("disabled", true);
            let startDate = $("#start-date").val();
            let endDate = $("#end-date").val();
            let data = {
                "house_id":houseId,
                "start_date":startDate,
                "end_date":endDate
            };
            $.ajax({
                url:"/api/v1.0/orders",
                type:"POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
                headers:{
                    "X-CSRFToken":getCookie("csrf_token"),
                },
                success: function (resp) {
                    if ("4101" == resp.errno) {
                        location.href = "/login.html";
                    } else if ("4004" == resp.errno) {
                        showErrorMsg("房间已被抢定，请重新选择日期！");
                    } else if ("0" == resp.errno) {
                        location.href = "/orders.html";
                    }
                }
            });
        }
    });
})
