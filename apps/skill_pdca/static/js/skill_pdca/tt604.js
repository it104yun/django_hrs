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
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            clearError();
            break;
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
    }
}


function gridSelectTo(dg,currentEvent){
    var dg = '#'+ dg;
    switch(currentEvent) {
        case 'new':
            $(dg).datagrid('selectRecord', idFieldValue);
            clearError();
            break
        case 'update':
            $(dg).datagrid('selectRecord', idFieldValue);
            clearError();
            break
        case 'delete':     //刪除之後,INDEX不變,還是原來的位置
            var rowsCount = $(dg).datagrid('getRows').length;
            //刪除最後一筆資料時, 還是移到最後一筆資料
            if (currentRowIndex==rowsCount){
                $(dg).datagrid('selectRow', currentRowIndex-1);
            } else {
                $(dg).datagrid('selectRow', currentRowIndex);
            }
            clearError();
            break
        default:
            $(dg).datagrid('selectRow', 0);
            break
    }
}

var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var rowCount = 0;
var idFieldValue = null;       //新增時的值
var currentEvent = null;

config.main_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,                              // 資料已經查好，由轉發得來，不需要再後端查詢
    idField: "id",
    columns: [[
        {field: 'work_code', title: '工號', width: 80,align: 'center', sortable:true,},
        {field: 'chi_name', title: '姓名', width: 80,align: 'center', sortable:true,},
        {field: 'the_time', title: '次數', width: 60,align: 'center', sortable:true,},
        {field: 'job_code', title: '職務代號', width: 70, align: 'center',sortable:true,},
        {field: 'job_name', title: '職務名稱', width: 150,align: 'center', sortable:true,},
        {field: 'bpm_number', title: 'BPM單號', width: 190, align: 'center',sortable:true,},
        {field: 'bpm_desc1', title: 'BPM狀態', width: 100, align: 'center',sortable:true,},
        {field: 'bpm_desc2', title: '狀態說明', width: 100, align: 'center',sortable:true,},
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
     ]],
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
        gridSelectTo('main_dg',currentEvent);
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
    $('#main_dg').datagrid('enableFilter');

    $('#new_btn').click(function(){
        resetForm('main_form');
        main_form.elements[0].focus();
         centerControl('new');
    });

    $('#create_btn').click(function(){
        // 新增
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        $.ajax({
        type :"post",
        url :formSourceUrl,
        data :data,
        async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success :function(res){
                console.log(data);
                if (res.success) {
                    alert('新增成功!');
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['id'];
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
                console.log(queryParams);
                $('#main_dg').datagrid('reload');
                currentEvent = 'delete';
            } else {
                currentEvent = null;
                alert('錯誤'+'\n\n'+res.message);
            }
        });
    });

});




