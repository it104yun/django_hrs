function getDivData() {
    var inputData = {};
    inputData['factory_select'] = $('#factory_select').val();
    inputData['month_start'] = $('#month_start').val();
    inputData['month_end'] = $('#month_end').val();
    inputData['jobtitle_select'] = $('#jobtitle_select').combobox('getValues');
    return inputData;
}

function jobTitle_multiple_select(){
    optionTxt = job_titles;
    $('#jobtitle_select').combobox({
        multiple: true,
        valueField: 'code',
        textField: 'name',
        data: optionTxt,
        //改成checkbox
        formatter:function (row){
            var opts = $(this).combobox('options');
            return '<input type="checkbox" class="combobox-checkbox">'+row[opts.textField];
        },
        onLoadSuccess: function () {
            var opts = $(this).combobox('options');
            var target = this;
            var values = $(target).combobox('getValues');
            $.map(values, function (value) {
                var el = opts.finder.getEl(target, value);
                el.find('input.combobox-checkbox')._propAttr('checked', true);
                })
            },
        onSelect: function (row) {
            var opts = $(this).combobox('options');
            var el = opts.finder.getEl(this, row[opts.valueField]);
            el.find('input.combobox-checkbox')._propAttr('checked', true);
            },
        onUnselect: function (row) {
            var opts = $(this).combobox('options');
            var el = opts.finder.getEl(this, row[opts.valueField]);
            el.find('input.combobox-checkbox')._propAttr('checked', false);
        }
    });
}

function valid_data() {
    var month_start = $('#month_start').val();
    var month_end = $('#month_end').val();
    var jobtitle_select = $('#jobtitle_select').combobox('getValues');
    var err_msg="";
    month_start =  month_start.substr(0,4) + month_start.substr(5,2)
    month_end =  month_end.substr(0,4) + month_end.substr(5,2)
    if ( parseInt(month_start) > parseInt(month_end) ) {
        // alert('日期輸入錯誤\n 起始年月需『小於或等於』截止年月');
        err_msg = err_msg + "\n*起始年月需『小於或等於』截止年月*";
    }
    if ( jobtitle_select.length==0 ) {
         err_msg = err_msg + "\n*未選擇職務*";
    }
    return err_msg;
}


$(document).ready(function(){
    document.getElementsByTagName("TITLE")[0].text = "TT422 技能盤點資料匯出";
    jobTitle_multiple_select();
    var err_msg = ""
    $('#matrix_detail_export_btn').click(function() {
        err_msg = valid_data();
        if ( err_msg=="" ){
            var data = getDivData();
            url = "/sk_api/export_matrix_detail";
            $.ajax({
            type :"post",
            url :url,
            data :JSON.stringify(data),
            async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
            success :function(res){
                    if ( res.success ){
                        alert('匯出成功\n\n'+'檔名如下:\n'+res.filename)
                        window.open(res.openFile, target = 'blank');
                    } else {
                        alert("匯出失敗")
                    }
                }
            })
        } else {
            alert("資料選擇有錯誤\n"+err_msg + "\n\n無法匯出");
        }
    });

});