from django.conf import settings

from account.models import Account, AnonymousAccount

def openid(request):
    return {'openid': request.openid}

def account(request):
    if request.user.is_authenticated():
        try:
            account = Account._default_manager.get(user=request.user)
        except Account.DoesNotExist:
            account = AnonymousAccount(request)
    else:
        account = AnonymousAccount(request)
    return {'account': account}

def account_settings(request):
    return {
        'account_supports_openid': settings.ACCOUNT_SUPPORTS_OPENID,
        'account_allow_signup': settings.ACCOUNT_ALLOW_SIGNUP,
    }