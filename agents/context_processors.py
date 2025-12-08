# agents/context_processors.py
def agent_context(request):
    """Context processor pour les templates agents"""
    context = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'agent'):
        context['current_agent'] = request.user.agent
        context['is_agent'] = True
    else:
        context['is_agent'] = False
        
    return context