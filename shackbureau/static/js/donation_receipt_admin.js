// member_admin.js
var $ = django.jQuery;

$(function(){
//hide iban fields
$('#id_donation_type').show(function(){
  if(this.value==="benefits") {
    benefits_fields().show();
    allowance_in_money_fields().hide();
  } else {
    benefits_fields().hide();
    allowance_in_money_fields().show();
  }
});

$('#id_donation_type').change(function(){
  if(this.value==="benefits") {
    benefits_fields().show();
    allowance_in_money_fields().hide();
  } else {
    benefits_fields().hide();
    allowance_in_money_fields().show();
  }
});

function benefits_fields() {
  return $('.field-description_of_benefits, .field-is_from_business_assets, .field-is_from_private_assets, .field-no_information_about_origin, .field-has_documents_of_value');
}

function allowance_in_money_fields() {
  return $('.field-is_waive_of_charge');
}

});

