/*
自定義表單載入

*/
$.extend($.fn.form.methods, {
	load2: function(jq, source){
		return jq.each(function(){
			var target = this;
			var opts = $(target).data('form').options;
			if (typeof source == 'string'){
				var param = {};
				if (opts.onBeforeLoad.call(target, param) == false) return;

				$.ajax({
					url: source,
					data: param,
					dataType: 'json',
					success: function(res){
						// 不需要以下資料
						if(!res.length) return;
						if(res[0].operator == null) {
							delete res[0]['operator'];
							delete res[0]['section_manager'];
							delete res[0]['director'];
						}
						_load(res);
					},
					error: function(){
						opts.onLoadError.apply(target, arguments);
					}
				});
			} else {
				_load(source);
			}
			function _load(data){
				if ($.isArray(data)){
					data = data[0];
				}
				$(target).form('load', data);
				// 遇到select可能要讀取 "_id" 結尾的資訊
				$('#main_form select').each(function(){
					var name = $(this).attr('name');
					var value = data[name + '_id'] || data[name];
					if(this.options.length == 0) {
						this.innerHTML = '<option>' + value + '</option>';
					} else {
						this.value = value;
					}
				});
			}
		})
	}
});
