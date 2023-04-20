$(document).ready(function(){
    $('.tree').each(function(){
        var treeID= $(this).prop('id');
        if(!(window.hasOwnProperty('config') && config.hasOwnProperty(treeID))) return;
        var theConfig = config[treeID];
        theConfig['url'] = $(this).data().url;
        $(this).tree(theConfig);
    });
});