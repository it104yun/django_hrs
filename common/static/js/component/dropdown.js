$('#primary_dropdown').change(function(){
	var value = $(this).val();
	$('#primary_selected').text(value);
	$.ajax({
		url: "{% url 'dynamic_dropdowns' %}",
		method: 'post',
		data: {
			'query': value
		},
		success: function(res){
			var response = JSON.parse(res);
			var optionList = response.map(function(item){
				return '<option value=' + item.pk + '>' + item.fields.name + '</option>';
			});
			$('#secondary_dropdown').html('<option></option>').append(optionList.join(''));
		}
	})
});

// set request parameters
$('#secondary_dropdown').change(function(){
	queryStrings = [];
	// get all select names and values
	$('select').each(function(){
		var self = $(this);
		queryStrings.push(self.prop('name') + '=' + self.val()); 
	})
	// append the query parameters 
	window.location = '?' + queryStrings.join('&');
});