// member_admin.js
var $ = django.jQuery;

$(function(){

$('#id_payment_type').show(function(){
  if(this.value==="SEPA") {
    iban_fields().show();
  } else {
    iban_fields().hide();
  }
});

$('#id_payment_type').change(function(){
  if(this.value==="SEPA") {
    iban_fields().show();
  } else {
    iban_fields().hide();
  }
});

function iban_fields() {
    return $('.field-iban, .field-bic, .field-iban_fullname, .field-iban_address, .field-iban_zip_code, .field-iban_city, .field-iban_country, .field-iban_issue_date');
}

});
