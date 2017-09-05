
def deduplicate_transactions(year):
    attribs = ['member', 'amount', 'due_date', 'transaction_type', 'booking_type', 'payment_reference']
    for member in Member.objects.all():
        to_be_deleted = []
        qs = member.accounttransaction_set.filter(due_date__year=year, booking_type='deposit')
        for transaction in qs.all():
            if qs.filter(**{a: getattr(transaction, a) for a in attribs}).exclude(id__in=[b.id for b in to_be_deleted + [transaction]]).exists():
                to_be_deleted.append(transaction)
        [t.delete() for t in to_be_deleted]
