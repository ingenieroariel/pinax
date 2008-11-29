from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required

from groups.models import Group
from groups.forms import CreateGroupForm

def group_list(request, group_type, group_config):
    
    if group_type not in group_config:
        raise Http404
    
    template_name = group_config[group_type].get("list_template_name", "groups/group_list.html")
    form_class = group_config[group_type].get("create_group_form", CreateGroupForm)
    
    groups = Group.objects.filter(group_type=group_type)
    
    group_form = form_class()
    
    return render_to_response(template_name, {
        "groups": groups.order_by("-created"),
        "group_form": group_form,
    }, context_instance=RequestContext(request))


def group_create(request, group_type, group_config):
    
    if group_type not in group_config:
        raise Http404
    
    template_name = group_config[group_type].get("create_template_name", "groups/group_create.html")
    form_class = group_config[group_type].get("create_group_form", CreateGroupForm)
    
    if request.method == "POST":
        group_form = form_class(request.POST)
        if group_form.is_valid():
            group = group_form.save(commit=False)
            group.creator = request.user
            group.group_type = group_type
            group.save()
            group.members.add(request.user)
            group.save()
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        group_form = form_class()
    
    return render_to_response(template_name, {
        "group_form": group_form,
    }, context_instance=RequestContext(request))
group_create = login_required(group_create)


def your_groups(request, group_type, group_config):
    pass # @@@


def group_detail(request, group_type, slug, group_config):
    
    group = get_object_or_404(Group, slug=slug, group_type=group_type)
    
    if group.deleted:
        raise Http404
    
    template_name = group_config[group_type].get("detail_template_name", "groups/group_detail.html")
    
    # @@@ update, join and leave forms TODO
    
    # @@@ are_member = request.user in tribe.members.all()
    
    return render_to_response(template_name, {
        "group": group,
    }, context_instance=RequestContext(request))
