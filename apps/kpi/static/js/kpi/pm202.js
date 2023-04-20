function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        formData[fieldName] = field.value;
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
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        $(this).datagrid('selectRow', 0);
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
}

$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);


    // $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#main_dg').datagrid('selectRow', 0);

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
                    alert('bsym.js---錯誤'+'\n\n'+res.message);
                }
            }
        )
    });

});




