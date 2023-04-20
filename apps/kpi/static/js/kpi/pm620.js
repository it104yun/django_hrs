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
        switch (event) {
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
var idFieldValue = null;       //新增時的值
var currentEvent = null;

config.main_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    remoteSort: false,           // 資料已經查好，由轉發得來，不需要再後端查詢
    columns:[[
        {field:'work_code',title:'員工',width:130,align: 'center',sortable:true,},
        {field:'date_yyyy',title:'年度',width:75,align: 'center',sortable:true,},
        {field:'quarter',title:'季度',width:50,align: 'center',sortable:true,},
        // {field:'report_url',title:'報表位置/名稱<br>( 滑鼠按一下,可開啟檔案 )',width:550,align: 'center',sortable:true,
        //     formatter: function(value,row,index){ return "<a href='"+value+"' target='_blank'>"+value+"</a>"; }
        // },
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
        {field:'bpm_number',title:'BPM單號<br>(無自評者,無此單號)',width:150,align: 'center',sortable:true,},
        {field:'bpm_status',title:'BPM<br>送簽狀態',width:80,align: 'center',sortable:true,},
        {field:'director',title:'評核主管<br>(BPM確認的主管)',width:150,align: 'center',sortable:true,},
    ]],
    onSelect: function (index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function (data) {
        rowCount = data.total;
    },
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

        document.querySelector('.layout-split-east .panel-body').scrollTo(0, 0);
        $('#create_btn').hide();

        $('#main_dg').datagrid('reorderColumns', columnOrder);
        // $('#main_dg').datagrid({filterBtnIconCls:'icon-filter'});
        $('#main_dg').datagrid('enableFilter');
    });

