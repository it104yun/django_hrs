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
        if(row[fieldName] == undefined) continue;
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
            main_form.program.disabled=false;
            var programExcludes = $("#main_dg").datagrid('getData').rows.map(function(row){
                return row.program_id
            });
            var programs = allPrograms.filter(function(program){
                return !programExcludes.includes(program.program_id);
            });
            var options = programs.map(function(program){
                return '<option value="'+program.program_id+'">'+program.program+'</option>';
            }).join('');
            $("#id_program").focus();
            main_form.program.innerHTML = options;
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.program.disabled=true;
            var options = allPrograms.map(function(program){
                return '<option value="'+program.program_id+'">'+program.program+'</option>';
            }).join('');
            main_form.program.innerHTML = options;
            break
        default:
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            break
    }
}


var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var rowCount = 0;
config.user_dg = {
    method: 'get',
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    columns:[[
        {field:'user_id',title:'帳號',sortable:true,},
        {field:'user',title:'姓名',sortable:true,},
    ]],
    queryParams: {
        factory: currentFactory
    },
    autoRowHeight: false,
    singleSelect: true,
    onSelect: function(index, row) {
        centerControl('update');
        $("#main_dg").datagrid({
            queryParams: {
                factory_id: currentFactory,
                user_id: row['user_id']
            },
        });
        main_form.user_id.value = row['user_id'];
    },
    onLoadSuccess: function(data) {
        $(this).datagrid('selectRow', 0);
    }
}

config.main_dg = {
    singleSelect: true,
    method: 'get',
    autoLoad: true,
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$('#main_dg').data().key];
        centerControl('update');
        setFormData(main_form,row);
    },
    onLoadSuccess: function(data) {
        $("#main_dg").datagrid('selectRow', currentRowIndex);
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
    var userUrl = $('#user_dg').data().source;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#user_dg').datagrid('enableFilter');

    $('#new_btn').click(function(){
        resetForm(main_form);
        main_form.elements[1].focus();
        centerControl('new');
    });
    $('#create_btn').click(function(){
        // 新增
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
                    alert('錯誤!')
                }
            }
        )
    });
    $('#cancel_btn').click(function(){
        // 取消新增
        $('#main_dg').datagrid('selectRow', 0);
    });
    $('#update_btn').click(function(){
        // 修改
        data = getFormData(main_form);
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('錯誤!')
                }
            }
        )
    });
    $('#delete_btn').click(function(){
        // 刪除
        if(!confirm('確定要刪除?')) return;
        $.get(
            formSourceUrl + '/' + currentKey,
            function(res) {
                if(res.success) {
                    alert('刪除成功!')
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('錯誤!')
                }
            }
        );
    });


        program_id_url = "/api/get_factory_auth_user/"+currentFactory;
    $.get(
        program_id_url,
        function (res) {
            if (res) {
                optionTxt = res;
                $('#searchWordCode').combobox({
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
        var user_account = $('#searchWordCode').val().split(' ');
        if ( user_account!='') {
            $("#user_dg").datagrid({
                queryParams: {
                    factory_id: currentFactory,
                    user_id: user_account[0],
                },
            });
            $('#main_dg').datagrid('reload');
        }
    });


    $('#search_clear').click(function (){
        $("#searchWordCode").combobox('setValue','');
        $("#user_dg").datagrid({
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


