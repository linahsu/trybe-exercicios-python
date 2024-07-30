from django.contrib import admin
from budget.models import Vendor, Marriage, Budget

# Colocar um modelo inline com o outro significa ser capaz de criar as duas
# entidades na mesma tela! Nesse caso, estamos configurando o painel de
# admin para que permita a criação de um Budget dentro da tela de criação
# de Marriage. Note que, para isso, definimos duas classes: uma herdou de
# admin.StackedInline e definiu um atributo model com o model a ficar inline
# e a outra definiu um atributo inlines, recebendo numa lista a classe
# anterior. Efetue as alterações e veja como tudo já funciona.


class BudgetInline(admin.StackedInline):
    model = Budget


class MarriageAdmin(admin.ModelAdmin):
    inlines = [BudgetInline]


admin.site.site_header = 'Weddings Manager Admin Panel'
admin.site.register(Vendor)
admin.site.register(Marriage, MarriageAdmin)
