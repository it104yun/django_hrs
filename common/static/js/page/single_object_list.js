function centerControl(event) {
    switch(event) {
        case 'new':
            // 點下新增按鈕
            $(document).trigger('event-new');
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            break
        case 'update':
            // 點下更新按鈕
            $(document).trigger('event-update');
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
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

/*
config.main_mono_search_dlg = {
        resizable: true,
        modal: true,
        closed: true,

}
*/


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




config.main_dg = {
    //FIXME: component
    method: 'get',
    autoRowHeight: false,
    ctrlSelect: true,
    onSelect: function (index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        $(document).trigger('select-update');
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function (data) {
        $(this).datagrid('selectRow', currentRowIndex);
        rowCount = data.total;
    }
}




$(document).ready(function(){
    var formSourceUrl = $('#main_form').attr('action');
    centerControl('update');
    document.querySelector('.layout-split-east .panel-body').scrollTop = 0;
    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#new_btn').click(function(){
        resetForm(main_form);
        main_form.elements[1].focus();
        centerControl('new');
    });
    $('#create_btn').click(function(){
        if(!formValidate(main_form)) return;
        // 新增
        if(!confirm('確定新增?')) return;
        $('#main_form').form('submit', {
            success: function(res) {
                var res = JSON.parse(res);
                if(res.success) {
                    alert( '已儲存');
                    $('#main_dg').datagrid('reload');
                    centerControl('update');
                } else {
                    alert( '發生錯誤!');
                }
            }
        });
    });
    $('#cancel_btn').click(function(){
        // 取消新增
        resetForm(main_form);
        $('#main_dg').datagrid('selectRow', currentRowIndex);
    });
    $('#update_btn').click(function(){
        if(!formValidate(main_form)) return;
        if(!confirm('確定變更?')) return;
        // 更新
        $('#main_form').form('submit',{
            url: formSourceUrl + '/' + currentKey,
            success: function(res) {
                //res = JSON.parse(res);
                if(res.success) {
                    alert('...已儲存!')
                    $('#main_dg').datagrid('reload');
                } else {
                    alert('...發生錯誤!');
                }
            }
        });
    });
    $('#delete_btn').click(function(){
        // 刪除
        if(!confirm( '確定要刪除?')) return;
        $.get(formSourceUrl + '/' + currentKey,
            function(res) {
                if(res.success) {
                    alert( '已刪除!');
                    $('#main_dg').datagrid('reload');
                } else {
                    alert( '發生錯誤!');
                }
            }
        );
    });


    $("#complex_search_btn").click(function(){
        $("#cpx_search_dlg").dialog('open');
    });

    $('#main_monoSearchForm').submit(false);

    $('#main_monoSearchForm').keydown(function(e){
        if(e.keyCode==13) $('#search_btn_main').click();
    });

    $('#search_btn_main').click(function(){
        var searchParam = main_monoSearchForm.field_main.value +
                          '=' + main_monoSearchForm.keyword_main.value;
        var url = $('#main_dg').data().source + '?' + searchParam;
        $('#main_dg').datagrid({
            url: url
        });
        rowCount = $('#main_dg').datagrid('getData').total;
        $('#main_mono_search_dlg').dialog('close');
        $('#main_dg').datagrid('selectRow', 0);
    });



    $(document).keydown(function(e){
        // 主資料表上下移動選取資料。
        if(document.activeElement != document.getElementsByTagName('body')[0]) return;
        if(e.keyCode === 38) {
            // up
            currentRowIndex = currentRowIndex - 1 >= 0 ? currentRowIndex - 1 : currentRowIndex;
            $('#main_dg').datagrid('unselectAll');
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        } else if(e.keyCode === 40) {
            //down
            currentRowIndex = currentRowIndex + 1 <= rowCount ? currentRowIndex + 1 : currentRowIndex;
            $('#main_dg').datagrid('unselectAll');
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        }
    });

});


