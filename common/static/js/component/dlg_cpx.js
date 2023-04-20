$(document).ready(function(){
    $('.dlg_cpx').each(function() {

        var filterRow = 0;
        var dlg = $(this);
        var dlgID = dlg.prop('id');
        var searchBtn = dlg.find('.search_btn');
        var triggerBtn = $(dlg.data().trigger);
        var filterArea = dlg.find('.filter_area');
        var addFilterBtn = dlg.find('.add_filter_btn');
        var searchForm = dlg.find('form')[0];
        var keyWordField = dlg.find('input[name=keyword]');
        if(window.hasOwnProperty('config') && config.hasOwnProperty(dlgID)) {
            var theDlgConfig = config[dlgID]['dlg'];
            var theSearchConfig = config[dlgID]['search'];
            $(this).dialog(theDlgConfig);
        } else {
            $(this).dialog();
        }
        searchBtn.hide();
        triggerBtn.click(function () {
            dlg.dialog('open');
        });
        filterArea.on('click', '.del', function () {
            $(this).parents('.row').remove();
            if (!--filterRow) {
                searchBtn.hide();
            }
        });
        searchBtn.click(function () {
            if (!filterRow) return;
            var queryData = {
                'filter': {},
                'logic': null,
            }
            filterArea.find('.row').each(function (id, row) {
                var elements = row.children
                queryData['filter'][id] = {
                    'field': elements[0].dataset.value,
                    'relation': elements[1].dataset.value,
                    'value': elements[2].dataset.value
                };
            });
            queryData['logic'] = searchForm.logic.value;
            var url = theSearchConfig.hasOwnProperty('url') ? theSearchConfig.url : searchForm.action;
            $.post(
                url,
                data = {'data': JSON.stringify(queryData)},
                function (res) {
                    theSearchConfig.afterSearch(res);
                }
            );
        });
        addFilterBtn.click(function () {
            addRow()
        });
        keyWordField.keypress(function (e) {
            if (e.keyCode == 13) {
                addFilterBtn.click();
            }
        });
        function addRow(){
            var field_val = searchForm.field.value;
            var field_txt = searchForm.field.selectedOptions[0].text;
            var relation_val = searchForm.relation.value;
            var relation_txt = searchForm.relation.selectedOptions[0].text;
            var value_val = searchForm.keyword.value;
            filterArea.append(
                '<div class="d-flex row col-12 p-1 text-center">'
                + '<div class="col-3 p-1 border mr-1 field" data-value="' + field_val + '">' + field_txt + '</div>'
                + '<div class="col-2 p-1 border mr-1 relation" data-value="' + relation_val + '">' + relation_txt + '</div>'
                + '<div class="col-5 p-1 border mr-1 value"  data-value="' + value_val + '">' + value_val + '</div>'
                + '<button class="del col-1 btn btn-sm">移除</button>'
                + '</div>');
            if(++filterRow) searchBtn.show();
        }
    });
});
