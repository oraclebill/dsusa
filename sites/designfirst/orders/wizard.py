'''
Base class for wizard views
'''
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.template.context import RequestContext
from django.template.defaultfilters import capfirst
from django.core.urlresolvers import reverse

from models import WorkingOrder, RequestNotation

BTN_SAVENEXT = '_savenext_'

NEXT_STEP_VAR = 'next_step_'
GO_NEXT = '_next_'
GO_PREVIOUS = '_prev_'


class WizardBase(object):
    
    def __call__(self, request, id, step, complete):
        self.order = get_object_or_404(WorkingOrder, id=id)
        self.request = request
        
        #Permission check
        if self.order.owner.id != request.user.id and not request.user.is_staff:
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
            'BTN_PREVIOUS': GO_PREVIOUS,
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
        note_text = self.get_page_note()
        if request.method == 'POST':
            form = FormClass(request.POST, instance=self.order)
            if form.is_valid():
                if self.order.status == WorkingOrder.Const.DEALER_EDIT:
                    form.save()
                    new_note_text = request.POST.get('section_notes', '')
                    if not note_text == new_note_text:
                        self.set_page_note(request.user.id, new_note_text)
                    self.order.finish_step(self.step)
                return self.dispatch_next_step()
        else:
            form = FormClass(instance=self.order)
        
        context = { 
            'form': form, 
            'section_notes': note_text 
        }
        context.update(extra_context)
        return context
    
    def get_page_note(self):
        note_text = ''
        try:
            note_text = self.order.notes.filter(area_reference=self.step).latest('id').note_text
        except:
            pass
        return note_text

    def set_page_note(self, authorid, note_text):
        section_note, created = self.order.notes.get_or_create(area_reference=self.step, 
                                       defaults={ 'author_id': authorid })
        section_note.note_text = note_text
        section_note.save()   
        
        
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
        if GO_PREVIOUS in self.request.POST:
            step = self.previous_step()
        elif step == GO_NEXT:
            step = self.next_step()
        elif step == GO_PREVIOUS:       # TODO: broken
            step = self.previous_step()
        if step is None:
            return self.complete(self.request)
        return self.go_to_step(step)
    
    
    def next_step(self):
        next = self.steps.index(self.step) + 1
        if next >= len(self.steps):
            return None
        return self.steps[next]
    
    def previous_step(self):
        previous = self.steps.index(self.step) - 1
        print 2, 'previous step = %d' % previous
        if previous < 0:
            return None
        return self.steps[previous]
    
    def is_first_step(self):
        return self.steps.index(self.step) == 0
    
    def is_last_step(self):
        return self.steps.index(self.step) == len(self.steps)-1
    
    def is_valid_order(self):
        return self.order.is_complete()
    
    def go_to_step(self, step):
        return HttpResponseRedirect(reverse('order-wizard-step', args=[self.order.id, step]))
    
    def step_title(self):
        if hasattr(self.method, 'title'):
            return self.method.title
        return capfirst(' '.join(self.step.split('_')))
    
