'''
Base class for wizard views
'''
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.template.context import RequestContext
from models import WorkingOrder
from django.template.defaultfilters import capfirst
from django.core.urlresolvers import reverse


BTN_SAVENEXT = '_savenext_'

NEXT_STEP_VAR = 'next_step_'
GO_NEXT = '_next_'
GO_PREVIOUS = '_prev_'


class WizardBase(object):
    
    def __call__(self, request, id, step, complete):
        self.order = get_object_or_404(WorkingOrder, id=id)
        self.request = request
        
        #Permission check
        if self.order.owner.id != request.user.id:
            return HttpResponseForbidden("Not allowed to update this order")
        
        if complete:
            return self.complete(request)
        if step is None:
            step = self.steps[0]
        self.step = step
        
        result = self.dispatch(request)
        if isinstance(result, HttpResponse):
            return result
        
        template = 'wizard/step_%s.html' % self.step
        context = {
            'wizard': self,
            'BTN_SAVENEXT': BTN_SAVENEXT
        }
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
                self.order.finish_step(self.step, commit=True)
                return self.dispatch_next_step()
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
    
    def dispatch_next_step(self):
        assert self.request.method == 'POST', 'dispatch_next_step works only with POST'
        step = self.request.POST[NEXT_STEP_VAR]
        assert step is not None
        if step == GO_NEXT:
            step = self.next_step()
        elif step == GO_PREVIOUS:
            step = self.previous_step()
        if step is None:
            return HttpResponseRedirect(reverse(
                        'order-wizard-complete', args=[self.order.id]))
        return self.go_to_step(step)
    
    
    def next_step(self):
        next = self.steps.index(self.step) + 1
        if next >= len(self.steps):
            return None
        return self.steps[next]
    
    def previous_step(self):
        previous = self.steps.index(self.step) - 1
        if previous < 0:
            return None
        return self.steps[previous]
    
    def is_first_step(self):
        return self.steps.index(self.step) == 0
    
    def go_to_step(self, step):
        return HttpResponseRedirect(reverse('order-wizard-step', args=[self.order.id, step]))
    
    def step_title(self):
        if hasattr(self.method, 'title'):
            return self.method.title
        return capfirst(' '.join(self.step.split('_')))
    
