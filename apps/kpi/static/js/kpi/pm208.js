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
        // if (fieldName=='confirmed'){
        //     formData[fieldName] = 'False';
        // }
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
            fields[i].value = row[fieldName];
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
    Swork_code = main_form.work_code.value;
    Sdate_yyyy = main_form.date_yyyy.value;
    Sdate_mm = main_form.date_mm.value;
    sequence_numberUrl = "/api/get_metrics_order_number/" +Swork_code+"/"+Sdate_yyyy+"/"+Sdate_mm;
        $.get(
            sequence_numberUrl,
            function (res) {
                if (res) {
                    main_form.order_number.value = res.next_number;
                    get_order_item(res.next_number);
                }else {
                    main_form.order_number.value = 1;
                }
            }
        )
}


function get_order_item(thisVal){
    Swork_code = main_form.work_code.value;
    Sdate_yyyy = main_form.date_yyyy.value;
    Sdate_mm = main_form.date_mm.value;
    Sorder_number = thisVal;
    sequence_numberUrl = "/api/get_metrics_order_item/" +Swork_code+"/"+Sdate_yyyy+"/"+Sdate_mm+"/"+Sorder_number;
        $.get(
            sequence_numberUrl,
            function (res) {
                if (res) {
                    main_form.order_item.value = res.next_number;
                }else {
                    main_form.order_item.value = 0;
                }
            }
        )
}




function textbox_onChange_expand(expandYear){
       copyToSourceUrl = "/api/get_employee_data/" + userId +"_expand_"+expandYear;
        $.get(
            copyToSourceUrl,
            function (res) {
                if (res) {
                    optionTxt = res;
                    // copyTo : 存在的工號，才能複製
                    var copyNum = 6;
                    for (var i=1;i<=copyNum;i++){
                        copyTo = "#expandTo_WorkCode"+i;
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
    copyFromSourceUrl = "/api/get_employee_data/"+userId+"_copy_"+id1.val()+"_"+id2.val();
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
    id1.textbox({ value:$('#copyFrom_val1').val()  });    //easyUI textbox給值的方式
    id2.textbox({ value:$('#copyFrom_val2').val()  });   //easyUI textbox給值的方式
}


function copyto_textbox_value(id1,id2,id3){
        id1.combobox({
            onChange: function(param){
            textbox_value_from(id2,id3)
        }
    });

    id3.textbox({
        onChange: function(){
            to_month = parseInt(id3.val());
            if (to_month<0 || to_month>12){
                alert('月份應介於0<年度目標> 及 1~12,錯誤的月份將被清除');
                $(this).textbox('setValue', '');
            }
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





// 移除共同指標的工號
function filter_work_code_options(){
    var option_length = $('#id_work_code option').length;
     $('#id_work_code option').each(function (){
         //移除共同指標
         if ( $(this).val().search("-") > -1) {
            $(this).remove();
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

     sub_employee_Url = "/api/get_employee_data/" + userId;

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

function centerControl(event) {
    main_form.id_metrics_type.disabled=true;
    main_form.date_yyyy.disabled=true;
    main_form.date_mm.disabled=true;
    // main_form.date_yyyy.value=workingYear;
    main_form.allocation_tot.disabled=true;
    main_form.confirmed.disabled=true;
    main_form.id_metrics_type.options[2].selected=true;
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
              {field:'work_code',title:'工號', width:80,},
              {field:'chi_name',title:'姓名', width:80,},
              {field:'dept_name',title:'部門', width:150,},
              {field:'pos_name',title:'職位', width:80, },
              // {field:'director_id',title:'主管工號', width:80,},
              // {field:'director_name',title:'主管姓名', width:80,},
              {field:'arrival_date',title:'到職日', width:90, align:'center',},
              {field:'resign_date',title:'離職日', width:90, align:'center',},
              {field: 'rank',title:'職等', width:40, align:'center',},
              {field: 'bonus_factor',title:'點數', width:40, align:'center',},
              // {field: 'eval_class',title:'KPI/BSC', width:70, align:'center',},
              {field: 'nat',title:'國籍', width:80, align:'center',},
              {field: 'factory_name',title:'公司', width:80, align:'center',},
              {field: 'factory_area',title:'廠區', width:80, align:'center',},
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
    },
    onLoadSuccess: function(data) {
         //不是主管,又開了衡量指標設定
         // if ( data.total == 0) {
         if ( is_director == 'False') {
            $("#main_dg").datagrid({
                queryParams: {
                    work_code_id: '',
                    date_yyyy: 0,
                    date_mm:0,
                },
            });
            // main_form.id_work_code.value = '';
            // controlDisabled();             //改由programauth來判斷, 是否要檢查人事基本資料的eval_class,director, 若是主管且有管人, 才可新增相關權限,目前先做人為判斷
            Empty_centerControl();
            $(":input").attr("disabled","disabled");    //不可使用, 連登出也disabled(待日後有空, 再使用, 然後單獨恢復"登出"按鈕)
            $("#logout").removeAttr("disabled");
            $("#factory_select").removeAttr("disabled");
            $("#change_factory_btn").removeAttr("disabled");
        } else {
            //個人指標:共同指標不出現
            var len = data.total;
            if (len==0){
                //沒有資料,清空main_dg
                // for ( var i=0,thislen=$('#main_dg').datagrid('getRows').length;i<thislen;i++ ){
                //     $('#main_dg').datagrid('deleteRow',0);
                //     Empty_centerControl();
                // }
                centerControl('update');
                // alert(workingYear+'年度\n無任何資料\n 請新增');
            } else {
                var i = 0;
                while (i < len) {
                    if (data.rows[i]['work_code'].search("-") > -1) {
                        //有找到的("共同指標")，刪除
                        $(this).datagrid('deleteRow', i);
                        len--;
                    } else {
                        i++;
                    }
                    ;
                }
            }
            /*  function datagridSelectRow 模組化前的原型
             switch (currentEvent) {
                case 'new':
                    for ( var i=0, len= data.rows.length; i < len ; i++){
                        if (data.rows[i]['work_code'] == main_form.id_work_code.value) {
                            $(this).datagrid('selectRow', i);
                            break;    //for的break
                        }
                    }
                    clearError();
                    break;           //switch的break
                case 'update':
                    $(this).datagrid('selectRow', currentRowIndex);
                case 'delete':     //刪除之後,INDEX不變,還是原來的位置
                    //刪除最後一筆資料時, 還是移到最後一筆資料
                    if (currentRowIndex == data.rows.length) {
                        $(this).datagrid('selectRow', currentRowIndex - 1);
                    } else {
                        $(this).datagrid('selectRow', currentRowIndex);
                    }
                    clearError();
                    break
                default:
                    $(this).datagrid('selectRow', 0);
                    break;
            }
             */
             // if ( data.rows.length == 0 ){
             //        alert( "data.rows.length=\n"+data.rows.length );
             //        for (var i=0,len=$('#main_dg').datagrid('getRows').length;i<=len;i++) {
             //            $('#main_dg').datagrid('deleteRow',i);
             //            alert(i);
             //        }
             // } else {
             conditions = "data.rows[i]['work_code'] == main_form.id_work_code.value";
             //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']
             datagridSelectRow($(this), data, conditions, currentRowIndex_north);
             // }
         }
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
        $("#main_dg").datagrid({
            queryParams: {
                work_code_id: row['work_code'],
                date_yyyy: row['date_yyyy'],
                date_mm: row['date_mm'],
            },
        });
        main_form.work_code.value =row['work_code'];
        main_form.date_yyyy.value = row['date_yyyy'];
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
                // $("#cancel_btn").attr("disabled","disabled");
                $("#main_form :input").attr("disabled","disabled");
            }
        };
    },
    onLoadSuccess: function(data,row) {
        // find_month = parseInt(workingMonth)+1;
        // findRowDatas(workingYear, find_month);
        //如果當年度沒資料, 就清空grid
        // if ( data.total == 0) {
        if ( is_director == 'False') {
            $("#main_dg").datagrid({
                queryParams: {
                    work_code_id: '',
                    date_yyyy: 0,
                    date_mm:0,
                },
            });
            Empty_centerControl();
            $(this).datagrid('unselectRow');
        } else {
              conditions = "data.rows[i]['date_yyyy'] == main_form.date_yyyy.value && data.rows[i]['date_mm'] == main_form.date_mm.value";
            //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']
            datagridSelectRow($(this),data,conditions,currentRowIndex_east);
            rowCount = data.total;``
        }
        // $('#searchYear').val('');

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
        {field:'order_number',title:'順序', width:50, align:'right',},
        {field:'order_item',title:'順序<br>細項', width:50, align:'right',},
        {field:'asc_desc',title:'計算方式<br>遞增/遞減', width:90, align:'center',},
        {field:'asc_desc_score',title:'得分<br>遞增/遞減', width:89, align:'center',},
        {field:'metrics_content',title:'衡量指標(一定要有數字)', width:650,
              formatter : function(value, row, index){
                return "<pre style='font-size: 100%;'>"+value+"</pre>";
            }
        },
        {field:'unit_Mcalc',title:'單<br>位', width:55, align:'center',},
        {field:'allocation',title:'配分&nbsp;<br>(權重)', width:80, align:'right',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
        {field:'confirmed',title:'確認', width:45, align:'center',},
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
    },
    onLoadSuccess: function(data,index,row) {
        rowCount_main_dg = data.total;
        // 計算grid指標分數
        var allocation_tot = 0;
        for (var i=0 ; i<rowCount_main_dg ; i++){
            // 去除共同指標的配分
            if (data.rows[i]['order_number'] < 900){
                allocation_tot += parseFloat(data.rows[i]['allocation']);
            }
        }

        if (rowCount_main_dg==0){
            centerControl('update');
        } else {
            var i = 0;
            while (i < rowCount_main_dg) {
                if (data.rows[i]['order_number'] > 900) {
                    //有找到的("共同指標")，刪除
                    $(this).datagrid('deleteRow', i);
                    rowCount_main_dg--;
                } else {
                    i++;
                }
                ;
            }
        }

        // main_form.allocation_tot.value = allocation_tot.toString();
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
    currentEvent = 'ready';

    northSourceUrl = "/api/get_metrics_setup_subs_data/" + userId;
    $('#employee_info_easy_dg').datagrid({url:northSourceUrl});

    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#id_order_number').change(function (){
        var thisVal = $(this).val();
        get_order_item(thisVal);
        if ( thisVal<1 || thisVal>30){
            alert("順序只能為1~30，錯誤的值將被清除");
            $(this).val("");
        }
    });


    $('#id_order_item').change(function (){
        var thisVal = $(this).val();
        if ( thisVal<0 || thisVal>30){
            alert("順序只能為0~30，錯誤的值將被清除");
            $(this).val("");
        }
    });

    $('#id_metrics_txt1').mouseenter(function (){
        $(this).attr('style','width:500px;height:125px;');
    });

    $('#id_metrics_txt1').mouseleave(function (){
        $(this).attr('style','width:500px;height:28px;');
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

    $('#new_btn').click(function(){
        $("#main_form :input").removeAttr('disabled');  //因為$('#id_date_mm option')把『小於等於』目前的月份都移除了，所以，可以把欄位都打開哦！
        main_form.elements[0].focus();
        assign_work_code_options();
        get_order_number();

        main_form.elements[0].focus();
        $('#copy_btn').hide();
        $('#expand_btn').hide();
        $('#batch_dele_btn').hide();
        centerControl('new');
        //只要選項一改變(main_form),main_dg的值就重新查詢
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
            if (new_allocation_tot > 100) {
                alert("**錯 誤***\n配分合計：" + new_allocation_tot + "＞１００\n**不可新增**");
            } else {
                if (data.allocation == 0) {
                    alert("*警 告**\n配分等於０，指標將失效，無法評分，警請注意。");
                }
                ;
                // allocation_tot 為暫時的欄位, 不存入資料庫()
                // 若未移除,會出現server 500 的錯誤(pymssql.DatabaseError)
                data['asc_desc'] = data.asc_desc_id;
                delete data.asc_desc_id;
                data['asc_desc_score'] = data.asc_desc_score_id;
                delete data.asc_desc_score_id;
                data['date_mm'] = data.date_mm_id;
                delete data.date_mm_id;
                delete data.allocation_tot;
                unit_txt = $('#id_unit_Mcalc').find("option:selected").text();
                data['metrics_content'] = main_form.metrics_txt1.value + main_form.metrics_number.value + unit_txt + main_form.metrics_txt2.value;
                $.post(
                    formSourceUrl,
                    data,
                    function (res) {
                        if (res.success) {
                            currentEvent = 'new';
                            dg_reload();
                            allocation_x = 100 - new_allocation_tot;
                            if (allocation_x > 0) {
                                a_msg = "\n\n***警告***\n    總配分不足100\n    新增後尚缺" + allocation_x.toFixed(2) + "分";
                            } else {
                                a_msg = "\n\n---總配分已達100分---";
                            }
                            alert('新增成功!' + a_msg);
                        } else {
                            currentEvent = null;
                            alert('錯誤');
                        }
                    })
            }
            ;
            $('#copy_btn').show();
            $('#expand_btn').show();
            $('#batch_dele_btn').show();
        }
    });

    $('#batch_dele_btn').click(function () {
        $('#batch_dele_dd').attr('hidden',false);

        $('#batch_dele_dd').dialog({
            title: '請選取要刪除的工號',
            width: 600,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });


        sub_employee_Url = "/api/get_employee_data/" + userId;
        $.get(
            sub_employee_Url,
            function (res) {
                if (res) {
                    optionTxt = res;
                    $('#deleWorkCode').combobox({
                        multiple: true,
                        valueField: 'value',
                        textField: 'text',
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


        $('#batch_dele_clear').click(function (){
            $('#deleWorkCode').combobox('setValue','');
            $('#deleYear').textbox('setValue','');
            $('#deleMonthBegin').textbox('setValue','');
            $('#deleMonthEnd').textbox('setValue','');
        });



        $('#batch_dele_sumit').click(function () {
            var data = {};
            data['deleWorkCode'] = $('#deleWorkCode').val();
            data['deleYear'] = $('#deleYear').val();
            data['deleMonthBegin'] = $('#deleMonthBegin').val();
            data['deleMonthEnd'] = $('#deleMonthEnd').val();
            /*
            console.log(data.deleWorkCode, data.deleYear, data.deleMonthBegin, data.deleMonthEnd);
            console.log(data.deleWorkCode == '');
            console.log(data.deleYear == '');
            console.log(data.deleMonthBegin == '');
            console.log(data.deleMonthEnd == '');
             */
            err_msg = ''
            err = false
            if (parseInt(data.deleYear) < workingYear){
                err_msg += '年度小於評核年度\n';
                err = true;
            }

            if (parseInt(data.deleMonthEnd)<parseInt(data.deleMonthBegin)){
                err_msg += '終止月份小於等於起始月份\n';
                err = true;
            }

            if (parseInt(data.deleYear) == workingYear){
                if (parseInt(data.deleMonthBegin)<=workingMonth){
                    err_msg += '起始月份小於等於評核月份\n';
                    err = true;
                }
                if (parseInt(data.deleMonthEnd)<=workingMonth){
                    err_msg += '終止月份小於等於評核月份\n';
                    err = true;
                }
            }
            if (err){
                alert(err_msg);
            } else {
                if (data.deleWorkCode == '' || data.deleYear == '' || data.deleMonthBegin == '' || data.deleMonthEnd == '') {
                    alert('資料輸入錯誤');
                } else {
                    var batch_dele_sure = confirm("整批刪除是很危險的動作\n衡量指標及計算方式將一併刪除\n請再次確認您要刪除的範圍\n再按下『確定』");
                    /*
                    $('#batch_dele_dd').dialog({closed: true,});
                    $('#submit_batch_dele_dd').attr('hidden',false);

                    $('#submit_batch_dele_dd').dialog({
                        title: '批次刪除確認',
                        width: 600,
                        height: 'auto',
                        closed: false,
                        cache: false,
                        modal: true,
                    });
                     */
                    // console.log(batch_dele_sure);
                    if (batch_dele_sure) {
                        batchDeleSourceUrl = '/api/metrics_setup_batch_dele/';

                        $.post(
                            batchDeleSourceUrl,
                            data,
                            function (res) {
                                if (res.success) {
                                    dg_reload();
                                    alert('批次刪除成功');
                                    $('#batch_dele_dd').dialog({closed: true,});
                                } else {
                                    alert('批次刪除失敗');
                                }
                            });
                    }
                }
            }
        });
    })


  // 顯示展開的對話方塊
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
                expandYear = $(this).textbox('getValue');
                if (expandYear<workingYear) {
                    alert('年月小於評核年月,將清空');
                    $(this).textbox('setValue','');
                } else if (expandYear==workingYear) {
                    if (workingMonth==12){
                        alert('本年度已無法展開，評核月份為１２月，年度將清空');
                        $(this).textbox('setValue','');
                    }
                } else {
                    textbox_onChange_expand($(this).textbox('getValue'));
                }
            }
        })

        $('#expand_dd').attr('hidden',false);
        $('#expand_dd').dialog({
            title: '請選取要展開的工號',
            width: 575,
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
            // if (data['expandYear'] == '') {
            //     alert('未輸入年度');
            // } else {
                $.post(
                copySourceUrl,
                data,
                function (res) {
                    if (res.success) {
                        dg_reload();
                        alert('展開成功');
                    }
                });
            // }
        });
        
     });


    // 顯示複製對話方塊
    $('#copy_btn').click(function () {
        $('#copy_dd').attr('hidden',false);

        $('#copy_dd').dialog({
            title: '請選取要複製的工號',
            width: 600,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });



        //easyUi的寫法(copyFrom_val2使用了easyUI的class，所以jquery的event會失效,要使用easyUI的event)
        //輸入完年份/月份，重新取得符合標準的工號

        // textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));

        //複製的來源年月, 不需防呆
        $('#copyFrom_val1').textbox({
              onChange: function(){
                  textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));
                  }
		});

        $('#copyFrom_val2').textbox({
              onChange: function(){
                  textbox_onChange_copy($('#copyFrom_val1'),$('#copyFrom_val2'),$('#copyFrom_id'));

                  }
		});



        /*
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
         */

        //複製的目的年月, 需要防呆
        for (var i=1;i<=6;i++){
            id2 = "$('#copyTo_val1_"+i.toString()+"')";
            id3 = "$('#copyTo_val2_"+i.toString()+"')";
            copyto_YearMonth_onChange(eval(id2),eval(id3));    //eval 動態變數
        }


        copyToSourceUrl = "/api/get_employee_data/"+userId;
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




    $('#south_search_open').click(function (){
        $('#south_search_dd').attr('hidden',false);

        $('#south_search_dd').dialog({
            title: '指標資料搜尋',
            width: 300,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });



        $('#south_search_sumit').click(function(){
            searchWorkCode = $('#searchWorkCode').val();
            searchChiName =$('#searchChiName').val();
            searchDept =$('#searchDept').val();

            //若未給x,會認定沒有此參數,url=/api/get_metrics_setup_data///,會找不到
            //給了x,才會有參數
            if (searchWorkCode == ''){
                searchWorkCode = 'x'
            }
            if (searchChiName == ''){
                searchChiName = 'x'
            }
            if (searchDept == ''){
                searchDept = 'x'
            }
            southSourceUrl = "/api/get_metrics_setup_data/"+searchWorkCode +"/"+searchChiName+"/"+searchDept+"/"+ userId;
            $('#employee_info_easy_dg').datagrid({url : southSourceUrl});
        });
        $('#south_search_clear').click(function (){
            $("#south_search_dd input").val('');
        });
    });


    $('#cancel_btn').click(function(){
         $('#copy_btn').show();
         $('#expand_btn').show();
         $('#batch_dele_btn').show();
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
        if (new_allocation_tot>100){
            alert("**錯 誤***\n配分合計："+new_allocation_tot+"＞１００\n**不可修改**");
        }
        else {
            if (data.allocation==0){
                alert("*警 告**\n配分等於０，指標將失效，無法評分，警請注意。");
            };
            // allocation_tot 為暫時的欄位, 不存入資料庫()
            // 若未移除,會出現server 500 的錯誤(pymssql.DatabaseError)
            data['asc_desc'] = data.asc_desc_id;
            delete data.asc_desc_id;
            data['asc_desc_score'] = data.asc_desc_score_id;
            delete data.asc_desc_score_id;
            data['date_mm']　= data.date_mm_id;
            delete data.date_mm_id;
            delete data.allocation_tot;
            // console.log(JSON.stringify(data));
            unit_txt = $('#id_unit_Mcalc').find("option:selected").text();
            data['metrics_content'] = main_form.metrics_txt1.value + main_form.metrics_number.value + unit_txt + main_form.metrics_txt2.value;
            $.post(
                formSourceUrl + '/' + currentKey,
                data,
                function (res) {
                    if (res.success) {
                        currentEvent = 'update';
                        $('#main_dg').datagrid('reload');
                        allocation_x = 100 - new_allocation_tot;
                        if (allocation_x > 0){
                            a_msg = "\n\n***警告***\n    總配分不足100\n    更新後尚缺"+allocation_x+"分";
                        } else {
                            a_msg = "\n\n---總配分已達100分---";
                        }
                        $('#id_metrics_txt1').attr('style','width:500px;height:28px;');
                        alert('更新成功!'+a_msg);
                    } else {
                        currentEvent =  null;
                        alert('hr01.js---錯誤');
                    }
                }
            )
        };
    });

    $('#delete_btn').click(function(){
       // 刪除
       if (!confirm('若有計算方式存在『刪除不會成功』請先刪除計算方式\n請確認您要刪除\n再按下『確定』')) return;
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
        });
    });


     $("#custom_mono_search_btn").click(function(){
        $('#custom_mono_search_dlg').dialog('open');
    });

    $("#custom_cpx_search_btn").click(function(){
        $('#c_cpx_search_dlg ').dialog('open');
    });

    // $('#custom_monoSearchForm').submit(false);

    // $('#custom_monoSearchForm').keydown(function(e){
    //     if(e.keyCode==13) $('#search_btn_custom').click();
    // });

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

    //過去我們在 beforeunload 事件可以自訂提示訊息，這個功能在 Chrome v51 (2016/04) 時被取消了，理由是防止 beforeunload 的自訂訊息被用來做為詐騙用途。
    //https://developers.google.com/web/updates/2016/04/chrome-51-deprecations?hl=en#remove_custom_messages_in_onbeforeunload_dialogs
    /*
    window.onbeforeunload = function(e) {
        confirm("xxxxxxxxx");
        e.returnValue = "sure";
    };
     */



});




