from babosiki.models import Account, Operation

def global_data(request):
    accounts = Account.objects.filter(user=request.user, calculated=True)

    total_sum = 0
    for account in accounts:
        total_sum += account.initial_balance*account.type
        operations = Operation.objects.filter(account=account)

        for operation in operations:
            total_sum += operation.value*operation.type
        
    

    return {'all_accounts': Account.objects.all(),
            'total': total_sum}