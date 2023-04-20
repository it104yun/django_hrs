$(document).ready(function(){
    //dlg
    var dlg_mono_dg= $('.dlg_mono_dg');
    dlg_mono_dg.each(function(){
        var dlg = $(this);
        var dlgID = dlg.prop('id')
        var searchBtn = dlg_mono_dg.find('.btn-search');
        var confirmBtn = dlg_mono_dg.find('.btn-confirm');
        var triggerBtn = $(dlg.data().trigger);
        var dlg_mono_dgRow = null;
        var form = dlg_mono_dg.find('form');
        //dg
        var dg = dlg_mono_dg.find('.dg');
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
            dlg_mono_dgRow = row;
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
            theDlgConfig['confirmHandler'](dlg_mono_dgRow);
        });
    });
});
