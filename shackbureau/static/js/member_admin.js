// member_admin.js
var $ = django.jQuery;

$(function(){
//hide iban fields
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

//hide leave fields
$('#id_is_active').show(function(){
  if(this.checked) {
    leave_fields().hide();
  } else {
    leave_fields().show();
  }
});

$('#id_is_active').change(function(){
  if(this.checked) {
    leave_fields().hide();
  } else {
    leave_fields().show();
  }
});

function leave_fields() {
  return $('.field-leave_date, .field-is_cancellation_confirmed');
}

//hide additionals_fields
$('#id_show_additional_information').show(function(){
  if(this.checked) {
    additional_fields().show();
  } else {
    additional_fields().hide();
  }
});

$('#id_show_additional_information').change(function(){
  if(this.checked) {
    additional_fields().show();
  } else {
    additional_fields().hide();
  }
});

function additional_fields() {
  return $('.field-member_id, .field-copy_paste_information, .field-modified, .field-created, .field-created_by, .field-is_registration_to_mailinglists_sent, .field-is_welcome_mail_sent, .field-is_payment_instruction_sent, .field-is_cancellation_mail_sent_to_cashmaster, .field-is_revoke_memberspecials_mail_sent');
}

});


function copyMemberAddressInSepa() {
  id_iban_fullname.value = id_name.value + " " + id_surname.value;
  id_iban_address.value = id_address1.value;
  id_iban_zip_code.value = id_zip_code.value;
  id_iban_city.value = id_city.value;
  id_iban_country.value = id_country.value;
}
