function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    formData['factory'] = [];
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        if(field.type === 'select-one') {
            formData[fieldName + '_id'] = field.value;
            formData[fieldName] = field.selectedOptions[0].innerText;
        }
        else if(fieldName == 'factory') {
            if(field.checked) {
                formData['factory'].push(field.value);
            }
        }
        else if(field.type === 'radio') {
            formData[fieldName + '_id'] = $('input[name='+fieldName+']:checked').val();
            formData[fieldName] = $('input[name='+fieldName+']:checked').parent('label').text().trim()
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
        else if(fieldName == 'factory') {
            if(row['factories'].includes(field.value)) field.checked = true;
            else field.checked = false;
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
            main_form.username.disabled=false;
            $("#id_username").focus();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            clearError();
            main_form.username.disabled='inline-block';
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
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    columns:[[
        {field:'username',title:'帳號',sortable:true,},
        {field:'name',title:'姓名',sortable:true,},
    ]],
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        $(this).datagrid('selectRow', currentRowIndex);
        rowCount = data.total;
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

$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);

    $('#main_dg').datagrid('reorderColumns', columnOrder);

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
        $.post(
            formSourceUrl,
            data,
            function(res) {
                if(res.success) {
                    alert('新增成功!')
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('錯誤');
                }
            }
        )
    });
    $('#cancel_btn').click(function(){
        // 取消新增
        $('#main_dg').datagrid('selectRow', currentRowIndex);
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
                } else {
                    alert('錯誤');
                }
            }
        )
    });
    $('#delete_btn').click(function(){
        // 刪除
        $.get(formSourceUrl + '/' + currentKey,
            function(res) {
                if(res.success) {
                    alert('刪除成功!')
                    currentRowIndex = 0;
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('錯誤');
                }
            }
        );
    });

    $(document).keydown(function(e){
        // 主資料表上下移動選取資料。
        if(document.activeElement != document.getElementsByTagName('body')[0]) return;
        if(e.keyCode === 38) {
            // up
            currentRowIndex = currentRowIndex - 1 >= 0 ? currentRowIndex - 1 : currentRowIndex;
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        } else if(e.keyCode === 40) {
            //down
            currentRowIndex = currentRowIndex + 1 <= rowCount ? currentRowIndex + 1 : currentRowIndex;
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        }
    });
    function resetForm(form_id) {
        $('#' + form_id).form('reset');
        $(document).trigger('reset_' + form_id);
    }

    $('#main_monoSearchForm').submit(false);
    $('#main_monoSearchForm').keydown(function(e){
        if(e.keyCode==13) $('#search_btn_main').click();
    });

    $('#search_btn_main').click(function(){
        var searchParam = main_monoSearchForm.field_main.value
                        + '='
                        + main_monoSearchForm.keyword_main.value;
        var url = $('#main_dg').data().source + '?' + searchParam;
        $('#main_dg').datagrid({
            url: url,
        });
        rowCount = $('#main_dg').datagrid('getData').total;
        $('#mono_search_dlg').dialog('close');
        $('#main_dg').datagrid('selectRow', 0);
    });

});


