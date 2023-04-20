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
                if (isNaN(values[i]))
                    rowData[fields[i]] = ' '
                else
                    rowData[fields[i]] = parseFloat(values[i]).toFixed(2);
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
                        {field: 'calc_content', title: '計算方式', width: 750,},
                        {field: 'lower_limit', title: '下限&nbsp;&nbsp;<br>( >= )', width: 70, align: 'right',},
                        {field: 'upper_limit', title: '上限<br>( < )', width: 70, align: 'right',},
                        {
                            field: 'score', title: '得分', width: 68, align: 'right', styler: function (value, row, index) {
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

function saveEditRow(target){
    var rowIndex = getRowIndex(target);
    //以下動作, 只是為了『動一下』好讓『後端資料庫的資料得以顯示在螢幕上』; 重點在動一下, 除此之外, 無任何意義
    target.datagrid('endEdit', rowIndex);
    target.datagrid('collapseRow', rowIndex);
    target.datagrid('beginEdit', rowIndex);
}

function getRowIndex(target){
    var tr = $(target).closest('tr.datagrid-row');
    return parseInt(tr.attr('datagrid-row-index'));
}


function custom_alert_dd(){
    $('#alert_dd').attr('hidden', false);

    $('#alert_dd').dialog({
            title: '送出資訊',
            width: 400,
            height: 'atuo',
            closed: false,
            cache: false,
            modal: true,
    });

    $('#msg_sure').click(function (){
        $('#alert_dd').dialog({closed: true,});
    });

}


function getScore(currTarget,index, row) {
        var ed = currTarget.datagrid('getEditor', {
            index: lastIndex,
            field: 'actual_score',
        });
        if (ed) {
            var score = parseFloat($(ed.target).val());
            $.ajax({
                type: "get",
                url: '/api/get_metrics_calc/' + row.metrics_id,
                async: false,                 //非同步:false-->所以是冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
                success: function (res) {
                    var ll = res.length;
                    var out_of_limit = 'N';
                    if ( !isNaN(score) ) {
                        for (var i = 0; i < ll; i++) {
                            if (score >= res[i].lower_limit && score < res[i].upper_limit) {
                                row['metrics_calc'] = res[i].score;
                                row['calc_content'] = res[i].calc_content;
                                out_of_limit = 'N';
                                break;
                            } else {
                                row['metrics_calc'] = '';
                                row['calc_content'] = '';
                                out_of_limit = 'Y';
                            }
                        }
                    } else {
                        row['metrics_calc'] = '';
                        row['calc_content'] = '';
                    }

                    if ( out_of_limit=='Y' ) { 　
                        alert('輸入的『實績』不在"計算方式"的範圍內，請修正\n\n 若您未修正，得分將會設為０');
                    }
                    }
            });

            rows = currTarget.datagrid('getRows');
            var score_tot = 0;
            var rowsLen = 0;
            rowCount_main_dg = rows.length;
            for (var i = 0; i < rowCount_main_dg; i++) {
                if ( rows[i]['metrics_calc']!=null && rows[i]['metrics_calc']!='') {
                    score_tot += parseFloat(rows[i]['metrics_calc']);
                }
            }
            if (score_tot == 0) {
                $('#id_score_tot').attr('style', 'width:200px;height:68px;text-align: right;font-size:28px;background:LightYellow ;color:red;');
            } else {
                $('#id_score_tot').attr('style', 'width:200px;height:68px;text-align: right;font-size:28px;background:Black;color:White;');
            }
            if ( isNaN(score_tot) ){
                main_form.score_tot.value = '0';
            } else {
                main_form.score_tot.value = score_tot.toFixed(2);
            }
            row.editing = false;
            currTarget.datagrid('refreshRow', index);
        }
    }

function submit_dialog(close_yn){
    var target = $("#submit_dialog");
    target.empty();   //清空，避免上次顯示dialog的內容，再累加進來
    //使用append兩種方式的差別
    //1-target.append 只用一次,再將所有內容加起來
    //2-target.append 使用多次累加
    //第2種會於『current's appand之後』自動補上 ending tag，會造成許多困擾，將不符合預期的效果
    //第1種會原汁原味的呈現，不會自動補上任何東西（因為都符合html的寫法了）
    target.append('<div id="submit_dd">' +
        '			<div class="easyui-panel" title="" style="width:100%;height: auto;padding:0px;">' +
        '				<div id="score_zero_msg"  style="color:white;font: 15px bloder;background-color: #8b0000;"></div>' +
        '               <p></p>'+
        '				<span style="padding-left:20px;font-size: x-large;">您確定送出嗎?</span>' +
        '               <hr>				' +
        '               <div style="text-align:center;padding:10px;">' +
        '				   <button  id="submit_sure" class="btn btn-light btn-outline-danger">確定</button>' +
        '				   <span style="padding-left: 50px;padding-top: 10px;"></span>' +
        '				   <button  id="submit_cancel" class="btn btn-light btn-outline-secondary">取消</button>' +
        '				</div>' +
        '			</div>' +
        '		</div>	');

    $('#submit_dd').dialog({
        title: '送出',
        width: 750,
        height: 'auto',
        closed: close_yn,
        cache: false,
        modal: true,
    });
}


var currentKey = '';
var currentRow = null;
var currentRowIndex = 0;
var rowCount = 0;
var rowCount_main_dg = 0;
var lastIndex = 0;             //初值:預防一開始點選0行以上時, 無法編輯( currentIndex<> lastIndex)
var currentYear;
var currentMonth;
var lastEditRow;

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
        if ( row['date_yyyy']==workingYear && row['date_mm']==workingMonth && eval_class!='BSC'){
            $('#update_btn').attr('disabled',false);
            $('#submit_btn').attr('disabled',false);
            $('#recall_btn').attr('disabled',false);
            $('#cancel_btn').attr('disabled',false);
            // $(":input").removeAttr("disabled");
            // centerControl();
        }
        else {
            $('#update_btn').attr('disabled',true);
            $('#submit_btn').attr('disabled',true);
            $('#recall_btn').attr('disabled',true);
            $('#cancel_btn').attr('disabled',true);
            // $(":input").attr("disabled","disabled");
            // $("#logout").removeAttr("disabled");
            // $("#factory_select").removeAttr("disabled");
        };
    },
    onLoadSuccess: function(data) {
        // $(this).datagrid('selectRow', currentRowIndex);
        findRowDatas(workingYear, workingMonth);
        rowCount = data.total;
        if (rowCount==0) {
            $('#update_btn').attr('disabled',true);
            $('#submit_btn').attr('disabled',true);
            $('#recall_btn').attr('disabled',true);
            $('#cancel_btn').attr('disabled',true);
        }
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
        {field: 'metrics_content', title: '指標內容', width: 425,},
        {field: 'unit_Mcalc', title: '單<br>位', width: 50, align: 'center',},
        {
            field: 'allocation', title: '配分<br>(權重)', width: 75, align: 'right',
            styler: function (value, row, index) {
                return 'color:blue;';
            },
        },
        {field: 'actual_score', title: '實績', width: 100, align: 'right',
            // formatter:function(value,row,index){ if (value == 0){ return '0'} else { return  value }  },    //解決easyui值為 integer 而且 == 0, 不顯示的bug  2021/7/29 add
            // 上列取消的原因:為後端的問題 'actual_score':dataTuple[15] if dataTuple[15] else None-->'actual_score':dataTuple[15] if dataTuple[15] else ( 0 if dataTuple[15]==0 else None)
            //  dataTuple[15] if dataTuple[15] else None    # 0 和 null 都會為false, 若不加第二段if, 傳到前端會變成null
            //  dataTuple[15] if dataTuple[15] else ( 0 if dataTuple[15]==0 else None)
            editor: {type: 'text'},
        },
        {
            field: 'calc_content', title: '計算方式', width: 200, align: 'left',
            styler: function (value, row) {
                if (row.metrics_calc == '0') {
                    return 'background:LightYellow ;color:red;';
                } else {
                    return 'background:Black;color:White;';
                }
            }
        },
        {
            field: 'metrics_calc', title: '得分', width: 100, align: 'right',
            // formatter:function(value,row,index){ if (value == 0){ return '0'} else { return  value }  },    //解決easyui值為 integer 而且 == 0, 不顯示的bug  2021/7/29 add
            styler: function (value, row) {
                if (value == 0) {
                    return 'background:LightYellow ;color:red;';
                } else {
                    return 'background:Black;color:White;';
                }
            }
        },
        {field: 'status_desc', title: '狀態', width: 80, align: 'center',},
        // {field: 'score_type', title: '評核<br>方式', width: 80, align: 'center',},
        {field: 'metrics_type', title: '指標<br>類型', width: 80, align: 'center',},
        /*
        {field:'action',title:'',width:80,align:'center',
                formatter:function(value,row,index){
                    var s = '<a href="javascript:void(0)" onclick="saveEditRow(this)" class="btn btn-outline-primary">確定</a> ';
                    lastEditRow = this;
                    return s;
                }
            },
         */
    ]],
    onClickRow: function (rowIndex, row) {
        if (((row.last_status >= last_status && row.last_status < next_status) || row.last_status == null) &&
            (row.date_yyyy == workingYear && row.date_mm == workingMonth ) &&
            ( eval_class != 'BSC')
        ) {
            // if (lastIndex != rowIndex) {    2021/7/29 加入 ( lastIndex==0 && rowIndex==0) )
            // if ( (lastIndex != rowIndex) || ( lastIndex==0 && rowIndex==0) ){
                $(this).datagrid('endEdit', lastIndex);
                $(this).datagrid('collapseRow', lastIndex);
                $(this).datagrid('beginEdit', rowIndex);
            // }
        } else {
            $(this).datagrid('endEdit', rowIndex);
            $(this).datagrid('collapseRow', lastIndex);
        }
        lastIndex = rowIndex;
    },
    onEndEdit: function (index,row){ getScore($(this),index,row); },
    onBeforeEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
        $(this).datagrid('expandRow', index);
     },
    onAfterEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
    },
    onCancelEdit:function(index,row){
        row.editing = false;
        $(this).datagrid('refreshRow', index);
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
                {field:'calc_content',title:'計算方式', width:600,},
                {field:'lower_limit',title:'下限&nbsp;&nbsp;<br>( >= )', width:50, align:'right',},
                {field:'upper_limit',title:'上限<br>( < )', width:50, align:'right',},
                {field:'score',title:'得分', width:50, align:'right',styler: function(value,row,index){return 'background-color:#eeeeee;color:blue;';}},
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
        //若grid沒有任何一筆資料，會沒反應，回不到主畫面;若有資料，currentRowIndex會是east grid的，不會是main grid的
        // $("#main_dg").datagrid('selectRow', 0)
        // 計算grid指標分數
        var rowCount_main_dg = data.rows.length;
        var allocation_tot = 0;
        var score_tot = 0;
        for (var i = 0; i < rowCount_main_dg; i++) {
            // console.log(typeof data.rows[i]['allocation'],data.rows[i]['allocation']);
            if ( parseInt(data.rows[i]['order_number'])<900 ){
                if ( data.rows[i]['order_number'] != null){
                     allocation_tot += parseFloat(data.rows[i]['allocation']);
                }
            }
            if ( data.rows[i]['metrics_calc']!=null &&  data.rows[i]['metrics_calc']!=''){
                score_tot += parseFloat(data.rows[i]['metrics_calc']);
            }
            if (score_tot == 0) {
                $('#id_score_tot').attr('style', 'width:200px;height:68px;text-align: right;font-size:28px;background:LightYellow ;color:red;');
            } else {
                $('#id_score_tot').attr('style', 'width:200px;height:68px;text-align: right;font-size:28px;background:Black;color:White;');
            };
            if ( i==0) {
                //狀態碼在允許編輯範圍
                if (((data.rows[i]['last_status'] >= last_status && data.rows[i]['last_status'] < next_status) ||
                    data.rows[i]['last_status'] == null) &&
                    (data.rows[i]['date_yyyy'] == workingYear && data.rows[i]['date_mm'] == workingMonth)
                ) {
                    $('#update_btn').attr('disabled', false);
                    if ( data.rows[i]['last_status'] < last_status || data.rows[i]['last_status'] == null ){
                        $('#submit_btn').attr('disabled', true);     // 沒有儲存更新, "送出"按鈕不顯示
                    } else {
                        $('#submit_btn').attr('disabled', false);
                    }
                    $('#recall_btn').attr('disabled', false);
                    $('#cancel_btn').attr('disabled', false);
                } else {
                    $('#update_btn').attr('disabled', true);
                    $('#submit_btn').attr('disabled', true);
                    $('#recall_btn').attr('disabled', true);
                    $('#cancel_btn').attr('disabled', true);
                    //2021/3/29增加
                    // if ( data.rows[i]['actual_score']==null   ) {
                    //     data.rows[i]['actual_score'] = ' ';
                    // }
                }

            }
        }
        main_form.allocation_tot.value = allocation_tot.toFixed(2);
        // if ( isNaN(score_tot) ){
        //     main_form.score_tot.value = '0';
        // } else {
        main_form.score_tot.value = score_tot.toFixed(2);
        // }
    }
}


$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $("#main_dg").data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);

    $('#main_dg').datagrid('reorderColumns', columnOrder);
    if (eval_class!='BSC'){
        $('#update_btn').attr('disabled',false);
        $('#submit_btn').attr('disabled',false);
        $('#cancel_btn').attr('disabled',false);
        // $(":input").removeAttr("disabled");
        // centerControl();
    } else {
        $('#update_btn').attr('disabled',true);
        $('#submit_btn').attr('disabled',true);
        $('#cancel_btn').attr('disabled',true);
        // $(":input").attr("disabled","disabled");
        // $("#logout").removeAttr("disabled");
    }

    centerControl();

    //EasyUI控制Grid的Column格式
    //field : 必需在〝Dj)ango view〞中有定義
    //title : 就算在〝Django view〞中有定義，在這兒還是要重新定義一次，若無定義會顯示為〝空白〞
    // subgrid(expand grid)

    // eastSourceUrl = "/api/get_metrics_setupDate_data/"+work_code_key+"/"+workingYear
    eastSourceUrl = "/api/get_metrics_setupDate_data/"+work_code_key+"/"+workingYear+"/"+workingMonth
    $('#metrics_setupDate_dg').datagrid({
            url : eastSourceUrl,
            columns:[[
                // {field:'work_code',title:'工號',},
                {field:'date_yyyy',title:'年度',width:60,align:'center',styler: function(value,row,index){return 'color:blue;';}},
                {field:'date_mm',title:'月(季)',width:60,align:'center',styler: function(value,row,index){return 'color:blue;';}},
            ]],
        });

    // alert("***目前評核年月\n\n"+"      "+workingYear +" 年"+ workingMonth +" 月");



    $('#actual_score').textbox({
        onChange: function () {
            var current_main_row=$("#main_dg").datagrid('getSelected');
            alert(current_main_row);
        }
    })

// 顯示送出對話方塊
    $('#submit_btn').click(function () {
        submit_dialog(false);
        var arrayData = $('#main_dg').datagrid('getRows');
        var data = {};
        var arrayLen = arrayData.length;
        //送出前,得分0的檢查
        var zeroScore = [];
        var c=0;
        //檢查得分為0, 提出警告
        for (var i = 0; i < arrayLen; ++i) {
            if ( arrayData[i]['metrics_calc']==0 ){
                zeroScore[c] = "順序:　"+arrayData[i]['order_number']+"-"+arrayData[i]['metrics_content']+"  得分=０ <br>";
                c++;
            }
        }
        var score_zero_msg = zeroScore.toString().replace(/,/g,'')
        $("#score_zero_msg").empty();
        if (c!=0){
            //padding:20px  不能設定在html裏, 當沒有"得分=0"的錯誤訊息時, 會顯示沒有文字, 紅紅的一條, 很難看
            $("#score_zero_msg").append('<div style="padding:20px;">'+score_zero_msg+'</div>');
        }

        $('#submit_cancel').click(function (){
            $('#submit_dd').dialog('destroy');  //銷毀
        });

        $('#submit_sure').click(function (){
            var arrayData = $('#main_dg').datagrid('getRows');
            var data = {};
            var arrayLen = arrayData.length;
            var update_results = [];
            var update_success = [];
            var updated = true;
            var this_view_code = 'PM402';
            var this_action = 'submit';
            var this_status = status_submit;

            for (var i = 0; i < arrayLen; ++i) {
                statusSourceUrl = '/api/set_score_sheet_status/' + arrayData[i]['metrics_id'] + "/" + this_view_code + "/" + this_action;
                $.ajax({
                    type: "post",
                    url: statusSourceUrl,
                    data: data,
                    async: false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
                    success: function (res) {
                        if (res.success) {
                            $('#main_dg').datagrid('reload');
                            update_results [i] = '順序' + JSON.stringify(arrayData[i]['order_number']) + '-' + JSON.stringify(arrayData[i]['order_item']) + ' : 送出成功';
                            update_success [i] = true;
                        } else {
                            update_results [i] = '***順序' + JSON.stringify(arrayData[i]['order_number']) + '-' + JSON.stringify(arrayData[i]['order_item']) + ' : 送出失敗***';
                            update_success [i] = false;
                        }
                    }
                });
            }

            for (var i = 0; i < arrayLen; i++) {
                if (!update_success[i]) {
                    updated = false;
                    break;
                }
            }

            if (updated) {
                mailSourceUrl = '/api/get_score_sheet_sendmail_to_director/' + main_form.id_work_code.value + "/" + main_form.id_date_yyyy.value + "/" + main_form.id_date_mm.value;
                $('#mail_success').empty();
                $('#mail_success').empty();
                $('#send_fail').empty();
                $.get(mailSourceUrl,
                    function (res) {
                        if (res.success) {
                            $('#mail_success').append('送出成功！');
                            custom_alert_dd();
                        } else {
                            $('#mail_fail').append('送出失敗！');
                            custom_alert_dd();
                        }
                    }
                );
            } else {
                $('#send_fail').append('送出至主管 : 失敗');
                custom_alert_dd();
            }

            // $('#submit_dd').dialog({closed: true,});
            $('#submit_dd').dialog('destroy');//銷毀

        });
    });


// 顯示收回對話方塊
    $('#recall_btn').click(function () {
        $('#recall_dd').attr('hidden',false);

        $('#recall_dd').dialog({
            title: '收回',
            width: 400,
            height: 200,
            closed: false,
            cache: false,
            modal: true,
        });

        $('#recall_sure').click(function (){

        });


        $('#recall_cancel').click(function (){
            $('#recall_dd').dialog({closed: true,});
        });

     });


    $('#update_btn').click(function() {
        //----避免在存檔前, 最後一次的修改, 沒有寫進資料庫-------------2021/05/28 add------------Begin
            //取得最後一次edit grid的資料, 並將其寫入grid
            $('#main_dg').datagrid('endEdit', lastIndex);
            //取得最後一筆得分
            getScore($('#main_dg'),lastIndex,$('#main_dg').datagrid('getRows')[lastIndex]);
            //收合最後一次的row
            $('#main_dg').datagrid('collapseRow', lastIndex);
        //----避免在存檔前, 最後一次的修改, 沒有寫進資料庫-------------2021/05/28 add------------Ending

        processSourceUrl = '/api/score_sheet_process';
        var arrayData = $('#main_dg').datagrid('getRows');
        var data = {};
        var arrayLen = arrayData.length;
        var this_status = status_new;
        var update_results = [];
        var update_success = [];
        var updated = true;
        for (var i = 0; i < arrayLen; ++i) {
            data = setGridData(arrayData[i], this_status);
            $.ajax({
            type :"post",
            url :processSourceUrl,
            data :data,
            async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
            success :function(res){
                    if (res.success) {
                        $('#main_dg').datagrid('reload');
                        update_results [i] = '順序'+JSON.stringify(arrayData[i]['order_number'])+'-'+JSON.stringify(arrayData[i]['order_item'])+' : 更新成功';
                        update_success [i] = true;
                    } else {
                        update_results [i] = '***順序'+JSON.stringify(arrayData[i]['order_number'])+'-'+JSON.stringify(arrayData[i]['order_item'])+' : 更新失敗***';
                        update_success [i] = false;
                    }
                }
            });
        }
        // var alert_str ='';                                                  //偵錯用, 勿刪
        for (var i=0;i<arrayLen;i++){
            // alert_str += update_results[i]+'\n\n';                         //偵錯用, 勿刪
            // console.log(update_success[i],"   ",update_results[i]);        //偵錯用, 勿刪
            if (!update_success[i]){
                updated = false;
                break;
            }
        }
        // alert(alert_str);
        if (updated){
            alert('更新成功');
        } else {
            alert('錯誤');
        }
        $('#main_dg').datagrid('reload');
    })


    $('#search_sumit').click(function () {
        eastSourceUrl = "/api/get_metrics_setupDate_data/" + work_code_key + "/" + $('#searchYear').val();
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

    $('#cancel_btn').click(function(){
        $('#main_dg').datagrid('reload');
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


