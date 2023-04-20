$(document).ready(function(){
    var dg = $('.dg');
    dg.each(function(){
        var self = $(this);
        var dgId = self.attr('id');
        if(!(window.hasOwnProperty('config') && config[dgId])) return;
        config[dgId]['url'] = self.data().source;
        config[dgId]['idField'] = self.data().key;
        $(this).datagrid(config[dgId]);
    });
});

