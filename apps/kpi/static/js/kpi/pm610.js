function getDivData(div_id) {
    var array = $(div_id).find(":input");
    var divData = {};
    array.each(function (){
        divData[$(this).attr("name")] = $(this).attr("value");
    })
    return divData;
}

function getFormatedDateTime(){
    var dt = new Date();
    var Year,Month,Day,Hour,Minute,Second,MSecond;
    Year = (dt.getFullYear()).toString();
    Month = (dt.getMonth()+1).toString().padStart(2,'0');
    Day = (dt.getDate()).toString().padStart(2,'0');
    Hour = (dt.getHours()).toString().padStart(2,'0');
    Minute = (dt.getMinutes()).toString().padStart(2,'0');
    Second = (dt.getSeconds()).toString().padStart(2,'0');
    MSecond = (dt.getMilliseconds()).toString().padStart(3,'0');  //取得毫秒數 0~999
    return (Year+Month+Day+Hour+Minute+Second+MSecond)
}


function set_combobox(url,mtf,selectID) {
    $.get(
        url,
        function (res) {
            if (res) {
                optionTxt = res;
                $(selectID).combobox({
                    multiple: mtf,
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                    //改成checkbox
                    formatter: function (row) {
                        var opts = $(this).combobox('options');
                        return '<input type="checkbox" class="combobox-checkbox">' + row[opts.textField];
                    },
                    onLoadSuccess: function () {
                        var opts = $(this).combobox('options');
                        var target = this;
                        var values = $(target).combobox('getValues');
                        $.map(values, function (value) {
                            var el = opts.finder.getEl(target, value);
                            el.find('input.combobox-checkbox')._propAttr('checked', true);
                        })
                        $(this).combobox('setValue', '');    //加空白,會自動在選擇時....加一個逗號, 這樣不論是否有在此輸入查詢關鍵字, 只要將第一個逗號前的資料去除,就可順利做多筆查詢
                    },
                    onSelect: function (row) {
                        //console.log(row);
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
        })

}

$(document).ready(function(){
    console.log("/api/get_employee_data/" + userId);
    set_combobox( "/api/get_employee_data/" + userId ,false,'#work_code_id');


    $('#report_sumit').click(function() {
        var fileName = 'KPI' + getFormatedDateTime();
        var data = getDivData('#report_box');
        data['fileName'] = fileName;
        data['curr_url_prefix'] = location.protocol+"//"+location.hostname+":"+location.port
        reportSourceUrl = "/api/kpi_report_quarter/";
        $.post(
            reportSourceUrl,
            data,
             function(res) {
                if(res.success) {
                    alert('***產生成功***\n\n 報表名稱：'+res.fileName+"\n\n BPM單號："+res.bpm_number);
                    fileName = res.fileName+".pdf";
                    window.open('/api/kpi_report_quarter?fileName=' + fileName , target = 'blank');
                } else {
                    alert('產生錯誤');
                }
            })
    })

    $('#clear').click(function (){
        $("#report_dd input").val('');
    });

});




