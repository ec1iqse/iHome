function hrefBack() {
    history.go(-1);
}
// 解析提取url中的查询字符串参数
function decodeQuery() {
    let search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {

    let queryData=decodeQuery();
    let houseId=queryData["id"];

    $.get("/api/v1.0/houses/"+houseId,function(resp){
        if("0"===resp.errno){
            $(".swiper-container").html(template("house-image-tmpl",{img_url:resp.data.house.im}));
            $(".detail-con").html(template("house-image-tmpl",{house:resp.data.house}));
            if (resp.data.user_id!=resp.data.house.user_id){
                $(".book-house").attr("href","/booking.html+hid="resp.data.house.hid);
                $(".book-house").show();
            };

            let mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
        }
    });
});