function getDivData(div_id) {
    var array = $(div_id).find(":input");
    var divData = {};
    array.each(function (){
        divData[$(this).attr("name")] = $(this).attr("value");
    })
    return divData;
}


function open_select(select_dept) {
    $.ajax({
        type: "get",
        url: '/sk_api/update_session/' + select_dept,
        async: false,                 //非同步:false-->所以是冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
    })

    window.open( 'tt407',"_self");
}


$(document).ready(function(){
    document.getElementsByTagName("TITLE")[0].text = "TT406 技能盤點作業";
    var dept_numbers =  $('#all_dept option').length;
    var select_dept;
    switch (dept_numbers){
        case 0:
            break;
        case 1:
            $('#all_dept :nth-child(0)').prop('selected', true);
            select_dept = $('#all_dept').val();
            open_select(select_dept);
            break;
        default:
            $('#dept_choice_dd').attr('hidden', false);
            $('#dept_choice_dd').dialog({
                title: '技能盤點作業-部門選擇',
                top: 250,
                width: 600,
                height: 'auto',
                closed: false,
                cache: false,
                modal: true,
            });
            break;
    }

    $('#check_btn').click(function() {
        select_dept = $('#all_dept').val();
        open_select(select_dept);
    });

});