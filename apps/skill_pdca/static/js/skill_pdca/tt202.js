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
        if(field.tagName === 'SELECT') {
            field.value = row[fieldName + '_id'] || row[fieldName];
        }
        else {
            fields[i].value = row[fieldName];
        }
    }
}




function level1_options() {
    var options = l1_jobtitles.map(function (job) {
        return '<option value="' + job.value + '">' + job.text + '</option>';
    }).join('');
    main_form.id_job_parent_parent.innerHTML = options;
}


function level2_options() {
    var options = l2_jobtitles.map(function (job) {
        return '<option value="' + job.value + '">' + job.text + '</option>';
    }).join('');
    main_form.id_job_parent.innerHTML = options;
}



function filter_level_number3_options(){
    var option_length = $('#id_job_parent option').length;
     $('#id_job_parent option').each(function (){
         //移除1階(大分類)/2階(中分類)
         if ( $(this).val().length != 4 ) {
            $(this).remove();
        }
     });
}


function filter_level_number2_options(){
    level2_options();
    $('#id_job_parent option').each(function (){
        if ( $(this).val().length != 4 ) {
            $(this).remove();
        }
        if ( $(this).val().substring(0,2) != $('#id_job_parent_parent').val() ) {
            $(this).remove();
        }
     });
}


function gridSelectTo(dg,currentEvent){
    var dg = '#'+ dg;
    switch(currentEvent) {
        case 'new':
            $(dg).datagrid('selectRecord', idFieldValue);
            clearError();
            break
        case 'update':
            $(dg).datagrid('selectRecord', idFieldValue);
            clearError();
            break
        case 'delete':     //刪除之後,INDEX不變,還是原來的位置
            var rowsCount = $(dg).datagrid('getRows').length;
            //刪除最後一筆資料時, 還是移到最後一筆資料
            if (currentRowIndex==rowsCount){
                $(dg).datagrid('selectRow', currentRowIndex-1);
            } else {
                $(dg).datagrid('selectRow', currentRowIndex);
            }
            clearError();
            break
        default:
            $(dg).datagrid('selectRow', 0);
            break
    }
}


function get_last_job_code(l2_option){
    var rtn_value="";
    $.ajax({
        type: "get",
        url: "/sk_api/get_last_job_code/" + l2_option,
        async: false,                 //非同步:false-->所以是冋步傳輸:收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success: function (res) {
            if (res) {
                console.log(" last_job_code:", res.last_job_code);
                rtn_value = res.last_job_code;
            }
        }
    })
    return rtn_value;
}


function centerControl(event) {
    filter_level_number3_options();
    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.id_job_parent.disabled = false;
            main_form.id_job_parent_parent.disabled = false;
            main_form.id_job_code.disabled = false;
            filter_level_number2_options();
            main_form.id_job_code.value = get_last_job_code(main_form.id_job_parent.value);
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.id_job_parent.disabled = true;
            main_form.id_job_parent_parent.disabled = true;
            main_form.id_job_code.disabled = true;
            main_form.id_job_parent_parent.value = (main_form.id_job_parent.value).substring(0,2);
            clearError();
            break
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            // main_form.job_code.disabled=true;
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
    idField: "job_code",
    columns: [[
        {field: 'job_parent', title: '中分類', width: 150, sortable:true,},
        {field: 'job_code', title: '職務代號', width: 120, sortable:true,},
        {field: 'job_name', title: '職務名稱', width: 200, sortable:true,},
        // {field: 'job_desc', title: '職務說明', width: 200, sortable:true,},
        {field: 'level_number', title: '階層',align: 'center',styler: function(value,row,index){return 'color:white;';}},
     ]],
    rowStyler: function(index,row){
        switch ( row.level_number){
            case 1:
                return 'background:#000000 ;color:white;font-weight: bolder;font-size: larger;';
            case 2:
                return 'background:#dddddd ;color:black;';
        }
    },
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        // return opts.autoLoad;
    },
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        level2_options();
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        var len = data.total;
        /*    改用 filterRules 過濾
        var i = 0;
        while (i < len) {
            if (data.rows[i]['level_number'] != 3) {
                //有找到的("共同指標")，刪除
                $(this).datagrid('deleteRow', i);
                len--;
            } else {
                i++;
            }
            ;
        }
         */
        gridSelectTo('main_dg',currentEvent);
    }
}

config.cpx_search_dlg = {
    'dlg': {
        resizable: true,
        modal: true,
        closed: true,
    },
    'search': {
        afterSearch: function(res){
            $("#main_dg").datagrid('loadData', res);
        }
    }
}


$(document).ready(function(){
    var key = $('#main_dg').data().key;
    var mainUrl = $('#main_dg').data().source;                   // view.py 裏定義的
    var formSourceUrl = $('#main_form').attr('action');   // form.py 裏定義的
    var l2_options = $('#id_job_parent option').val();

    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#main_dg').datagrid('reorderColumns', columnOrder);
    centerControl('update');


    $('#main_dg').datagrid('hideColumn', 'level_number');

    //只設定level_number=3,才顯示, user只編輯第三階的職務
    $('#main_dg').datagrid({
        filterRules:[{
            field:'level_number',
            op:'equal',
            value:3,
	    }],
    });
    $('#main_dg').datagrid('enableFilter');

    /*    2021/11/30remark user有要求, 再寫需求單, 開啟吧!
    var dg = $('#main_dg').datagrid({
	    defaultFilterType:'label'
    });
    dg.datagrid('enableFilter', [{
            field:'job_code',
            type:'textbox',
            options:{precision:1},
            op:['contains','equal','notequal','less','lessorequal','greater','greaterorequal','beginwith','endwith']
        },{
            field:'job_name',
            type:'textbox',
            options:{precision:1},
            op:['contains','equal','notequal','less','lessorequal','greater','greaterorequal','beginwith','endwith']
        },
    ]);
     */

    $('#id_job_parent_parent').change(function (){
        filter_level_number2_options();
        main_form.id_job_code.value = get_last_job_code($('#id_job_parent').val());
    });

    $('#id_job_parent').change(function (){
        main_form.id_job_code.value = get_last_job_code($(this).val());
    });


    $('#new_btn').click(function(){
        main_form.elements[0].focus();
        centerControl('new');
    });


    $('#create_btn').click(function(){
        // 新增
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        console.log(data);
        delete data.job_parent_parent_id;
        delete data.filterRules;
        data['level_number'] = 3;
        $.ajax({
        type :"post",
        url :formSourceUrl,
        data :data,
        async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success :function(res){
                console.log(data);
                if (res.success) {
                    alert('新增成功!');
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['job_code'];
                    currentEvent = 'new';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('錯誤!'+'\n\n'+res.message);
                }
            }
        });
    });


    $('#cancel_btn').click(function(){
        centerControl('update');
        $('#main_dg').datagrid('reload');
    });

    $('#update_btn').click(function(){
        // 更新
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['job_code'];
                    currentEvent = 'update';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('錯誤'+'\n\n'+res.message);
                }
            }
        )
    });


    $('#delete_btn').click(function(){
        // 刪除
        idFieldValue = null;
        $.get(formSourceUrl + '/' + currentKey,
        function(res) {
            if(res.success) {
                alert('刪除成功!');
                var queryParams = $('#main_dg').datagrid('options').queryParams;
                console.log(queryParams);
                $('#main_dg').datagrid('reload');
                currentEvent = 'delete';
            } else {
                currentEvent = null;
                alert('錯誤'+'\n\n'+res.message);
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

    function resetForm(form_id) {
        $('#' + form_id).form('reset');
        $(document).trigger('reset_' + form_id);
    }

});




