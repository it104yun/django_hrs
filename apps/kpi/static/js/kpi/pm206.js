function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for (var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        //# _id 結尾通常是 foreignkey
        if (field.type === 'select-one') {
            formData[fieldName + '_id'] = field.value;
        } else if (field.type === 'checkbox') {
            formData[fieldName] = field.checked;
        } else {
            formData[fieldName] = field.value;
        }
    }
    return formData;
}

function setFormData(form, row) {
    var fields = form.elements;
    for (var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        if (row[fieldName] == undefined) continue;
        if (field.tagName === 'SELECT') {
            field.value = row[fieldName + '_id'] || row[fieldName];
        } else if (field.type === 'checkbox') {
            field.checked = row[fieldName];
        } else {
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
    Smetrics = main_form.metrics.value;
    sequence_numberUrl = "/api/get_metricsCalc_order_number/" +Smetrics
        $.get(
            sequence_numberUrl,
            function (res) {
                if (res) {
                    main_form.order_number.value = res.next_number;
                }else {
                    main_form.order_number.value = 1;
                }
            }
        )
}


function valid_save_data() {
    var alert_msg = '.';
    var rtn_val = true;
    var getRow = $('#metrics_setup_dg').datagrid('getSelected');
    var low_limit = parseFloat(getRow.low_limit);
    var allocation = parseFloat(getRow.allocation);
    var score= main_form.score.value;

    if (getRow) {
        if ( score>allocation || score<low_limit ) {
            alert_msg = "計分大於最高配分或小於最低配分，不允存檔\n";
            rtn_val = false;
        }
    }

    var items = $('#main_dg').datagrid('getRows');
    for (var i = 0, thislen = items.length; i < thislen; i++) {
        //不同行才做"得分"是否存在的檢查
        if( main_form.order_number.value!=items[i]['order_number']){
            if ( main_form.score.value==items[i]['score'] ){
                alert_msg += " "+items[i]['score']+"得分已存在，不允存檔\n";
                rtn_val = false;
            }
        }
    }

    if (parseFloat(main_form.lower_limit.value) >= parseFloat(main_form.upper_limit.value)) {
        alert_msg += " 「下限」>=「上限」，不允存檔";
        rtn_val = false;
    }
    if (alert_msg != '.') {
        alert(alert_msg);
    }
    return rtn_val;
}


function main_dg_query(selVal) {
    $("#main_dg").datagrid({
        queryParams: {
            metrics_id: selVal,
        },
    });
}

function dg_reload() {
    $('#main_dg').datagrid('reload');
    $('#employee_info_easy_dg').datagrid('reload');
    $('#metrics_setupDate_dg').datagrid('reload');
    $('#metrics_setup_dg').datagrid('reload');
}

function centerControl(event) {
    main_form.metrics.disabled = true;
    $('#id_metrics').hide();
    $('#div_id_metrics label').hide();
    switch (event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
        default:
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            break
    }
}

function Empty_centerControl() {
    main_form.order_number.value = '';
    main_form.calc_content.value = '';
    main_form.lower_limit.value = '';
    main_form.upper_limit.value = '';
    main_form.score.value = '';
}

function Empty_main_dg() {
    for (var i = 0, thislen = $('#main_dg').datagrid('getRows').length; i < thislen; i++) {
        $('#main_dg').datagrid('deleteRow', 0);
        Empty_centerControl();
    }
}

function Empty_datagrid(dg) {
    for (var i = 0, thisLen = dg.datagrid('getRows').length; i < thisLen; i++) {
        dg.datagrid('deleteRow', 0);
        Empty_centerControl();
    }
}


function controlDisabled() {
    $("#new_btn").attr("disabled", "true");
    $("#create_btn").attr("disabled", "true");
    $("#update_btn").attr("disabled", "true");
    $("#cancel_btn").attr("disabled", "true");
    $("#delete_btn").attr("disabled", "true");
    $("#expand_btn").attr("disabled", "true");
    $("#copy_btn").attr("disabled", "true");
    $("#south_search_open").attr("disabled", "true");
    $("#east_search").attr("disabled", "true");
    $("#_easyui_textbox_input4").attr("disabled", "true");
    Empty_centerControl();

    main_form.order_number.disabled = true;
    main_form.calc_content.disabled = true;
    main_form.lower_limit.disable = true;
    main_form.upper_limit.disabled = true;
    main_form.score.disabled = true;
}


//crIndex : currentRowIndex
function datagridSelectRow(dg, data, conditions, crIndex) {
    switch (currentEvent) {
        case 'new':
            for (var i = 0, len = data.rows.length; i < len; i++) {
                if (eval(conditions)) {
                    dg.datagrid('selectRow', i);
                    break;    //for的break
                }
            }
            //沒選到row的處理,避免main_dg,main_form顯示舊資料
            if (dg.datagrid('getSelected') == null) {
                dg.datagrid('selectRow', 0);
            }
            //重新指定中間main_form的data
            var rr = $("#main_dg").datagrid('getSelected');
            if ($("#main_dg").datagrid('getRowIndex', rr) == -1) {
                $("#main_dg").datagrid('selectRow', 0);
            }
            clearError();
            break;           //switch的break
        case 'update':
            dg.datagrid('selectRow', crIndex);
            //沒選到row的處理,避免main_dg,main_form顯示舊資料
            if (dg.datagrid('getSelected') == null) {
                dg.datagrid('selectRow', 0);
            }
            //重新指定中間main_form的data
            if ($("#main_dg").datagrid('getSelected') == null) {
                $("#main_dg").datagrid('selectRow', 0);
                if ($("#main_dg").datagrid('getSelected') == null) {
                    $("#main_dg").datagrid('unselectRow');
                };
            }
            clearError();
            break;
        case 'delete':     //刪除之後,INDEX不變,還是原來的位置
            //刪除最後一筆資料時, 還是移到最後一筆資料
            if (crIndex == data.rows.length) {
                dg.datagrid('selectRow', crIndex - 1);
            } else {
                dg.datagrid('selectRow', crIndex);
            }
            //沒選到row的處理,避免main_dg,main_form顯示舊資料
            if (dg.datagrid('getSelected') == null) {
                dg.datagrid('selectRow', 0);
                if ( dg.datagrid('getSelected') == null) {
                    dg.datagrid('unselectRow');
                };
            }
            clearError();
            break;
        case 'ready':
            dg.datagrid('selectRow', crIndex);
            //沒選到row的處理,避免main_dg,main_form顯示舊資料
            if (dg.datagrid('getSelected') == null) {
                dg.datagrid('selectRow', 0);
                if ( dg.datagrid('getSelected') == null) {
                    dg.datagrid('unselectRow');
                };
            }
            clearError();
            break;
        default:
            dg.datagrid('selectRow', 0);
            if ( dg.datagrid('getSelected') == null) {
                    dg.datagrid('unselectRow');
            };
            clearError();
            break;
    }
}


function controlEnabled() {
    $("#cancel_btn").removeAttr("disabled");
    if (perm.create == "True") {
        $("#new_btn").removeAttr("disabled");
        $("#create_btn").removeAttr("disabled");

        $("#expand_btn").removeAttr("disabled");
        $("#copy_btn").removeAttr("disabled");
        $("#south_search_open").removeAttr("disabled");
        $("#south_search_sumit").removeAttr("disabled");
        $("#south_search_clear").removeAttr("disabled");
        $("#east_search").removeAttr("disabled");
        $("#_easyui_textbox_input4").removeAttr("disabled");
        $("#_easyui_textbox_input1").removeAttr("disabled");
        $("#_easyui_textbox_input2").removeAttr("disabled");
        $("#_easyui_textbox_input3").removeAttr("disabled");
    }

    if (perm.update == "True") {
        $("#update_btn").removeAttr("disabled");
        Empty_centerControl();
        main_form.order_number.disabled = false;
        main_form.calc_content.disabled = false;
        main_form.lower_limit.disabled = false;
        main_form.upper_limit.disabled = false;
        main_form.score.disabled = false;
    }

    if (perm.delete == "True") {
        $("#delete_btn").removeAttr("disabled");
    }
}



var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var currentRowIndex_center = 0;
var currentRowIndex_north = 0;
var currentRowIndex_east = 0;
var currentRowIndex_south = 0;
var currentEvent = null;
var rowCount = 0;
var rowCount_main_dg = 0;
var work_code_key = '';
var conditions = null;

//east_grid-->main_form-->up
//EasyUI控制Grid的Column格式
//field : 必需在〝Django view〞中有定義
//title : 就算在〝Django view〞中有定義，在這兒還是要重新定義一次，若無定義會顯示為〝空白〞
config.employee_info_easy_dg = {
    method: 'get',
    autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    columns: [[
        {field:'work_code',title:'編號', width:80,},
        {field:'chi_name',title:'名稱', width:150,},
        {field:'factory_name',title:'公司', width:150,},
        {field:'dept_name',title:'部門', width:150,},
    ]],
    // 要加入下列程式碼 autoLoad:false才能回傳的grid
    // onBeforeLoad: function () {
    //     var opts = $(this).datagrid('options');
    //     return opts.autoLoad;
    // },
    onSelect: function (index, row) {
        currentRowIndex_north = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        work_code_key = row['work_code']
        searchYear = $('#searchYear').textbox('getValue');
        if (parseInt(searchYear)>2020){
            eastSourceUrl = "/api/get_metrics_setupDate_data/" + work_code_key + "/" + searchYear;
        } else {
            eastSourceUrl = "/api/get_metrics_setupDate_data/" + work_code_key + "/" + workingYear;
        }
        $('#metrics_setupDate_dg').datagrid({autoLoad:true,url : eastSourceUrl});
        $('#metrics_setupDate_dg').datagrid('selectRow',currentRowIndex_east);
    },
    onLoadSuccess: function (data) {
        var len = data.total;
        if (len == 0) {
            //沒有資料,清空子dg
            Empty_datagrid($("#main_dg"));
        } else {
            while (i < len) {
                //個人指標:共同指標不出現
                var i = 0;
                if (data.rows[i]['work_code'].search("-") > -1) {
                    //有找到的("共同指標")，刪除
                    $(this).datagrid('deleteRow', i);
                } else {
                    i++;
                }
                ;
            }
            $(this).datagrid('selectRow', currentRowIndex_north);
        }
    }
}


//east_grid-->main_form-->down
config.metrics_setupDate_dg = {
    method: 'get',
    autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    columns: [[
        {
            field: 'date_yyyy', title: '年度', width: 60, align: 'center', styler: function (value, row, index) {
                return 'color:blue;font-weight:bold;';
            }
        },
        {
            field: 'date_mm', title: '月(季)', width: 60, align: 'center', styler: function (value, row, index) {
                return 'color:blue;font-weight:bold;';
            }
        },
    ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function (index, row) {
        currentRowIndex_east = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');

        $("#metrics_setup_dg").datagrid({
            queryParams: {
                work_code_id: work_code_key,
                date_yyyy: row['date_yyyy'],
                date_mm: row['date_mm'],
            },
        });
        // main_form.work_code.value =row['work_code'];
        // main_form.date_yyyy.value = row['date_yyyy'];
        // main_form.date_mm.value = row['date_mm'];
        $('#metrics_setup_dg').datagrid({autoLoad:true});
        $('#metrics_setup_dg').datagrid('selectRow',currentRowIndex_south);
    },
    onLoadSuccess: function (data) {
        //如果當年度沒資料, 就清空grid
        find_month = parseInt(workingMonth)+1;
        findRowDatas(workingYear, find_month);
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
    }
}


//east_grid-->main_form-->down
config.metrics_setup_dg = {
    singleSelect: true,
    autoLoad: false,
    autoRowHeight: true,
    autoRowHeight: true,
    method: 'get',
    columns: [[
        {field: 'order_number', title: '順序&nbsp;&nbsp;&nbsp;', width: 50, align: 'right',},
        {field:'order_item',title:'順序<br>細項', width:50, align:'right',},
        // {field:'asc_desc',title:'計算<br>方式', width:40, align:'center',},
        {field:'score_type',title:'評核方式', width:75, align:'center',},
        {
            field: 'metrics_content', title: '衡量指標(一定要有數字)', width: 900,
            formatter: function (value, row, index) {
                return "<pre style='font-size: 100%;'>" + value + "</pre>";
            }
        },
        {field: 'unit_Mcalc', title: '單<br>位', width: 40, align: 'center',},
        {
            field: 'low_limit',
            title: '最低<br>配分',
            width: 80,
            align: 'right',
            styler: function (value, row, index) {
                return 'background-color:#eeeeee;color:blue;';
            }
        },
        {
            field: 'allocation',
            title: '最高<br>配分',
            width: 100,
            align: 'right',
            styler: function (value, row, index) {
                return 'background-color:#eeeeee;color:blue;';
            }
        }
    ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function (index, row) {
        currentRowIndex_south = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');

        $("#main_dg").datagrid({
            queryParams: {
                metrics_id: row['metrics_id']
            },
        });

        $('#id_metrics option').each(function (){
            $(this).remove();
         });
        var options="";
        options = "<option value='"+row['metrics_id']+"'>"+row['metrics_id']+"</option>";
        $('#id_metrics').append(options);
        $('#id_metrics').get(0).options[0].selected = true;


        $('#main_dg').datagrid({autoLoad:true});
        $('#main_dg').datagrid('selectRow',currentRowIndex_center);

        main_form.order_number.value = '';
        main_form.calc_content.value = '';
        main_form.score.value = ''

        if ( row['date_yyyy']>workingYear){
            $(":input").removeAttr("disabled");
            centerControl('update');
        }
        else {
            if ( row['date_yyyy']==workingYear && row['date_mm']>workingMonth){
                $(":input").removeAttr("disabled");
                centerControl('update');
            } else {
                $("#cancel_btn").attr("disabled","disabled");
                $("#new_btn").attr("disabled","disabled");
                $("#update_btn").attr("disabled","disabled");
                $("#delete_btn").attr("disabled","disabled");
                $("#main_form :input").attr("disabled","disabled");
            }
        };
    },
    onLoadSuccess: function (data, row) {
        //如果當年度沒資料, 就清空grid
        // if ( data.total == 0) {
        // if (is_director == 'False') {
        //     Empty_centerControl();
        //     $(this).datagrid('unselectRow');
        // } else {
            if ($('#employee_info_easy_dg').datagrid('getRows').length > 0) {
                conditions = "data.rows[i]['metrics_id'] == main_form.metrics.value";
                //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['work_code']

                datagridSelectRow($(this), data, conditions, currentRowIndex_south);
            }
        // }
    }
}


// east grid 和 center的main_form 同步
config.main_dg = {
    singleSelect: true,
    autoLoad: false,
    autoRowHeight: true,
    method: 'get',
    columns: [[
        {field: 'order_number', title: '計算<br>順序', width: 40, align: 'right',},
        {field: 'calc_content', title: '計算方式', width: 750,},
        {field: 'lower_limit', title: '下限&nbsp;&nbsp;<br>( >= )', width: 80, align: 'center',},
        {field: 'upper_limit', title: '上限<br>( < )', width: 80, align: 'center',},
        {
            field: 'score', title: '得分', width: 80, align: 'right', styler: function (value, row, index) {
                return 'background-color:#eeeeee;color:blue;';
            }
        },
    ]],
    rowStyler: function (index, row) {
        if (row.allocation == 0) {
            return 'background-color:pink;color:blue;font-weight:bold;'; // return inline style
        }
    },
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function (index, row) {
        currentRowIndex_center = index;
        currentRow = row;
        currentKey = row[$('#main_dg').data().key];
        centerControl('update');
        setFormData(main_form, row);

        // $('#id_metrics option').each(function (){
        //     $(this).remove();
        //  });
        // var options="";
        // options = "<option value='"+row['metrics_id']+"'>"+row['metrics_id']+"</option>";
        // $('#id_metrics').append(options);
        $('#id_metrics').get(0).options[0].selected = true;
    },
    onLoadSuccess: function (data) {
        rowCount_main_dg = data.total;
        conditions = "data.rows[i]['order_number'] == main_form.order_number.value";
        //(不可只傳data.rows[i].length)要傳data過去,因為conditions裏有用到 data.rows[i]['order_number']
        datagridSelectRow($(this), data, conditions, currentRowIndex_center);
    }
}

config.main_mono_search_dlg = {
    resizable: true,
    modal: true,
    closed: true,
}


config.cpx_search_dlg = {
    'dlg': {
        resizable: true,
        modal: true,
        closed: true,
    }
}


$(document).ready(function () {
    var key = $('#main_dg').data().key;
    var userUrl = $('#metrics_setup_dg').data().source;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0, 0);
    // alert("***目前作業年度:\n"+"          "+workingYear +"年");
    currentEvent = "ready";
    centerControl('update');
    northSourceUrl = "/api/get_metrics_setup_common";


    // $('#show_employee').click(function (){
    $('#employee_info_easy_dg').datagrid({url: northSourceUrl});
    // });

    // $('#show_year_month').click(function (){
    //    $('#metrics_setupDate_dg').datagrid({autoLoad:true,url: eastSourceUrl});
    // });

    // $('#show_metrics').click(function (){
    //     $('#metrics_setup_dg').datagrid({autoLoad:true});
    //     $('#main_dg').datagrid({autoLoad:true});
    // });

    $('#main_dg').datagrid('reorderColumns', columnOrder);
    /*
    $('#id_order_number').change(function (){
        var thisVal = $(this).val();
        get_order_item(thisVal);
        if ( thisVal<1 || thisVal>50){
            alert("順序只能為1~50，錯誤的值將被清除");
            $(this).val("");
        }
    });
     */

    $('#id_order_item').change(function (){
        var thisVal = $(this).val();
        if ( thisVal<0 || thisVal>50){
            alert("順序只能為0~50，錯誤的值將被清除");
            $(this).val("");
        }
    });

    //計分不得大於指標配分
    $('#id_score').change(function () {
        var getRow = $('#metrics_setup_dg').datagrid('getSelected');
        var low_limit = parseFloat(getRow.low_limit);
        var allocation = parseFloat(getRow.allocation);
        var score = parseFloat(main_form.score.value);

        if (getRow) {
            if ( score > allocation || score<low_limit ) {
                alert("得分大於最高配分或小於最低配分，請更正");
                $(this).val('');
                $(this).focus();
            }
        }
        var items = $('#main_dg').datagrid('getRows');
        for (var i = 0, thislen = items.length; i < thislen; i++) {
            if ( main_form.score.value==items[i]['score'] ){
                alert("得分已存在");
                $(this).val('');
                $(this).focus();
            }
        }

    });

    $('#id_lower_limit').change(function () {
        if (parseFloat(main_form.lower_limit.value) >= parseFloat(main_form.upper_limit.value)) {
            alert("「下限」>=「上限」，請更正");
            $(this).focus();
        }
    });

    $('#id_upper_limit').change(function () {
        if (parseFloat(main_form.lower_limit.value) >= parseFloat(main_form.upper_limit.value)) {
            $(this).focus();
        }
    });


    $('#new_btn').click(function () {
        // resetForm(main_form);
        main_form.elements[1].focus();
        centerControl('new');
        get_order_number();
    });


    $('#create_btn').click(function () {
        // 新增
        if (valid_save_data()) {
            var data = getFormData(main_form);
            JSON.stringify(data);
            $.post(
                formSourceUrl,
                data,
                function (res) {
                    if (res.success) {
                        currentEvent = 'new';
                        $('#main_dg').datagrid('reload');
                        alert('新增成功!')
                    } else {
                        currentEvent = null;
                        alert('錯誤!')
                    }
                }
            )
        }
    });


    $('#east_search').click(function () {
        eastSourceUrl = "/api/get_metrics_setupDate_data/" + work_code_key + "/" + $('#searchYear').val();
        $('#metrics_setupDate_dg').datagrid({
            url: eastSourceUrl,
            columns: [[
                // {field:'work_code',title:'工號',},
                {
                    field: 'date_yyyy', title: '年度', width: 65, align: 'center', styler: function (value, row, index) {
                        return 'color:blue;font-weight:bold;';
                    }
                },
                {
                    field: 'date_mm', title: '月(季)', width: 65, align: 'center', styler: function (value, row, index) {
                        return 'color:blue;font-weight:bold;';
                    }
                },
            ]],
            onLoadSuccess: function (data) {
                $(this).datagrid('selectRow', 0);
            }
        });
    });

    $('#south_search_open').click(function () {
        $('#south_search_dd').attr('hidden', false);

        $('#south_search_dd').dialog({
            title: '指標資料搜尋',
            width: 305,
            height: 300,
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });

        $('#south_search_sumit').click(function () {
            searchWorkCode = $('#searchWorkCode').val();
            searchChiName = $('#searchChiName').val();
            searchDept = $('#searchDept').val();

            //若未給x,會認定沒有此參數,url=/api/get_metrics_setup_data///,會找不到
            //給了x,才會有參數
            if (searchWorkCode == '') {
                searchWorkCode = 'x'
            }
            if (searchChiName == '') {
                searchChiName = 'x'
            }
            if (searchDept == '') {
                searchDept = 'x'
            }
            southSourceUrl = "/api/get_metrics_setup_common/" + searchWorkCode + "/" + searchChiName + "/" + searchDept + "/" + userId;
            $('#employee_info_easy_dg').datagrid({url: southSourceUrl});
        });
        $('#south_search_clear').click(function () {
            $("#south_search_dd input").val('');
        });
    });


    $('#cancel_btn').click(function () {
        dg_reload();
        // $('#main_dg').datagrid('reload');
    });

    $('#update_btn').click(function () {
        // 修改
        if (valid_save_data()) {
            data = getFormData(main_form);
            $.post(
                formSourceUrl + '/' + currentKey,
                data,
                function (res) {
                    if (res.success) {
                        currentEvent = 'update';
                        $('#main_dg').datagrid('reload');
                        alert('更新成功!')
                    } else {
                        currentEvent = null;
                        alert('錯誤!')
                    }
                }
            )
        }
    });

    $('#delete_btn').click(function () {
        // 刪除
        if (!confirm('確定要刪除?')) return;
        $.get(
            formSourceUrl + '/' + currentKey,
            function (res) {
                if (res.success) {
                    currentEvent = 'delete';
                    $('#main_dg').datagrid('reload');
                    alert('刪除成功!')
                } else {
                    currentEvent = null;
                    alert('錯誤!')
                }
            }
        );
    });

    $(document).keydown(function (e) {
        // 主資料表上下移動選取資料。
        if (document.activeElement != document.getElementsByTagName('body')[0]) return;
        if (e.keyCode === 38) {
            // up
            currentRowIndex = currentRowIndex - 1 >= 0 ? currentRowIndex - 1 : currentRowIndex;
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        } else if (e.keyCode === 40) {
            //down
            currentRowIndex = currentRowIndex + 1 <= rowCount ? currentRowIndex + 1 : currentRowIndex;
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        }
    });

});


