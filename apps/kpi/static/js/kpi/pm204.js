function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        //# _id 結尾通常是 foreignkey
        if(field.type === 'select-one') {
            formData[fieldName + '_id'] = field.value;
        }
        else if(field.type === 'radio') {
            formData[fieldName + '_id'] = $('input[name='+fieldName+']:checked').val();
            formData[fieldName] = $('input[name='+fieldName+']:checked').parent('label').text().trim();
        }
        else {
            formData[fieldName] = field.value;
        }
    }
    return formData;
}

function setFormData(form, row) {
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        if(row[fieldName] == undefined) continue;
        if(field.tagName === 'SELECT') {
            field.value = row[fieldName + '_id'] || row[fieldName];
        }
        else if(field.type === 'checkbox') {
            field.checked = row[fieldName];
        }
        else {
            if (row[fieldName]!=false) {
                fields[i].value = row[fieldName];
            } else {
                fields[i].value = '';
            };
        }
    }
}


function findRowDatas(Year, Month){
    var dg = $('#metrics_setupDate_dg');
    var row = null;
    var rows = dg.datagrid('getRows');
    for(var i=0,len=rows.length; i<len; i++){
        if ( rows[i]['date_yyyy']==Year && rows[i]['date_mm']==Month ){
            row = rows[i];
            break;
        }
    }
    if (row){
        var index = dg.datagrid('getRowIndex', row);
        dg.datagrid('selectRow', index);
    }
}



function get_order_number(){
    /*
    Swork_code = main_form.work_code.value;
    Sdate_yyyy = main_form.date_yyyy.value;
    Sdate_mm = main_form.date_mm.value;
     */
    Swork_code = $('#id_work_code').val();
    Sdate_yyyy = parseInt($('#id_date_yyyy').val());
    Sdate_mm = parseInt($('#id_date_mm').val());
    sequence_numberUrl = "/api/get_metrics_order_number/" +Swork_code+"/"+Sdate_yyyy+"/"+Sdate_mm;
        $.get(
            sequence_numberUrl,
            function (res) {
                if (res) {
                    // main_form.order_number.value = res.next_number;
                    $('#id_order_number').val(res.next_number);
                    get_order_item(res.next_number);
                }else {
                    // main_form.order_number.value = 1;
                    $('#id_order_number').val(1);
                }
            }
        )
    // alert($('#id_order_number').val());
}


function get_order_item(thisVal){
    /*
    Swork_code = main_form.work_code.value;
    Sdate_yyyy = main_form.date_yyyy.value;
    Sdate_mm = main_form.date_mm.value;
     */
    Swork_code = $('#id_work_code').val();
    Sdate_yyyy = parseInt($('#id_date_yyyy').val());
    Sdate_mm = parseInt($('#id_date_mm').val());
    Sorder_number = thisVal;
    sequence_numberUrl = "/api/get_metrics_order_item/" +Swork_code+"/"+Sdate_yyyy+"/"+Sdate_mm+"/"+Sorder_number;
        $.get(
            sequence_numberUrl,
            function (res) {
                if (res) {
                    // main_form.order_item.value = res.next_number;
                    $('#id_order_item').val(res.next_number);
                }else {
                    // main_form.order_item.value = 0;
                    $('#id_order_item').val(0);
                }
            }
        )
}

function valid_save_data() {
    var alert_msg = '.';
    var rtn_val = true;
    var low_limit = parseFloat(main_form.low_limit.value);
    var allocation = parseFloat(main_form.allocation.value);

    if ( low_limit>= allocation) {
        alert_msg += " 「最低配分」>=「最高配分」，不允存檔";
        rtn_val = false;
    }
    if (alert_msg != '.') {
        alert(alert_msg);
    }
    return rtn_val;
}

function textbox_onChange_expand(Year,Month){
       if ( Month == null){ Month = 0};
       copyToSourceUrl = "/api/get_employee_common_data/"+Year+"/"+Month;
        $.get(
            copyToSourceUrl,
            function (res) {
                if (res) {
                    optionTxt = res;
                    // copyTo : 存在的工號，才能複製
                    $('#expandTo_WorkCode1').combobox({
                        valueField:'value',
                        textField:'text',
                        data: optionTxt,
                        });
                }else {
                    optionTxt = null;
                }
            }
        )
}


function textbox_onChange_expandCommon(Year,Month){
    if ( Month == null){ Month = 0};
    copyToSourceUrl = "/api/get_employee_common_data/"+Year+"/"+Month;
    $.get(
        copyToSourceUrl,
        function (res) {
            // copyTo : 存在的工號，才能複製
            if (res) {
                optionTxt = res;
                var copyNum = 6;
                for (var i=1;i<=copyNum;i++){
                    copyTo = "#expandTo_Common"+i;
                    $(copyTo).combobox({
                        valueField:'value',
                        textField:'text',
                        data: optionTxt,
                        });
                }
            }else {
                optionTxt = null;
            }
        }
    )
}


function textbox_onChange_copy(id1,id2,target_id){
    var from_month = id2.val();
    var month_err = null;
    if (parseInt(from_month)<0 || parseInt(from_month)>12){
        alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
        id2.textbox('setValue', '');
    }
    // copyFromSourceUrl = "/api/get_employee_common_data/"+userId+"_copy_"+id1.val()+"_"+id2.val();
    copyFromSourceUrl = "/api/get_employee_common_data/"+id1.val()+"/"+id2.val();
    $.get(
        copyFromSourceUrl,
        function (res) {
            if (res) {
              optionTxt = res;
              target_id.combobox({
                  valueField: 'value',
                  textField: 'text',
                  data: optionTxt,
              });
          }
       })
}

function textbox_value_from(id1,id2){
    if (workingMonth==12){
        id1.textbox({value: parseInt(workingYear)+1});    //easyUI textbox給值的方式
        id2.textbox({value: 1});   //easyUI textbox給值的方式
    } else {
        id1.textbox({value: workingYear});    //easyUI textbox給值的方式
        id2.textbox({value: parseInt(workingMonth) + 1});   //easyUI textbox給值的方式
    }
}


function copyto_textbox_value(id1,id2,id3){
    id1.combobox({
            onChange: function(param){
            textbox_value_from(id2,id3)
        }
    });
}


//Listening Year&Month change to do
function copyto_YearMonth_onChange(id1,id2){
    id1.textbox({
        onChange:function (){
            to_year = $(this).val();
            if (to_year<workingYear){
                alert('年月小於等於評核年月,錯誤的年份將被清除');
                $(this).textbox('setValue', '');
            }
          }
    });

    id2.textbox({
         onChange:function (){
            to_year = parseInt(id1.val());
            to_month = parseInt($(this).val());
            if (to_month<0 || to_month>12){
                alert('月份應介於0<年度目標> 及 1~12,錯誤的月份將被清除');
                $(this).textbox('setValue', '');
            }
            if (to_year==workingYear){
                if (to_month<=workingMonth){
                    alert('年月小於等於評核年月,錯誤的月份將被清除');
                    $(this).textbox('setValue', '');
                }
            }
          }
    });
}




function assign_work_code_options() {
    var option_length = $('#id_work_code option').length;
    var current_work_code= main_form.id_work_code.value;
     $('#id_work_code option').each(function (){
         //移除所有選項
           $(this).remove();
     });

     sub_employee_Url = "/api/get_employee_common_data/" ;

    $.ajax({
        type: "get",
        url: sub_employee_Url,
        async: false,                 //非同步:false-->所以是冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success: function (res) {
            var options='';
            if (res) {
                $.each(res, function(index, value){
                      options += "<option value='"+value['value']+"'>"+value['text']+"</option>";
                    });
                $('#id_work_code').append(options);
            }
        }
    });
    main_form.id_work_code.value = current_work_code;
}


function main_dg_query(){
    console.log($('#id_work_code').val());
    console.log($('#id_date_yyyy').val());
    console.log($('#id_date_mm').val());
    $("#main_dg").datagrid({
        queryParams: {
            work_code: $('#id_work_code').val(),
            date_yyyy: $('#id_date_yyyy').val(),
            date_mm: $('#id_date_mm').val(),
        },
    });
}

function dg_reload(){
    $('#main_dg').datagrid('reload');
    $('#employee_info_easy_dg').datagrid('reload');
    $('#metrics_setupDate_dg').datagrid('reload');
}


function months_1to12_append() {
    var options='';
    $('#id_date_mm option').each(function () {
        $(this).remove();
    });
    for (var M = 1; M <= 12; M++) {
        options += "<option value='" + M + "'>" + M + "</option>";
    }
    $('#id_date_mm').append(options);
}

function centerControl(event) {
    main_form.id_metrics_type.disabled=true;
    main_form.date_yyyy.disabled=true;
    main_form.date_mm.disabled=true;
    // main_form.date_yyyy.value=workingYear;
    main_form.allocation_tot.disabled=true;
    main_form.id_metrics_type.options[1].selected=true;
    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.id_work_code.disabled=false;
            main_form.date_yyyy.disabled=false;
            main_form.id_date_mm.disabled=false;
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.id_work_code.disabled=true;
            main_form.id_date_mm.disabled=true;
            clearError();
            break
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.id_work_code.disabled=true;
            main_form.id_date_mm.disabled=true;
            break
    }
}

function Empty_centerControl(){
    main_form.work_code.value='';
    main_form.id_metrics_type.value='';
    main_form.date_yyyy.value = '';
    main_form.date_mm.value = '';
    main_form.order_number.value = '';
    main_form.order_item.value = '';
    main_form.metrics_txt1.value = '';
    main_form.metrics_number.value = '';
    main_form.metrics_txt2.value = '';
    main_form.unit_Mcalc.value = '';
    main_form.allocation.value = '';
    main_form.allocation_tot.value = '';
}


//crIndex : currentRowIndex
function datagridSelectRow(dg,data,conditions,crIndex){
       switch (currentEvent) {
           case 'new':
                for ( var i=0, len= data.rows.length; i < len ; i++){
                    if ( eval(conditions)) {
                        dg.datagrid('selectRow', i);
                        break;    //for的break
                    }
                }
                //沒選到row的處理,避免main_dg,main_form顯示舊資料
                if (dg.datagrid('getSelected') == null){
                    // var rr = dg.datagrid('getSelected');
                    // var ii = dg.datagrid('getRowIndex', rr);
                    // update=null index==-1
                    dg.datagrid('selectRow', 0);
                }
                //重新指定中間main_form的data
                var rr = $("#main_dg").datagrid('getSelected');
                if ($("#main_dg").datagrid('getRowIndex', rr)==-1){
                    $("#main_dg").datagrid('selectRow', 0);
                }
                clearError();
                break;           //switch的break
            case 'update':
                dg.datagrid('selectRow', crIndex);
                //沒選到row的處理,避免main_dg,main_form顯示舊資料
                if (dg.datagrid('getSelected') == null){
                    dg.datagrid('selectRow', 0);
                }
                //重新指定中間main_form的data
                var rr = $("#main_dg").datagrid('getSelected');
                if ($("#main_dg").datagrid('getRowIndex', rr)==-1){
                    $("#main_dg").datagrid('selectRow', 0);
                }
                clearError();
                break;
            case 'delete':     //刪除之後,INDEX不變,還是原來的位置
                //刪除最後一筆資料時, 還是移到最後一筆資料
                if ( crIndex == data.rows.length) {
                    dg.datagrid('selectRow', crIndex - 1);
                } else {
                    dg.datagrid('selectRow', crIndex);
                }
                //沒選到row的處理,避免main_dg,main_form顯示舊資料
                if (dg.datagrid('getSelected') == null){
                    dg.datagrid('selectRow', 0);
                }
                clearError();
                break;
           case 'ready':
                dg.datagrid('selectRow', crIndex);
                //沒選到row的處理,避免main_dg,main_form顯示舊資料
                if (dg.datagrid('getSelected') == null) {
                    dg.datagrid('selectRow', 0);
                }
                clearError();
                break;
           default:
                dg.datagrid('selectRow', 0);
                break;
    }
}


var currentKey = '';
var currentRow = null;
var currentRowIndex_center = 0;
var currentRowIndex_north = 0;
var currentRowIndex_east = 0;
var rowCount = 0;
var currentEvent = null;

var rowCount_main_dg = 0;
var work_code_key = '';
var conditions=null;


//north_grid-->main_form

//EasyUI控制Grid的Column格式
//field : 必需在〝Django view〞中有定義
//title : 就算在〝Django view〞中有定義，在這兒還是要重新定義一次，若無定義會顯示為〝空白〞
config.employee_info_easy_dg = {
    method: 'get',
    // autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    columns:[[
        {field:'work_code',title:'編號', width:80,},
        {field:'chi_name',title:'共同指標.隸屬公司', width:150,},
        // {field:'factory_name',title:'公司', width:80,},
        // {field:'dept_name',title:'部門', width:150,},
    ]],
    onSelect: function(index, row) {
        currentRowIndex_north = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        work_code_key = row['work_code']
        searchYear = $('#searchYear').textbox('getValue');
        if (parseInt(searchYear)>2020){
            eastSourceUrl = "/api/get_metrics_setupDate_data/"+ work_code_key+"/"+searchYear;
        } else {
            eastSourceUrl = "/api/get_metrics_setupDate_data/"+ work_code_key+"/"+workingYear;
        }
        $('#metrics_setupDate_dg').datagrid({autoLoad:true,url : eastSourceUrl});
        $('#metrics_setupDate_dg').datagrid('selectRow',currentRowIndex_east);
        // datagridSelectRow($('#metrics_setupDate_dg'));
    },
    onLoadSuccess: function(data) {
         conditions = "data.rows[i]['work_code'] == main_form.id_work_code.value";
         //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']
         datagridSelectRow($(this), data, conditions, currentRowIndex_north);
         // }
    }
}


//east_grid-->main_form-->down
config.metrics_setupDate_dg = {
    method: 'get',
    autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    columns:[[
        {field:'date_yyyy',title:'年度',width:60,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
        {field:'date_mm',title:'月(季)',width:60,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
    ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function(index, row) {
        currentRowIndex_east = index;
        currentRow = row
        currentKey =row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
        if (row['date_yyyy']==false){ thisYear = workingYear } else { thisYear=row['date_yyyy'] };
        $("#main_dg").datagrid({
            queryParams: {
                work_code_id: row['work_code'],
                date_yyyy: thisYear,
                date_mm: row['date_mm'],
            },
        });
        main_form.work_code.value =row['work_code'];
        main_form.date_yyyy.value = thisYear;
        main_form.date_mm.value = row['date_mm'];
        $('#main_dg').datagrid({autoLoad:true});
        $('#main_dg').datagrid('selectRow',currentRowIndex_center);

        if ( row['date_yyyy']>workingYear){
            $(":input").removeAttr("disabled");
            centerControl('update');
        }
        else {
            if ( row['date_yyyy']==workingYear && row['date_mm']>workingMonth){
                $(":input").removeAttr("disabled");
                centerControl('update');
            } else {
                //按紐雖開啟...但改由新增按下時判斷月份, 是否可以進入資料庫
                // $("#new_btn").attr("disabled","disabled");
                // $("#create_btn").attr("disabled","disabled");
                $("#update_btn").attr("disabled","disabled");
                $("#delete_btn").attr("disabled","disabled");
                $("#main_form :input").attr("disabled","disabled");
            }
        };

    },
    onLoadSuccess: function(data,row) {
        //如果當年度沒資料, 就清空grid
        //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']
        var len = data.total;
        if (len == 0) {
            //沒有資料,清空子dg
            // Empty_datagrid($("#metrics_setup_dg"));
            centerControl('update');
        } else {
            $(this).datagrid('selectRow', currentRowIndex_east);
            if ($('#employee_info_easy_dg').datagrid('getRows').length > 0) {
                if ($(this).datagrid('getSelected') == null) {
                    $(this).datagrid('selectRow', 0);
                }
            }
        }
        // $('#searchYear').val('');
        conditions = "data.rows[i]['date_yyyy'] == main_form.date_yyyy.value && data.rows[i]['date_mm'] == main_form.date_mm.value";
        datagridSelectRow($(this),data,conditions,currentRowIndex_east);
    }
}


// east grid 和 center的main_form 同步
config.main_dg = {
    singleSelect: true,
    autoLoad: false,
    autoRowHeight: true,
    autoRowWidth: true,
    method: 'get',
    columns:[[
        {field:'order_number',title:'順序', width:40, align:'right',},
        {field:'order_item',title:'順序<br>細項', width:40, align:'right',},
        {field:'metrics_content',title:'衡量指標(一定要有數字)', width:750,
              formatter : function(value, row, index){
                return "<pre style='font-size: 100%;'>"+value+"</pre>";
            }
        },
        {field:'unit_Mcalc',title:'單<br>位', width:60, align:'center',},
        {field:'low_limit',title:'最低配分', width:80, align:'center',},
        {field:'allocation',title:'最高配分', width:80, align:'right',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
        {field:'score_type',title:'評核<br>方式', width:80, align:'center',},
        {field:'metrics_txt1', title:'',width:2,styler: function(value,row,index){return 'color:white;';}},   //color:white...隱藏內容用
        {field:'metrics_number', title:'',width:2,styler: function(value,row,index){return 'color:white;';}},
        {field:'metrics_txt2', title:'',width:2,styler: function(value,row,index){return 'color:white;';}}
    ]],
    rowStyler: function(index,row){
        if (row.allocation==0){
            return 'background-color:#ffffe0;color:blue;'; // return inline style
        }
    },
    onBeforeLoad:function(){
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function(index, row) {
        currentRowIndex_center = index;
        currentRow = row;
        currentKey = row[$('#main_dg').data().key];
        centerControl('update');
        setFormData(main_form,row);
        if (row['metrics_txt2']==undefined){
            main_form.metrics_txt2.value="";
        };
        if (row['low_limit']==undefined){
            main_form.low_limit.value="";
        };
    },
    onLoadSuccess: function(data,index,row) {
        rowCount_main_dg = data.total;
        // 計算grid指標分數
        var allocation_tot = 0;
        for (var i=0 ; i<rowCount_main_dg ; i++){
            allocation_tot += parseFloat(data.rows[i]['allocation']);
        }
        main_form.allocation_tot.value = allocation_tot.toFixed(2);
        // var rows = $(this).datagrid('getRows');
        c1 = "data.rows[i]['order_number'] == main_form.id_order_number.value";
        c2 = "data.rows[i]['order_item'] == main_form.id_order_item.value";
        conditions = c1 + "&&" + c2;
        //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']
        datagridSelectRow($(this),data,conditions,currentRowIndex_center);
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
    'search': {
        afterSearch: function(res){
            $("#main_dg").datagrid('loadData', res);
        }
    }
}


config.custom_mono_search_dlg = {
    resizable: true,
    modal:true,
    closed: true,
}

config.custom_complex_search_dlg  = {
    'dlg': {
        resizable: true,
        modal: true,
        closed: true,
    },
    'search': {
        afterSearch: function(res){
            $("#employee_info_easy_dg").datagrid('loadData', res);
        }
    }
}

$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var employeeUrl = $('#employee_info_easy_dg').data().source;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    // currentEvent = 'ready';
    centerControl('update');

    northSourceUrl = "/api/get_metrics_setup_common" ;
    $('#employee_info_easy_dg').datagrid({url:northSourceUrl});

    $('#main_dg').datagrid('reorderColumns', columnOrder);

    $('#id_order_number').change(function (){
        var thisVal = $(this).val();
        get_order_item(thisVal);
        if ( thisVal<1 || thisVal>50){
            alert("順序只能為1~50，錯誤的值將被清除");
            $(this).val("");
        }
    });


    $('#id_order_item').change(function (){
        var thisVal = $(this).val();
        if ( thisVal<0 || thisVal>50){
            alert("順序只能為0~50，錯誤的值將被清除");
            $(this).val("");
        }
    });

    $('#id_metrics_txt1').mouseenter(function (){
        $(this).attr('style','width:500px;height:125px;');
    });

    $('#id_metrics_txt1').mouseleave(function (){
        $(this).attr('style','width:500px;height:28px;');
    });

    $('#new_btn').bind('newEvent', function () {
        centerControl('new');
    });

     //只要選項一改變(main_form),main_dg的值就重新查詢
    $('#id_work_code').change(function(){
        main_dg_query();
        $('#main_dg').datagrid('reload');   //根據選到的內容重新查詢,此行不可刪
        get_order_number();
        // $('#new_btn').trigger('newEvent');
    });

    $('#id_date_yyyy').change(function (){
        var thisVal = parseInt($(this).val());
        if ( thisVal < workingYear){
            alert("年度不可小於評核年月，年度將設為工作年月");
            $(this).val(workingYear);
        } else {
            main_dg_query();
            $('#main_dg').datagrid('reload');   //根據選到的內容重新查詢,此行不可刪
            get_order_number();
            // $('#new_btn').trigger('newEvent');
        }
    });

    $('#id_date_mm').change(function(){
        var thisVal = parseInt($(this).val());
        var thisYear = parseInt($('#id_date_yyyy').val());
        if (thisYear==workingYear) {
            if (thisVal <= workingMonth) {
                alert("月份不可小於或等於評核年月，月份將清空");
                $(this).val('');
            } else {
                main_dg_query();
                $('#main_dg').datagrid('reload');   //根據選到的內容重新查詢,此行不可刪
                get_order_number();
                // $('#new_btn').trigger('newEvent');
            }
        } else {
            main_dg_query();
            $('#main_dg').datagrid('reload');   //根據選到的內容重新查詢,此行不可刪
            get_order_number();
            // $('#new_btn').trigger('newEvent');
        }
    });


    $('#id_low_limit').change(function (){
        var low_limit = parseFloat($(this).val());
        var allocation = parseFloat($('#id_allocation').val());
        if (low_limit>=allocation){
            alert('最低配分不可大於或等於最高配分，最低配分將清空');
            $(this).val('');
            $(this).focus();
        };
    });

    $('#id_allocation').change(function (){
　　　　　var low_limit = parseFloat($('#id_low_limit').val());
        var allocation = parseFloat($(this).val());
        if (allocation<=low_limit){
            alert('最高配分不可小於或等於最低配分，最高配將清空');
            $(this).val('');
            $(this).focus();
        };
    });



    $('#new_btn').click(function(){
　　　　　$("#main_form :input").removeAttr('disabled');  //因為$('#id_date_mm option')把『小於等於』目前的月份都移除了，所以，可以把欄位都打開哦！
        assign_work_code_options();
        get_order_number();

        main_form.elements[0].focus();
        $('#copy_btn').hide();
        $('#expand_btn').hide();
        centerControl('new');
    });


    $('#create_btn').click(function(){

        var thisYear = parseInt($('#id_date_yyyy').val());
        var thisMonth = parseInt($('#id_date_mm').val());
        var validResult = false;
        if (thisYear==workingYear) {
            if (thisMonth <= workingMonth) {
                alert("月份不可小於或等於評核年月，月份將清空");
                $('#id_date_mm').val('');
            } else {
                validResult = true;
            }
        } else if (thisYear < workingYear){
            alert("年度不可小於評核年月，年度將清空");
            $('#id_date_yyyy').val('');
        } else {
            validResult = true;
        }

        if (validResult) {
            // 新增
            if (!formValidate(main_form)) return;
            var data = getFormData(main_form);
            var new_allocation_tot = parseFloat(data.allocation_tot) + parseFloat(data.allocation);
            if (data.allocation == 0) {
                alert("*警 告**\n配分等於０，指標將失效，無法評分，警請注意。");
            }
            ;
            // allocation_tot 為暫時的欄位, 不存入資料庫()
            // 若未移除,會出現server 500 的錯誤(pymssql.DatabaseError)
            data['score_type'] = data.score_type_id;
            delete data.score_type_id;
            data['date_mm'] = data.date_mm_id;
            delete data.date_mm_id;
            delete data.allocation_tot;

            data['order_number']　= data.order_number_id;
            delete data.order_number_id;
            data['order_item']　= data.order_item_id;
            delete data.order_item_id;


            unit_txt = $('#id_unit_Mcalc').find("option:selected").text();
            data['metrics_content'] = main_form.metrics_txt1.value + main_form.metrics_number.value + unit_txt + main_form.metrics_txt2.value;
            if (valid_save_data()){
                $.post(
                formSourceUrl,
                data,
                function (res) {
                    if (res.success) {
                        currentEvent = 'new';
                        dg_reload();
                        alert('新增成功!');
                    } else {
                        currentEvent = null;
                        alert('錯誤');
                    }
                })
            }

            $('#copy_btn').show();
            $('#expand_btn').show();
        }
    });


    // 顯示~展開至員工~的對話方塊
    $('#expandCommon_btn').click(function () {
        textbox_onChange_expandCommon($('#commonExpandYear').textbox('getValue'),$('#commonExpandMonth').textbox('getValue'));

        $('#expandCommon_dd').attr('hidden',false);

        $('#expandCommon_dd').dialog({
            title: '請選取要展開的共同衡量指標，已評核月份，不可展開',
            width: 800,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });

        $('#expandTo_Common1').combobox({
            onChange: function (){
                var thisCommon= $(this).textbox('getValue');
                deptUrl = "/api/get_dept_data/"+thisCommon;
                $.get(
                    deptUrl,
                    function (res) {
                        if (res) {
                            optionTxt = res;
                            $('#expandDept').combobox({
                                valueField:'value',
                                textField:'text',
                                data: optionTxt,
                                });
                        }else {
                            optionTxt = null;
                        }
                    }
                )

            }
        })

        $('#expandDept').combobox(
            {
                onChange: function (){
                    var thisCommon = $('#expandTo_Common1').textbox('getValue');
                    var thisDept = $(this).textbox('getValue');
                    facoryEmployeeUrl = "/api/get_factory_employee_data/"+thisCommon+"/"+thisDept;
                    $.get(
                        facoryEmployeeUrl,
                        function (res) {
                            if (res) {
                                optionTxt = res;
                                $('#expandWorkCode').combobox({
                                    valueField:'value',
                                    textField:'text',
                                    data: optionTxt,
                                    });
                            }else {
                                optionTxt = null;
                            }
                        }
                    )
                }

            }
        );


        //來源年份不用限制小於工作年月
        $('#commonExpandYear').textbox({
            onChange: function () {
                var thisYear = $(this).textbox('getValue');
                var thisMonth = $('#commonExpandMonth').textbox('getValue');
                $('#commonExpandToYear1').textbox('setValue',thisYear);
                textbox_onChange_expandCommon(thisYear,thisMonth);
            }
        });

        //來源月份不用限制小於工作年月
        $('#commonExpandMonth').textbox({
            onChange: function () {
                var thisMonth = parseInt($(this).textbox('getValue'));
                if (thisMonth<0 || thisMonth>12) {
                    alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
                    $('#commonExpandMonth').textbox('setValue', '');
                }
                var thisYear = $('#commonExpandYear').textbox('getValue');
                textbox_onChange_expandCommon(thisYear,thisMonth);
            }
        });


        $('#commonExpandToYear1').textbox(
            {
                setValue:workingYear,
                onChange: function (){
                    thisYear = parseInt( $(this).textbox('getValue') );
                    if ( thisYear < workingYear) {
                        alert('年月小於等於評核年月,錯誤的年份將被清除');
                        $(this).textbox('setValue','')
                    }
                }

            }
        );

        $('#commonExpandStart').textbox({
            onChange: function () {
                var thisYear =parseInt($('#commonExpandToYear1').textbox('getValue'));
                var thisMonth = parseInt($(this).textbox('getValue'));
                if (thisMonth<0 || thisMonth>12) {
                    alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
                    $(this).textbox('setValue', '');
                }
                if (thisYear==workingYear){
                    if (thisMonth<=workingMonth){
                        alert('年月小於等於評核年月,錯誤的月份將被清除');
                        $(this).textbox('setValue', '');
                    }
                }
            }
        });

        $('#commonExpandEnding').textbox({
            onChange: function () {
                var thisYear = parseInt($('#commonExpandToYear1').textbox('getValue'));
                var thisMonth = parseInt($(this).textbox('getValue'));
                if (thisMonth<0 || thisMonth>12) {
                    alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
                    $(this).textbox('setValue', '');
                }
                if (thisYear==workingYear){
                    if (thisMonth<=workingMonth){
                        alert('年月小於等於評核年月,錯誤的月份將被清除');3
                        $(this).textbox('setValue', '');
                    }
                }
            }
        });

        $('#expandCommon_clear').click(function (){
            $('#expandCommon_form')[0].reset();
        });


        $('#expandCommon_sumit').click(function () {
            var startMonth = parseInt($('#commonExpandStart').textbox('getValue'));
            var endingMonth = parseInt($('#commonExpandEnding').textbox('getValue'));
            if ( startMonth>endingMonth ){
               alert('起始月份輸入錯誤');
            } else {
                alert("...展開中...\n\n請梢待數分鐘,勿關閉畫面,勿再按一次按鈕");
                expandCommonSourceUrl = $('#expandCommon_form').attr('action');
                data = getFormData(expandCommon_form);
                $.post(
                    expandCommonSourceUrl,
                    data,
                    function (res) {
                        if (res.success) {
                            dg_reload();
                            alert('展開成功');
                        }
                    });
                }
        });

     });


    // 顯示~收回~的對話方塊
    $('#recallCommon_btn').click(function () {
        $('#recallYear').textbox('setValue',workingYear);

        $('#recallCommon_dd').attr('hidden',false);

        $('#recallCommon_dd').dialog({
            title: '請選取要收回的共同衡量指標月份(已評核月份,不可收回)',
            width: 600,
            height: 'auto',
            closed: false,
            cache: false,
            modal: true,
        });

         commonUrl = "/api/get_employee_common_data/";
        $.get(
            commonUrl,
            function (res) {
                if (res) {
                    optionTxt = res;
                    $('#recallCommon').combobox({
                        valueField:'value',
                        textField:'text',
                        data: optionTxt,
                        });
                }else {
                    optionTxt = null;
                }
            }
        )

        $('#recallCommon').combobox({
            onChange: function (){
                var thisCommon= $('#recallCommon').textbox('getValue');
                deptUrl = "/api/get_dept_data/"+thisCommon;
                $.get(
                    deptUrl,
                    function (res) {
                        if (res) {
                            optionTxt = res;
                            $('#recallDept').combobox({
                                valueField:'value',
                                textField:'text',
                                data: optionTxt,
                                });
                        }else {
                            optionTxt = null;
                        }
                    }
                )

            }
        })


        $('#recallDept').combobox(
            {
                onChange: function (){
                    var thisCommon = $('#recallCommon').textbox('getValue');
                    var thisDept = $(this).textbox('getValue');
                    facoryEmployeeUrl = "/api/get_factory_employee_data/"+thisCommon+"/"+thisDept;
                    $.get(
                        facoryEmployeeUrl,
                        function (res) {
                            if (res) {
                                optionTxt = res;
                                $('#recallWorkCode').combobox({
                                    valueField:'value',
                                    textField:'text',
                                    data: optionTxt,
                                    });
                            }else {
                                optionTxt = null;
                            }
                        }
                    )
                }

            }
        );

        $('#recallYear').textbox(
            {
                setValue:workingYear,
                onChange: function (){
                    thisYear = parseInt( $(this).textbox('getValue') );
                    if ( thisYear < workingYear) {
                        alert('年月小於等於評核年月,錯誤的年份將被清除');
                        $(this).textbox('setValue','')
                    }
                }

            }
        );


        $('#recallYear').textbox(
            {
                setValue:workingYear,
                onChange: function (){
                    thisYear = parseInt( $(this).textbox('getValue') );
                    if ( thisYear < workingYear) {
                        alert('年月小於等於評核年月,錯誤的年份將被清除');
                        $(this).textbox('setValue','')
                    }
                }

            }
        );

        $('#recallStart').textbox({
            onChange: function () {
                var thisYear = parseInt($('#recallYear').textbox('getValue'));
                var thisMonth = parseInt($(this).textbox('getValue'));
                if (thisMonth<0 || thisMonth>12) {
                    alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
                    $(this).textbox('setValue','')
                } else {
                    if (thisYear==workingYear){
                        if (thisMonth<=workingMonth){
                            alert('年月小於等於評核年月,錯誤的月份將被清除');
                            $(this).textbox('setValue','')
                        }
                     }
                }

            }
        });

        $('#recallEnding').textbox({
            onChange: function () {
                var thisYear = parseInt($('#recallYear').textbox('getValue'));
                var thisMonth = parseInt($(this).textbox('getValue'));
                if (thisMonth<0 || thisMonth>12) {
                    alert('月份應介於0<年度目標> 及 1~12，錯誤的月份將被清除');
                    $(this).textbox('setValue','')
                } else {
                    if (thisYear==workingYear){
                        if (thisMonth<=workingMonth){
                            alert('年月小於等於評核年月,錯誤的月份將被清除');
                            $(this).textbox('setValue','')
                        }
                     }
                }
            }
        });


        $('#recallCommon_clear').click(function (){
            $('#recallCommon_form')[0].reset();
        });


        $('#recallCommon_sumit').click(function () {
            data = getFormData(recallCommon_form); //取得年度,起始月份,終止月份
            recallSourceUrl = $('#recallCommon_form').attr('action');
            var confirm_msg1 = "按下「確定收回」後，收回年月的『共同指標』，將被『刪除』。";
            var confirm_msg2 = "\n\n***在您按下『確定收回』前***\n***請您再次確認***";
            var confirm_msg3 = "\n\n您確定要『收回』嗎?";
            var confirm_msg4 = "\n...報行收回時...請梢待數分鐘,勿關閉畫面,勿再按一次按鈕";
            var sure = confirm(confirm_msg1 + confirm_msg2 + confirm_msg3 + confirm_msg4);
            if (sure) {
                $.post(
                    recallSourceUrl,
                    data,
                    function (res) {
                        if (res.success) {
                            dg_reload();
                            alert('收回成功');
                        }
                    });
            } else {
                alert('***您取消了『收回』***\n\n ***系統並未執行『收回』作業***');
            }
        })
    });


    // 顯示~"展開1~12月"~的對話方塊
    $('#expand_btn').click(function () {
        // var expandYear = workingYear;
        $('#expandYear').textbox('setValue',workingYear);


        if (workingMonth==12){
            alert('本年度已無法展開，評核月份為１２月，年度將清空');
            $('#expandYear').textbox('setValue','');
        }

        textbox_onChange_expand(workingYear);
        $('#expandYear').textbox({
            onChange: function () {
                expandYear = parseInt($(this).textbox('getValue'));
                if (expandYear<workingYear) {
                    alert('年月小於評核年月,將清空');
                    $(this).textbox('setValue','');
                } else if (expandYear==workingYear) {
                    if (workingMonth == 12) {
                        alert('本年度已無法展開，評核月份為１２月，年度將清空');
                        $(this).textbox('setValue', '');
                    }
                }
                textbox_onChange_expand($(this).textbox('getValue'))
            }
        })

        $('#expand_dd').attr('hidden',false);
        $('#expand_dd').dialog({
            title: '請選取要展開的工號',
            width: 500,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });

        $('#expand_clear').click(function (){
            $('#expand_form')[0].reset();
        });


        $('#expand_sumit').click(function () {
            copySourceUrl = $('#expand_form').attr('action');
            data = getFormData(expand_form); //取得來源工號, 複製1, 複製2, 複製3
            $.post(
            copySourceUrl,
            data,
            function (res) {
                if (res.success) {
                    dg_reload();
                    alert('展開成功');
                }
            });
        });

     });


    // 顯示複製對話方塊
    $('#copy_btn').click(function () {
        $('#copy_dd').attr('hidden',false);

        $('#copy_dd').dialog({
            title: '請選取要複製的工號',
            width: 800,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });


        //easyUi的寫法(copyFrom_val2使用了easyUI的class，所以jquery的event會失效,要使用easyUI的event)
        //輸入完年份/月份，重新取得符合標準的工號
        // $('#copyFrom_val2').textbox('setValue', workingMonth);

        textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));

        //複製的來源年月, 不需防呆
        $('#copyFrom_val1').textbox({
              onChange: function(){
                  textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));
                  }
		});

      //複製的來源年月, 不需防呆
        $('#copyFrom_val2').textbox({
              onChange: function(){
                  textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));
              }
		});

         //複製的目的年月, 需要防呆
        $('#copyFrom_id').combobox({
            onChange:function (){
                //只要有選擇工號,就自動帶出來源的年月
                for (var i=1;i<=6;i++){
                    id1 = "$('#copyToId1_"+i.toString()+"')";
                    id2 = "$('#copyTo_val1_"+i.toString()+"')";
                    id3 = "$('#copyTo_val2_"+i.toString()+"')";
                    copyto_textbox_value(eval(id1),eval(id2),eval(id3));    //eval 動態變數
                }
            }
        });

        for (var i=1;i<=6;i++){
            id2 = "$('#copyTo_val1_"+i.toString()+"')";
            id3 = "$('#copyTo_val2_"+i.toString()+"')";
            copyto_YearMonth_onChange(eval(id2),eval(id3));    //eval 動態變數
        }

        copyToSourceUrl = "/api/get_employee_common_data";
          $.get(
            copyToSourceUrl,
            function (res) {
                if (res) {
                    // copyTo : 存在的工號，才能複製
                    var copyNum = 6;
                    optionTxt = res;
                    for (var i=1;i<=copyNum;i++){
                        copyTo = "#copyToId1_"+i;
                        $(copyTo).combobox({
                            valueField:'value',
                            textField:'text',
                            data: optionTxt,
                            });
                    }



                    $('#copy_clear').click(function (){
                        $('#copy_form')[0].reset();
                    });

                    $('#copy_submit').click(function (){
                        copySourceUrl = $('#copy_form').attr('action');
                        data = getFormData(copy_form); //取得來源工號, 複製1, 複製2, 複製3
                        $.post(
                            copySourceUrl,
                            data,
                            function (res){
                               if (res.success) {
                                   dg_reload();
                                   alert('複製成功');
                               } else {
                                   alert('複製失敗!');
                               }
                            });
                    });
                }else {
                    optionTxt = null;
                }
            }
        )
     });


    $('#east_search').click(function (){
        eastSourceUrl = "/api/get_metrics_setupDate_data/"+work_code_key+"/"+$('#searchYear').val();
        $('#metrics_setupDate_dg').datagrid({
            url : eastSourceUrl,
            columns:[[
                // {field:'work_code',title:'工號',},
                {field:'date_yyyy',title:'年度',width:65,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
                {field:'date_mm',title:'月(季)',width:65,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
            ]],
            onLoadSuccess: function (data) {
                $(this).datagrid('selectRow', 0);
            }
        });
    });

    $('#cancel_btn').click(function(){
         $('#copy_btn').show();
         $('#expand_btn').show();
         currentEvent = 'ready';
         dg_reload();
    });

    $('#update_btn').click(function(){
        // 更新
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        var currentSelected = $("#main_dg").datagrid('getSelected')
        // 新的配分 = 配分總合 - 目前選擇的配分 + 目前選擇修改的配分
        var new_allocation_tot = parseFloat(data.allocation_tot)-parseFloat(currentSelected.allocation)+parseFloat(data.allocation);
        if (data.allocation==0){
            alert("*警 告**\n配分等於０，指標將失效，無法評分，警請注意。");
        };
        // allocation_tot 為暫時的欄位, 不存入資料庫()
        // 若未移除,會出現server 500 的錯誤(pymssql.DatabaseError)
        data['score_type'] = data.score_type_id;
        delete data.score_type_id;
        data['date_mm']　= data.date_mm_id;
        delete data.date_mm_id;
        delete data.allocation_tot;

        data['order_number']　= data.order_number_id;
        delete data.order_number_id;
        data['order_item']　= data.order_item_id;
        delete data.order_item_id;

        unit_txt = $('#id_unit_Mcalc').find("option:selected").text();
        data['metrics_content'] = main_form.metrics_txt1.value + main_form.metrics_number.value + unit_txt + main_form.metrics_txt2.value;
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function (res) {
                if (res.success) {
                    currentEvent = 'update';
                    $('#main_dg').datagrid('reload');
                    $('#id_metrics_txt1').attr('style','width:500px;height:28px;');
                    alert('更新成功!');
                } else {
                    currentEvent =  null;
                    alert('hr01.js---錯誤');
                }
            })
    });

    $('#delete_btn').click(function(){
         if (!confirm("若有計算方式存在『刪除不會成功』請先刪除計算方式\n請確認您要刪除\n再按下『確定』")) return;

         // 刪除
         $.get(formSourceUrl + '/' + currentKey,
             function(res) {
                 if(res.success) {
                     currentEvent = 'delete';
                     dg_reload();
                     alert('刪除成功!')
                 } else {
                     currentEvent = null;
                     alert('錯誤');
                 }
             }
         );


    });


     $("#custom_mono_search_btn").click(function(){
        $('#custom_mono_search_dlg').dialog('open');
        $('#custom_mono_search_dlg').dialog('open');
    });

    $("#custom_cpx_search_btn").click(function(){
        $('#c_cpx_search_dlg ').dialog('open');
    });

    $('#search_btn_custom').click(function(){
        var searchParam = custom_monoSearchForm.field_custom.value +
                          '=' + custom_monoSearchForm.keyword_custom.value;
        var url = $('#custom_mono_search_dlg').data().source + '?' + searchParam;
        $('#custom_mono_search_dlg').datagrid({
            url: url
        });
        rowCount = $('#employee_info_easy_dg').datagrid('getData').total;
        $('#custom_mono_search_dlg').dialog('close');
        $('#employee_info_easy_dg').datagrid('selectRow', 0);
    });

});





