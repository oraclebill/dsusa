from django import template
from datetime import datetime, timedelta
from dsprovider.ordermgr.models import DesignOrder

register = template.Library()


@register.inclusion_tag("designer/order_stats.html")
def order_stats():
    today = datetime.today()
    monday = today - timedelta(datetime.weekday(today))
    sunday = monday + timedelta(6)

    def stats(field, qs=None):
        """
        Stats for today, week, and month.
        """
        qs = qs or DesignOrder.objects.all()
        return (
            qs.filter(**{
                field: datetime.today,
            }).count(),

            qs.filter(**{
                '%s__range' % field: (monday, sunday)
            }).count(),

            qs.filter(**{
                '%s__month' % field: today.month,
                '%s__year' % field: today.year,
            }).count(),
        )

    return {
        'headers': ('Today', 'This Week', 'This Month'),
        'arrived': stats('arrived'),
        'completed': stats('completed'),
    }
