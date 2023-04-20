$(document).ready(function(){
    //dlg
    var dlg_dg= $('.dlg_dg');
    dlg_dg.each(function(){
        var dlg = $(this);
        var dlgID = dlg.prop('id')
        var triggerBtn = $(dlg.data().trigger);
        var form = dlg_dg.find('form');
        //dg
        var dg = dlg_dg.find('.dg');
        var source = dg.data().source;
        //
        if(!(window.hasOwnProperty('config') && config.hasOwnProperty(dlgID))) return;
        else {
            var theDlgConfig = config[dlgID]['dlg'];
            var theDgConfig = config[dlgID]['dg'];
        }
        triggerBtn.click(function(){
            dlg.dialog('open');
        });
        theDgConfig['onSelect'] = function (index, row) {
            dlg_dgRow = row;
        }
        theDgConfig['url'] = source;

        if(!theDlgConfig.hasOwnProperty('onOpen')) {
            config[dlgID]['onOpen'] = function () {
                $(this).dialog('resize');
            }
        }
        dlg.dialog(theDlgConfig);
        dg.datagrid(theDgConfig);

        searchBtn.click(function(){
            form.submit(false);
            var conditions = form.serialize();
            var url = source + '?' + conditions;
            dg.datagrid({
                url: url,
            })
        });
        confirmBtn.click(function(){
            theDlgConfig['confirmHandler'](dlg_dgRow);
        });
    });
});
