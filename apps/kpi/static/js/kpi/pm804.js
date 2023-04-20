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

function setGridData(row,this_status) {
    var rowData = {};
    var row,fields,values,rowNums,colNums,rowVal;
    fields = Object.keys(row);
    values = Object.values(row);
    colNums = fields.length;
    for ( var i=0 ; i<colNums ; i++){
        switch (fields[i]){
            case 'metrics_id':
                rowData[fields[i]] = values[i];
                break;
            case 'actual_score':
                rowData[fields[i]] = values[i];
                break;
            case 'metrics_calc':
                 rowData[fields[i]] = values[i];
                break;
            case 'calc_content':
                rowData[fields[i]] = values[i];
                break;
            case 'last_status':
                rowData[fields[i]] = this_status;
                break;
            default:
                break;
        }
    }
    return rowData;
}


function findRowDatas(Year, Month){
    var dg = $('#metrics_setupDate_dg');
    var row = null;
    var rows = dg.datagrid('getRows');
    for(var i=0,len=rows.length; i<len; i++){
        if ( rows[i]['date_yyyy']==Year && rows[i]['date_mm']==Month ){
            row = rows[i];
            break;
        }
    }
    if (row){
        var index = dg.datagrid('getRowIndex', row);
        dg.datagrid('selectRow', index);
    } else {
       dg.datagrid('selectRow', 0);
    }
}


function centerControl(event) {
    main_form.id_work_code.disabled=true;
    main_form.id_metrics_type.disabled=true;
    main_form.id_metrics_type.options[2].selected=true;
    main_form.id_date_yyyy.disabled=true;
    main_form.id_date_mm.disabled=true;
    switch(event) {
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



//About grid editor------------------------------------------------------------------------------------------begin
function customCollapseRow() {
     $('#main_dg').datagrid({
         collapseRow: function (jq, index) {
             return jq.each(function () {
                 var opts = $(this).datagrid('options');
                 var dc = $.data(this, 'datagrid').dc;
                 var expander = $(this).datagrid('getExpander', index);
                 if (expander.hasClass('datagrid-row-collapse')) {
                     expander.removeClass('datagrid-row-collapse').addClass('datagrid-row-expand');
                     var tr1 = opts.finder.getTr(this, index, 'body', 1).next();
                     var tr2 = opts.finder.getTr(this, index, 'body', 2).next();
                     tr1.hide();
                     tr2.hide();
                     dc.body2.triggerHandler('scroll');
                     if (opts.onCollapseRow) {
                         var row = $(this).datagrid('getRows')[index];
                         opts.onCollapseRow.call(this, index, row);
                     }
                 }
             });
         }
     })
}

function customExpandRow() {
    $('#main_dg').datagrid({
            onExpandRow: function (index, row) {
                var ddv = $(this).datagrid('getRowDetail', index).find('table.ddv');
                ddv.datagrid({
                    url: '/api/get_metrics_calc/' + row.metrics_id,
                    fitColumns: true,
                    singleSelect: true,
                    rownumbers: false,
                    loadMsg: '',
                    height: 'auto',
                    columns: [[
                        {field: 'order_number', title: '計算<br>順序', width: 40, align: 'right',},
                        {field: 'calc_content', title: '計算方式', width: 600,},
                        {field: 'lower_limit', title: '下限&nbsp;&nbsp;<br>( >= )', width: 70, align: 'right',},
                        {field: 'upper_limit', title: '上限<br>( < )', width: 70, align: 'right',},
                        {
                            field: 'score', title: '得分', width: 100, align: 'right', styler: function (value, row, index) {
                                return 'background-color:#eeeeee;color:blue;';
                            }
                        },
                    ]],
                    onResize: function () {
                        $('#main_dg').datagrid('fixDetailRowHeight', index);
                    },
                    onLoadSuccess: function () {
                        setTimeout(function () {
                            $('#main_dg').datagrid('fixDetailRowHeight', index);
                        }, 0);
                    }
                });
                $('#main_dg').datagrid('fixDetailRowHeight', index);
            },
    })
}



var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var rowCount = 0;
var rowCount_main_dg = 0;
var lastIndex;
var currentYear;
var currentMonth;


//north_grid-->main_form
config.employee_info_easy_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    rowStyler: function(index,row){
        if (row.allocation==0){
            return 'background-color:#ffffe0;color:blue;'; // return inline style
        }
    },
    onSelect: function(index, row) {
        work_code_key = row['work_code']
        eastSourceUrl = "/api/get_metrics_setupDate_data_search/"+ work_code_key+"/"+workingYear;
        $('#metrics_setupDate_dg').datagrid({
                url : eastSourceUrl,
                columns:[[
                    // {field:'work_code',title:'工號',},
                    {field:'date_yyyy',title:'年度',width:60,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
                    {field:'date_mm',title:'月(季)',width:60,align:'center',styler: function(value,row,index){return 'color:blue;font-weight:bold;';}},
                ]]
            });
        $('#metrics_setupDate_dg').datagrid('selectRow',0);
    },
    onLoadSuccess: function(data) {
        //個人指標:共同指標不出現
        var i = 0;
        while( i < data.rows.length ){
            if ( data.rows[i]['work_code'].search("-") > -1) {
                //有找到的("共同指標")，刪除
                $(this).datagrid('deleteRow',i);
            }
            else {
              i++;
            };
        }
        $(this).datagrid('selectRow', 0);
    }
}


//east_grid-->main_form-->down
config.metrics_setupDate_dg = {
    method: 'get',
    autoRowHeight: false,
    singleSelect: true,
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        currentYear = row['date_yyyy'];
        currentMonth = row['date_mm'];
        setFormData(main_form, row);
        centerControl('update');
        $("#main_dg").datagrid({
            queryParams: {
                work_code_id:work_code_key,
                date_yyyy: row['date_yyyy'],
                date_mm: row['date_mm'],
            },
        });
        main_form.date_yyyy.value = row['date_yyyy'];
        main_form.date_mm.value = row['date_mm'];
    },
    onLoadSuccess: function(data) {
        findRowDatas(workingYear, workingMonth);
        rowCount = data.total;
        $('#searchYear').val('');
    }
}


// east grid 和 center的main_form 同步
config.main_dg = {
    singleSelect: true,
    method: 'get',
    autoLoad: true,
    iconCls: 'icon-edit',
    idField: 'metrics_id',

    //----------------------------------------------------------------------------------------------------------------------------------------------------------
    view: detailview,
    columns: [[
        // {field:'metrics_id',title:'', width:80, align:'left',},
        // {field:'date_yyyy',title:'年', width:80, align:'center',},
        // {field:'date_mm',title:'月', width:40, align:'center',},
        {field: 'order_number', title: '順序', width: 40, align: 'right',},
        {field: 'order_item', title: '順序<br>細項', width: 40, align: 'right',},
        {field: 'metrics_content', title: '指標內容', width: 450,},
        {field: 'unit_Mcalc', title: '單<br>位', width: 50, align: 'center',},
        {
            field: 'allocation', title: '配分<br>(權重)', width: 100, align: 'right',
            styler: function (value, row, index) {
                return 'color:blue;';
            },
        },
        {field: 'actual_score', title: '實績', width: 100, align: 'center'},
        {
            field: 'calc_content', title: '計算方式', width: 200, align: 'left',
            styler: function (value, row) {
                if (row.metrics_calc == 0) {
                    return 'background:LightYellow ;color:red;';
                } else {
                    return 'background:Black;color:White;';
                }
            }
        },
        {
            field: 'metrics_calc', title: '得分', width: 100, align: 'right',
            styler: function (value, row) {
                if (value == 0) {
                    return 'background:LightYellow ;color:red;';
                } else {
                    return 'background:Black;color:White;';
                }
            }
        },
        {field: 'status_desc', title: '狀態', width: 100, align: 'center',},
        {field: 'score_type', title: '評核<br>方式', width: 100, align: 'center',},
    ]],
    onClickRow: function (rowIndex, row) {
        if (lastIndex != rowIndex) {

            $(this).datagrid('collapseRow', lastIndex);

        }
        lastIndex = rowIndex;
    },
    rowStyler: function(index,row){
        if (row.allocation==0){
            return 'background-color:#ffffe0;color:blue;'; // return inline style
        }
    },
    detailFormatter:function(index,row){
        return '<div style="padding:2px"><table class="ddv"></table></div>';
    },
    onExpandRow: function(index,row){
        var ddv = $(this).datagrid('getRowDetail',index).find('table.ddv');
        ddv.datagrid({
            url:'/api/get_metrics_calc/'+row.metrics_id,
            fitColumns:true,
            singleSelect:true,
            rownumbers:false,
            loadMsg:'',
            height:'auto',
            columns:[[
                {field:'order_number',title:'計算<br>順序', width:40, align:'right',},
                {field:'calc_content',title:'計算方式', width:650,},
                {field:'lower_limit',title:'下限&nbsp;&nbsp;<br>( >= )', width:50, align:'right',},
                {field:'upper_limit',title:'上限<br>( < )', width:50, align:'right',},
                {field:'score',title:'得分', width:100, align:'right',styler: function(value,row,index){return 'background-color:#eeeeee;color:blue;';}},
                {field:' ',title:' ', width:12, align:'right',styler: function(value,row,index){return 'background-color:#eeeeee;color:blue;';}},
                {field:' ',title:' ', width:12, align:'right',styler: function(value,row,index){return 'background-color:#eeeeee;color:blue;';}},
            ]],
            onResize:function(){
                $('#main_dg').datagrid('fixDetailRowHeight',index);
            },
            onLoadSuccess:function(){
                setTimeout(function(){
                    $('#main_dg').datagrid('fixDetailRowHeight',index);
                },0);
            }
        });
        $('#main_dg').datagrid('fixDetailRowHeight',index);
    },
    //----------------------------------------------------------------------------------------------------------------------------------------------------------
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$('#main_dg').data().key];
        centerControl('update');
        setFormData(main_form,row);
    },
    onLoadSuccess: function(data) {
        rowCount_main_dg = data.total;
        //若grid沒有任何一筆資料，會沒反應，回不到主畫面;若有資料，currentRowIndex會是east grid的，不會是main grid的
        // $("#main_dg").datagrid('selectRow', 0)
        // 計算grid指標分數
        var allocation_tot = 0;
        var score_tot = 0;
        for (var i=0 ; i<rowCount_main_dg ; i++){
            if ( parseFloat(data.rows[i]['order_number'])<900 ){
                allocation_tot += parseFloat(data.rows[i]['allocation']);
            }
            if ( data.rows[i]['metrics_calc']!=null){
                score_tot += parseFloat(data.rows[i]['metrics_calc']);
            }
        }
        if ( score_tot==0 ){
            $('#id_score_tot').attr('style','width:100px;height:28px;text-align: right;background:LightYellow ;color:red;');
        }else {
            $('#id_score_tot').attr('style','width:100px;height:28px;text-align: right;background:Black;color:White;');
        }
        main_form.allocation_tot.value = allocation_tot.toFixed(2);
        main_form.score_tot.value = score_tot.toFixed(2);
    }
}


$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    centerControl();
    $('#main_dg').datagrid('reorderColumns', columnOrder);

    //EasyUI控制Grid的Column格式
    //field : 必需在〝Django view〞中有定義
    //title : 就算在〝Django view〞中有定義，在這兒還是要重新定義一次，若無定義會顯示為〝空白〞
    // subgrid(expand grid)

    // northSourceUrl = "/api/get_metrics_setup_subs_data/" + work_code_key;
    northSourceUrl = "/api/get_metrics_setup_subs_data/" + "all";
    $('#employee_info_easy_dg').datagrid({
        url: northSourceUrl,
        columns: [[
            {field: 'work_code', title: '工號', width: 80,},
            {field: 'chi_name', title: '姓名', width: 80,},
            {field: 'dept_name', title: '部門', width: 160,},
            {field: 'pos_name', title: '職位', width: 80,},
            {field: 'director_id', title: '主管工號', width: 80,},
            {field: 'director_name', title: '主管姓名', width: 80,},
            {field: 'arrival_date', title: '到職日', width: 100, align: 'center',},
            {field: 'resign_date', title: '離職日', width: 100, align: 'center',},
            {field: 'rank', title: '職等', width: 50, align: 'center',},
            {field: 'bonus_factor', title: '點數', width: 50, align: 'center',},
            {field: 'eval_class', title: 'KPI/BSC', width: 80, align: 'center',},
            {field: 'nat', title: '國籍', width: 70, align: 'center',},
        ]],
    })


    eastSourceUrl = "/api/get_metrics_setupDate_data_search/"+work_code_key+"/"+workingYear
    $('#metrics_setupDate_dg').datagrid({
            url : eastSourceUrl,
            columns:[[
                // {field:'work_code',title:'工號',},
                {field:'date_yyyy',title:'年度',width:60,align:'center',styler: function(value,row,index){return 'color:blue;';}},
                {field:'date_mm',title:'月(季)',width:60,align:'center',styler: function(value,row,index){return 'color:blue;';}},
            ]],
        });

    // alert("***目前評核年月\n\n"+"      "+workingYear +" 年"+ workingMonth +" 月");


// 顯示送出對話方塊
    $('#submit_btn').click(function () {
        $('#submit_dd').attr('hidden',false);

        $('#submit_dd').dialog({
            title: '送出',
            width: 400,
            height: 205,
            closed: false,
            cache: false,
            modal: true,
        });
    });


     $('#south_search_open').click(function (){
        $('#south_search_dd').attr('hidden',false);

        $('#south_search_dd').dialog({
            title: '指標資料搜尋',
            width: 350,
            height: 300,
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });



        $('#south_search_sumit').click(function(){
            work_code_key = $('#searchWorkCode').val();
            chi_name_key =$('#searchChiName').val();
            dept_key =$('#searchDept').val();

            //若未給x,會認定沒有此參數,url=/api/get_metrics_setup_data///,會找不到
            //給了x,才會有參數
            if (work_code_key==''){
                work_code_key='x'
            }
            if (chi_name_key==''){
                chi_name_key='x'
            }
            if (dept_key==''){
                dept_key='x'
            }
            // southSourceUrl = "/api/get_metrics_setup_data/"+ work_code_key+"/"+chi_name_key+"/"+dept_key;
            southSourceUrl = "/api/get_metrics_setup_data/"+ work_code_key+"/"+chi_name_key+"/"+dept_key+"/all";
             $('#employee_info_easy_dg').datagrid({url: southSourceUrl});
        });
        $('#south_search_clear').click(function (){
            $("#south_search_dd input").val('');
        });
    });



    $('#search_sumit').click(function () {
        eastSourceUrl = "/api/get_metrics_setupDate_data_search/" + work_code_key + "/" + $('#searchYear').val();
        $('#metrics_setupDate_dg').datagrid({
            url: eastSourceUrl,
            columns: [[
                // {field:'work_code',title:'工號',},
                {
                    field: 'date_yyyy', title: '年度', width: 65, align: 'center', styler: function (value, row, index) {
                        return 'color:blue;';
                    }
                },
                {
                    field: 'date_mm', title: '月(季)', width: 65, align: 'center', styler: function (value, row, index) {
                        return 'color:blue;';
                    }
                },
            ]],
            onLoadSuccess: function (data) {
                if ( $('#searchYear').val()==workingYear ) {
                    findRowDatas(workingYear, workingMonth);
                } else {
                    $(this).datagrid('selectRow', 0);
                };
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

    function resetCenterArea(form_id,dg_id) {
        $('#' + form_id).form('reset');                                 //jQuery 清空form
        $('#'+ dg_id).datagrid('loadData', {"total":0,"rows":[]});　　　//easyUi 清空Grid

        $(document).trigger('reset_' + form_id);
        $(document).trigger('reset_' + dg_id);

    }

});


