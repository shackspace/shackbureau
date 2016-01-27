// memberspecials_admin.js
var $ = django.jQuery;

$(function(){

$('#id_is_keyholder').show(function(){
  if(this.checked) {
    ssh_key_fields().show();
  } else {
    ssh_key_fields().hide();
  }
});

$('#id_is_keyholder').change(function(){
  this.value
  if(this.checked) {
    ssh_key_fields().show();
  } else {
    ssh_key_fields().hide();
  }
});

function ssh_key_fields() {
    return $('.field-ssh_public_key');
}

});
