// member_admin.js
var $ = django.jQuery;

$(function(){

$('#id_payment_type').show(function(){
  if(this.value==="SEPA") {
    show_iban_fields();
  } else {
    hide_iban_fields();
  }
});

$('#id_payment_type').change(function(){
  if(this.value==="SEPA") {
    show_iban_fields();
  } else {
    hide_iban_fields();
  }
});

function show_iban_fields() {
    $('.field-iban').show();
    $('.field-bic').show();
    $('.field-iban_fullname').show();
    $('.field-iban_address').show();
    $('.field-iban_zip_code').show();
    $('.field-iban_city').show();
    $('.field-iban_country').show();
}

function hide_iban_fields() {
    $('.field-iban').hide();
    $('.field-bic').hide();
    $('.field-iban_fullname').hide();
    $('.field-iban_address').hide();
    $('.field-iban_zip_code').hide();
    $('.field-iban_city').hide();
    $('.field-iban_country').hide();
}

});
