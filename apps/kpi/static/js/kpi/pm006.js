function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
         //# _id 結尾通常是 foreignkey
        if(field.type === 'select-one' && fieldName!="date_yyyy") {
            formData[fieldName + '_id'] = field.value;
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
        else {
            fields[i].value = row[fieldName];
        }
    }
}

function filter_work_code_options() {
    var option_length = $('#id_work_code option').length;
    $('#id_work_code option').each(function () {
        //移除共同指標
        if ($(this).val().search("-") > -1) {
            $(this).remove();
        }
    });
}


function centerControl(event) {
        var Today = new Date();
        var Year = Today.getFullYear();
        var Month = Today.getMonth();
        //Date物件用0表示一年中的第一個月, 用1表示一個月中的第一天。
        // 1,2,3月--都自動減一年)。
        if (Month <= 2) {
            Year--;
        }
        main_form.date_yyyy.value = Year;
        switch (event) {
            case 'new':
                buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
                main_form.id_work_code.disabled=false;
                main_form.id_date_yyyy.disabled=false;
                clearError();
                break
            case 'update':
                buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
                main_form.id_work_code.disabled=true;
                main_form.id_date_yyyy.disabled=true;
                clearError();
                break
            default:
                buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
                main_form.id_work_code.disabled=true;
                main_form.id_date_yyyy.disabled=true;
                break
        }
}

function gridSelectTo(dg,currentEvent){
    var dg = '#'+ dg;
    switch(currentEvent) {
        case 'new':
            var rows = $(dg).datagrid('getRows');
            for(var i=0,len=rows.length; i<len; i++){
                if (rows[i]['work_code_id'] == idFieldValue){
                    row = rows[i];
                    break;
                }
            }
            if (row){
                var index = $(dg).datagrid('getRowIndex', row);
                $(dg).datagrid('selectRow',index);
            }
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
    idField : 'work_code_id',
    onSelect: function (index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function (data) {
        rowCount = data.total;
        gridSelectTo('main_dg',currentEvent);
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
        },
        'search': {
            afterSearch: function (res) {
                $("#main_dg").datagrid('loadData', res);
            }
        }
    }

    $(document).ready(function () {
        var key = $('#main_dg').data().key;
        var mainUrl = $('#main_dg').data().source;
        var formSourceUrl = $('#main_form').attr('action');
        filter_work_code_options();

        document.querySelector('.layout-split-east .panel-body').scrollTo(0, 0);
        $('#create_btn').hide();

        $('#main_dg').datagrid('reorderColumns', columnOrder);

        $('#new_btn').click(function () {
            resetForm('main_form');
            main_form.elements[0].focus();
            $('#create_btn').show();
            $('#import_btn').hide();
            centerControl('new');
        });

        $('#create_btn').click(function () {
            // 新增

            if (!formValidate(main_form)) return;
            var data = getFormData(main_form);
            $.post(
                formSourceUrl,
                data,
                function (res) {
                    if (res.success) {
                        alert('新增成功!')
                        $('#main_dg').datagrid('reload');
                        idFieldValue = data['work_code_id'];
                        currentEvent = 'new';
                    } else {
                        idFieldValue = null;
                        currentEvent = null;
                        alert('錯誤');
                    }
                }
            );
            $('#import_btn').show();
        });

        // 顯示excel匯入對話方塊
        $('#import_btn').click(function () {
            $('#import_dd').attr('hidden', false);
            $('#import_dd').dialog({
                title: '請挑選要匯入的excel檔(.xlsx)',
                width: 400,
                height: 190,
                closed: false,
                cache: false,
                // href: '',
                modal: true,
            });
        });

        $('#cancel_btn').click(function () {
            // 取消新增
            $('#main_dg').datagrid('selectRow', currentRowIndex);
            $('#import_btn').show();
        });

        $('#update_btn').click(function () {
            // 更新
            if (!formValidate(main_form)) return;
            var data = getFormData(main_form);
            $.post(
                formSourceUrl + '/' + currentKey,
                data,
                function (res) {
                    if (res.success) {
                        alert('更新成功!')
                        $('#main_dg').datagrid('reload');
                        idFieldValue = data['work_code_id'];
                        currentEvent = 'update';
                    } else {
                        idFieldValue = null;
                        currentEvent = null;
                        alert('hr01.js---錯誤');
                    }
                }
            )
        });

        $('#delete_btn').click(function () {
            // 刪除
            idFieldValue = null;
            $.get(formSourceUrl + '/' + currentKey,
                function (res) {
                    if (res.success) {
                        alert('刪除成功!')
                        $('#main_dg').datagrid('reload');
                        currentEvent = 'delete';
                    } else {
                        currentEvent = null;
                        alert('錯誤');
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

        function resetForm(form_id) {
            $('#' + form_id).form('reset');
            $(document).trigger('reset_' + form_id);
        }

    });

