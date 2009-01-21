from django.shortcuts import render_to_response
from django.db.models import Q 

#blog,tribes,projects
from blog.models import Post
from tribes.models import Tribe
from profiles.models import Profile

OBJ_REFERENCES = {
    'Post': {
            'obj_title':'title',
            'obj_description':'tease'        
        },
        
    'Tribe': {
        'obj_title':'name',
        'obj_description':'description'        
        },
        
    'Profile': {
        'obj_title':'name',
        'obj_description':'about'
    }
    
}

def set_obj_info(objects,model_type):
    results = []
    for obj in objects:
        obj.model_type = model_type
        obj_definition = OBJ_REFERENCES[model_type]
        obj.obj_title = getattr(obj,obj_definition['obj_title'],'title fail')
        obj.obj_description = getattr(obj,obj_definition['obj_description'],'title fail')        
        results.append(obj)
    return results

def search_form(request):
    query = request.GET.get('q', '') 
    qset = u''
    results = []

    if query:    
        # Handle blogs
        qset = ( 
        Q(title__icontains=query) | 
        Q(body__icontains=query) | 
        Q(tease__icontains=query) 
        )   
        results += set_obj_info(Post.objects.filter(qset).distinct(),'Post')
        
        # Handle tribes
        qset = (
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        results += set_obj_info(Tribe.objects.filter(qset).distinct(),'Tribe')
        
        # Handle profiles
        qset = (
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(job_description__icontains=query) |
            Q(work_done__icontains=query) |
            Q(work_doing_now__icontains=query) |
            Q(awards__icontains=query) |                            
            Q(certifications__icontains=query) |
            Q(about__icontains=query)|
            Q(tags__icontains=query)            
        ) 
        results += set_obj_info(Profile.objects.filter(qset).distinct(),'Profile')        
        
    return render_to_response('search.html',
            {"query": query,
            "results":results,
            "dump":qset}
        )
  
