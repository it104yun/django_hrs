function getDivData(div_id) {
    var array = $(div_id).find(":input");
    var divData = {};
    array.each(function (){
        divData[$(this).attr("name")] = $(this).attr("value");
    })
    return divData;
}


$(document).ready(function(){
    document.getElementsByTagName("TITLE")[0].text = "TT404 技能盤點底稿產生";
    $('#matrix_gen_btn').click(function() {
        var data = getDivData('#matrix_master_box');
        reportSourceUrl = "/sk_api/gen_matrix_master/"+data.factory_select;
        $.post(
            reportSourceUrl,
            data,
             function(res) {
                if(res.success) {
                    alert('***產生成功***');
                } else {
                    alert('產生錯誤');
                }
            })
    })

});