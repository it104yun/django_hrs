var currentKey = '';
var currentRow = null;
var currentRowIndex_center = 0;
var currentRowIndex_north = 0;
var currentRowIndex_east = 0;
var rowCount = 0;
var currentEvent = null;

var rowCount_main_dg = 0;
var work_code_key = '';
var conditions=null;

config.employee_info_easy_dg = {
    method: 'get',
    // autoLoad: false,
    autoRowHeight: false,
    singleSelect: true,
    // url:"/sk_api/get_pdca_subs_data/" + userId,
    columns:[[
              {field: 'factory_name',title:gettext('公司'), width:80, align:'center',},
              {field:'dept_name',title:gettext('部門'), width:120,},
              {field:'work_code',title:gettext('工號'), width:80,},
              {field:'chi_name',title:gettext('姓名'), width:90,},
              {field:'arrival_date',title:gettext('到職日'), width:90, align:'center',},
              {field:'resign_date',title:gettext('離職日'), width:90, align:'center',},
              {field: 'rank',title:gettext('職等'), width:50, align:'center',},
              {field:'pos_name',title:gettext('職位'), width:100, },
              {field:'the_time',title:gettext('最新版本'), width:80, align:'center'},
              // {field:'change_time',title:'填寫日期', width:120, align: 'center' },
              // {field:'director_id',title:'主管工號', width:80,},
              // {field:'director_name',title:'主管姓名', width:80,},
              // {field: 'bonus_factor',title:'點數', width:40, align:'center',},
              // {field: 'eval_class',title:'KPI/BSC', width:70, align:'center',},
              // {field: 'nat',title:'國籍', width:80, align:'center',},
              // {field: 'factory_area',title:'廠區', width:80, align:'center',},
    ]],
    onSelect: function(index, row) {
        var frames = window.frames;
        $.ajax({
            type: "get",
            // url: '/sk_api/update_session_pdca/' + row['work_code']+"/"+row['work_code'],
            url: '/sk_api/update_session_pdca/' + row['work_code']+"/"+row['chi_name'],
            async: false,                 //非同步:false-->所以是冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        })
        frames[0].open('tt603_tab',"_self");
        currentRowIndex_north = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        work_code_key = row['work_code']
    },
    onLoadSuccess: function(data) {
        //個人指標:共同指標不出現
        var len = data.total;
        if (len==0){
            // centerControl('update');
        } else {
            var i = 0;
            while (i < len) {
                if (data.rows[i]['work_code'].search("-") > -1) {
                    //有找到的("共同指標")，刪除
                    $(this).datagrid('deleteRow', i);
                    len--;
                } else {
                    i++;
                }
                ;
            }
        }

     }
}



$(document).ready(function(){
    northSourceUrl = "/sk_api/get_pdca_subs_data/" + userId;
    $('#employee_info_easy_dg').datagrid({url:northSourceUrl});

    $('#south_search_open').click(function (){
        $('#south_search_dd').attr('hidden',false);

        $('#south_search_dd').dialog({
            title: gettext('指標資料搜尋'),
            width: 300,
            height: 'auto',
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });



        $('#south_search_sumit').click(function(){
            searchWorkCode = $('#searchWorkCode').val();
            searchChiName =$('#searchChiName').val();
            searchDept =$('#searchDept').val();

            //若未給x,會認定沒有此參數,url=/api/get_metrics_setup_data///,會找不到
            //給了x,才會有參數
            if (searchWorkCode == ''){
                searchWorkCode = 'x'
            }
            if (searchChiName == ''){
                searchChiName = 'x'
            }
            if (searchDept == ''){
                searchDept = 'x'
            }
            southSourceUrl = "/api/get_metrics_setup_data/"+searchWorkCode +"/"+searchChiName+"/"+searchDept+"/"+ userId;
            $('#employee_info_easy_dg').datagrid({url : southSourceUrl});
        });
        $('#south_search_clear').click(function (){
            $("#south_search_dd input").val('');
        });
    });


});

