$(document).ready(function(){
    var dlg = $('.dlg');
    dlg.each(function(){
        var self = $(this);
        var dlgID = self.prop('id');
        var triggerBtn = $(self.data().trigger);
        if(window.hasOwnProperty('config') && config.hasOwnProperty(dlgID)) {
            var conf = config[dlgID];
            $(this).dialog(conf);
        } else {
            conf = {
                closed: true,
            }
            $(this).dialog(conf);
        }
        triggerBtn.click(function(){
            self.dialog('open');
        });
    });
});