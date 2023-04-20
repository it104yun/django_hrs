$(document).ready(function(){
    var edg = $('.edg');
    edg.each(function(){
        var dataSource = $(this).data().source;
        var edgID = $(this).prop('id');
        config[edgID]['url'] = dataSource;
        config[edgID]['onClickCell'] = onClickCell;
        $(this).datagrid(config[edgID]);
    });
});

function onClickCell(index, field){
    if (editIndex != index){
        if (endEditing($(this))){
            $(this).datagrid('beginEdit', index);
            var ed = $(this).datagrid('getData', {index:index,field:field});
            if (ed){
                ($(ed.target).data('textbox') ? $(ed.target).textbox('textbox') : $(ed.target)).focus();
            }
            editIndex = index;
        }
    }
}

var editIndex = undefined;
function endEditing(dg){
    if (editIndex == undefined){return true}
    if ($(dg).datagrid('validateRow', editIndex)){
        $(dg).datagrid('endEdit', editIndex);
        return true;
    } else {
        return false;
    }
}
function append(btn){
    var dg = btn.dataset.dg;
    if (endEditing(dg)){
        editIndex = $(dg).datagrid('getRows').length;
        var columns = $(dg).datagrid('getColumnFields');
        var dgID = $(dg).prop('id');
        if(config[dgID].hasOwnProperty('getNewRow')) {
            var row = config[dgID]['getNewRow'](columns);
        } else {
            var row = columns;
        }
        $(dg).datagrid('appendRow', row);
        $(dg).datagrid('beginEdit', editIndex);
    }
}
function removeit(btn){
    if (editIndex == undefined){return}
    var dg = btn.dataset.dg;
    var row = $(dg).datagrid('getData').rows[editIndex];
    var dgID = $(dg).prop('id');
    if(!confirm('確定要刪除?')) return;

    if(config[dgID].hasOwnProperty('onRemove')) {
        config[dgID]['onRemove'](row);
    } else {
        $(dg).datagrid('cancelEdit', editIndex)
             .datagrid('deleteRow', editIndex);
    }
    editIndex = undefined;
}
function acceptit(btn){
    var dg = btn.dataset.dg;
    if (endEditing(dg)){
        if(editIndex==undefined) return;
        $(dg).datagrid('acceptChanges');
        var dgID = $(dg).prop('id');
        var row = $(dg).datagrid('getData').rows[editIndex];
        var columns = $(dg).datagrid('getColumnFields');

        if(config[dgID].hasOwnProperty('onAccept')) {
            config[dgID]['onAccept'](row, columns);
        }
        editIndex = undefined;
    }
}
function getChanges(btn){
    var dg = btn.dataset.dg;
    var rows = $(dg).datagrid('getChanges');
    alert(rows.length+' 筆資料已變更。');
}
