// member_admin.js
var $ = django.jQuery;

$(function(){
$('#id_is_stored_by_account').show(function(){
  if(this.checked) {
    transaction_fields().hide();
    account_fields().show();
  } else {
    transaction_fields().show();
    account_fields().hide();
  }
});

$('#id_is_stored_by_account').change(function(){
  if(this.checked) {
    transaction_fields().hide();
    account_fields().show();
  } else {
    transaction_fields().show();
    account_fields().hide();
  }
});

function transaction_fields() {
  return $('.field-transaction_coin_001, .field-transaction_coin_002, .field-transaction_coin_005, .field-transaction_coin_010, .field-transaction_coin_020, .field-transaction_coin_050, .field-transaction_coin_100, .field-transaction_coin_200, .field-transaction_bill_005, .field-transaction_bill_010, .field-transaction_bill_020, .field-transaction_bill_050, .field-transaction_bill_100, .field-transaction_bill_200, .field-transaction_bill_500');
}

function account_fields() {
  return $('.field-account_coin_001, .field-account_coin_002, .field-account_coin_005, .field-account_coin_010, .field-account_coin_020, .field-account_coin_050, .field-account_coin_100, .field-account_coin_200, .field-account_bill_005, .field-account_bill_010, .field-account_bill_020, .field-account_bill_050, .field-account_bill_100, .field-account_bill_200, .field-account_bill_500');
}
});

