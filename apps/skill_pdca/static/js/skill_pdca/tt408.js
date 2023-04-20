var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var currentRowIndex_center = 0;
var currentRowIndex_east = 0;
var rowCount = 0;
var idFieldValue = null;       //新增時的值
var currentEvent = null;
var conditions=null;


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
        if(field.tagName === 'SELECT') {
            field.value = row[fieldName + '_id'] || row[fieldName];
        }
        else {
            fields[i].value = row[fieldName];
        }
    }
}


function centerControl(event) {
    switch(event) {
        case 'new':
            main_form.id_year.disabled = false;
            main_form.id_month.disabled = false;
            main_form.id_work_code_title.disabled = false;
            if ( main_form.id_direct_supv.value == '' ) {
                main_form.id_direct_supv.value = "　";
                main_form.id_supv_name.value = "　";
                main_form.id_dept.value = "　";
            }
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            clearError();
            break
        case 'update':
            main_form.id_year.disabled = true;
            main_form.id_month.disabled = true;
            main_form.id_work_code_title.disabled = true;
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            clearError();
            break;
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
    }
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


function supv_work_code_title(direct_supv,dept_udc){
    $('#id_work_code_title option').each(function (){
        $(this).remove();
    });
   var url="/sk_api/supv_work_code_title/"+direct_supv+"/"+dept_udc;
    $.get(
        url,
        function (res) {
            var options='';
            if (res) {
                $.each(res, function(index, value){
                      options += "<option value='"+value['value']+"'>"+value['text']+"</option>";
                    });
                $('#id_work_code_title').append(options);
            }
        })
}


config.main_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,                              // 資料已經查好，由轉發得來，不需要再後端查詢
    idField: "id",
    columns: [[
        {field: 'work_code', title: '工號', width: 85,align: 'center', sortable:true,},
        {field: 'chi_name', title: '姓名', width: 85,align: 'center', sortable:true,},
        {field: 'job_code', title: '職務代號', width: 100, align: 'center',sortable:true,},
        {field: 'job_name', title: '職務名稱', width: 220,align: 'center', sortable:true,},
        {field: 'detail_yn', title: '已盤點', width: 80,align: 'center', sortable:true,},
        // {field:'direct_supv',title:'直接主管<br>工號',width:80,align: 'center',sortable:true,},
        // {field:'supv_name',title:'直接主管<br>(BPM首簽)',width:80,align: 'center',sortable:true,},
        // {field: 'dept', title: '一級部門', width: 150,align: 'center', sortable:true,},
        // {field: 'work_code_title', title: '', width: 1,align: 'center', sortable:true,},
        // {field: 'year', title: '年', width: 50, align: 'center',sortable:true,},
        // {field: 'month', title: '月', width: 50, align: 'center',sortable:true,},
        // {field: 'bpm', title: 'BPM單號', width: 190, align: 'center',sortable:true,},
        // {field: 'bpm_desc1', title: 'BPM狀態', width: 100, align: 'center',sortable:true,},
        // {field: 'bpm_desc2', title: '狀態說明', width: 100, align: 'center',sortable:true,},
        /*
        {field: 'report_url', title: '報表名稱<br>( 滑鼠按一下,可開啟檔案 )', width: 250, align: 'center',sortable:true,
            formatter: function(value,row,index){
                if ( value===null ){
                    return " ";
                } else {
                    var pdf_url = value.split("/");
                    return "<a href='"+value+"' target='_blank'>"+pdf_url[pdf_url.length-1]+"</a>";
                }
            }
        },
         */
     ]],
    onSelect: function(index, row) {
        currentRowIndex_center = index;
        currentRow = row;
        // currentKey = row[$(this).data().key];
        currentKey = row['id'];
        main_form.id_work_code_title.value = row['work_code_title'];
        // setFormData(main_form, row);
        // centerControl('update');
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
        // var selected = $("#id_work_code_title").find("option:selected").text().split(" ");
        // conditions = "data.rows[i]['work_code'] == selected[0] && data.rows[i]['job_code'] == selected[2]";
        datagridSelectRow($(this),data,conditions,currentRowIndex_center);
    }
}



config.east_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,                              // 資料已經查好，由轉發得來，不需要再後端查詢
    idField: ["direct_supv","dept_udc","year","month"],
    columns: [[
        {field:'direct_supv',title:'直接主管<br>工號',width:80,align: 'center',sortable:true,},
        {field:'supv_name',title:'直接主管<br>(BPM首簽)',width:70,align: 'center',sortable:true,},
        {field: 'dept', title: '一級部門', width: 165,align: 'center', sortable:true,},
        // {field: 'work_code', title: '工號', width: 80,align: 'center', sortable:true,},
        // {field: 'chi_name', title: '姓名', width: 80,align: 'center', sortable:true,},
        // {field: 'job_code', title: '職務代號', width: 70, align: 'center',sortable:true,},
        // {field: 'job_name', title: '職務名稱', width: 150,align: 'center', sortable:true,},
        {field: 'year', title: '年', width: 50, align: 'center',sortable:true,},
        {field: 'month', title: '月', width: 40, align: 'center',sortable:true,},
        {field: 'bpm', title: 'BPM單號', width: 145, align: 'center',sortable:true,},
        {field: 'bpm_desc1', title: 'BPM狀態', width: 60, align: 'center',sortable:true,},
        {field: 'bpm_desc2', title: '狀態說明', width: 60, align: 'center',sortable:true,},
        {field: 'report_url', title: '報表名稱<br>( 滑鼠按一下,可開啟檔案 )', width: 210, align: 'center',sortable:true,
            formatter: function(value,row,index){
                if ( value===null ){
                    return " ";
                } else {
                    var pdf_url = value.split("/");
                    return "<a href='"+value+"' target='_blank'>"+pdf_url[pdf_url.length-1]+"</a>";
                }
            }
        },
     ]],
    onSelect: function(index, row) {
        currentRowIndex_east = index;
        currentRow = row;
        // currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
        $("#main_dg").datagrid({
            url : "/sk_api/matrix_master_employee/"+row['direct_supv']+"/"+row['dept_udc']+"/"+row['year']+"/"+row['month']+"/"+row['bpm'],
        });
        supv_work_code_title(row['direct_supv'],row['dept_udc']);
    },
    onUnselectAll: function (rows) {
        main_form.id_direct_supv.value = '';
        main_form.id_supv_name.value = '';
        main_form.id_dept.value = '';
        main_form.id_year.value = '';
        main_form.id_month.value = '';
        main_form.id_work_code_title.value = '';
        $('#main_dg').datagrid('unselectAll');
        $('#main_dg').datagrid('loadData',[]);
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
        conditions = "data.rows[i]['direct_supv'] == main_form.id_direct_supv.value && data.rows[i]['dept'] == main_form.id_dept.value && data.rows[i]['year'] == main_form.id_year.value && data.rows[i]['month'] == main_form.id_month.value";
        datagridSelectRow($(this), data, conditions, currentRowIndex_east);
    }
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


$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;                   // view.py 裏定義的
    var formSourceUrl = $('#main_form').attr('action');   // form.py 裏定義的
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#main_dg').datagrid('reorderColumns', columnOrder);

    centerControl('update');
    // $('#main_dg').datagrid('enableFilter');
    $('#east_dg').datagrid('enableFilter');

    $('#cancel-select').click(function(){
        $('#east_dg').datagrid('unselectAll');
        supv_work_code_title();
    });

    $('#id_work_code_title').change(function(){
        var selected = $(this).find("option:selected").text();
        // alert(selected.split(" ")[0]+"\n"+selected.split(" ")[1]+"\n"+selected.split(" ")[2]+"\n"+selected.split(" ")[3]);
        if ( main_form.id_direct_supv.value == "　" ){
            var url = "/sk_api/get_work_code_direct_supv/"+selected.split(" ")[0];
            $.get(url,
                function(res) {
                    if(res.success) {
                        // alert(res.direct_supv+"\n"+res.supv_name);
                        $("#id_direct_supv").val(res.direct_supv);
                        $("#id_supv_name").val(res.supv_name);
                        $("#id_dept").val(res.dept);
                    } else {
                    }
                });
        }
    });


    $('#new_btn').click(function(){
        main_form.elements[0].focus();
        centerControl('new');
    });

    $('#create_btn').click(function(){
        // 新增
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        var direct_supv = data.direct_supv;
        delete data.direct_supv;
        delete data.supv_name;
        delete data.dept;
        $.ajax({
        type :"post",
        url :formSourceUrl,
        data :data,
        async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success :function(res){
                if (res.success) {
                    $('#main_dg').datagrid('reload');
                    $('#east_dg').datagrid('reload');
                    currentEvent = 'new';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('錯誤!'+'\n\n'+res.message);
                }
            }
        });
    });


    $('#cancel_btn').click(function(){
        centerControl('update');
        $('#main_dg').datagrid('reload');
    });

    $('#update_btn').click(function(){
        // 更新
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        alert(currentKey);
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['id'];
                    currentEvent = 'update';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('k錯誤'+'\n\n'+res.message);
                }
            }
        )
    });


    $('#delete_btn').click(function(){
        // 刪除
        idFieldValue = null;
        $.get(formSourceUrl + '/' + currentKey,
        function(res) {
            if(res.success) {
                alert('刪除成功!');
                var queryParams = $('#main_dg').datagrid('options').queryParams;
                $('#main_dg').datagrid('reload');
                if ( $('#main_dg').datagrid('getRows').length==1 ){
                    $('#east_dg').datagrid('reload');
                    // $('#east_dg').datagrid('unselectAll');
                }
                currentEvent = 'delete';
            } else {
                currentEvent = null;
                alert('錯誤'+'\n\n'+res.message);
            }
        });
    });

});




