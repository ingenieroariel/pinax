from datetime import datetime
from math import log

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import connection

from voting.models import Vote

register = template.Library()

def do_order_by_reddit(parser, token):
    split = token.split_contents()
    if len(split) == 3:
        return OrderByRedditNode(*split[1:])
    else:
        raise template.TemplateSyntaxError('%r tag takes one argument.' % split[0])

class OrderByRedditNode(template.Node):
    def __init__(self, queryset_var, date_var):
        self.queryset_var = template.Variable(queryset_var)
        self.date_var = date_var
    
    def render(self, context):
        key = self.queryset_var.var
        values = self.queryset_var.resolve(context)
        votes = Vote.objects.get_scores_in_bulk(values)
        ratings = []
        for obj in values:
            age = (getattr(obj, self.date_var) - datetime(2005, 12, 8, 7, 46, 43)).seconds
            obj_votes = votes[obj.id]['score']
            if obj_votes > 0:
                y = 1
            elif obj_votes < 0:
                y = -1
            else:
                y = 0
            z = max(abs(obj_votes), 1)
            
            rating = log(z, 10) + (y * age) / 45000
            ratings.append((rating, obj))
        ratings.sort(cmp=lambda x, y: y[0] - x[0])
        by_score = [x[1] for x in ratings]
        

        context[key] = by_score
        return u""

register.tag('order_by_reddit', do_order_by_reddit)
