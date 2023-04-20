function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        formData[fieldName] = field.value;
    }
    return formData;
}

function centerControl(event) {
    var old_year = parseInt(main_form.date_yyyy.value);
    var old_month = parseInt(main_form.date_mm.value);
    var new_year,new_month;
    if ( old_month==12 ) {
        main_form.id_new_date_yyyy.value = old_year + 1;
        main_form.id_new_date_mm.value = 0;
    } else {
        main_form.id_new_date_yyyy.value = old_year;
        main_form.id_new_date_mm.value = old_month+1;
    }

    var Today=new Date();
    var current_year=Today.getFullYear();
    var current_month=Today.getMonth()+1;
    var current_day=Today.getDay();
    var lastDay= new Date(main_form.id_new_date_yyyy.value,main_form.id_new_date_mm.value,0);
    var year = lastDay.getFullYear();
    var month = lastDay.getMonth() + 1;
    var day = lastDay.getDate()-before_lastdate;
    month = month < 10 ? '0'+month : month ;
    day = day < 10 ? '0'+day : day;

    //比較日期, 若日期等於今天, 將日期設定為今天+1天
   main_form.id_new_diy_date.value = old_year + "-"+month+"-"+day;

    if ( current_year == old_year && (current_month) == old_month){
        // 當月不可再進行關帳
        $('#update_btn').attr('disabled','disabled');
    } else　{
        $('#update_btn').remove('disabled');
    }


    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            clearError();
            break
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
    }
}

var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var rowCount = 0;

config.main_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        main_form.date_yyyy.value = row['date_yyyy'];
        main_form.date_mm.value = row['date_mm'];
        main_form.diy_date.value = row['diy_date'];
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        $(this).datagrid('selectRow', 0);
    }
}

config.main_mono_search_dlg = {
    resizable: true,
    modal:true,
    closed: true,
}
config.cpx_search_dlg = {
    'dlg': {
        resizable: true,
        modal: true,
        closed: true,
    },
}


$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#progressArea').hide();

   $('#update_btn').click(function(){
        $('#update_btn').hide();    //隱藏，預防使用者再按一次
        var confirm_msg1="按下「確定關帳」後\n關帳前的評核年月，將無法新增/修改/刪除，只可查詢";
        var confirm_msg2="\n\n***在您按下『確定關帳』前***\n***請您確定所有『衡量指標評核』的作業流程都已執行完成***";
        var confirm_msg3="\n\n\n您確定要『關帳』嗎?";
        var sure = confirm(confirm_msg1+confirm_msg2+confirm_msg3);
        if (sure){
            if(!formValidate(main_form)) return;
            $('#progressArea').show();

            // jquery hide() 或 show 無效時的另類寫法
            $("#progressArea").show("slow",function(){$(this).css("display","block")});
            /* 關帳前的檢核
               目前評核年月
            　　   (1)-主管是否已審核
               下個評核年月
                  (2)A-衡量指標未達100
                     B-計算方式沒有0分,及最高配分
                  (3)-未達以上檢核點，產生excel表匯出
                  (4)-全部達以上檢核點，才關帳
            */

            //關帳前的檢核----------------------------------------------------------------------------------------------------------------------Begin 2021/04/28
            var data = getFormData(main_form);
            //                                        關帳前:評核-年           關帳前:評核-月        關帳後:評核-年           關帳後:評核-月
            validationUrl = "/api/valid_all_metrics/"+data['date_yyyy'] +"/"+data['date_mm']+"/"+data['new_date_yyyy']+"/"+data['new_date_mm'];
            $.get(
                    validationUrl,
                    function (res) {
                        if (res.success) {
                            alert('檢核完成!');
                            $('#progressArea').hide();
                            // jquery hide() 或 show 無效時的另類寫法
                            // $("#progressArea").hide("slow",function(){$(this).css("display","none")});
                            //檢核成功(都沒有問題)，進行關帳-------------------------------------------------Begin
                            data['date_yyyy'] = data.new_date_yyyy;
                            data['date_mm'] = data.new_date_mm;
                            data['diy_date'] = data.new_diy_date;
                            delete data.new_date_yyyy;
                            delete data.new_date_mm;
                            delete data.new_diy_date;
                            $.post(
                                formSourceUrl + '/' + currentKey,
                                data,
                                function(res) {
                                    if(res.success) {
                                        alert('關帳成功!');
                                        $('#update_btn').attr('disabled','disabled');
                                        $('#main_dg').datagrid('reload');
                                    } else {
                                        alert('錯誤!');
                                    }
                                }
                            )
                            //檢核成功，進行關帳--------------------------------------------------------Ending
                        } else {
                            //匯出excel檔
                            alert('檢核有錯誤'+'\n無法進行關帳\n\n'+'檢核檔名如下:\n'+res.filename);
                            window.open(res.openFile, target = 'blank');
                            $('#progressArea').hide();
                            // jquery hide() 或 show 無效時的另類寫法
                            // $("#progressArea").hide("slow",function(){$(this).css("display","none")});
                        }

                    });
             //要做什麼是情,還千萬別放這兒呀!  $.get 預設是-->非同步(Asynchronous request)
            //客戶端 (client) 對伺服器端 (server) 送出 request 之後，不需要等待結果，仍可以持續處理其他事情，甚至繼續送出其他 request。Responese 傳回之後，就被融合進當下頁面或應用中。
            //關帳前的檢核----------------------------------------------------------------------------------------------------------------------Ending 2021/04/28
        } else {
            alert('***您取消了『關帳』***\n\n ***系統並未執行『關帳』作業***');
            $('#update_btn').show();    //隱藏，預防使用者再按一次
        }
    });

    // window.onbeforeunload = function (e){
    //     e.returnValue = "";
    // }
});




