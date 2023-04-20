function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        if(field.type === 'select-one') {
            formData[fieldName + '_id'] = field.value;
        }
        else if(field.type === 'checkbox') {
            formData[fieldName] = field.checked;
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
        if(row[fieldName] === undefined) continue;
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
function centerControl(event) {
    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.user.disabled=false;
            var userExcludes = $("#main_dg").datagrid('getData').rows.map(function(row){
                return row.user_id
            });
            var users = allUsers.filter(function(user){
                return !userExcludes.includes(user.user_id);
            });
            var options = users.map(function(user){
                return '<option value="'+user.user_id+'">'+user.user_id+" "+user.user+'</option>';
            }).join('');
            main_form.user.innerHTML = options;
            $("#id_user").focus();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.user.disabled=true;
            var options = allUsers.map(function(user){
                return '<option value="'+user.user_id+'">'+user.user_id+" "+user.user+'</option>';
            }).join('');
            main_form.user.innerHTML = options;
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
config.program_dg = {
    method: 'get',
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    columns:[[
        {field:'id',title:'程式代號',sortable:true,},
        {field:'program_id',title:'程式代號',sortable:true,},
        {field:'program',title:'程式名稱',sortable:true,},
    ]],
    queryParams: {
        factory: currentFactory
    },
    autoRowHeight: false,
    singleSelect: true,
    onSelect: function(index, row) {
        main_form.program_id.value = row.id;
        $("#main_dg").datagrid({
            queryParams: {
                factory_id: currentFactory,
                program_id: row['program_id']
            }
        });
    },
    onLoadSuccess: function() {
        $(this).datagrid('selectRow', 0);
    }
}
config.main_dg = {
    singleSelect: true,
    autoLoad: false,
    method: 'get',
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$("#main_dg").data().key];
        centerControl('update');
        setFormData(main_form, row);
    },
    onLoadSuccess: function(data) {
        $("#main_dg").datagrid('selectRow', 0);
        centerControl('update');
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
    }
}
$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var programUrl = $('#program_dg').data().source;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);

    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#program_dg').datagrid('enableFilter');

    $('#new_btn').click(function(){
        resetForm('main_form');
        main_form.elements[1].focus();
        centerControl('new');
    });
    $('#create_btn').click(function(){
        // 新增
        //
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        $.post(
            formSourceUrl,
            data,
            function(res) {
                if(res.success) {
                    alert('新增成功!')
                    $('#main_dg').datagrid('reload');
                    $('#main_dg').datagrid('selectRow', 0);
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
        // 新增
        var data = getFormData(main_form);
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                    $('#main_dg').datagrid('selectRow', currentRowIndex);
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
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('錯誤');
                }
            }
        );
    });


    program_id_url = "/api/get_factory_program_id/"+currentFactory+"/"+"ProgramID";
    $.get(
        program_id_url,
        function (res) {
            if (res) {
                optionTxt = res;
                $('#searchProgramID').combobox({
                    multiple: false,
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

    $('#east_search').click( function(){
        var program_id = $('#searchProgramID').val().split(' ');
        if ( program_id!='') {
            $("#program_dg").datagrid({
                queryParams: {
                    factory_id: currentFactory,
                    program_id: program_id[0],
                },
            });
            $('#main_dg').datagrid('reload');
        }
    });


    $('#search_clear').click(function (){
        $("#searchProgramID").combobox('setValue','');
        $("#program_dg").datagrid({
            queryParams: {
                factory_id: currentFactory,
            },
        });
        $('#main_dg').datagrid('loadData',[]);
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

});


