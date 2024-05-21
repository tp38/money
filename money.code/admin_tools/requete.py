from banks.models import Operation
from management.models import HashTag
from django.db.models import Sum
from django.db.models import Q
# Tous les comptes
amount_sum=Sum( 'operations__amount', filter=Q(operations__value_date__gte='2023-01-27') & Q(operations__value_date__lte='2023-02-27') )
# BP cpt joint
#amount_sum=Sum( 'operations__amount', filter=Q(operations__value_date__gte='2023-01-27') & Q(operations__value_date__lte='2023-02-27') & Q(operations__paymedia__in=[5, 6, 19]) )
# BSA Ty
#amount_sum=Sum( 'operations__amount', filter=Q(operations__value_date__gte='2023-01-27') & Q(operations__value_date__lte='2023-02-27') & Q(operations__paymedia__in=[22, 23, 24]) )
# BSA Nat
#amount_sum=Sum( 'operations__amount', filter=Q(operations__value_date__gte='2023-01-27') & Q(operations__value_date__lte='2023-02-27') & Q(operations__paymedia__in=[25, 26, 27]) )


qs = HashTag.objects.all().annotate(amount_sum=amount_sum).order_by('word')

for h in qs :
  if not h.amount_sum == None :
    print( f"{h.word} : {h.amount_sum}" )

# Résultats dans fichier Calc sous /home/th/Famille/Documents/Banque
