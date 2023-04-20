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
        fieldValue = field.value;
        if(field.tagName === 'SELECT') {
            field.value = row[fieldName + '_id'] || row[fieldName];
        }
        else if(fieldName == 'factory') {
            if(row['factory'].includes(field.value)) field.checked = true;
            else field.checked = false;
        }
        else {
            fields[i].value = row[fieldName];
        }
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
        {field:'program_id',title:'程式代號',sortable:true,},
        {field:'program_name',title:'程式名稱',sortable:true,},
    ]],
    onSelect: function (index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$('#main_dg').data().key];
        setFormData(main_form, row);
        buttonControl(false, false, false, false, false);
    },
    onLoadSuccess: function (data) {
        $(this).datagrid('selectRow', currentRowIndex);
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
            console.log(res)
            $("#main_dg").datagrid('loadData', res);
        }
    }
}
$(document).ready(function(){
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);

    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#main_dg').datagrid('enableFilter');

    $('#cancel_btn').click(function(){
        // 取消新增
        $('#main_dg').datagrid('selectRow', currentRowIndex);
    });
    $('#update_btn').click(function(){
        // 新增
        if(!formValidate(main_form)) return;
        if(!confirm("確定? 改變所屬工廠可能會造成權限的問題喔。")) return;
        var data = getFormData(main_form);

        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                //res = JSON.parse(res);
                if(res.success) {
                    alert('sy011...更新成功!')
                    $('#main_dg').datagrid('reload');
                    $('#main_dg').datagrid('selectRow', currentRowIndex);
                } else {
                    alert('sy011...發生錯誤');
                };
            }
        )
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

    $('#main_monoSearchForm').submit(false);
    $('#main_monoSearchForm').keydown(function(e){
        if(e.keyCode==13) $('#search_btn_main').click();
    });
    $('#search_btn_main').click(function(){
        var searchParam = main_monoSearchForm.field_main.value +
                          '=' + main_monoSearchForm.keyword_main.value;
        var url = '/api/data/factory_program?' + searchParam;
        $('#main_dg').datagrid({
            url: url
        });
        rowCount = $('#main_dg').datagrid('getData').total;
        $('#main_mono_search_dlg').dialog('close');
        $('#main_dg').datagrid('selectRow', 0);
    });
});


