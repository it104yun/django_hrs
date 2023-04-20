function formValidate(form) {
    clearError();
    var fields = form.elements;
    var checkFlag = true;
    for(var i = 0; i < fields.length; i++) {
        var field = fields[i];
        var fieldName = field.name;
        if(field.required && field.type === 'select-one') {
            if(field.value==undefined||field.value=='') {
                $("#" + field.id).toggleClass('error');
                checkFlag = false;
            }
        }
        else if(field.required && field.type === 'checkbox') {
            var checkedNum = $('[name='+ field.name + ']:checked').length;
            if(checkedNum == 0) {
                $("#div_id_" + field.name).toggleClass('error');
                checkFlag = false;
            }
        }
        else if(field.required && field.type === 'radio') {
            var checkedVal = $('input[name='+fieldName+']:checked').val();
            if (checkedVal==undefined) {
                $('#div_id_' + field.name).toggleClass('error');
                checkFlag = false;
            }
        }
        else {
            if (field.required && (field.value==undefined || field.value=='')) {
                $('#' + field.id).toggleClass('error');
                checkFlag = false;
            }
        }
    }
    return checkFlag;
}

function getFormData(form) {
    var formData = {};
    var fields = form.elements;
    for(var i = 0; i < fields.length; i++) {
        field = fields[i];
        fieldName = field.name;
        if(field.type === 'select-one') {
            formData[fieldName + '_id'] = field.value;
            if(field.selectedOptions.length) {
                formData[fieldName] = field.selectedOptions[0].innerText || '';
            }
        }
        else if(field.type === 'checkbox') {
            formData[fieldName] = field.checked;
        }
        else if(field.type === 'radio') {
            var checkedVal = $('input[name='+fieldName+']:checked').val();
            formData[fieldName + '_id'] = checkedVal;
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
        if(row[fieldName] == undefined) continue;
        if(field.tagName === 'SELECT') {
            val = row[fieldName + '_id'] || row[fieldName];
            if(field.options.length == 0) {
                field.innerHTML = '<option>' + val + '</option>';
            } else {
                field.value = val;
            }
        }
        else if(field.type === 'checkbox') {
            field.checked = row[fieldName];
        }
        else if(field.type === 'radio') {
            form[field.name].value = row[fieldName + '_id'] || row[fieldName];
        }
        else {
            fields[i].value = row[fieldName];
        }
    }
}

function buttonControl(nb, cb, cnb, ub, db) {
    $("#new_btn").css('display', nb);
    $("#create_btn").css('display', cb);
    $("#cancel_btn").css('display', cnb);
    $("#update_btn").css('display', ub);
    $("#delete_btn").css('display', db);
}

function resetForm(form) {
    $('#' + form.id).form('reset');
    clearError();
}

function clearError() {
    var allError = $('.error');
    for(errrr of allError) {
        $(errrr).toggleClass('error');
    }
}


