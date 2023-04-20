
config.cpx_search_dlg = {
    'dlg': {
        resizable: true,
        modal: true,
        closed: true,
    },
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
    remoteSort: false,
    idField: "id",
    columns: [[
        {field: 'date_yyyy', title: '年', width: 60,align: 'center', sortable:true,},
        {field: 'quarter', title: '季', width: 40,align: 'center', sortable:true,},
        {field: 'work_code', title: '工號/姓名', width: 150,align: 'center', sortable:true,},
        {field: 'bpm_number', title: 'BPM單號', width: 180, align: 'center',sortable:true,},
        {field: 'bpm_status', title: 'BPM狀態', width: 100, align: 'center',sortable:true,},
        {field: 'report_url', title: '報表名稱<br>( 滑鼠按一下,可開啟檔案 )', width: 250, align: 'center',sortable:true,
            formatter: function(value,row,index){
                if ( value===null ){
                    return " ";
                } else {
                    var pdf_url = value.split("/");
                    return "<a href='"+value+"' target='_blank'>"+pdf_url[pdf_url.length-1]+"</a>";
                }
            }
        },
        {field: 'director', title: '評核主管', width: 150, align: 'center',sortable:true,},
        {field: 'changer', title: '異動人', width: 100, align: 'center',sortable:true,},
        {field: 'change_time', title: '異動時間', width: 150, align: 'center',sortable:true,},
     ]],
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
    }
}



$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;                   // view.py 裏定義的
    var formSourceUrl = $('#main_form').attr('action');   // form.py 裏定義的
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#main_dg').datagrid('reorderColumns', columnOrder);
    $('#main_dg').datagrid('enableFilter');
});




