var lastRowIndex=0;
var last_work_item="start";
var allow_edit_other = true;
var err_tabData = [];
var err_job_title = "";

var calc01_tot=0;
var calc02_tot=0;
var ptot_tot=0;
var dtot_tot=0;
var ctot_tot=0;
var ctot01_tot=0;
var ctot02_tot=0;
var ctot03_tot=0;
var atot_tot=0;
var import_data = {};


function toggleDescription(dg){
     var dgOptions = dg.datagrid("options");
     var rows = dg.datagrid("getRows");
     var row = null;
     var tr = null;
     var height1 =0;
     var height2 =0;
     // setTimeout(function(){
       for(var i in rows){
          row = rows[i];
          tr = dgOptions.finder.getTr(dg[0],i);
          height1 = $(tr[0]).height();//冻结行的高度
          height2 = $(tr[1]).height();//非冻结行的高度
          if (height2>height1) {
               //冻结部分在显示时的高度取较大的那个
               $(tr[0]).css("height",height2+"px");
          }
        }
     // },1000);//延后一秒执行
}

function getSelectedTab(){
    //取得所選取的tab
    var tab = $('#main-tab').tabs('getSelected');
    var index = $('#main-tab').tabs('getTabIndex',tab);
    var tab_dg = '#tab' + tabs[index].job_title + '_dg';
    return tab_dg;
}


function Rearrange_order_number() {
    var tab_dg = getSelectedTab();
    var thisTabRows = $(tab_dg).datagrid("getRows");
    var thisTabRows_length = thisTabRows.length;

    //重排order_number------------------------------------------------------------------------begin
    xRows = $(tab_dg).datagrid("getData").rows;
    for (var k = 0; k < thisTabRows_length; k++) {
        if (xRows[k] == undefined) {
            xRows.push({'order_number': k + 1});
        } else {
            xRows[k].order_number = k + 1;
        }
    }
    //重排order_number------------------------------------------------------------------------ending

    //取出已計算好的row & 重排過的rows
    $(tab_dg).datagrid('loadData', xRows);
}


function Row_Insert() {
    var tab_dg = getSelectedTab();
    var thisIndex = $(tab_dg).datagrid('getRowIndex', $(tab_dg).datagrid('getSelected'));
    $(tab_dg).datagrid('insertRow',{
        index : thisIndex,
        row : {
            order_number: thisIndex+1,
            work_item:"　",
        }
    });
    Rearrange_order_number();
}


function Row_Duplicate() {
    var tab_dg = getSelectedTab();
    var thisIndex = $(tab_dg).datagrid('getRowIndex', $(tab_dg).datagrid('getSelected'));
    $(tab_dg).datagrid('insertRow',{
        index : thisIndex,
        row : {
            order_number: thisIndex+1,
            work_item:"　",
        }
    });
    Rearrange_order_number();


    var fromNO = parseInt( prompt(gettext('輸入要複製的行號(no):')) );
    var fromRow = {};
    if ( isNaN(fromNO) ){
        // 未輸入，複製本行
        fromRow = $(tab_dg).datagrid('getRows')[thisIndex+1];     // $('#dg').datagrid('getRows')[index];
    } else {
        if ((fromNO - 1) >= thisIndex) {
            fromRow = $(tab_dg).datagrid('getRows')[fromNO];     // $('#dg').datagrid('getRows')[index];
        } else {
            fromRow = $(tab_dg).datagrid('getRows')[fromNO-1];      // $('#dg').datagrid('getRows')[index];
        }
    }

    delete fromRow.order_number;
    $(tab_dg).datagrid('updateRow', {
        index: thisIndex,
        row: fromRow,
    });
    Rearrange_order_number();

    // $('#dd_duplicate').dialog({ closed: true,});
}


function Row_Delete() {
    var tab_dg = getSelectedTab();
    var thisIndex = $(tab_dg).datagrid('getRowIndex', $(tab_dg).datagrid('getSelected'));
    $(tab_dg).datagrid('deleteRow', thisIndex);
    Rearrange_order_number();
}


function Row_Clear() {
    var tab_dg = getSelectedTab();
    var thisIndex = $(tab_dg).datagrid('getRowIndex',$(tab_dg).datagrid('getSelected'));
    $(tab_dg).datagrid('deleteRow',thisIndex);
    $(tab_dg).datagrid('insertRow',{
        index : thisIndex,
        row : {
            order_number: thisIndex+1,
            work_item:"　",
        }
    });
}


function exportData_singleSheet(from_bpm,last_the_time) {
   var job_title_desc = "";
   var tab_dg = "";
   var tab_numbers = tabs.length;
   var last_the_time = the_time.last;
   for (var index = 0; index < tab_numbers; index++) {
       job_title_desc = tabs[index].job_title_desc;
       tab_dg = '#tab' + tabs[index].job_title + '_dg';

       var fileName = select_work_code+select_chi_name+"-"+job_title_desc+"-PDCA-"+last_the_time.toString().padStart(2,"0")+"version-"+getFormatedDateTime();
       if ( from_bpm == "Y"){
           fileName = select_work_code+select_chi_name+"-"+job_title_desc+"-PDCA-"+last_the_time.toString().padStart(2,"0")+"version-sign-backup-"+getFormatedDateTime();
       }
       var rowData = $(tab_dg).datagrid('getRows');
       // var rowNumbers = rowData.length;  隨時在變, 不能設初值
       var i = 0;
       var field_titles = $(tab_dg).datagrid('options').columns;
       var master_id = 0;
       while ( i < rowData.length ) {
           if ( rowData[i].work_item == null && rowData[i].ptot01== null ){
               rowData.splice(i); //移除陣列中,指定位置的資料
           } else {
             master_id = rowData[i].master;
             delete rowData[i].id;
             delete rowData[i].master;
             Object.keys(rowData[i]).forEach( function (key,idx){
                 if ( rowData[i][key]==null ) { delete rowData[i][key] };
             })
             delete rowData[i].calc01;
             delete rowData[i].calc02;
             delete rowData[i].ptot01;
             delete rowData[i].dtot01;
             delete rowData[i].ctot01;
             delete rowData[i].ctot02;
             delete rowData[i].ctot03;
             delete rowData[i].atot01;
             delete rowData[i].okyn01;
             delete rowData[i].exp_count;
           }
           i++;
       }
       var column_header = {
           'order_number':'no',
           'work_item':"***"+gettext("工作項目")+"***",
       };
       $.each(tab_fields[index],function(idx,value) {
           if ( ['pdca','flow','cycl'].includes( (value.name).substr(0, 4) ) ){
               //在excel的儲存格中,應設定為"自動換列"
               column_header[value.name] = (value.verbose_name).replace('<br>','\n');
           }
       })
       // rowData.push(column_header);  從後面推進去
       rowData.unshift(column_header);   //從前面推進去
       var sheet0=XLSX.utils.json_to_sheet(rowData);
       var wopts = { bookType:'xlsx', bookSST:false, type:'binary' };
       var wb = { SheetNames: ['Sheet0'], Sheets: {}, Props: {} };
       wb.Sheets['Sheet0'] = sheet0;//轉化成workbooks形式。
       var wbout = XLSX.write(wb,wopts);
        //轉換流形式
       function s2ab(s) {
           var buf = new ArrayBuffer(s.length);
           var view = new Uint8Array(buf);
           for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
           return buf;
       }

       /* the saveAs call downloads a file on the local machine */
       //自定義儲存檔案方式,原專案採用的是cordova的檔案寫入方式，此演示只用模擬瀏覽器下載的形式
       saveAs(new Blob([s2ab(wbout)],{type:""}),fileName+".xlsx");

       $.get("/sk_api/pdca_export_data_count/"+master_id,
        function(res) {
            if(res.success) {console.log('匯出資料成功') }
            else { alert('錯誤') }
        });
   }
}


function saveAs(obj,fileName) {
    var tmpa = document.createElement("a");
    tmpa.download = fileName || gettext("下載");
    tmpa.href = URL.createObjectURL(obj);
    tmpa.click();
    setTimeout(function () {
        URL.revokeObjectURL(obj);
    }, 100);
}




function importf(obj) {//匯入
    $('#import_dd').dialog( {closed: true,} );
    var sure = confirm(gettext("是否確定匯入?")+ "\n\n\n***"+gettext("匯入前,請先『儲存』資料")+"***");
    if ( !sure ) {
        location.reload();
        return;
    };

    var wb;//讀取完成的資料
    var rABS = false; //是否將檔案讀取為二進位制字串
    if(!obj.files) {   return;   }

    var f = obj.files[0];
    var reader = new FileReader();
    //取得所選取的tab
    var tab_dg = getSelectedTab();

    var thisTabRows = $(tab_dg).datagrid("getRows");
    var thisTabRows_length = thisTabRows.length;
    var rowIndex = thisTabRows.length - 1;
    var newRows = [];

    reader.onload = function(e) {
        var data = e.target.result;
        if(rABS) {
            wb = XLSX.read(btoa(fixdata(data)), {//手動轉化
                type: 'base64'
            });
        } else {
            wb = XLSX.read(data, {
                type: 'binary'
            });
        }
        // wb.SheetNames[0]是獲取Sheets中第一個Sheet的名字
        // wb.Sheets[Sheet名]獲取第一個Sheet的資料
        // loadData 加載本地數據，不會跟後台發生交互，且加載以後。表的格式不會發生變化，除非自己修改
        var yRows = XLSX.utils.sheet_to_json( wb.Sheets[wb.SheetNames[0]] );
        var xRows=yRows.splice(1);   //刪除中文說明的那列
        for (var i=rowIndex ; i>=0 ; i--) {
            if ( thisTabRows[i].id > 0) {
                xRows.unshift(thisTabRows[i]);     //將原有的row, 由前面倒推回去( queue )
            }
        }

        //取出暫存在buffer的data, 丟給array
        $(tab_dg).datagrid( 'loadData' , xRows );

        //重新計算---------------------------------------------------------------------------------begin
        var newRows = $(tab_dg).datagrid("getData").rows ;
        var newRows_len = newRows.length;
        for ( var j=0 ; j < newRows_len ; j++) {  this_row_calc( j, newRows[j] );  }   //逐筆重新計算
        //重新計算---------------------------------------------------------------------------------ending

        //重排order_number------------------------------------------------------------------------begin
        xRows = $(tab_dg).datagrid("getData").rows;
        for ( var k=0 ; k < thisTabRows_length ; k++) {
            if ( xRows[k] == undefined ){
                xRows.push( { 'order_number':k+1 } );
            } else {
                xRows[k].order_number = k+1;
            }
        }
        //重排order_number------------------------------------------------------------------------ending

        //取出已計算好的row & 重排過的rows
        $(tab_dg).datagrid( 'loadData' , xRows );

        //重繪footer
        footer_pdca_calc($(tab_dg));
        redefine_dg_footer($(tab_dg));
        mergeCells_dg_footer($(tab_dg));
    };

    if(rABS) {
        reader.readAsArrayBuffer(f);
    } else {
        reader.readAsBinaryString(f);
    }
}


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
    // return (Year+Month+Day+Hour+Minute+Second)
}

function reConfigGridColumns(i) {
    var arr_title = [];      // columns[1]
    var title_length;
    var title_content;

    var pdca_cols = 0;
    var p_cols = 0;
    var d_cols = 0;
    var c_cols = 0;
    var a_cols = 0;
    var flow_cols = 0;
    var ctot_cols = 0;
    var all_cols = 1;
    var preTxt;

     $.each(tab_fields[i],function(index,value) {
         preTxt = (value.name).substr(0, 4);
         switch (preTxt) {
             case 'pdca':
                 title_length = 50;
                 pdca_cols++;
                 switch (value.pdca) {
                     case 'P':
                         p_cols++;
                         break;
                     case 'D':
                         d_cols++;
                         break;
                     case 'C':
                         c_cols++;
                         break;
                     case 'A':
                         a_cols++;
                         break;
                 }
                 break;
             case 'flow':
                 title_length = 250;
                 flow_cols++;
                 break;
             case 'calc':
                 title_length = 80;
                 break;
             case 'cycl':
                 title_length = 80;
                 break;
             case 'ctot':
                 title_length = 80;
                 ctot_cols++;
             default:
                 title_length = 80;
                 break;
         };

        switch (preTxt) {
             case 'pdca':
                 arr_title.push({
                     field: value.name,
                     title: '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                     width: title_length,
                     align: 'center',
                     editor: { type: 'numberbox',  options:{ precision:0 } },     //precision : 小數位數
                 });
                 break;
             case 'flow':
                 arr_title.push({
                     field: value.name,
                     title: '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                     width: title_length,
                     align: 'center',
                     editor: { type:'textbox',
                                options:{
                                    required:false,
                                    prompt:gettext('自行輸入資料(限100字)')
                                }
                            },
                 });
                 break;
             case 'cycl':
                 if (value.name=='cycl01') {
                     arr_title.push({
                         field: value.name,
                         title: '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                         width: title_length,
                         align: 'center',
                         editor: {
                             type: 'combobox',
                             options: {
                                 required : true, 　　　　　　　//2022/3/28修改　　　
                                 editable : false,          //2022/3/28加入
                                 data: cycle_choices,      //這裏不一樣
                                 valueField: 'text',
                                 textField: 'text',
                                 formatter: function (row) {
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
                                     $(this).combobox('setValue', '');
                                 },
                                 onSelect: function (row) {
                                     var opts = $(this).combobox('options');
                                     var el = opts.finder.getEl(this, row[opts.valueField]);
                                     el.find('input.combobox-checkbox')._propAttr('checked', true);
                                 },
                                 onUnselect: function (row) {
                                     var opts = $(this).combobox('options');
                                     var el = opts.finder.getEl(this, row[opts.valueField]);
                                     el.find('input.combobox-checkbox')._propAttr('checked', false);

                                 }
                             }
                         },
                     });
                 } else {
                     arr_title.push({
                     field: value.name,
                     title: '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                     width: 50,
                     align: 'center',
                     editor: { type:'numberbox',options:{required:false,precision:0}},     //precision 小數位數精確度
                    });
                 }
                 break;
             default:
                 arr_title.push({
                     field: value.name,
                     title: '<p style="word-break:break-all;word-wrap:break-word;white-space:pre-wrap;">' + value.verbose_name + '</p>',
                     width: title_length,
                     align: 'center',
                 });
                 break;
         };

     });


     var arr_title_group1 =[
        {title: gettext('工 作 方 式 ( 作業時間/分鐘 )')+'&nbsp;&nbsp;'+gettext('（至少要填一個）'), colspan: pdca_cols, align: 'center',},
        {title: gettext('流 程')+'<br>'+gettext('(每格務必填寫完整，不可空白，空白可填寫無）'), rowspan:2,colspan: flow_cols, align: 'center',},
        {title: gettext('作業時間'), rowspan:2, align: 'center',},
        {title: gettext('週期次數'), rowspan:2, colspan:2, align: 'center',},
        {title: gettext('每月合計'), rowspan:2, align: 'center',},
        {title: 'Ｐ', rowspan:2,align: 'center',},
        {title: 'Ｄ', rowspan:2,align: 'center',},
        {title: 'Ｃ', rowspan:2,colspan: ctot_cols, align: 'center',},
        {title: 'Ａ', rowspan:2,align: 'center',},
        {title: gettext('比對'), rowspan:2,align: 'center',},
    ]      // columns[0]

     var arr_title_group2 =[
        {title: 'Ｐ', colspan: p_cols, align: 'center',},
        {title: 'Ｄ', colspan: d_cols, align: 'center',},
        {title: 'Ｃ', colspan: c_cols, align: 'center',},
        {title: 'Ａ', colspan: a_cols, align: 'center',},


        {title: '', colspan: flow_cols, align: 'center',},
        {title: '',  align: 'center',},
        {title: '',  align: 'center',},
        {title: '',  align: 'center',},
        {title: '',  align: 'center',},
        {title: '',  align: 'center',},
        {title: '', colspan: ctot_cols, align: 'center',},
        {title: '', align: 'center',},
        {title: '', align: 'center',},
    ]      // columns[0]


    return [ arr_title_group1 , arr_title_group2 , arr_title] ;
}


function setGridHeaderStyle(dg){
    var columns = dg.datagrid('options').columns;                  //只會抓取columns( 未含frozenColumns )
    var col_field = '';
    var group_id = 'datagrid-td-group';
    var tabs_len = tabs.length+9;
    //columns[0]的color
    for ( var i=5; i<tabs_len ; i++){
        $( '#' + group_id + i.toString() +'-0-0').css('background-color', cr_color);
        $( '#' + group_id + i.toString() +'-0-1').css('background-color', ma_color);
        $( '#' + group_id + i.toString() +'-0-2').css('background-color', ge_color);
        $( '#' + group_id + i.toString() +'-0-3').css('background-color', pr_color);
        // $( '#' + group_id + i.toString() +'-0-4').css('background-color', ot_color);
        $( '#' + group_id + i.toString() +'-0-4').css('background-color', xa_color);
        $( '#' + group_id + i.toString() +'-0-5').css('background-color', xb_color);
    }
}


function get_datagrid_rows(dg,job_title,job_title_desc,work_code,the_time,bpm_yn){
    var rowsNumber;
    var rows;
    var fcolumns;           // frozen columns
    var columns;	        // unfrozen columns
    var fields;
    var fieldsLength;
    var gridData;       //objects
    var tabData = [];
    var cell_value=';'
    var this_pdcatot = 0;
    rows = dg.datagrid('getRows');
    rowsNumber = rows.length;
    fields = dg.datagrid('getColumnFields',true).concat(dg.datagrid('getColumnFields',false));
    fieldsLength = fields.length;
    err_job_title = job_title;
    for (var j = 0; j < rowsNumber; j++) {         //每個tab的datagrid 會不一樣, 所以rows也會不一樣, 每個tab的j都會重頭開始
        dg.datagrid('endEdit', j);               // 儲存前,先關掉每個row的編輯....才能順利取得所有欄位
        gridData = {};
        this_pdcatot = this_pdca_tot(rows[j]);
        this_work_item = rows[j].work_item;
        if ( this_work_item=="" ||this_work_item==undefined || this_work_item==null)  { continue }
        for (var k=0 ; k < fieldsLength ; k++){
            if ( fields[k]=="XXX" ) { continue };         //XXX為分隔線的欄位, 不需要儲存
            if ( fields[k]!="" && fields[k] != undefined ) { preTxt = fields[k].substr(0,4) }  else { preTxt="" };
            cell_value = rows[j][fields[k]];
            if ( fields[k]=="work_item" && ( cell_value=="" || cell_value==undefined || cell_value==null) ) {  //工作項目沒填寫, 就不繼續取資料
                // console.log("work_itme沒填",rows[j]);
                if ( this_pdcatot > 0 ){
                    alert(gettext("工作項目為空白，不允存檔"));
                    return 'error';
                }
                break;    //工作項目沒填寫, 就不繼續取資料
            } else {
                gridData['work_code'] = work_code;
                gridData['the_time'] = the_time;
                gridData['job_title'] = job_title;
                gridData['job_title_desc'] = job_title_desc;
                if (cell_value == null) { cell_value = ""  }
                //查出有空白資料, 而且是由"submit_btn"呼叫, 送出BPM前資料未填寫完, 不允送出
                if (cell_value == undefined || cell_value == "") {
                    if (preTxt == 'pdca' || preTxt == "calc" || preTxt == "ptot" || preTxt == "dtot" || preTxt == "ctot" || preTxt == "dtot" || preTxt == "atot") {
                        gridData[fields[k]] = "0"            // 數字轉為整數或浮點數, 後端才不會出錯
                    } else { gridData[fields[k]] = "" }     // 由$('#tab_save').click呼叫, 填入空白, 予以存檔
                } else {  gridData[fields[k]] = cell_value; }
            }
        }
        tabData[j] = gridData;
    }
    return tabData;
}


function config_tab(dg,lastRowIndex){
   $('#main-tab').tabs({
      onSelect:function (title,index){
      },
      onUnselect:function (title,index){
      },
      onAdd:function(e,title,index){
      },
      onUpdate:function(e,title,index){
      },
      onContextMenu:function(e,title,index){
      }

   });
}


function this_row_calc(index,row) {
    var fieldName='';
    var multiplicand = 0;
    var cycle_len = cycle_choices.length;
    var pdcatot = 0;
    var ptot = 0;
    var dtot = 0;
    var ctot = 0;
    var atot = 0;
    var pdca_len = pdca_calc.length;
    var c_numbers = 0;
    var ctot01 = 0;
    var ctot02 = 0;
    var ctot03 = 0;
    var formula = 0;
    var P0=0;
    var P1=0;
    var P2=0;
    var P3=0;
    var P4=0;
    var P5=0;
    var P6=0;
    var sub_tot=0;
    var current_pdca="";

    for (var j = 1; j <= pdca_len; j++) {
        fieldName = 'pdca' + j.toString().padStart(2, '0');
        // console.log(" fieldName=",fieldName,pdca_calc[j - 1].verbose_name,"=",pdca_calc[j - 1].pdca,"=",row[fieldName]);

        current_pdca = pdca_calc[j - 1].pdca;
        if ( current_pdca=='C' ){ c_numbers++ }   //不能放在下面的if (  遇到C有NaN 就不準了)
        if (!isNaN( parseInt(row[fieldName]) )) {
            pdcatot += parseInt(row[fieldName]);
            switch ( current_pdca ) {
                case 'P':
                    ptot += parseInt(row[fieldName]);
                    break;
                case 'D':
                    dtot += parseInt(row[fieldName]);
                    break;
                case 'C':
                    ctot += parseInt(row[fieldName]);
                    switch (c_numbers) {
                        case 1:
                            ctot01 = parseInt(row[fieldName]);
                            break;
                        case 2:
                            ctot02 = parseInt(row[fieldName]);
                            break;
                        case 3:
                            ctot03 = parseInt(row[fieldName]);
                            break;
                    }
                    break;
                case 'A':
                    atot += parseInt(row[fieldName]);
                    break;
            }

            row['calc01'] = pdcatot;
            for (var i = 0; i < cycle_len; i++) {
                if (cycle_choices[i].text == row['cycl01']) {
                    if ( row['cycl02']!="" && row['cycl02']!="0")  {
                        // 有輸入次數
                        formula = parseFloat(row['cycl02']) * cycle_choices[i].multiplicand;

                        P0 = parseFloat( (pdcatot * formula).toFixed(2) );
                        P1 = parseFloat( (ptot * formula).toFixed(2) );
                        P2 = parseFloat( (dtot * formula).toFixed(2) );

                        P3 = parseFloat( (ctot01 * formula).toFixed(2) );
                        P4 = parseFloat( (ctot02 * formula).toFixed(2) );
                        P5 = parseFloat( (ctot03 * formula).toFixed(2) );

                        P6 = parseFloat( (atot * formula).toFixed(2) );


                        row['calc02'] = P0;
                        row['ptot01'] = P1;
                        row['dtot01'] = P2;

                        row['ctot01'] = P3;
                        row['ctot02'] = P4;
                        row['ctot03'] = P5;

                        row['atot01'] = P6;
                        sub_tot = parseFloat( (P1 + P2 + P3 + P4 + P5 + P6).toFixed(2) );
                        if ( pdcatot > 0 ){                      //pdca至少有輸入一個, 才判斷
                            if ( parseInt(P0) == parseInt( sub_tot )  ){
                                row['okyn01'] = "OK";
                            } else {
                                row['okyn01'] = "Ｘ";
                            }
                        }
                        break;
                    } else {
                        row['calc02'] = "";
                        row['ptot01'] = "";
                        row['dtot01'] = "";

                        row['ctot01'] = "";
                        row['ctot02'] = "";
                        row['ctot03'] = "";

                        row['atot01'] = "";

                        row['okyn01'] = "Ｘ";
                    }

                }
            }
        }
    }
}


function footer_pdca_calc(dg){
    var rows = dg.datagrid('getRows');
    var rowsNumber = rows.length;
    calc01_tot=0;
    calc02_tot=0;
    ptot_tot=0;
    dtot_tot=0;
    ctot_tot=0;
    ctot01_tot=0;
    ctot02_tot=0;
    ctot03_tot=0;
    atot_tot=0;
    for( var i = 0; i < rowsNumber ; i++ ){
      dg.datagrid( 'endEdit' , i );
      if ( rows[i]['calc01'] != undefined && rows[i]['calc01'] != "" ) { calc01_tot += parseFloat(rows[i]['calc01']) };
      if ( rows[i]['calc02'] != undefined && rows[i]['calc02'] != "" ) { calc02_tot += parseFloat(rows[i]['calc02']) };
      if ( rows[i]['ptot01'] != undefined && rows[i]['ptot01'] != "" ) { ptot_tot += parseFloat(rows[i]['ptot01']) };
      if ( rows[i]['dtot01'] != undefined && rows[i]['dtot01'] != "" ) { dtot_tot += parseFloat(rows[i]['dtot01']) };
      if ( rows[i]['ctot01'] != undefined && rows[i]['ctot01'] != "" ) { ctot01_tot += parseFloat(rows[i]['ctot01']) };
      if ( rows[i]['ctot02'] != undefined && rows[i]['ctot02'] != "" ) { ctot02_tot += parseFloat(rows[i]['ctot02']) };
      if ( rows[i]['ctot03'] != undefined && rows[i]['ctot03'] != "" ) { ctot03_tot += parseFloat(rows[i]['ctot03']) };
      if ( rows[i]['atot01'] != undefined && rows[i]['atot01'] != "" ) { atot_tot += parseFloat(rows[i]['atot01']) };
    }
}


function get_data_2calc(){
    var tab_numbers = tabs.length;
    var rowsNumber;
    var tabData;
    var arrData = [];
    var err_arrData = [];
    for ( var i = 0; i < tab_numbers ; i++ ) {
        tab_dg = '#tab' + tabs[i].job_title + '_dg';
        footer_pdca_calc($(tab_dg));
        redefine_dg_footer($(tab_dg));
        mergeCells_dg_footer($(tab_dg));
    }
}


function this_row_validate(job_title_desc,index,row,flow_numbers){
    var preTxt = "";
    var val = "";
    var alert_msg = "";
    var order_number = 0;
    var have_work_item = true;
    var pdcatot = 0;                  //有一個就可
    var have_pdca = true;                  //有一個就可
    var have_flow = true;                  //每個都要
    var have_flow_count = 0;
    var have_cycl = true;
    var cycl_count = 0;
    var valid_result = {};
    var this_row_flow_count = 0;
    var cycle_text = [];
    var cycl01_select = true;

    Object.keys(cycle_choices).forEach( function (key,idx){
        cycle_text.push(cycle_choices[key].text);
    })
    //逐項檢查這個row的每個field的值
    Object.keys(row).forEach( function (key,idx){
        preTxt = key.substr(0,4)
        val = row[key];
        if ( key=="order_number" ){ order_number = val };
        switch (preTxt){
            case 'work':
                if ( val == "" || val == null || val == undefined ) { have_work_item = false; }
                break;
            case 'pdca':
                if ( val != null ) {   pdcatot += parseInt(val) }
                break;
            case 'flow':　　　　
                if ( !( val == "" || val == null || val == undefined ) ) { have_flow_count++ };
                break;
            case 'cycl':
                console.log(cycle_text);
                if ( key == "cycl01"){
                    if ( !cycle_text.includes(row[key]) ){
                        cycl01_select = false;
                    } else {
                        console.log(row[key])
                    }
                }
                if ( !( val == "" || val == null || val == undefined ) ) { cycl_count++ };
                break;
        }
    })
    have_pdca = pdcatot > 0 ? true:false;
    have_flow = have_flow_count==flow_numbers ? true:false;
    have_cycl = cycl_count==2 ? true:false;

    // console.log( pdcatot,flow_numbers,have_flow_count,job_title_desc,order_number,have_work_item,have_pdca,have_flow,have_cycl);
    // cycl_count : 週期次數,2個(週期+次數)都要選
    // if ( have_work_item && have_pdca && have_flow && have_cycl ){
    if ( have_work_item && have_pdca && have_flow && have_cycl && cycl01_select){
        valid_result['order_number'] = order_number;
        valid_result['result'] = true;
        return valid_result
    } else {
        // 只要一個有問題,就不允送bpm
        valid_result['job_title_desc'] = job_title_desc;
        valid_result['order_number'] = order_number;
        valid_result['result'] = false;
        valid_result['work_item'] = have_work_item ? '':gettext('工作項目空白');
        valid_result['pdca'] = have_pdca ? '':gettext('PDCA未輸入');
        valid_result['flow'] = have_flow ? '':gettext('流程至少有1個未輸入');
        valid_result['cycl'] = have_cycl ? '' : gettext('週期、次數至少有一個未填寫');
        valid_result['cycl01'] = cycl01_select ? '' : gettext('週期錯誤(疑匯入的excel檔"輸入錯誤")');
        return valid_result
    }
}


function this_pdca_tot(row){
    var this_pdcatot=0;
    Object.keys(row).forEach( function (key,idx){
        preTxt = key.substr(0,4)
        val = row[key];
        if ( preTxt=='pdca' && val != null ){
            this_pdcatot += parseInt(val);
        }
    })
    return this_pdcatot
}


function config_tabs_datagrid(add_version){
    var rowCount = 0;
    var tab_dg = '';
    var len = tabs.length;
    var tab_url;

    var hours_stand = 60*wfactor[0].hours_day*wfactor[0].days_month;
    var labor_hours = wfactor[0].labor_hours_desc+wfactor[0].hours_day+"*"+ gettext('小時') +"*"+wfactor[0].days_month + gettext('天')+"="+hours_stand + gettext("分鐘");

    if ( len == 0){
        $("#main_form").hide();
        $("#main-tab").hide();
        alert(gettext("『 TT208 人員職務名稱 』，尚未綁定職務( 無法填寫 )，請洽人資中心！"));
        return;
    }

    for (var i=0 ; i<len ; i++){
        tab_dg = '#tab'+tabs[i].job_title+'_dg'
        tab_url="/sk_api/pdca_detail/"+tabs[i].job_title+"/"+select_work_code+"/"+add_version;
        $(tab_dg).datagrid( {
            title : gettext("職務代碼 : ")+tabs[i].job_title+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+gettext("職務名稱 : ")+tabs[i].job_title_desc,
            singleSelect: true,
            method:'get',
            iconCls: 'icon-edit',
            rowsNumber: true,
            nowrap:false,
            showFooter:true,             //頁小計
            // fitColumns:true,
            autoRowHeight:true,
            data:{
                "total":1,
                "rows":[{"order_number":1,"calc01":1,"calc02":1,}],
                "footer":[{
                    // "work_item":"若工作項目不夠填寫，請依需求自行增加",
                    "work_item":"",
                    "flow06":gettext("小計"),
                    "cycl02":gettext("小計"),
                    "calc01":calc01_tot,
                    "calc02": calc02_tot,
                    "ptot01":ptot_tot,
                    "dtot01":dtot_tot,
                    "ctot01":ctot01_tot,
                    "ctot02":ctot02_tot,
                    "ctot03":ctot03_tot,
                    "atot01":atot_tot,
                    },
                    {
                    // "work_item":"台灣.大陸工時標準：60分*8H*22天=10,560分",
                    "work_item":labor_hours,
                    "cycl02":gettext("總計"),
                    "calc02": calc02_tot,
                    },
                    {
                    "work_item":gettext("平均工作時數/天"),
                    "cycl01":gettext("小計"),
                    "calc02": calc02_tot,
                    "ptot01":ptot_tot,
                    "dtot01":dtot_tot,
                    "ctot01":ctot01_tot,
                    "ctot02":ctot02_tot,
                    "ctot03":ctot03_tot,
                    "atot01":atot_tot,
                    },
                    ]
            },
            url : tab_url,     //2-根據tab的"職務名稱"來抓取grid的data
            frozenColumns:[[
                {field:'order_number',title:gettext('NO.'),width: 40,align:'center',},
                {field:'work_item',title:gettext('工作項目( 不 可 空 白 )'),width: 800,align:'left',
                editor: { type:'textbox',
                            options:{
                                required:false,
                                prompt:gettext('自行輸入資料(限100字)')
                            }
                        },
                },
                {field:'XXX',height: 50,
                    styler: function (value, row, index) {
                        return 'color:MidnightBlue;background-color: MidnightBlue;';
                    },
                },

            ]],
            columns :  reConfigGridColumns(i),
            onClickCell:function (index,field,value) {
               $(this).datagrid('selectRow', index);
            },
            onDblClickCell:function (index,field,value) {
                // if ( field=='work_item' && value=='　'){
                //     $(this).datagrid('updateRow',{
                //         index: index,
                //         row: { work_item: '',}
                //     });
                // }
                $(this).datagrid('selectRow', index);
            },
            onDblClickRow: function (index,row) {
                $(this).datagrid('endEdit', lastRowIndex);      //關掉, 才能取得last_row的data
                var last_row = $(this).datagrid('getRows')[lastRowIndex];
                var last_pdcatot = this_pdca_tot(last_row);
                last_work_item = last_row.work_item;
                row.editing = true;
                // alert("   index="+index+"   lastRowIndex="+lastRowIndex);
                if (( last_work_item == "" || last_work_item == null || last_work_item == "　") && index!=0){
                        var alert_str = "NO : " + (lastRowIndex + 1).toString() + gettext("　以下資料未填寫完成,不能選其他列,儲存也不會成功")+"\n\n"+gettext("1-工作項目")+"\n"+gettext("2- Ｐ、Ｄ、Ｃ、Ａ至少填一個")+"\n"+gettext("3- 週期、次數都必須填寫");
                        $(this).datagrid('endEdit', index);
                        $(this).datagrid('selectRow', lastRowIndex);
                        $(this).datagrid('beginEdit', lastRowIndex);
                        last_work_item = row['work_item'];
                        lastRowIndex = index;
                }
                else {
                    $(this).datagrid('endEdit', lastRowIndex);
                    $(this).datagrid('selectRow', index);
                    $(this).datagrid('beginEdit', index);
                    last_work_item = row['work_item'];
                    lastRowIndex = index;
                }
            },
            onBeforeEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
             },
            onEndEdit: function (index,row){
                this_row_calc(index,row);
                if ( row['okyn01'] == "NO" ){
                    // alert("請確認輸入分鐘數是否正確\n 每月合計(分鐘數)=加總PDCA ");
                    alert(gettext("請確認輸入分鐘數是否正確")+"\n"+gettext(" 每月合計(分鐘數)=加總PDCA ") );
                }
                //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------begin
                var button = document.getElementById("button_get_data_2calc");
                if ( button.disabled == false ) { button.click(); }
                //若未用按鈕去執行, 直接執行, edit的cell的資料都是undifened--------------ending
            },
            onAfterEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
            },
            onCancelEdit:function(index,row){
                row.editing = false;
                $(this).datagrid('refreshRow', index);
            },
            onLoadSuccess: function(data) {
                  mergeCells_dg_footer($(this));
                  get_data_2calc();
                },
            onRowContextMenu: function(e,index,row){
                $(this).datagrid('endEdit', lastRowIndex);
                e.preventDefault();                     //禁止browser catch right click
                $(this).datagrid("clearSelections");    //取消所有選中的列
                $(this).datagrid("selectRow", index);   //根據index選中該行
                $('#Row_Menu').menu('show', {
                    left: e.pageX,                      //在mouse點選出顯示menu
                    top: e.pageY
                })
                e.preventDefault();                     //禁止browser catch right click
            },
        });
        config_tab($(tab_dg),lastRowIndex);
        // toggleDescription($(tab_dg));
    }
}

function updateToBackEnd(arrData){
    var arrLength = arrData.length;
    var data={};
    for( var n=0 ; n < arrLength; n++){
        data[n] = arrData[n];
    }
    url = "/sk_api/update_tabs_datagrid_rows_pdca";
    $.ajax({
    type :"post",
    url :url,
    data :JSON.stringify(data),
    async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
    success :function(res){
                var results = res.results;
                var resultsLength= results.length;
                var alertResults = '';
                var fail_count = 0;
                for ( var i = 0; i < resultsLength ; i++ ){
                    // alertResults = alertResults + results[i].job_title_desc+"      NO : "+(results[i].order_number).toString()+"  "+(results[i].success ? "更新成功":"更新失敗")+"\n";
                    if ( !results[i].success ){
                      fail_count ++;
                      alertResults = alertResults + results[i].job_title_desc+gettext("   NO:")+(results[i].order_number).toString()+" "+gettext("更新失敗")+"\n";
                    }
                }
                if ( fail_count > 0) { alert(alertResults) } else { alert(gettext("更新成功")) }
        }
    });
}


function mergeCells_dg_footer(dg){
      dg.datagrid('mergeCells', {index: 0, field: 'pdca01',colspan:14,type: 'footer'});
      dg.datagrid('mergeCells', {index: 1, field: 'pdca01',colspan:17,type: 'footer'});
      dg.datagrid('mergeCells', {index: 2, field: 'pdca01',colspan:18,type: 'footer'});

      dg.datagrid('mergeCells', {index: 1, field: 'ptot01',colspan:10,type: 'footer'});
}


function redefine_dg_footer(dg){
    var calc1_x = parseFloat(calc01_tot.toFixed(2));
    var calc2_x = parseFloat(calc02_tot.toFixed(2));
    var ptot1_x = parseFloat(ptot_tot.toFixed(2));
    var dtot1_x = parseFloat(dtot_tot.toFixed(2));
    var ctot1_x = parseFloat(ctot01_tot.toFixed(2));
    var ctot2_x = parseFloat(ctot02_tot.toFixed(2));
    var ctot3_x = parseFloat(ctot03_tot.toFixed(2));
    var atot1_x = parseFloat(atot_tot.toFixed(2));
    var pdca_total = parseFloat( (ptot1_x + dtot1_x + ctot1_x + ctot2_x + ctot3_x + atot1_x).toFixed(2) );
    var days_month = wfactor[0].days_month;
    var whours_day = parseFloat( (pdca_total/60/days_month).toFixed(2) );                 //每月工作幾天( 依國籍不同)

    var ptot1_y = ( ptot1_x==0 ? '0':( (ptot1_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var dtot1_y = ( dtot1_x==0 ? '0':( (dtot1_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var ctot1_y = ( ctot1_x==0 ? '0':( (ctot1_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var ctot2_y = ( ctot2_x==0 ? '0':( (ctot2_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var ctot3_y = ( ctot3_x==0 ? '0':( (ctot3_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var atot1_y = ( atot1_x==0 ? '0':( (atot1_x/pdca_total)*100 ).toFixed(2　) ).concat("%");
    var ok_y = ( ptot1_x==0 ? '0': ( (pdca_total/pdca_total)*100).toFixed(0　) ).concat("%");
    var hours_stand = 60*wfactor[0].hours_day*wfactor[0].days_month;           //60*每天8小時*每月26天或22天
    var labor_hours = wfactor[0].labor_hours_desc+wfactor[0].hours_day+gettext('小時')+"*"+wfactor[0].days_month+gettext('天')+"="+hours_stand+gettext("分鐘");

    dg.datagrid('reloadFooter',
        [{
            // "work_item":"若工作項目不夠填寫，請依需求自行增加",
            "work_item":"",
            "flow06":gettext("小計"),
            "cycl02":gettext("小計"),
            "calc01":calc1_x,
            "calc02":calc2_x,
            "ptot01":ptot1_x,
            "dtot01":dtot1_x,
            "ctot01":ctot1_x,
            "ctot02":ctot2_x,
            "ctot03":ctot3_x,
            "atot01":atot1_x,
            "okyn01": pdca_total,
         },
        {
            // "work_item":gettext("台灣.大陸工時標準：60分*8H*22天=10,560分"),
            "work_item":labor_hours,
            "cycl02":gettext("總計"),
            "calc02": calc2_x,
        },
        {
            "work_item":gettext("平均工作時數/天"),
            "calc02" : whours_day,
            "ptot01" : ptot1_y,
            "dtot01" : dtot1_y,
            "ctot01" : ctot1_y,
            "ctot02" : ctot2_y,
            "ctot03" : ctot3_y,
            "atot01" : atot1_y,
            "okyn01" : ok_y,
        },
        ]
    );
}


function get_footer_rows(dg,job_title,job_title_desc,work_code,the_time,){
    var gridData;
    var tabData = [];
    var footerRows = dg.datagrid("getFooterRows");
    var footerLen = footerRows.length ;
    var fieldsLength = 0;
    var cell_value;
    var order_number = 9991;
    var row;
    for (var j=0 ; j < footerLen ; j++) {
        row = footerRows[j];
        gridData = {};
        gridData['work_code'] = work_code;
        gridData['the_time'] = the_time;
        gridData['job_title'] = job_title;
        gridData['job_title_desc'] = job_title_desc;
        gridData['order_number'] = order_number;
        gridData['work_item'] = 'TAB FOOTER : SUMMARY_' + (order_number - 9990).toString();
        order_number++;
        Object.keys(row).forEach( function (key,idx){
            cell_value = row[key];
            //清洗資料
            if ( cell_value != undefined || cell_value != "") {
                if ( (cell_value.toString()).indexOf('%') > 0) {    // 去除%
                    cell_value = cell_value.substr(0, cell_value.length - 1);
                }
                if (key != "work_item") {
                    if ( cell_value == "小計" || cell_value == "總計" ){
                        gridData[key] = 0;
                    } else {
                        gridData[key] = cell_value;
                    }
                }
            }
        })
        tabData[j] = gridData;
    }
    return tabData;
}


function disable_tabs_datagrid(add_version){
    var rowCount = 0;
    var tab_dg = '';
    var len = tabs.length;
    var tab_url;
    var hours_stand = 60*wfactor[0].hours_day*wfactor[0].days_month;
    var labor_hours = wfactor[0].labor_hours_desc+wfactor[0].hours_day+"*"+gettext('小時')+"*"+wfactor[0].days_month+gettext('天')+"="+hours_stand+gettext("分鐘");
    // var labor_hours = wfactor[0].labor_hours_desc+wfactor[0].hours_day+"*"+'小時'+"*"+wfactor[0].days_month+'天'+"="+hours_stand+"分鐘";
    for (var i=0 ; i<len ; i++){
        tab_url="/sk_api/pdca_detail/"+tabs[i].job_title+"/"+select_work_code+"/"+add_version;
        tab_dg = '#tab'+tabs[i].job_title+'_dg'
        $(tab_dg).datagrid( {
            title : gettext("職務代碼 : ")+tabs[i].job_title+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+gettext("職務名稱 : ")+tabs[i].job_title_desc,
            // title : "職務代碼 : "+tabs[i].job_title+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+"職務名稱 : "+tabs[i].job_title_desc,
            rowsNumber: true,
            showFooter:true,             //頁小計
            data:{
                "total":1,
                "rows":[{"order_number":1,"calc01":1,"calc02":1,}],
                "footer":[{
                    // "work_item":"若工作項目不夠填寫，請依需求自行增加",
                    "work_item":"",
                    "flow06":gettext("小計"),
                    "cycl02":gettext("小計"),
                    "calc01":calc01_tot,
                    "calc02": calc02_tot,
                    "ptot01":ptot_tot,
                    "dtot01":dtot_tot,
                    "ctot01":ctot01_tot,
                    "ctot02":ctot02_tot,
                    "ctot03":ctot03_tot,
                    "atot01":atot_tot,
                    },
                    {
                    "work_item":labor_hours,
                    "cycl02":gettext("總計"),
                    "calc02": calc02_tot,
                    },
                    {
                    "work_item":gettext("平均工作時數/天"),
                    "cycl01":gettext("小計"),
                    "calc02": calc02_tot,
                    "ptot01":ptot_tot,
                    "dtot01":dtot_tot,
                    "ctot01":ctot01_tot,
                    "ctot02":ctot02_tot,
                    "ctot03":ctot03_tot,
                    "atot01":atot_tot,
                    },
                    ]
            },
            url : tab_url,     //2-根據tab的"職務名稱"來抓取grid的data
            frozenColumns:[[
                {field:'order_number',title:gettext('NO.'),width: 40,align:'center'},
                {field:'work_item',title:gettext('工作項目'),width: 600,align:'left',
                editor: { type:'textbox',
                            options:{
                                required:false,
                                prompt:gettext('自行輸入資料(限100字)')
                            }
                        },
                    },
                {field:'XXX',
                    styler: function (value, row, index) {
                        return 'color:MidnightBlue;background-color: MidnightBlue;';
                    },
                },

            ]],
            columns :  reConfigGridColumns(i),
            onDblClickRow: function (index,row) {
                row.editing = false;
            },
            onLoadSuccess: function(data) {
                  mergeCells_dg_footer($(this));
                  get_data_2calc();
                }
        });
    }
}


function after_submit_bpm_success() {
    $("#tab_save").hide();
    $('#preview_report').hide();
    $('#submit_bpm').hide();
    $('#import_btn').hide();
    disable_tabs_datagrid("X");
}

function panel_component_control(){
    $("#tab_save").show();
    $('#preview_report').show();
    $('#submit_bpm').show();
    $('#import_btn').show();

    $('#add_version').hide();
    $('#copy_version').hide();

}

function fixdata(data) { //檔案流轉BinaryString
    var o = "",
        l = 0,
        w = 10240;
    for(; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
    o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
    return o;
}



function rowEmptyValid(i){
    var tab_dg = '#tab' + tabs[i].job_title + '_dg';
    var rows = $(tab_dg).datagrid('getRows');
    var rowNumbers = rows.length;
}



$(document).ready(function(){
    if ( ["zh-hant", "zh-hans"].includes(choice_language) ) {
        $('#submit_bpm').linkbutton('enable');
        $('#submit_bpm').show();
    }  else {
        $('#submit_bpm').linkbutton('disable');
        $('#submit_bpm').linkbutton('resize', {
                width: 1,
                height: 1
            });
    }

    var tab_numbers = tabs.length;
    var tab_dg;
    var rowsNumber;
    var exec_import = "N";
    if (the_time.last == 999999) {
        after_submit_bpm_success();
        $('#add_version').hide();
        $('#copy_version').hide();
        // alert("第" + (the_time.current).toString() + "版___送簽狀態: " + the_time.bpm_desc1 + "   " + the_time.bpm_desc2 + "\n\n  1-送簽中，不可修改資料。\n  2-送簽中，不允新增版本。");
        var alert_str = gettext("第") + (the_time.current).toString() + gettext("版___送簽狀態: ") + the_time.bpm_desc1 + "   " + the_time.bpm_desc2 + "\n\n"+gettext("  1-送簽中，不可修改資料。")+"\n"+gettext("  2-送簽中，不允新增版本。");
        // alert("第" + (the_time.current).toString() + "版___送簽狀態: " + the_time.bpm_desc1 + "   " + the_time.bpm_desc2 + "\n\n  1-送簽中，不可修改資料。\n  2-送簽中，不允新增版本。");
        alert(alert_str);
    } else {
        if (the_time.bpm_desc1 == "signed") {
            after_submit_bpm_success();
            $('#add_version').show();
            $('#copy_version').show();
            var alert_str = gettext("第") + (the_time.current).toString() + gettext("版___已送簽完成。可再新增版次。")+"\n\n"+gettext("   匯入 : 複製舊版次資料再修改。")+"\n"+gettext("   新增 : 完全空白，從頭開始輸入。");
            // alert("第" + (the_time.current).toString() + "版___已送簽完成。可再新增版次。\n\n   匯入 : 複製舊版次資料再修改。 \n   新增 : 完全空白，從頭開始輸入。");
            alert(alert_str);
        } else {
            panel_component_control();
            config_tabs_datagrid("X");
        }
    }

    // window.onbeforeunload=function(e){
    // 　　var e = window.event||e;
    //     e.returnValue=("");
    // }  //離開業面提醒
    //
    // window.onunload=function(e){
    // 　　var e = window.event||e;
    //     e.returnValue=("");
    // }  //離開業面提醒
    //
    // window.onclose=function(e){
    // 　　var e = window.event||e;
    //     e.returnValue=("");
    // }  //離開業面提醒
    $("#choice_lang").change( function () {
        var choice_language = $("#choice_lang").find(":selected").val();
        // $.get("/sk_api/set_language_code/"+choice_language,function (res) {res});
        //show出選取語言, 只為了延緩時間, 好讓server有時間, 把翻譯好的"文字"送到 client
        //alert("您選取的語言是:" + choice_language);

        //show出選取語言, 只為了延緩時間, 好讓server有時間, 把翻譯好的"文字"送到 client, 若前項alert時間還是無法來得及, 再加下面這個
        // setTimeout(function(){
        //     location.reload();
        //     },500);
        $.ajax({
            type: "get",
            url: "/sk_api/set_language_code/"+choice_language,
            //非同步:false-->冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情
            //把翻譯好的"文字"送到 client, reload()文字才會正確
            async: false,
        })
        tab_save(false);   //上列, 語言設定完成, 再儲存資料(儲存時會翻譯), 先儲存目前資料
        location.reload();
    })


    $('#export_btn').click( function () {
        exportData_singleSheet("");
    })

    // 顯示excel匯入對話方塊
    $('#import_btn').click(function () {
        $('#import_dd').attr('hidden', false);
        // tab_save(false);
        $('#import_dd').dialog({
            // title: '請挑選要匯入的excel檔(.xlsx)',
            title:gettext("請挑選要匯入的excel檔(.xlsx)"),
            width: 715,
            closed: false,
            cache: false,
            modal: true,
        });
    });


    $("#add_version").click(function () {
            var new_version = (the_time.current + 1).toString();
            var new_legend = gettext("新增版本   第") + new_version + gettext("版");
            $('legend:first').text(new_legend);
            $("#id_the_time").val(new_version);

        panel_component_control();
        config_tabs_datagrid("Y");
    });

    function tab_dg_reload() {
        for (var i = 0; i < tab_numbers; i++) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            $(tab_dg).datagrid('reload');
        }
    }

    function tab_save(bpm_yn) {
        var rowsNumber;
        var tabData;
        var tabFooterData;
        var err_arrData = [];
        var all_job_title = [];
        var arrData = [];
        for (var i = 0; i < tab_numbers; i++) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            footer_pdca_calc($(tab_dg));
            redefine_dg_footer($(tab_dg));
            mergeCells_dg_footer($(tab_dg));
            tabData = get_datagrid_rows($(tab_dg), tabs[i].job_title, tabs[i].job_title_desc, select_work_code, the_time.last , bpm_yn);      //取得每個TAB的GridRows，
            tabFooterData = get_footer_rows($(tab_dg), tabs[i].job_title, tabs[i].job_title_desc, select_work_code, the_time.last);
            arrData = arrData.concat(tabData);             //array的合併
            arrData = arrData.concat(tabFooterData);             //array的合併
        }
        updateToBackEnd(arrData);                         //將蒐集的資料，傳給後端儲存
        tab_dg_reload();
    }


    $("#button_get_data_2calc").click(function () {
        get_data_2calc();
    });


    //儲存( 所有 )
    $("#tab_save").click(function () {
        tab_save(false);
    });


    $("#preview_report").click(function () {
        tab_save(false);
        var fileName = "PREVIEW_" + 'PDCA' + getFormatedDateTime() + ".pdf";
        window.open(location.href + '2pdf?fileName=' + fileName);
    })


    $("#submit_bpm").click(function () {
        var valid = {};
        var rows;
        var rowNumbers = 0;
        var err_msg = [];
        var err_len = 0;
        var err_line = "";
        var tabEmpty = [];
        var empty_len = 0;
        var tabNotEmptyCount=0;
        var flow_numbers=0;
        tab_save(true);
        $.each(tab_fields[0], function (index, value) {
            //計算flow的個數
            if ((value.name).substr(0, 4) == "flow") { flow_numbers++ }
        })
        for (var i = 0; i < tab_numbers; i++) {
            tab_dg = '#tab' + tabs[i].job_title + '_dg';
            rows = $(tab_dg).datagrid('getRows');　　　　//不會取header及footer
            // console.log(rows);
            rowNumbers = rows.length;
            tabNotEmptyCount = 0;

            //計算"流程"有幾個欄位
            for (var j = 0; j < rowNumbers; j++) {
                // if (rows[j].work_item != null && rows[j].work_item != "") {              //避開沒有填的格子
                if (rows[j].work_item != null && rows[j].work_item != "" && rows[j].work_item != "　") {              //避開沒有填的格子
                    valid = this_row_validate(tabs[i].job_title_desc, j, rows[j],flow_numbers);
                    if (!valid.result) {
                        err_msg.push(valid);
                    }
                    tabNotEmptyCount ++;
                }
            }
            if ( tabNotEmptyCount == 0 ){  tabEmpty.push(tabs[i].job_title_desc)  }
        }

        var val = "";
        err_len = err_msg.length;
        empty_len = tabEmpty.length;
        // if (err_len > 0) {    //若只有檢查這個, 完全沒填, err_len=0, 也可以送出     20220310修改
        // console.log(" err_msg=",err_msg);
        // console.log(" tabEmpty=",tabEmpty);
        if (err_len > 0 || empty_len>0 ) {     //有錯誤訊息 or 有tab為空
            for (var n = 0; n < err_len; n++) {
                Object.keys(err_msg[n]).forEach(function (key, idx) {
                    val = err_msg[n][key];
                    if (val != "") {
                        switch (key) {
                            case "job_title_desc":
                                err_line += gettext("職務名稱: ") + val + "   ";
                                break;
                            case "order_number":
                                err_line += gettext("NO:") + val + "   ";
                                break;
                            default:
                                err_line += val + "，";
                                break;
                        }
                    }
                })
                err_line += "\n";
            }
            switch (true){
                case ( err_len > 0 && empty_len == 0 ) :
                    alert("＊"+gettext("不允送ＢＰＭ，以下資料未填寫完整")+"\n" + err_line);
                    break;
                case ( err_len == 0 && empty_len > 0):
                    alert("＊"+gettext("不允送ＢＰＭ，以下的資料全部為空白")+"\n"+gettext("職務名稱:")+"\n     " + tabEmpty.join('\n     '));
                    break;
                case (err_len > 0 && empty_len > 0):
                    alert("＊"+gettext("不允送ＢＰＭ")+"\n"+gettext("1-以下的資料全部為空白")+"\n"+gettext("職務名稱:")+"\n     " + tabEmpty.join('\n     ') + "\n"+gettext("2-以下資料未填寫完整")+"\n" + err_line);
                    break;
            }
        } else if ( err_len == 0 && empty_len == 0 ) {     //全都沒有錯誤
            var fileName = 'PDCA' + getFormatedDateTime() + ".pdf";
            var port = location.port;
            var pdf_url = "";
            var new_tabs = [];
            var button;
            for (var i = 0; i < tab_numbers; i++) {
                new_tabs[i] = tabs[i].job_title;;
            }
            alert(" the_time=",the_time.last);
            exportData_singleSheet("Y",the_time.last);

            if (port.length > 0) {
                // http://127.0.0.1:8000
                pdf_url = location.protocol + "//" + location.hostname + ":" + location.port
            } else {
                // httpd://pmsbeta.tiongliong.com............
                // httpd://pms.tiongliong.com............
                pdf_url = location.protocol + "//" + location.hostname
            }


            var data = {
                job_titles: tabs.map(item => item.job_title),
                the_time: the_time.last,
                report_name: fileName,
                report_url: pdf_url
            };
            var url = "/sk_api/submit_bpm_pdca";
            data = JSON.stringify(data);
            $.post(
                url,
                data,
                function (res) {
                    if (res.success) {
                        alert(gettext('送出成功!'));
                        after_submit_bpm_success();
                    } else {
                        alert(gettext('錯誤!'))
                    }
                }
            )
            window.open(location.href + '2pdf?fileName=' + fileName);
        }
    })
});

