from ajax_select import register, LookupChannel
from django.db.models import Q

from .models import Member


@register('member')
class MemberLookup(LookupChannel):

    model = Member

    def get_query(self, q, request):
        query_set = self.model.objects.all()
        for element in q.split():
            q_object = (Q(nickname__icontains=element) |
                        Q(name__icontains=element) |
                        Q(surname__icontains=element)
                        )
            try:
                q_object = q_object | Q(member_id=int(q))
            except ValueError:
                pass
            query_set = query_set.filter(q_object)
        return query_set[:50]
