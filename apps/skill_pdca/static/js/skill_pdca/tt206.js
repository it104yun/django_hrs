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

function filter_work_code_options(){
    var option_length = $('#id_director option').length;
     $('#id_director option').each(function (){
         //移除共同指標
         if ( $(this).val().search("-") > -1) {
            $(this).remove();
        }
     });
}



function centerControl(event) {
    main_form.id_job_title.disabled = true;
    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.id_order_number.disabled = false;
            main_form.id_job_skill.disabled = false;
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
             main_form.id_order_number.disabled = true;
            clearError();
            break;
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
    }
}


function gridSelectTo(dg,currentEvent){
    switch(currentEvent) {
        case 'new':
            dg.datagrid('selectRecord', idFieldValue);
            clearError();
            break;
        case 'update':
            dg.datagrid('selectRecord', idFieldValue);
            clearError();
            break;
        case 'delete':     //刪除之後,INDEX不變,還是原來的位置
            var rowsCount = $(dg).datagrid('getRows').length;
            //刪除最後一筆資料時, 還是移到最後一筆資料
            if (currentRowIndex==rowsCount){
                dg.datagrid('selectRow', currentRowIndex-1);
            } else {
                dg.datagrid('selectRow', currentRowIndex);
            }
            clearError();
            break;
        default:
            dg.datagrid('selectRow', 0);
            clearError();
            break;
    }
}

function get_order_number(){
    job_title = main_form.id_job_title.value;
    url = "/sk_api/get_job_tiitle_skill_order_number/" +job_title
    $.get(
        url,
        function (res) {
            main_form.id_order_number.value = res.next_number;
        }
    )
}


var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var currentRowIndex_center = 0;
var currentRowIndex_east = 0;


var rowCount = 0;
var idFieldValue = null;       //新增時的值
var currentEvent = null;

config.main_dg = {
    method: 'get',
    autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    // selectOnCheck: true,
    // checkOnSelect: true,
    idField: "id",
    columns:[[
        // {field:'chk_to_do',checkbox:true,},
        {field:'order_number',title:'順序',align:'center',},
        {field:'job_skill',title:'職能',width: 600,
            /*
            editor: { type:'combobox',
                  options:{
                            data: rotation_jobs,      //這裏不一樣
                            // valueField:'value',
                            valueField:'value',
                            textField:'text',
                            }
            },
             */
        },
    ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    /*
    onDblClickRow: function (index,row) {
        row.editing = true;
        $(this).datagrid('beginEdit', index);
        lastRowIndex = index;
    },
    onBeforeEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
     },
    onAfterEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
    },
    onCancelEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
    },
     */
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

        var rr = $(this).datagrid('getSelected');
        if ($(this).datagrid('getRowIndex', rr)==-1){
            // alert("沒有資料");
            row = $("#job_title_dg").datagrid('getSelected');
            if ($("#job_title_dg").datagrid('getRowIndex', row)>-1){
                console.log(" job_title=",row['job_code'],"  job_name=",row['job_name']);
                main_form.id_job_title.value = row['job_code'];
                main_form.id_job_skill.value = '';
            }
        }
    }
}

config.job_title_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    idField: "job_code",
    columns: [[
        {field: 'job_code', title: '職務代號', width: 120, sortable:true,},
        {field: 'job_name', title: '職務名稱', width: 200, sortable:true,},
     ]],
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
    },
    onSelect: function(index, row) {
        currentRowIndex_east = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        main_form.id_job_title.value = row['job_code']
        $("#main_dg").datagrid({
            queryParams: {
                job_title_id: row['job_code'],
            },
        });
        setFormData(main_form, row);
        centerControl('update');

        $('#main_dg').datagrid({autoLoad:true});
        $('#main_dg').datagrid('selectRow',currentRowIndex_center);
    },

    onLoadSuccess: function(data) {
        var len = data.total;
        currentEvent = '';
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
    $('#job_title_dg').datagrid('enableFilter');

    $('#new_btn').click(function(){
         centerControl('new');
         get_order_number();
    });

    $('#create_btn').click(function(){
        // 新增
        currentEvent= 'new';
        if(!formValidate(main_form)) return;
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
                    // $('#job_title_dg').datagrid('reload');
                    idFieldValue = data['id'];
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('錯誤!'+'\n\n'+res.message);
                }
            }
        });
    });


    $('#cancel_btn').click(function(){
         currentEvent = 'ready';
        centerControl('update');
        $('#main_dg').datagrid('reload');
        // $('#job_title_dg').datagrid('reload');
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
                    // $('#job_title_dg').datagrid('reload');
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
                // $('#job_title_dg').datagrid('reload');
                currentEvent = 'delete';
            } else {
                currentEvent = null;
                alert('錯誤'+'\n\n'+res.message);
            }
        });
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
});




