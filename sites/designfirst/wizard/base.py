'''
Base class for wizard views
'''
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from models import WorkingOrder
from django.template.defaultfilters import capfirst
from django.core.urlresolvers import reverse


class WizardBase(object):
    
    def __call__(self, request, id, step):
        self.order = get_object_or_404(WorkingOrder, id=id)
        if step is None:
            step = self.steps[0]
        self.step = step
        
        result = self.dispatch(request)
        if isinstance(result, HttpResponse):
            return result
        
        template = 'wizard/%s.html' % self.step
        context = {'wizard': self}
        if isinstance(result, (list, tuple)):
            result, template = result
        context.update(result)
        
        return render_to_response((template, 'wizard/form.html'), 
                                  context, RequestContext(request))
    
    def dispatch(self, request):
        method = 'step_%s' % self.step
        if not hasattr(self, method):
            raise Http404('"%s" method not exist' % method)
        self.method = getattr(self, method)
        
        return self.method(request)
    
    def handle_form(self, request, FormClass, extra_context={}):
        if request.method == 'POST':
            form = FormClass(request.POST, instance=self.order)
            if form.is_valid():
                form.save()
                return self.next_step()
        else:
            form = FormClass(instance=self.order)
        context = {'form':form}
        context.update(extra_context)
        return context
    
    def get_tabs(self):
        """
        Returns iterator if tab items(icon+text on top of wizard)
        """
        for step in self.steps:
            yield {
                'title': capfirst(' '.join(step.split('_'))),
                'url': reverse('order-wizard-step', args=[self.order.id, step]),
                'selected': self.step == step,
                'slug': step,
            }
    
    def next_step(self):
        next = self.steps.index(self.step) + 1
        return self.go_to_step(self.steps[next])
    
    
    def go_to_step(self, step):
        return HttpResponseRedirect(reverse('order-wizard-step', args=[self.order.id, step]))
    
    def step_title(self):
        if hasattr(self.method, 'title'):
            return self.method.title
        return capfirst(' '.join(self.step.split('_')))
    
    def _get_summary(self, summary_fields):
        result = []
        for name, list in summary_fields:
            values = []
            for field in list:
                item_name = WorkingOrder._meta.get_field(field).verbose_name
                if hasattr(self.order, 'get_%s_display' % field):
                    item_value = getattr(self.order, 'get_%s_display' % field)()
                else:
                    item_value = getattr(self.order, field)
                values.append((item_name,item_value))
            result.append((name, values))
        return result