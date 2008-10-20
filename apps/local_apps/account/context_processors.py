
from account.models import Account, AnonymousAccount

def openid(request):
    return {'openid': request.openid}

def account(request):
    account = AnonymousAccount(request)
    if request.user.is_authenticated():
        try:
            account = Account._default_manager.get(user=request.user)
        except (Account.DoesNotExist, Account.MultipleObjectsReturned):
            account = None
    return {'account': account}
