from babosiki.models import Account, Operation

def global_data(request):
    try:
        accounts = Account.objects.filter(user=request.user, calculated=True)

        total_sum = 0
        for account in accounts:
            if account.type == Account.DEBIT:
                total_sum += account.initial_balance
            operations = Operation.objects.filter(account=account)

            for operation in operations:
                total_sum += operation.value*operation.type
            
        

        return {'accounts': Account.objects.all(),
                'total_money': total_sum}
    except TypeError:
        return {}