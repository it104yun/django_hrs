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
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.id_work_code.disabled = false;
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.id_work_code.disabled = true;
            clearError();
            break;
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
    }
}


function onAfterNewSelect(dg,newKey,field){
    var rows = dg.datagrid('getRows');
    var len = rows.length;
    var fieldValue= '';
    for ( var i=0 ; i < len ; i++){
        if ( field=="work_code" ) {  fieldValue = rows[i].work_code } else { fieldValue = (rows[i].job_title).split(" ")[0] }  ;
        if ( fieldValue == newKey ){
            dg.datagrid('selectRow', i);
            break;    //for的break
        }
    }
}




function gridSelectTo(dg,currentEvent){
    switch(currentEvent) {
        case 'new':
            if (newKey_east!=''){
                onAfterNewSelect($("#employee_title_dg"),newKey_east,"work_code");
            };
            // if (newKey_center!=''){
            //     onAfterNewSelect($("#main_dg"),newKey_center,"job_title");
            // };
            clearError();
            break
        case 'update':
            clearError();
            break
        case 'delete':     //刪除之後,INDEX不變,還是原來的位置
            var rowsCount = dg.datagrid('getRows').length;
            //刪除最後一筆資料時, 還是移到最後一筆資料
            if (currentRowIndex_center==rowsCount){
                dg.datagrid('selectRow', currentRowIndex_center-1);
            } else {
                dg.datagrid('selectRow', currentRowIndex_center);
            }
            //沒選到row的處理,避免main_dg,main_form顯示舊資料
            if (dg.datagrid('getSelected') == null){
                dg.datagrid('selectRow', 0);
            }
            clearError();
            break
        default:
            dg.datagrid('selectRow', 0);
            break
    }
}

function main_dg_query(){
    $("#main_dg").datagrid({
        queryParams: {
            work_code: $('#id_work_code').val(),
        },
    });

}

var currentKey = '';
var newKey_center = '';
var newKey_east = '';
var currentRow = null;
var currentRowIndex_center = 0;
var currentRowIndex_east = 0;
var rowCount = 0;
var currentEvent = null;

config.main_dg = {
    method: 'get',
    autoLoad: false,
    rownumbers : true,
    autoRowHeight: false,
    singleSelect: true,
    idField: "id",
    columns: [[
        {field: 'job_title', title: '職務', width: 500},
     ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function(index, row) {
        currentRowIndex_center = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
        // gridSelectTo($(this),currentEvent);
        $(this).datagrid('selectRow',0);
    }
}


config.employee_title_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    columns: [[
        {field: 'job_code', title: '職務代號', width: 80, sortable:true,},
        {field: 'job_name', title: '職務名稱', width: 300, sortable:true,},
        {field: 'work_code', title: '工號', width: 100, sortable:true,},
        {field: 'chi_name', title: '姓名', width: 150, sortable:true,},
        {field: 'id', title: 'id',},
     ]],
    onSelect: function(index, row) {
        currentRowIndex_east = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        main_form.id_work_code.value = row['work_code']
        $("#main_dg").datagrid({
            queryParams: {
                work_code_id: row['work_code'],
            },
        });
        setFormData(main_form, row);
        centerControl('update');

        $('#main_dg').datagrid({autoLoad:true});
        $('#main_dg').datagrid('selectRow',currentRowIndex_center);
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
        gridSelectTo($(this),currentEvent);
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
    currentEvent = 'ready';
    centerControl('update');
    $('#employee_title_dg').datagrid('enableFilter');
    $('#employee_title_dg').datagrid('hideColumn', 'id');


    $('#id_job_title').change( function () {
        $.get("/sk_api/valid_employee_title_skill/"+$(this).val(),
        function(res) {
            if(!res.success) {
                alert('錯誤'+'\n\n'+res.message);
            }
        });
    });

    $('#new_btn').click(function(){
        centerControl('new');
    });

    $('#id_work_code').change( function(){
        newKey_east = $(this).val();
        $('#id_job_title').val('');
        main_dg_query();
        $('#main_dg').datagrid('reload');   //根據選到的內容重新查詢,此行不可刪
    });

    $('#id_job_title').change( function(){
        newKey_east = $('#id_work_code').val();
        newKey_center = $(this).val();
    });


    $('#create_btn').click(function(){
        // 新增
        $.get("/sk_api/valid_employee_title_skill/"+$('#id_job_title').val(),
        function(res) {
            if(res.success) {
                if(!formValidate(main_form)) return;
                currentEvent = 'new';
                var data = getFormData(main_form);
                $.ajax({
                type :"post",
                url :formSourceUrl,
                data :data,
                async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
                success :function(res){
                        if (res.success) {
                            alert('新增成功!');
                            $('#main_dg').datagrid('reload');
                            $('#employee_title_dg').datagrid('reload');
                        } else {
                            currentEvent = null;
                            alert('錯誤!'+'\n\n'+res.message);
                        }
                    }
                });
            }　else {
                alert('錯誤'+'\n\n'+res.message);
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
        currentEvent = 'update';
        var data = getFormData(main_form);
        data['disable'] = data.disable_id;
        delete data.disable_id;
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                    // $('#employee_title_dg').datagrid('reload');
                } else {
                    currentEvent = null;
                    alert('k錯誤'+'\n\n'+res.message);
                }
            }
        )
    });


    $('#delete_btn').click(function(){
        // 刪除
        currentEvent = 'delete';
        $.get(formSourceUrl + '/' + currentKey,
        function(res) {
            if(res.success) {
                alert('刪除成功!');
                var queryParams = $('#main_dg').datagrid('options').queryParams;
                $('#main_dg').datagrid('reload');
                $('#employee_title_dg').datagrid('reload');
            } else {
                currentEvent = null;
                alert('錯誤'+'\n\n'+res.message);
            }
        });
    });

});




