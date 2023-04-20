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
    var Year,Month,Day,Hour,Minute,Second;
    Year = (dt.getFullYear()).toString();
    Month = (dt.getMonth()+1).toString().padStart(2,'0');
    Day = (dt.getDate()).toString().padStart(2,'0');
    Hour = (dt.getHours()).toString().padStart(2,'0');
    Minute = (dt.getMinutes()).toString().padStart(2,'0');
    Second = (dt.getSeconds()).toString().padStart(2,'0');
    return (Year+Month+Day+'_'+Hour+Minute+Second)
}

$(document).ready(function(){

    // 取得所有員工的部門
    var comboboxSourceUrl_dept = "/api/get_dept_data";
    $.get(
        comboboxSourceUrl_dept,
        function (res) {
            if (res) {
                optionTxt = res;
                $("#dept_id").combobox({
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                })
            }
        })

    // 取得所有員工的<工號,姓名>
    var comboboxSourceUrl_work_code = "/api/get_employee_data";
    $.get(
        comboboxSourceUrl_work_code,
        function (res) {
            if (res) {
                optionTxt = res;
                $("#work_code_id1").combobox({
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                })
                $("#work_code_id2").combobox({
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                })

            }
        })



    $('#report_sumit').click(function() {
        var fileName = 'pm604_' + getFormatedDateTime();   // 程式代碼+日期時間
        var data = getDivData('#report_box');
        data['fileName'] = fileName;
        reportSourceUrl = "/api/kpi_report_quarter/";
        $.post(
            reportSourceUrl,
            data,
             function(res) {
                if(res.success) {
                    alert('***產生成功***\n\n 檔案名稱:'+res.fileName);
                    window.open('/api/kpi_report_year?fileName=' + res.fileName, target = 'blank');
                } else {
                    alert('產生錯誤');
                }
            })
    })

    $('#clear').click(function (){
        $("#report_dd input").val('');
    });

});




