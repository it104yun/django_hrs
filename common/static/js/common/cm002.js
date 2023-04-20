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


function centerControl(event) {
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
    idField: "topic_code",
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        rowCount = data.total;
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
    var mainUrl = $('#main_dg').data().source;
    var formSourceUrl = $('#main_form').attr('action');
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);

    $('#main_dg').datagrid('reorderColumns', columnOrder);


    $('#id_email').change(function() {
        $(".error").hide();
        var hasError = false;
        var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

        var this_email = $(this).val();
        if(this_email == '') {
            $(this).after(function (){
                alert('請輸入email位址');
                }
            );
            hasError = true;
        }else if(!emailReg.test(this_email)) {
            $(this).after( function(){
                alert('請輸入符合格式的e-mail位址, 例如'+"exmaple@abc.com");
                $(this).val('');
            });
            hasError = true;
        }

        // if(hasError == true) { return false; }

    });

    $('#id_rank').change(function(){
        var rank_number=$(this).val();
        var rank_selected=$('option:selected',this).text();;
        if (parseInt(rank_selected)<=7) {                 //BSC
            $('#id_eval_class').get(0).options[2].selected = true;
            // $('#id_eval_class').find("option:contains('BSC')").attr("selected",true);
        } else if (parseInt(rank_selected)>7){                                         //KPI
                    $('#id_eval_class').get(0).options[1].selected = true;
                    // $('#id_eval_class').find("option:contains('KPI')").attr("selected",true);
                } else {
                    $("#id_eval_class").children().each(function() {
                        //清空選定的狀態
                        // $(this).attr("selected", "false");
                        this.selected = false;
                    })
        }
    });

    $('#new_btn').click(function(){
        resetForm('main_form');
        main_form.elements[0].focus();
        $('#import_btn').hide();
        $('#copy_btn').hide();
         centerControl('new');
    });

    $('#create_btn').click(function(){
        // 新增
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        /*
                $.post(
                    formSourceUrl,
                    data,
                    function(res) {
                        if(res.success) {
                            alert('新增成功!')
                            $('#main_dg').datagrid('reload');
                        } else {
                            alert('錯誤!'+'\n\n'+res.message);
                        }
                    }
                );
         */


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
                    currentEvent = 'new';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('錯誤!'+'\n\n'+res.message);
                }
            }
        });
        $('#import_btn').show();
        $('#copy_btn').show();
    });


    // 顯示複製對話方塊
    $('#copy_btn').click(function () {
        // 取得所有員工的<工號,姓名>
        comboboxSourceUrl = "/api/get_employee_data";
        $.get(
            comboboxSourceUrl,
            function (res) {
                if (res) {
                    optionTxt = res;
                    $("#copyFrom_id").combobox({
                    valueField:'value',
                    textField:'text',
                    data: optionTxt,
                    /*
                        [
                          {value:'水泥',text:'水泥'},
                          {value:'食品',text:'食品'},
                          {value:'塑膠',text:'塑膠'},
                          {value:'鋼鐵',text:'鋼鐵'},
                          {value:'電子',text:'電子',selected:true},
                          {value:'金融',text:'金融'}
                       ]
                     */
                    });

                    $('#copy_dd').attr('hidden',false);

                    $('#copy_dd').dialog({
                        title: '請選取要複製的工號',
                        width: 600,
                        height: 340,
                        closed: false,
                        cache: false,
                        // href: '',
                        modal: true,
                    });


                    $('#copy_clear').click(function (){
                        $('#copy_form')[0].reset();
                    });


                    $('#copy_sumit').click(function (){
                        copySourceUrl = $('#copy_form').attr('action');
                        data = getFormData(copy_form); //取得來源料號, 複製1, 複製2, 複製3
                        $.post(
                            copySourceUrl,
                            data,
                            function (res){
                               if (res.success) {
                                   alert('複製成功');
                               } else {
                                   alert('複製失敗!');
                               }
                            });
                    });
                }else {
                    optionTxt = null;
                }
            }
        )
     });

    // 顯示excel匯入對話方塊
    $('#import_btn').click(function () {
        $('#import_dd').attr('hidden',false);
        $('#import_dd').dialog({
            title: '請挑選要匯入的excel檔(.xlsx)',
            width: 400,
            height: 190,
            closed: false,
            cache: false,
            // href: '',
            modal: true,
        });
     });

    $('#cancel_btn').click(function(){
        $('#main_dg').datagrid('reload');
        $('#import_btn').show();
        $('#copy_btn').show();
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
                    currentEvent = 'update';
                } else {
                    idFieldValue = null;
                    currentEvent = null;
                    alert('k錯誤'+'\n\n'+res.message);
                }
            }
        )
    });


    $('#delete_btn').click(function(){
        // 刪除
        if (!confirm('自定義碼主題關係著自定義碼設定\n請確認您要刪除\n再按下『確定』')) return;
        idFieldValue = null;
        $.get(formSourceUrl + '/' + currentKey,
            function(res) {
                if(res.success) {
                    alert('刪除成功!');
                    $('#main_dg').datagrid('reload');
                    currentEvent = 'delete';
                } else {
                    currentEvent = null;
                    alert('錯誤'+'\n\n'+res.message);
                }
            }
        );
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




