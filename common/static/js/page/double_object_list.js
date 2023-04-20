var timer = null;
var currentKey = '';
var currentRowIndex = 0;
var rowCount = 0;
var config = {
    'system_tree': {
        type: 'POST',
        checkbox: false,
        crossDomain: false,
        onClick: function (node) {
            if (node.attributes.url) {
                window.location = node.attributes.url;
            }
        }
    },
    'cpx_search_dlg': {
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
    },
    'main_dg': {
        //FIXME: component
        method: 'get',
        autoRowHeight: false,
        ctrlSelect: true,
        onSelect: function (index, row) {
            clearTimeout(detailTimer);
            var detailTimer = setTimeout(
                function() {
                    fetchDetailData();
                    // 延遲讀取細項資料
                }, 200
            )
            currentRowIndex = index;
            currentKey = row[$(this).data().key];
            $(document).trigger('select-update');
            setFormData(main_form, row);
            fetchMainData();
        },
        onLoadSuccess: function (data) {
            $(this).datagrid('selectRow', currentRowIndex);
            rowCount = data.total;
        }
    },
    'main_mono_search_dlg': {
        resizable: true,
        modal:true,
        closed: true,
    },
    'detail_dg': {
        singleSelect: true,
        toolbar: '#detail_dg_tb',
        method: 'get',
        autoLoad: false,
        onBeforeLoad:function(){
            var opts = $(this).datagrid('options');
            return opts.autoLoad;
        },
        getNewRow: function(columns){
            var row = {}
            for(i of columns) {
                row[i] = 0;
            }
            row['main_id'] = currentKey;
            return row
        },
        onAccept: function(row, columns) {
            var datas = {};
            for (var i = 0; i < columns.length; i++) {
                key = columns[i];
                datas[key] = row[key];
            }
            datas['main_id'] = currentKey;
            if (row.seq) {
                var url = this.url + '/' + row.seq;
            } else {
                var url = this.url ;
            }
            $.post(
                url, datas, function(res){
                    if(res.success) {
                        alert('Success!');
                        $('#detail_dg').datagrid('reload');
                    } else {
                        alert(res.message)
                    }
                }
            )
        },
        //FIXME: remove, update problem
        onRemove: function(row) {
            if(row.seq) {
                var url = this.url;
                $.get(
                    url + '/' + row.seq,
                    function (res) {
                        if (res.success) alert('Deleted!');
                    }
                );
            }
            $('#detail_dg').datagrid('reload');
        },
    }
}
function fetchMainData() {
    $('#form').form({
        onBeforeLoad: function() {
            resetForm(main_form);
        },
        onLoadSuccess: function() {
            form.main_id.value = currentKey;
            $(document).trigger('fetch-main');
        }
    });
}

function fetchDetailData() {
    var url = $('#detail_dg').data().source + '?' + $('#detail_dg').data().key + '=' + currentKey;
    $('#detail_dg').datagrid({
        autoLoad: true,
        url: url
    });
}
$(document).ready(function(){
    window.formSourceUrl = $('#form').attr('action');
    $('#main_dg').datagrid('reorderColumns', columnOrder);

    $('#update_btn').click(function(){
        if(!formValidate(main_form)) return;
        if(!confirm('確定變更?')) return;
        // 更新
        row = getFormData(main_form);
        console.log(rwow)
        $('#form').form('submit',{
            url: formSourceUrl + '/' + currentKey,
            success: function(res) {
                var res = JSON.parse(res);
                if(res.success) {
                    // $('#main_dg').datagrid('updateRow', {
                    //     index: currentRowIndex,
                    //     row: row
                    // });
                    alert(gettext('已儲存!'))
                } else {
                    console.log('[Error]' + res.message);
                    alert(gettext('發生錯誤!'))
                }
            }
        });
    });
    $('#cancel_btn').click(function(){
        // 取消新增
        $('#main_dg').datagrid('selectRow', currentRowIndex);
    });
    $('#mono_search_btn').click(function(){
        //單一條件篩選
        $('#mono_search_dlg').dialog('open');
        $('#monoSearchForm').form('reset');
        $('#id_keyword').focus();
    });
    $('#monoSearchForm').submit(false);
    $('#monoSearchForm').keydown(function(e){
        if(e.keyCode==13) $('#mono_confirm_btn').click();
    });
    $('#mono_confirm_btn').click(function(){
        var searchParam = main_monoSearchForm.field_main.value
                        + '='
                        + main_monoSearchForm.keyword_main.value;
        var url = $('#main_dg').data().source + '&' + searchParam;
        $('#main_dg').datagrid({
            url: url
        });
        rowCount = $('#main_dg').datagrid('getData').total;
        $('#mono_search_dlg').dialog('close');
        $('#main_dg').datagrid('selectRow', 0);
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
            currentRowIndex = currentRowIndex + 1 < rowCount ? currentRowIndex + 1 : currentRowIndex;
            $('#main_dg').datagrid('selectRow', currentRowIndex);
        }
    });
});


