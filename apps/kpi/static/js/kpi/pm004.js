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
            if ( row[fieldName]=='True'){ field.checked = true } else { field.checked = false };
        }
        else {
            fields[i].value = row[fieldName];
        }
    }
}


function filter_work_code_options(){

    $('#id_work_code option').each(function (){
         //移除共同指標direct_supv
         if ( $(this).val().search("-") > -1) {
            $(this).remove();
        }
     });

     $('#id_direct_supv option').each(function (){
         //移除共同指標direct_supv
         if ( $(this).val().search("-") > -1) {
            $(this).remove();
        }
     });

     $('#id_director option').each(function (){
         //移除共同指標director
         if ( $(this).val().search("-") > -1) {
            $(this).remove();
        }
     });
}



function centerControl(event) {
    switch(event) {
        case 'new':
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.work_code.disabled=false;
            clearError();
            break
        case 'update':
            buttonControl('inline-block', 'none', 'inline-block', 'inline-block', 'inline-block');
            main_form.work_code.disabled=true;
            clearError();
            break
        default:
            buttonControl('none', 'inline-block', 'inline-block', 'none', 'none');
            main_form.work_code.disabled=true;
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

/*
//去除使用者在combobox,自行輸入的"關鍵字"
function remove_keyword(choices){
    var choices_arr = choices.split(',');
    var rtn_choices=choices;
    choices_arr.forEach( function(value,index){
        var s_start = value.length+1;
        var s_end = choices.length - s_start;
        rtn_choices =  choices.substr(s_start,s_end);
    })
    return rtn_choices;
}
 */

function remove_keyword(choices){
    var s_start = choices.search(',')+1;
    var s_end = choices.length - s_start;
    return choices.substr(s_start,s_end);
}


//




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
    idField: "work_code",
    autoLoad: false,
    onBeforeLoad: function () {
        var opts = $(this).datagrid('options');
        return opts.autoLoad;
    },
    onSelect: function(index, row) {
        currentRowIndex = index;
        currentRow = row;
        currentKey = row[$(this).data().key];
        setFormData(main_form, row);
        centerControl('update');
    },
    onLoadSuccess: function(data) {
        /*
        rowCount = data.total;
        //個人指標:共同指標不出現
        var i = 0;
        while( i < data.rows.length ){
            if ( data.rows[i]['work_code'].search("-") > -1) {
                //有找到的("共同指標")，刪除
                $(this).datagrid('deleteRow',i);
            }
            else {
              i++;
            }
        }
         */
        gridSelectTo('main_dg',currentEvent);
    }
}


/*
config.main_mono_search_dlg = {
    resizable: true,
    modal: true,
    closed: true,
}
*/


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
    document.querySelector('.layout-split-east .panel-body').scrollTo(0,0);
    $('#main_dg').datagrid('reorderColumns', columnOrder);
    centerControl('update');

    // work_code_url = "/api/get_employee_data_factory/"+currentFactory;
    work_code_url = "/api/get_employee_data_factory"
    $.get(
        work_code_url,
        function (res) {
            if (res) {
                optionTxt = res;
                $('#searchWorkCode').combobox({
                    // multiple: false,
                    multiple: true,
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                    //改成checkbox
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
                    onSelect: function (row) {
                        //console.log(row);
                        var opts = $(this).combobox('options');
                        var el = opts.finder.getEl(this, row[opts.valueField]);
                        el.find('input.combobox-checkbox')._propAttr('checked', true);
                        },
                    onUnselect: function (row) {
                        var opts = $(this).combobox('options');
                        var el = opts.finder.getEl(this, row[opts.valueField]);
                        el.find('input.combobox-checkbox')._propAttr('checked', false);

                    }
                });
            }
        })

    // director_url = "/api/get_director_data_factory/"+currentFactory;
    director_url = "/api/get_director_data_factory";
    $.get(
        director_url,
        function (res) {
            if (res) {
                optionTxt = res;
                $('#searchDirector').combobox({
                    // multiple: false,
                    multiple: true,
                    valueField: 'value',
                    textField: 'text',
                    data: optionTxt,
                    //改成checkbox
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
                    onSelect: function (row) {
                        //console.log(row);
                        var opts = $(this).combobox('options');
                        var el = opts.finder.getEl(this, row[opts.valueField]);
                        el.find('input.combobox-checkbox')._propAttr('checked', true);
                        },
                    onUnselect: function (row) {
                        var opts = $(this).combobox('options');
                        var el = opts.finder.getEl(this, row[opts.valueField]);
                        el.find('input.combobox-checkbox')._propAttr('checked', false);

                    }
                });
            }
        })
    //設定初值(加",")

    udc_url = "/api/get_common_udc/"+"dept_id";
        $.get(
            udc_url,
            function (res) {
                if (res) {
                    optionTxt = res;
                    $('#searchDept').combobox({
                        // multiple: false,
                        multiple: true,
                        valueField: 'value',
                        textField: 'text',
                        data: optionTxt,
                        //改成checkbox
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
                        onSelect: function (row) {
                            //console.log(row);
                            var opts = $(this).combobox('options');
                            var el = opts.finder.getEl(this, row[opts.valueField]);
                            el.find('input.combobox-checkbox')._propAttr('checked', true);
                            },
                        onUnselect: function (row) {
                            var opts = $(this).combobox('options');
                            var el = opts.finder.getEl(this, row[opts.valueField]);
                            el.find('input.combobox-checkbox')._propAttr('checked', false);

                        }
                    });
                }
            })


    $('#east_search').click( function(){
        var work_code = remove_keyword( $('#searchWorkCode').val() );
        var director = remove_keyword( $('#searchDirector').val() );
        var dept = remove_keyword( $('#searchDept').val() );

        if ( work_code!='' && director!='' && dept!='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    work_code: work_code,
                    direct_supv: director,
                    dept: dept
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        } else if ( work_code!='' && director=='' && dept=='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    work_code: work_code,
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        } else if ( work_code!='' && director=='' && dept!='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    work_code: work_code,
                    dept: dept
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        }  else if ( work_code=='' && director=='' && dept!='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    dept: dept
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        }  else if ( work_code=='' && director!='' && dept=='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    direct_supv: director
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        } else if ( work_code=='' && director!='' && dept!='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    direct_supv: director,
                    dept: dept
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#main_dg').datagrid('reload');
        } else if ( work_code!='' && director!='' && dept=='' ) {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                    work_code: work_code,
                    direct_supv: director
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#mdin_dg').datagrid('reload');
        } else {
            $("#main_dg").datagrid({
                queryParams: {
                    // factory_id: currentFactory,
                },
            });
            $('#main_dg').datagrid({autoLoad:true});
            $('#mdin_dg').datagrid('reload');
        }
    });


    $('#search_clear').click(function (){
        $("#searchWorkCode").combobox('setValue','');
        $("#searchDirector").combobox('setValue','');
        $('#searchDept').combobox('setValue','');
        $("#main_dg").datagrid({
            queryParams: {
                factory_id: '',
            },
        });
        $('#main_dg').datagrid('loadData',[]);
    });


    filter_work_code_options()

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
        data['trans_type'] = data.trans_type_id;
        delete data.trans_type_id;

        $.ajax({
        type :"post",
        url :formSourceUrl,
        data :data,
        async :false,                 //同步 : 收到伺服器端的 response 之後才會繼續下一步的動作，等待的期間無法處理其他事情。
        success :function(res){
                if (res.success) {
                    alert('新增成功!');
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['work_code'];
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
        // comboboxSourceUrl = "/api/get_employee_data_factory/"+currentFactory;
        comboboxSourceUrl = "/api/get_employee_data_factory";
        $.get(
            comboboxSourceUrl,
            function (res) {
                if (res) {
                    optionTxt = res;
                    $("#copyFrom_id").combobox({
                    valueField:'value',
                    textField:'text',
                    data: optionTxt,
                            });

                    $('#copy_dd').attr('hidden',false);

                    $('#copy_dd').dialog({
                        title: '請選取要複製的工號',
                        width: 500,
                        height: 'auto',
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
        centerControl('update');
        $('#main_dg').datagrid('reload');
        $('#import_btn').show();
        $('#copy_btn').show();
    });


    $('#update_btn').click(function(){
        // 更新
        if(!formValidate(main_form)) return;
        var data = getFormData(main_form);
        data['trans_type'] = data.trans_type_id;
        delete data.trans_type_id;
        $.post(
            formSourceUrl + '/' + currentKey,
            data,
            function(res) {
                if(res.success) {
                    alert('更新成功!')
                    $('#main_dg').datagrid('reload');
                    idFieldValue = data['work_code'];
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
        if (!confirm('刪除的員工若為主管,下屬的『直接主管』將清空\n請確認您要刪除\n再按下『確定』')) return;
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




