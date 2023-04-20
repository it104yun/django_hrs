var cr_color = 'MistyRose';
// var ma_color = 'PaleGreen';
var ma_color = '#bfffbf';
var ge_color = 'lemonchiffon';
// var pr_color = 'PaleTurquoise';
var pr_color = '#CFEFEF';
// var xa_color = 'coral';
var xa_color = '#FFAF99';
var xb_color = 'SeaShell';
var col_field = '';
var datagridRowHeight = 40;
var lastRowIndex;
var err_work_code = "";
var err_chi_name = "";
var err_course = "";
var err_profession = "";    //沒有專業職能
var err_tabData = [];
var err_job_title = "";


function resetForm(form_id) {
    $('#' + form_id).form('reset');
    $(document).trigger('reset_' + form_id);
}

function getFormatedDateTime(){
    var dt = new Date();
    var Year,Month,Day,Hour,Minute,Second,MSecond;
    Year = (dt.getFullYear()).toString();
    Month = (dt.getMonth()+1).toString().padStart(2,'0');
    Day = (dt.getDate()).toString().padStart(2,'0');
    Hour = (dt.getHours()).toString().padStart(2,'0');
    Minute = (dt.getMinutes()).toString().padStart(2,'0');
    Second = (dt.getSeconds()).toString().padStart(2,'0');
    MSecond = (dt.getMilliseconds()).toString().padStart(3,'0');  //取得毫秒數 0~999
    return (Year+Month+Day+Hour+Minute+Second+MSecond)
}


function setGridHeaderStyle(dg){
    var columns = dg.datagrid('options').columns;                  //只會抓取columns( 未含frozenColumns )
    var col_field = '';
    var group_id = 'datagrid-td-group';
    var tabs_len = tabs.length+15;
    //columns[0]的color
    for ( var i=0; i<tabs_len ; i++){
        $( '#' + group_id + i.toString() +'-0-0').css({'background-color': cr_color});
        $( '#' + group_id + i.toString() +'-0-1').css({'background-color': ma_color});
        $( '#' + group_id + i.toString() +'-0-2').css({'background-color': ge_color});
        $( '#' + group_id + i.toString() +'-0-3').css({'background-color': pr_color});
        $( '#' + group_id + i.toString() +'-0-4').css({'background-color': xa_color});
        $( '#' + group_id + i.toString() +'-0-5').css({'background-color': xb_color});
    }

    len = columns[1].length;
    column = columns[1];
    for (var n = 0; n < len; n++) {
        col_field = column[n].field;
        sel_td = 'div.datagrid-header td[field=' + col_field + ']'
        var td = dg.datagrid('getPanel').find(sel_td);
        var color_area = col_field.substr(0, 2);
        switch (color_area) {
            case 'cr':            //核心職能
                td.css({'background-color':cr_color,'width':'120px'});
                break;
            case 'ma':           //管理職能
                td.css({'background-color':ma_color,'width':'120px'});
                break;
            case 'ge':          //一般職能
                td.css({'background-color':ge_color,'width':'120px'});
                break;
            case 'pr':          //專業職能
                td.css({'background-color':pr_color,'width':'120px'});
                break;
            case 'xa':          //加總,平均,等級
                td.css({'background-color':xa_color,'width':'120px'});
                break;
            case 'xb':          //人力資源策略-教育訓練方式
                td.css({'background-color':xb_color,'width':'300px'});
                break;
        }
    }

    columns = dg.datagrid('options').frozenColumns;                  //抓取frozenColumns
    len = columns[0].length;
    column = columns[0];

    var frozen_color = 'DarkSlateGrey';
    var font_color = 'white';
    for (var n = 0; n < len; n++) {
            fieldName = column[n].field;
            sel = 'div.datagrid-header td[field=' + fieldName + ']'
            var td = dg.datagrid('getPanel').find(sel);
            switch (fieldName) {
                case 'work_code':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '69px'});
                    // td.css({'background-color': frozen_color, 'color': font_color});
                    break;
                case 'chi_name':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '52px'});
                    // td.css({'background-color': frozen_color, 'color': font_color});
                    break;
                case 'year':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '40px'});
                    // td.css({'background-color': frozen_color, 'color': font_color,});
                    break;
                case 'month':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '25px'});
                    // td.css({'background-color': frozen_color, 'color': font_color,});
                    break;
                case 'pos_shc1':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '25px'});
                    break;
                case 'pos_shc2':
                    td.css({'background-color': frozen_color, 'color': font_color, 'width': '25px'});
                    break;
                case 'xx':
                    // td.css({'background-color': frozen_color, 'color': font_color, 'width': '4px'});
                    td.css({'background-color': frozen_color, 'color': font_color,});
                    break;
            }
        }
}



function reConfigGridColumns(i) {
    var arr_title = [];      // columns[1]
    var color_area="";
    var field_name = '';

    var cr_cols = 0;
    var ma_cols = 0;
    var ge_cols = 0;
    var pr_cols = 0;
    var xa_cols = 0;
    var xb_cols = 0;
    var all_cols = 1;
    var preTxt;
    var old_preTxt;
    var course_name = "";
    var tab_len = tabs.length;

    $.each(tab_fields[i],function(index,value){
        preTxt = (value.name).substr(0,2) ;
        if ( preTxt!=old_preTxt ){
            all_cols = 0;
        }
        old_preTxt = preTxt;
        all_cols ++ ;
        if ( preTxt=="xa" ) {
            //計算欄位:沒有editor
            arr_title.push({
                field: value.name,
                title: all_cols + '<br>' + '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                width: 120, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                align: value.name=="xa001" ? 'center':'left',
                editor: { type:'textbox', options:{disabled: true}},
                /*
                formatter: function (val,row,index){
                        if ( val == null ) { val="" };
                        var nbsp_num = 13-( val==null ? 0:val.length);
                        var rtn_nbsp = "";
                        if ( tab_len > 7 && i==0 ){
                            for ( var l=0 ; l <= nbsp_num ; l++){
                               rtn_nbsp += '&nbsp;';
                            }
                            if ( value.name == 'xa001'){
                                return "&nbsp;"+rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                            } else {
                                return val+rtn_nbsp+rtn_nbsp+"&nbsp;&nbsp;&nbsp;";
                            }
                        } else { return val }
                }
                 */
            })
        } else if ( preTxt=="xb" ){
            switch ( value.name ){
                case 'xb001':
                    //教育訓練
                    arr_title.push({
                    field: value.name,
                    title: all_cols+'<br>'+'<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">'+value.verbose_name+'</p>',
                    width: 300, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                    align: 'left',
                    editor: { type:'combobox',
                              options:{
                                        multiple: true,
                                        data: study_choices,      //這裏不一樣
                                        valueField:'value',
                                        textField:'text',
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
                                            $(this).combobox('setValue','');    //加空白,會自動在選擇時....加一個逗號, 這樣不論是否有在此輸入查詢關鍵字, 只要將第一個逗號前的資料去除,就可順利做多筆查詢
                                            },
                                        onChange: function (newValue,oldValue) {
                                            // console.log(" oldValue/newValue=",oldValue," / ",newValue);
                                            // if (oldValue.length!=0){    //避免已經有資料, 要修改時, 才click就又出現提示, 真正做到, 只有change才執行
                                            //     var last_select = newValue[newValue.length-1];
                                            //     if ( last_select != undefined && last_select != ""){
                                            //         study_choices.forEach( function (value, index, array){
                                            //             if ( value.text == newValue[newValue.length-1] && value.course == "Y" ){
                                            //                 alert('請記得輸入課程名稱');
                                            //             }
                                            //         })
                                            //     }
                                            // }
                                        },
                                        onSelect: function (row) {
                                            var opts = $(this).combobox('options');
                                            var el = opts.finder.getEl(this, row[opts.valueField]);
                                            var tab_dg = '#tab'+tabs[i].job_title+'_dg';
                                            var selected = $(tab_dg).datagrid('getSelected');
                                            el.find('input.combobox-checkbox')._propAttr('checked', true);
                                            // study_choices.forEach( function (value, index, array){
                                            //     if ( value.text == row[opts.valueField] && value.course == "Y" ){
                                            //             alert("請記得輸入課程名稱");
                                            //         }
                                            //     })
                                            //
                                            },
                                        onUnselect: function (row) {
                                            var opts = $(this).combobox('options');
                                            var el = opts.finder.getEl(this, row[opts.valueField]);
                                            el.find('input.combobox-checkbox')._propAttr('checked', false);

                                        }
                                    }
                            },
                        /*
                        formatter: function (val,row,index){
                                if ( val == null ) {  val=""; };
                                var nbsp_num = 75-( val==null ? 0:val.length);
                                var rtn_nbsp = "";
                                if ( tab_len > 7 && i==0 ){
                                    for ( var l=0 ; l <= nbsp_num ; l++){
                                       rtn_nbsp += '&nbsp;';
                                    }
                                    return val+rtn_nbsp;
                                } else { return val }
                        },
                         */
                    })
                    break;
                case 'xb002':
                    //教育訓練-課程名稱
                    arr_title.push({
                    id : value.name,
                    field: value.name,
                    title: all_cols+'<br>'+'<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">'+value.verbose_name+'</p>',
                    width: 300, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                    align: 'left',
                    editor: { type:'textbox',
                            options:{
                                required:false,
                                // disabled:true,
                                prompt:'自行輸入資料,不同課程以","間隔(限250字)'
                            }
                        },
                     /*
                     formatter: function (val,row,index){
                                if ( val == null ) { val="" };
                                var nbsp_num = 75-( val==null ? 0:val.length);
                                var rtn_nbsp = "";
                                if ( tab_len > 7 && i==0 ){
                                    for ( var l=0 ; l <= nbsp_num ; l++){
                                       rtn_nbsp += '&nbsp;';
                                    }
                                    return val+rtn_nbsp;
                                }  else { return val }
                        },
                      */
                    })
                    break;
                case 'xb003':
                    //輪調職務
                    arr_title.push({
                    field: value.name,
                    title: all_cols+'<br>'+'<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">'+value.verbose_name+'</p>',
                    width: 300, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                    align: 'left',
                    editor: { type:'combobox',
                                options:{
                                        multiple: true,
                                        data: rotation_jobs,      //這裏不一樣
                                        valueField:'value',
                                        textField:'text',
                                        formatter:function (row){
                                            var opts = $(this).combobox('options');
                                            return '<input type="checkbox" class="combobox-checkbox">' + row[opts.textField];
                                        },
                                        onLoadSuccess: function () {
                                            var opts = $(this).combobox('options');
                                            var target = this;
                                            var values = $(target).combobox('getValues');
                                            $.map(values, function (value) {
                                                var el = opts.finder.getEl(target, value);
                                                el.find('input.combobox-checkbox')._propAttr('checked', true);
                                                })
                                            $(this).combobox('setValue','');    //加空白,會自動在選擇時....加一個逗號, 這樣不論是否有在此輸入查詢關鍵字, 只要將第一個逗號前的資料去除,就可順利做多筆查詢
                                            },
                                        onSelect: function (row) {
                                            var opts = $(this).combobox('options');
                                            var sel_tab = $("#main-tab").tabs('getSelected');
                                            var index = $('#main-tab').tabs('getTabIndex',sel_tab);
                                            var tab_dg = '#tab'+tabs[index].job_title+'_dg';
                                            var sel_work_code = $(tab_dg).datagrid('getSelected')['work_code'];
                                            var ee = ee_jobs.find( function (ee){   return ee.work_code == sel_work_code  } );   //找出每個人有多少職務
                                            var jobs = ee.job_name;
                                            var job_len = jobs.length;
                                            var el;
                                            for ( var ii=0 ; ii<job_len ; ii++ ){
                                                el = opts.finder.getEl(this, row[opts.valueField]);
                                                if ( row.value == jobs[ii]){
                                                    alert('不可選擇與原本相同的職務名稱');
                                                    el.find('input.combobox-checkbox')._propAttr('checked', false);
                                                }
                                                else {
                                                        el.find('input.combobox-checkbox')._propAttr('checked', true);
                                                    }
                                                }
                                            },
                                        onChange: function (newValue,oldValue) {

                                            var sel_tab = $("#main-tab").tabs('getSelected');
                                            var index = $('#main-tab').tabs('getTabIndex',sel_tab);
                                            var tab_dg = '#tab'+tabs[index].job_title+'_dg';
                                            var sel_work_code = $(tab_dg).datagrid('getSelected')['work_code'];
                                            var ee = ee_jobs.find( function (ee){   return ee.work_code == sel_work_code  } );   //找出每個人有多少職務
                                            var jobs = ee.job_name;
                                            var job_len = jobs.length;

                                            for ( var ii=0 ; ii<job_len ; ii++ ) {
                                                if (newValue[newValue.length - 1] == jobs[ii]) {
                                                    //不可選擇與原本相同的職務名稱( 保持舊的值, 新的值不儲存 )
                                                    $(this).combobox('setValues', oldValue);
                                                }
                                            }


                                        },
                                        onUnselect: function (row) {
                                            var opts = $(this).combobox('options');
                                            var el = opts.finder.getEl(this, row[opts.valueField]);
                                            el.find('input.combobox-checkbox')._propAttr('checked', false);

                                        }
                                    }
                        },
                        /*
                        formatter: function (val,row,index){
                                if ( val == null ) { val="" };
                                var nbsp_num = 74-( val==null ? 0:val.length);
                                var rtn_nbsp = "";
                                if ( tab_len > 7 && i==0 ){
                                    for ( var l=0 ; l <= nbsp_num ; l++){
                                       rtn_nbsp += '&nbsp;';
                                    }
                                    return val+rtn_nbsp;
                                }  else { return val }
                        },
                         */
                    })
                    break;
            }
        } else {
            // 核心職能,一般職能,專業職能,管理職能
            if (preTxt=="ma"){
                arr_title.push({
                    field: value.name,
                    title: all_cols+'<br>'+'<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">'+value.verbose_name+'</p>',
                    width: 120, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                    align: 'center',
                    editor: { type:'combobox',
                              options:{
                                        data: score_choices_x, 　　　　　//這裏不一樣
                                        valueField:'value',
                                        textField:'text',
                                        },
                    },
                    /*
                    formatter: function (val,row,index){
                        var x_num = parseInt( (value.name).substr(2,3) );
                        if ( val == null ) {     val="";  };
                        var nbsp_num = 13-( val==null ? 0:val.length);
                        var rtn_nbsp = "";

                        var mod_num = x_num % 3;
                        if ( tab_len > 7 && i==0 ){
                            for ( var l=0 ; l <= nbsp_num ; l++){
                               rtn_nbsp += '&nbsp;';
                            }
                            if ( ( x_num >= 9 && x_num <= 10 ) || ( x_num >= 18 && x_num <= 19 ) ){
                                return rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                            }
                            switch (mod_num) {
                                case 1:
                                    return rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                                    break;
                                case 2:
                                    return rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                                    break;
                                case 3:
                                    return rtn_nbsp+val+rtn_nbsp+"&nbsp;&nbsp;";
                                    break;
                                default:
                                    return rtn_nbsp+val+rtn_nbsp;

                            }
                        }  else { return val }
                    }
                     */
                })
            } else {
                arr_title.push({
                    field: value.name,
                    title: all_cols + '<br>' + '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                    width: 120, 　　                     // 一定要設定width   1-否則會有錯誤  2-這樣 (header's width)=(cell's width)
                    align: 'center',
                    editor: {
                        type: 'combobox',
                        options: {
                            data: score_choices_x, 　　　　　//這裏不一樣
                            valueField: 'value',
                            textField: 'text',
                        }
                    },
                    /*
                    formatter: function (val,row,index){
                        if ( val == null ) { val="" };
                        var nbsp_num=0;
                        var preWord = (value.name).substr(0,2);
                        switch ( preWord ){
                            case 'ge':
                                nbsp_num = 13-( val==null ? 0:val.length);
                                break;
                            case 'cr':
                                nbsp_num = 12-( val==null ? 0:val.length);
                                break;
                            case 'pr':
                                nbsp_num = 12-( val==null ? 0:val.length);
                                break;
                        }
                        var x_num = parseInt( (value.name).substr(2,3) );
                        var mod_num = x_num % 3;
                        var rtn_nbsp = "";
                        if ( tab_len > 7 && i==0 ){
                            for ( var l=0 ; l <= nbsp_num ; l++){
                               rtn_nbsp += '&nbsp;';
                            }

                            switch ( preWord ){
                                case 'ge':
                                    return rtn_nbsp+val+rtn_nbsp;
                                    break;
                                case 'cr':
                                    if ( x_num >=5 ){
                                        return rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                                    } else {
                                        return rtn_nbsp+val+rtn_nbsp+"&nbsp;&nbsp;";
                                    }
                                    break;
                                case 'pr':
                                     if ( x_num == 16 || x_num == 23){
                                        return rtn_nbsp+val+rtn_nbsp+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                                    }
                                    if ( x_num >= 2){
                                        return rtn_nbsp+val+rtn_nbsp+"&nbsp;&nbsp;";
                                    }
                                    else {
                                        return rtn_nbsp+val+rtn_nbsp+"&nbsp;";
                                    }
                                    break;
                            }
                        }  else { return val }
                    }
                    */
                })
            }
        }


        switch (  preTxt  ){
            case 'cr':
                cr_cols++;
                break;
            case 'ma':
                ma_cols++;
                break;
            case 'ge':
                ge_cols++;
                break;
            case 'pr':
                pr_cols++;
                break;
            case 'xa':
                // 平均,等級
                xa_cols++;
                break;
            case 'xb':
                // 人力資源策略-教育訓練方式
                xb_cols++;
                break;
        }

    })

    var arr_title_group =[
        {title: '核 心 職 能 ( 單選 )', colspan: cr_cols, align: 'center',},
        {title: '管 理 職 能 ( 單選 )', colspan: ma_cols, align: 'center',},
        {title: '一 般 職 能 ( 單選 )', colspan: ge_cols, align: 'center',},
        {title: '專 業 職 能 ( 單選 )', colspan: pr_cols, align: 'center',},
        {title: '系統計算/判斷', colspan:xa_cols, align: 'center',},
        {title: '人力資源策略', colspan:xb_cols ,align: 'center',},
    ]      // columns[0]
    return [ arr_title_group , arr_title] ;
}


function getTabsDataGridRows(dg,job_title,bpm_yn){
    var rows_number;
    var rows;
    var fcolumns;           // frozen columns
    var columns;	        // unfrozen columns
    var fields;
    var fieldsLength;
    var gridData;       //objects
    var tabData = [];
    var cell_value=';'
    var xb001_ary;
    var gradeX=0;
    var grade0=0;
    var grade1=0;
    var grade2=0;
    var grade3=0;
    var grade4=0;
    var sub_total = 0;
    var WAverage=0;       //Weighted Average   加權平均
    var grade='';
    var xb001_course_yn="";
    var xb002_err="";
    var preTxt="";
    var pos_shc1="";
    var pos_shc2="";
    rows = dg.datagrid('getRows');
    rows_number = rows.length;
    fields = dg.datagrid('getColumnFields',true).concat(dg.datagrid('getColumnFields',false));
    fieldsLength = fields.length;
    err_job_title = job_title;
    have_score = "N"
    for (var j = 0; j < rows_number; j++) {         //每個tab的datagrid 會不一樣, 所以rows也會不一樣, 每個tab的j都會重頭開始
        gradeX=0;
        grade0=0;
        grade1=0;
        grade2=0;
        grade3=0;
        grade4=0;
        sub_total = 0;
        WAverage=0;
        grade='';
        xb001_course_yn="";

        dg.datagrid('endEdit', j);               // 儲存前,先關掉每個row的編輯....才能順利取得所有欄位
        gridData = {};
        for (var k=0 ; k < fieldsLength ; k++){
            if ( fields[k]!="" && fields[k] != undefined ) {  preTxt = fields[k].substr(0,2)  }  else {   preTxt=""   };
            cell_value = rows[j][fields[k]];
            if ( cell_value == null ){ cell_value = "" };
            if ( fields[k] == "pos_shc1" ) { pos_shc1=cell_value };
            if ( fields[k] == "pos_shc2" ) { pos_shc2=cell_value };
            if ( preTxt=="ma" && pos_shc1=="N"){
                //非主管職, 不需評核
                cell_value = "X";
            }
            if ( fields[k]=="ma022" && pos_shc2=="N" ){
                //非處階以上主管, 不需評核
                cell_value = "X";
            }
            switch (cell_value){
                case '─':
                    gradeX++;
                    break;
                case '○':
                    grade0++;
                    break;
                case '◔':
                    grade1++;
                    break;
                case '◑':
                    grade2++;
                    break;
                case '◕':
                    grade3++;
                    break;
                case '●':
                    grade4++;
                    break;
            }


            if ( fields[k] == "work_code" ) { err_work_code = cell_value};
            if ( fields[k] == "chi_name" ) { err_chi_name = cell_value};


            if (fields[k] == "xb001" && cell_value.length > 0) {
                xb001_ary = cell_value.split(',');
                xb001_ary.forEach(function (val, idx) {
                    study_choices.forEach(function (value, index, array) {
                        if (value.text == val && value.course == "Y") {
                            xb001_course_yn = "Y";
                        }
                    });
                });
            }

            //查出有空白資料, 而且是由"submit_btn"呼叫, 送出BPM前資料未填寫完, 不允送出
            if ( fields[k] == "xb002"  && xb001_course_yn == "Y"  &&  ( cell_value == undefined  ||  cell_value == "" ) ) {                          //xb002為空白, 而且規定要排課
                if (bpm_yn){
                    err_course = "\n *未輸入課程名稱* ";
                    err_tabData[j] = gridData;
                    return "error";
                }
                gridData[ fields[k] ] = "";            // 由$('#tab_save').click呼叫, 填入空白, 予以存檔
            };
            // if (  fields[k] != "xx" && cell_value == undefined  ){
            // if ( ( fields[k] != "xx" && preTxt !="xb") && ( cell_value == undefined  ||  cell_value == "" ) ){
            if ( ( fields[k] != "xx" && fields[k] != "xb002") && ( cell_value == undefined  ||  cell_value == "" ) ){
                if (bpm_yn) {
                    if ( fields[k] == undefined) {
                        err_profession = "\n\n\n ***請通知『人資』檢查,該職務『專業職能』的設定,是否合理?*** "
                    } else {
                        err_profession = "";
                    };

                    err_tabData[j] = gridData;
                    return "error";
                };
                gridData[ fields[k] ] = "";            // 由$('#tab_save').click呼叫, 填入空白, 予以存檔
            } else {
                gridData[fields[k]] = cell_value;
            };
            gridData['job_title'] = job_title;
        }
        sub_total = grade0 + grade1 + grade2 + grade3 + grade4;
        if ( sub_total==0 ) {
            WAverage = 0
        } else {
            WAverage = ( grade1*1 + grade2*2 + grade3*3 + grade4*4 )/( sub_total*4 )*100;   //乘以4，因為最高分為4分(就如最高分為100)
            switch (true){
                case ( WAverage>=81 ):
                    grade="導師級";
                    break;
                case ( WAverage>=61 &&  WAverage<81):
                    grade="熟手級";
                    break;
                case ( WAverage>=41 &&  WAverage<61):
                    grade="半熟手級";
                    break;
                 case ( WAverage>=21 &&  WAverage<41):
                    grade="新手級";
                    break;
                case ( WAverage<21):
                    grade="生手級";
                    break;
            }
            gridData['xa001'] = WAverage;
            gridData['xa002'] = grade;
            err_tabData[j] = gridData;
            tabData[j] = gridData;
        };     //百分比
    }
    return tabData;
}



function ValidCellValue(dg){
    var rows_number;
    var rows;
    var fields;
    var fieldsLength;
    var cell_value=''
    var preTxt="";
    var xb001_ary;
    var xb001_course_yn="";
    var xb002_err="";
    var err_tabData=[];
    var err_work_code="";
    var err_chi_name="";
    var err_cell="";
    var hr_item=['xb001','xb002','xb003']
    rows = dg.datagrid('getRows');
    rows_number = rows.length;
    fields = dg.datagrid('getColumnFields',true).concat(dg.datagrid('getColumnFields',false));
    fieldsLength = fields.length;
    for (var j = 0; j < rows_number; j++) {         //每個tab的datagrid 會不一樣, 所以rows也會不一樣, 每個tab的j都會重頭開始
        xb001_course_yn="";
        err_work_code="";
        err_chi_name="";
        err_cell="";
        dg.datagrid('endEdit', j);               // 儲存前,先關掉每個row的編輯....才能順利取得所有欄位
        for (var k=0 ; k < fieldsLength ; k++){
            switch (  fields[k].substr(0,2)  ){
                case 'cr':
                    preTxt = "核心";
                    break;
                case 'ma':
                    preTxt = "管理";
                    break;
                case 'ge':
                    preTxt = "一般";
                    break;
                case 'pr':
                    preTxt = "專業";
                    break;
                case 'xa':
                    preTxt = "系統計算";
                    break;
                case 'xb':
                    preTxt = "人力資源策略";
                    break;
            }
            cell_value = rows[j][fields[k]];
            if ( fields[k] == "work_code" ) { err_work_code = cell_value}
            if ( fields[k] == "chi_name" ) { err_chi_name = cell_value}

            // if ( ( fields[k] != "xx" && fields[k] != "xb002") && ( cell_value == undefined  ||  cell_value == "") ){
            if ( ( fields[k] != "xx" && !hr_item.includes(fields[k]) ) && ( cell_value == undefined  ||  cell_value == "") ){
                err_cell += preTxt+parseInt(fields[k].substr(3,2)).toString() +",";
            }

            if ( fields[k]=="xb001" && cell_value.length==0 ){
                err_cell += preTxt+parseInt(fields[k].substr(3,2)).toString() +"-教育訓練,"
            }
            if ( fields[k] == "xb001" && cell_value.length > 0) {
                xb001_ary = cell_value.split(',');
                xb001_ary.forEach(function (val, idx) {
                    study_choices.forEach(function (value, index, array) {
                        if (value.text == val && value.course == "Y") {
                            xb001_course_yn = "Y";
                        }
                    });
                });
            }
            if ( fields[k] == "xb002"  && xb001_course_yn == "Y"  &&  ( cell_value == undefined  ||  cell_value == "" ) ) {     //xb002為空白, 而且規定要排課
                err_cell += preTxt+parseInt(fields[k].substr(3,2)).toString() +"-課程名稱,";
            };
            if ( fields[k] == "xb003"   &&  ( cell_value == undefined  ||  cell_value == "" ) ) {
                err_cell += preTxt+parseInt(fields[k].substr(3,2)).toString() +"-預定輪調的職務,";
            };
        }
        if (  err_cell!="" ){
            // err_tabData[j] = err_work_code.trim()+err_chi_name.trim()+"  "+err_cell
            err_tabData[j] = err_work_code.trim()+" "+err_cell
        }
    }
    return err_tabData;
}



function updateToBackEnd(arrData){
    var arrLength = arrData.length;
    var data={};
    for( var n=0 ; n < arrLength; n++){
        data[n] = arrData[n];
    }
    url = "/sk_api/update_tabs_datagrid_rows";
    $.ajax({
    type :"post",
    url :url,
    data :JSON.stringify(data),
    async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
    success :function(res){
                var results = res.results;
                var resultsLength= results.length;
                var alertResults = '';
                var fail_data = '';
                var success_data = '';
                for ( var i = 0; i < resultsLength ; i++ ){
                    if ( results[i].success ){
                        success_data = success_data + results[i].job_title + " :  " + results[i].work_code + results[i].chi_name + "  " + results[i].year + "/" + results[i].month + "月  ..... " + "更新成功" + "\n";
                    } else {
                        fail_data = fail_data + results[i].job_title + " :  " + results[i].work_code + results[i].chi_name + "  " + results[i].year + "/" + results[i].month + "月\n";
                    }

                }
                if ( fail_data == ''){
                    alert('更新成功');
                } else {
                    alert("下列資料，更新失敗，請檢查\n\n"+fail_data);
                }
        }
    });
}


function config_tab(dg,lastRowIndex){
   $('#main-tab').tabs({
      onSelect:function (title,index){
      },
      onUnselect:function (title,index){
        //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------begin
            var button = document.getElementById("tab_endEdit");
            if ( button.disabled == false ) { button.click(); }
        //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------ending
          resetForm("main_form");
      },
      onAdd:function(e,title,index){
      },
      onUpdate:function(e,title,index){
      },
      onContextMenu:function(e,title,index){
      }

   });
}


function rowEditorControl( dg , index , row ){
    //row is an object
    // var sel_tab = $("#main-tab").tabs('getSelected');
    // var tab_field = tab_fields[$('#main-tab').tabs('getTabIndex',sel_tab)];
    var pos_shc1 = row['pos_shc1'];
    var pos_shc2 = row['pos_shc2'];
    var fieldName = "";
    var preTxt="";
    var object_index=0;

    Object.keys(row).forEach( key=>{
        var ed = dg.datagrid('getEditor', {
            index: index,
            field: key,
        });
        if ( ed != null) {
            if (key.substr(0, 2) == "ma") {
                if (pos_shc1 == "N") {
                    $(ed.target).combobox({
                        disabled: true,
                        valueField:'val',
                        textField:'txt',
                        data:[{
                            'val':'X',
                            'txt':'X',
                            "selected":true}
                        ],
                    });
                } else if (row.pos_shc2 == "N") {
                    if ( key == "ma022"){
                        $(ed.target).combobox({
                            disabled: true,
                            valueField:'val',
                            textField:'txt',
                            data:[{
                                'val':'X',
                                'txt':'X',
                                "selected":true}
                            ]
                        });
                    } else {
                        // $(ed.target).combobox({disabled: false});
                    }
                } else {
                    // $(ed.target).combobox({disabled: false});
                }
            }
        }
        object_index++;
    });
}

/*
function AllEditorSetDisabled( dg , index , row ){
    var object_index=0;

    Object.keys(row).forEach( key=>{
        var ed = dg.datagrid('getEditor', {
            index: index,
            field: key,
        });
        if ( ed != null) {
            $(ed.target).combobox({disabled: true,});
            $(ed.target).textbox({disabled: true,});
        }
        object_index++;
    });
}
 */




// var current_year=0;
// var current_month=0;

function config_tabs_datagrid(){
    var rowCount = 0;
    var tab_dg = '';

    var len = tabs.length;
    if ( len == 0 ) {
        $("#main_form").hide();
        $("#main-tab").hide();
        $("#note_table").hide();
        // tab_component_control() ;
        alert("1-未綁定職務( 無法填寫 )\n     或\n2-無人員需要盤點\n\n請洽人資中心！");
        return;
    };

    for (var i=0 ; i<len ; i++){
        tab_dg = '#tab'+tabs[i].job_title+'_dg'
        $(tab_dg).datagrid( {
            title : "職務代碼 : "+tabs[i].job_title+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;職務名稱 : "+tabs[i].job_title_desc,
            rowsNumber: true,
            // editorHeight:40,
            nowrap:false,
            singleSelect: true,
            // 以下三個都要這樣設定, 表頭勾選時, 才能全選/取消全選, 也才能多選
            // singleSelect: false,
            // selectOnCheck: true,
            // checkOnSelect: true,
            url : "/sk_api/matrix_score/"+tabs[i].job_title+"/"+userId,     //2-根據tab的"職務名稱"來抓取grid的data   YES:用來判段是否為第一次進入
            frozenColumns:[[
                {field:'work_code',title:'工號',align:'center',width:'69'},
                {field:'chi_name',title:'姓名',align:'center',width:'52'},
                {field:'year',title:'盤點<br>年度',align:'center',width:'40'},
                {field:'month',title:'月<br>份',align:'center',width:'25',
                    formatter: function(value,row,index){  return value.toString().padStart(2,'0');}
                },
                {field:'id',title:'',align:'center', hidden:true,},
                {field:'pos_shc1',title:'主<br>管<br>職',align:'center',width:'25',
                formatter: function(val){ return "&nbsp;"+val+"&nbsp;"; }
                },
                {field:'pos_shc2',title:'營<br>業<br>報<br>告<br>書',align:'center',width:'25',
                    formatter: function(val){ return "&nbsp;"+val+"&nbsp;"; }
                },
                {field:'xx',width:'4',
                    styler: function (value, row, index) {
                        return 'color:DarkSlateGrey;background-color: DarkSlateGrey;';
                    },
                },
                // {field:'chk_to_do',checkbox:true,},
            ]],
            columns :  reConfigGridColumns(i) ,   //在datagrid的editor : 不會有header's width <> cell's width的狀況發生
            onDblClickRow: function (index,row) {
                $(this).datagrid('endEdit', lastRowIndex);
                row.editing = true;
                $(this).datagrid('beginEdit', index);
                rowEditorControl( $(this) , index , row );
                lastRowIndex = index;
            },
            onBeforeEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
             },
            onAfterEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
            },
            onCancelEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
            },
            onClickRow: function  (index, row) {
                setFormData(main_form, row);
            },
            onUnselect: function (index, row) {
                $(this).datagrid('endEdit', index);
                row.editing = false;
            },
            onBeforeSelect: function (index,row){
                resetForm('main_form');
            },
            // onLoadSuccess: function(data) {
            //     current_year = data.rows[0]['year'];
            //     current_month = data.rows[0]['month'];
            // },
        });
        setGridHeaderStyle($(tab_dg));
        config_tab($(tab_dg),lastRowIndex);
    }
}


function tab_component_control() {
    $("#tab_edit").hide();
    $("#tab_endEdit").hide();
    $("#tab_save").hide();
    $("#submit_bpm").hide();
}



$(document).ready(function(){
    var tab_numbers = tabs.length;
    var tab_dg;
    var rows_number;
    // $('#main_dg').datagrid('hideColumn', 'xx');
    // $("#main-tab").hide();
    // $("#main_form").hide();
    config_tabs_datagrid();

    window.onbeforeunload=function(e){
    　　var e = window.event||e;
        e.returnValue=("");
    }  //離開業面提醒

    window.onunload=function(e){
    　　var e = window.event||e;
        e.returnValue=("");
    }  //離開業面提醒

    window.onclose=function(e){
    　　var e = window.event||e;
        e.returnValue=("");
    }  //離開業面提醒


    //重開所有datagrid
    function tabsDataGridReload(){
        for (var i=0 ; i<tab_numbers ; i++){
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            $(tab_dg).datagrid('reload');
        }
    }

    // bpm_yn 判斷是否為"submit_btn"而來
    function tab_save(bpm_yn) {
        //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------begin
            var button = document.getElementById("tab_endEdit");
            if ( button.disabled == false ) { button.click(); }
        //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------ending
        var rows_number;
        var tabData;
        var arrData = [];
        var err_arrData = [];
        for ( var i = 0; i < tab_numbers ; i++ ) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            tabData = getTabsDataGridRows($(tab_dg),tabs[i].job_title_desc,bpm_yn);      //取得每個TAB的GridRows，
            if (bpm_yn){
                if (tabData=="error") {
                    err_arrData = err_arrData.concat(err_tabData);
                    updateToBackEnd(err_arrData);                            //將蒐集的資料，傳給後端儲存
                    alert("您有資料未盤點, 不允BPM送簽\n"+err_job_title+" "+err_work_code+" "+err_chi_name +" "+err_course + err_profession);
                    return "error";
                    break;
                }
            }
            arrData = arrData.concat(tabData);                                   //array的合併
            err_arrData = err_arrData.concat(err_tabData);                                   //array的合併
        }
        updateToBackEnd(arrData);                         //將蒐集的資料，傳給後端儲存
        tabsDataGridReload();
    }

    //儲存( 所有 )
    $("#tab_save").click(function (){
        tab_save(false);
    })

    //編輯( 所有 )
    $("#tab_edit").click(function () {
        for ( var i=0 ; i < tab_numbers ; i++ ) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg'
            rows_number = $(tab_dg).datagrid('getRows').length;
            for (var j = 0; j < rows_number ; j++) {
                $(tab_dg).datagrid('beginEdit', j);
            }
        }
    })

    //關閉編輯
    $("#tab_endEdit").click(function () {
        if ( tab_numbers > 9) { var start_num=1 } else { var start_num=0 }
        for ( var i=start_num ; i < tab_numbers ; i++ ) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            rows_number = $(tab_dg).datagrid('getRows').length;
            for (var j = 0; j < rows_number; j++) {
                $(tab_dg).datagrid('endEdit', j);
            }
        }
    })

    function EndEdit() {
        for ( var i=0 ; i < tab_numbers ; i++ ) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            rows_number = $(tab_dg).datagrid('getRows').length;
            for (var j = 0; j < rows_number; j++) {
                $(tab_dg).datagrid('endEdit', j);
            }
        }
    }



    //送出至bpm( 1-產生報表 2-產生bpm相關資料 )
    $("#submit_bpm").click(function () {
        tab_save(false);
        var fileName = 'SKIL' + getFormatedDateTime() + ".pdf";
        var data = {};
        var tab_dg = '#tab' + tabs[0].job_title + '_dg';
        var fields = $(tab_dg).datagrid('getRows')[0];
        var id_count = 0;
        var port = location.port;     // add 2022/01/10

        data['year'] = fields.year;
        data['month'] = fields.month;
        data['report_name'] = fileName;

        if (port.length > 0) {
            // http://127.0.0.1:8000
            data['report_url'] = location.protocol + "//" + location.hostname + ":" + location.port
        } else {
            // httpd://pmsbeta.tiongliong.com............
            // httpd://pms.tiongliong.com............
            data['report_url'] = location.protocol + "//" + location.hostname
        }


        //---------------data_valid-----------------------------------------------
        var col;
        var err_msg = ""
        var err_length = 0;
        var err_field = "";
        for (var i = 0; i < tab_numbers; i++) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            err_msg = ValidCellValue($(tab_dg));
            err_length = err_msg.length;
            if (err_length > 0) {
                err_field += tabs[i].job_title_desc + "*有資料未輸入*\n";
                for (var k = 0; k < err_length; k++) {
                    if (err_msg[k] != undefined) {
                        err_field += "　" + err_msg[k] + "\n";
                    }
                }
                err_field += "\n------------------------------------\n"
            }
        }

        //---------------產生報表,更新backend檔案-----------------------------------------------
        if (err_field.length == 0) {
            tab_component_control();   //先關掉所有按紐,避免再按
            for (var i = 0; i < tab_numbers; i++) {
                tab_dg = '#tab' + tabs[i].job_title + '_dg';
                //---------------關掉editor-----------------------------------------------
                $(tab_dg).datagrid({
                    onBeforeEdit: function (index, row) {
                        col = $(this).datagrid('getColumnOption', 'columnName'); // Here your column name
                        $.extend(col.editor.options, {disabled: true});
                    } })

                //---------------取得更新資料-----------------
                rows_number = $(tab_dg).datagrid('getRows').length;
                for (var j = 0; j < rows_number; j++) {
                    id_count++;
                    tab_dg.padStart();
                    data['id' + id_count.toString()] = $(tab_dg).datagrid('getRows')[j].id; }
            }

            window.open(location.href + '_2pdf?fileName=' + fileName, '技能盤點表-送簽報表-可下載', config = 'width=750, height=600,location=no, menubar=no, toolbar=no, status=no , top=200 , left=300');
            //---------------更新MatrixStatus(BPM資訊檔)--------
            // ---設定timeout:因為在pdf檔才開始產生當下,
            // ---MatrixStatus的狀態就被更新為draft,導致產生pdf的app會排除draft的資料,使得pdf的明細為空白
            // ---為使pdf產生完,再讓程式更新MatrixStatus,因此設定timeout

            setTimeout(function () {
                var url = "/sk_api/submit_bpm";
                $.ajax({
                    type: "post",
                    url: url,
                    data: data,
                    async: true,
                    success: function (res) {
                        if (res.success) {
                            tabsDataGridReload();
                            alert('BPM送出成功!');
                        } else {
                            alert('錯誤!');
                        }
                    }
                })
            }, 3000);     // 1秒=1000毫秒( 1second=1000millisecond )<--10秒

        } else { alert(err_field) }
    })


    /*
    //只清除勾選的列
    $("#tab_clear").click(function (){
       var tab = $('#main-tab').tabs('getSelected');
       var index = $('#main-tab').tabs('getTabIndex', tab);
       var tab_dg = '#tab'+tabs[index].job_title+'_dg';
       var rows=$(tab_dg).datagrid('getSelections');
       // alert("按下清除     "+tab_dg+"\n\n"+rows);
       var rowsLength = rows.length;
       for ( var i=0 ; i<rowsLength ; i++){
           // console.log(rows[i]);
       }
    });
     */

});