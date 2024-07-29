# Vinculando Tabelas

<details>
<summary><strong> No Painel Admin </strong></summary>

 Não dá pra criar Marriage sem ter um Budget. No entanto, não podemos criar um Budget com antecedência e vinculá-lo ao Marriage ao criá-lo, porque o Budget também precisa obrigatoriamente de um Marriage! O painel de admin não sabe lidar com isso - e nossas requisições de API também não saberão. Vamos corrigir o problema? Altere o arquivo budget/admin.py:

```bash
# budget/admin.py

from django.contrib import admin
from .models import Vendor, Budget, Marriage


class BudgetInline(admin.StackedInline):
    model = Budget


class MarriageAdmin(admin.ModelAdmin):
    inlines = [BudgetInline]


admin.site.register(Vendor)
admin.site.register(Marriage, MarriageAdmin)
```

Colocar um modelo inline com o outro significa ser capaz de criar as duas entidades na mesma tela! Nesse caso, estamos configurando o painel de admin para que permita a criação de um Budget dentro da tela de criação de Marriage. Note que, para isso, definimos duas classes: uma herdou de admin.StackedInline e definiu um atributo model com o model a ficar inline e a outra definiu um atributo inlines, recebendo numa lista a classe anterior. Efetue as alterações e veja como tudo já funciona.

</details>
</br>

<details>
<summary><strong> Na API do DRF </strong></summary>

Você verá que estamos com o mesmo problema que vimos antes no painel de admin: até conseguimos, no corpo de uma mesma requisição, inserir dados de Marriage e Budget para criar ambos ao mesmo tempo, mas Budget insiste em dar erro se não receber o id de uma entidade de Marriage. O problema é que esse id, no momento em que fazemos a requisição, não existe, pois estamos criando as duas entidades ao mesmo tempo. Mas o serializer de Budget é categórico: sem id o modelo disparará um erro.

O que fazer?

## Configurando serializers para criar entidades com relação 1:1

Lembre-se de como o Django REST Framework funciona. O model é a nossa interface com o banco de dados, respeitando todas as suas restrições de integridade. Os viewsets, que faremos adiante, são os locais por onde as requisições vem para nossa API. Os serializers são os locais que recebem os dados, os entregam corretamente para os models e, em caso de problema, retornam erros bem formatados, tudo feito pra gente por traz dos panos.

Vendor e Budget tem os serializers que esperamos - uma contato simples e direto com o nosso modelo, sem maiores alterações, para criarmos entidades corretamente. Marriage, por outro lado, precisa ser capaz de receber uma requisição que cria duas entidades ao mesmo tempo. O problema de simplesmente fazer um serializer simples para Marriage - unindo-o com o serializer que já temos para Budget, é que os dois não conseguem funcionar ao mesmo tempo. O serializer de Budget vai disparar um erro sem um Marriage já criado para vincular à sua entidade - e sem um Budget criado, o serializer de Marriage também dispara um erro.

Não podemos simplesmente remover de BudgetSerializer a obrigação pela presença do campo marriage - caso contrário requisições de API diretamente aos endpoints de Budget dispararão erros de integridade do banco, pois precisam do id para serem criadas. A solução é criar um segundo serializer para vincular a Marriage - um sem essa restrição. Nós não iremos conectar esse serializer a nenhum Viewset, então o mundo exterior não conseguirá criar entidades inadequadas. Esse serializer será exclusivo para o vínculo com Marriage. Daí, dentro de Marriage, iremos garantir que o Budget criado junto com ele é criado corretamente. Veja como abaixo:

```bash
# budget/serializers.py


from rest_framework import serializers
from .models import Vendor, Marriage, Budget


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "price"]


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "vendors", "marriage"]


class NestedBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "vendors"]


class MarriageSerializer(serializers.ModelSerializer):
    budget = NestedBudgetSerializer()

    class Meta:
        model = Marriage
        fields = ["id", "codename", "date", "budget"]

    def create(self, validated_data):
        budget_data = validated_data.pop('budget')
        budget_data['marriage'] = Marriage.objects.create(**validated_data)
        BudgetSerializer().create(validated_data=budget_data)
        return budget_data['marriage']
```

Nós sobrescrevemos a função de create do serializer por uma lógica nossa - nós removemos dos dados validados os dados relacionados a Budget, e usamos os dados restantes para criar uma entidade Marriage no banco e atribuir a instância que tal criação retorna ao atributo marriage de budget_data. Em seguida, chamamos diretamente o serializer original de Budget para que crie nossa entidade já vinculada com o Marriage que criamos na linha acima. Por fim, retornamos o Marriage criado, fechando o comportamento esperado pela função create do serializer.

Ter o NestedBudgetSerializer vinculado ao MarriageSerializer lá em cima é importante - caso contrário o MarriageSerializer dispara o erro pela falta do id em Budget antes mesmo de chamar a função create que fizemos, que remedia o problema.

Rode esse código! Entenda como ele funciona, simule os erros. Se acessar as URLs pelo browser e/ou pelo Thunder Client agora poderá validar que já funcionam! Crie algumas entidades pelo painel de admin, pelas rotas, e veja tudo funcionando! Com o processo básico revisado e concluído pro nosso MVP, bora criar nossas autenticações?
</details>
</br>

# Basic Authentication

<details>
<summary><strong> Restringindo acesso a parte das operações C.R.U.D. para admins </strong></summary>

Com a nossa aplicação feita, vamos acrescentar nossa autenticação! Temos duas demandas aqui:

Permitir que só pessoas administradoras possam alterar os dados de fornecedores
Permitir que cada casamento esteja vinculado a uma pessoa usuária - e que cada uma só veja o próprio casamento
Vamos estudar os prós e contras de fazer a autenticação de várias formas ao longo do dia de hoje, mas vamos começar com a mais simples: a BasicAuthentication. Antes de mais nada, garanta que a sua dependência do Django REST Framework esteja na versão 3.12 ou superior. Para checar a versão da sua dependência, execute no ambiente virtual o seguinte comando:

```bash
pip show djangorestframework
```

Se for preciso, atualize a dependência:

```bash
 pip install djangorestframework --upgrade
```

O próximo passo é ir no arquivo marryme/settings.py e acrescentar a seguinte configuração:

```bash
# marryme/settings.py

# ...

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# ...
```

Essa configuração define quais serão, respectivamente, a autenticação e permissão padrão usada pela aplicação. Feito isso, nossa API está fechada e todas as rotas exigem autenticação básica! Vamos testar?

Com o servidor funcionando, faça uma requisição GET para 127.0.0.1:8000/vendors, observe o resultado. Tente também acessar 127.0.0.1:8000/vendors pelo navegador e veja o que aparece.

 janela que surge para se autenticar pelo navegador aparece devido à configuração de autenticação básica que fizemos no settings.py. Caso queira usar um template do DRF para fazer a autenticação, ou até mesmo deixar fazer com que o botão de login apareça na API navegável, você pode fazer essa configuração sugerida na documentação oficial.

Ao passar as credenciais corretas de qualquer pessoa usuária do Django, você conseguirá ter acesso aos dados, seja pelo navegador ou pelo Thunder Client.

Para acrescentar a lógica para somente uma parte administradora lidar com os dados de Fornecedores, primeiro, vamos aos serializers. Não remova os serializers que já existem, só acrescente esse:

```bash
# budget/serializers.py

# ...

class AdminVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_superuser:
            return super().create(validated_data)
        raise serializers.ValidationError("Você não tem permissão para criar fornecedores.")

# ...
```

Neste novo Serializer, estamos substituindo o método create padrão que o Django REST Framework nos fornece para verificar se a parte usuária que está fazendo a requisição é administradora (is_superuser). Se sim, o fornecedor será criado normalmente; caso contrário, uma exceção ValidationError será lançada. Note que a lógica de ter um user vinculado a uma requisição, e um que possui esse atributo is_superuser, é uma lógica que nos é fornecida pelo framework. Por hora, ela basta.

A seguir, vamos alterar o Viewset de fornecedores:

```bash
# budget/views.py


from rest_framework import viewsets
from .models import Vendor, Marriage, Budget
from .serializers import (VendorSerializer,
                          MarriageSerializer,
                          BudgetSerializer,
                          AdminVendorSerializer)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer

# ...
```

qui estamos usando o novo Serializer AdminVendorSerializer apenas para as ações de criação, atualização e remoção de Vendors. Para a ação de leitura, continuamos usando o Serializer padrão VendorSerializer. Note que aqui, também, substituímos a implementação de um método padrão por uma nossa - é o polimorfismo em ação!

Seu servidor já deve estar funcionando com autenticação. Vamos testar? Vá ao Thunder Client testar uma das requisições restritas.

Veja como, por padrão, as requisições já não são acessíveis por qualquer pessoa. Agora acrescente as credenciais do superuser que você criou na aba Auth, opção Basic e veja a diferença!

A maior parte dessa lógica de permissões é a mesma independente ao tipo de autenticação que usamos - mas a inserção das credenciais direto na requisição é uma característica da BasicAuthentication! Você entenderá melhor o que é o que quando implementarmos as outras modalidades de autenticação!
</details>
</br>

<details>
<summary><strong> Restringindo acesso a uma entidade a quem a cria </strong></summary>


Agora, o próximo passo: somente a pessoa que cria um casamento e orçamento poder acessá-lo! Fora, naturalmente admins terem acesso a tudo.

Para implementar a lógica onde um pessoa cadastrada só pode acessar os Casamentos e Orçamentos que ela criou, você pode utilizar um mecanismo de autorização personalizado no Django REST Framework. Vamos criar uma novo permission class que verificará as permissões para acessar esses objetos. Além disso, configuraremos o Viewset de Marriage para que apenas quem for admin tenha acesso a todos os registros. Vamos fazer isso passo a passo.

Primeiro, a tal permission class. Crie um novo arquivo chamado permissions.py dentro do diretório budget e adicione o seguinte conteúdo:

```bash
# budget/permissions.py

from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite acesso a admin sempre
        if request.user.is_superuser:
            return True
        # Permite acesso se o objeto pertence a quem faz a requisição
        return obj.user == request.user
```

Neste IsOwnerOrAdmin, definimos uma classe de permissão personalizada. Se quem usa tiver permissões de administrador (is_superuser), sempre se terá acesso. Caso contrário, o acesso será apenas aos objetos que pertencem à própria pessoa, verificando se o objeto (Marriage ou Budget) tem um atributo user que corresponde ao usuário autenticado.

Precisamos, então, adicionar um campo de relação com o usuário nos modelos Marriage e Budget. Para isso, atualize o arquivo budget/models.py:

```bash
# budget/models.py


from django.db import models
+ from django.contrib.auth.models import User


class Vendor(models.Model):
    # ...

class Marriage(models.Model):
+   user = models.ForeignKey(User, on_delete=models.CASCADE)
    codename = models.CharField(max_length=50)
    date = models.DateField()

    # ...

class Budget(models.Model):
+   user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendors = models.ManyToManyField(Vendor, related_name='budgets')
    marriage = models.OneToOneField(Marriage, on_delete=models.CASCADE, related_name='budget')

    # ...
```

Com isso, associamos os modelos Marriage e Budget a um usuário (User) através de um relacionamento 1:N. Se você for no painel de administração do Django irá perceber que, por padrão, ele já cria a entidade User para você - então usá-la aqui não dará problema, basta importarmos-na.

A seguir, vamos atualizar os Serializers para incluir o campo user e configurar os Viewsets para usar as permissões personalizadas.

```bash
# budget/serializers.py

# ...

class BudgetSerializer(serializers.ModelSerializer):
+    user = serializers.PrimaryKeyRelatedField(
+           read_only=True, default=serializers.CurrentUserDefault()
+           )

    class Meta:
        model = Budget
-       fields = ["id", "vendors", "marriage"]
+       fields = ["id", "vendors", "marriage", "user"]


class NestedBudgetSerializer(serializers.ModelSerializer):
+    user = serializers.PrimaryKeyRelatedField(
+           read_only=True, default=serializers.CurrentUserDefault()
+           )

    class Meta:
        model = Budget
-       fields = ["id", "vendors"]
+       fields = ["id", "vendors", "user"]


class MarriageSerializer(serializers.ModelSerializer):
    budget = NestedBudgetSerializer()
+   user = serializers.PrimaryKeyRelatedField(
+          read_only=True, default=serializers.CurrentUserDefault()
+          )

    class Meta:
        model = Marriage
-       fields = ["id", "codename", "date", "budget"]
+       fields = ["id", "codename", "date", "budget", "user"]

-   def create(self, validated_data):
-       budget_data = validated_data.pop('budget')
-       budget_data['marriage'] = Marriage.objects.create(**validated_data)
-       BudgetSerializer().create(validated_data=budget_data)
-       return budget_data['marriage']


+   # Sem a inteligência do serializer precisamos unir os dados todos 'na mão'
+   def create(self, validated_data):
+       # Recupera o user que fez a requisição
+       current_user = self.context['request'].user
+
+       '''
+       Recupera os dados de budget da requisição, acrescenta a eles
+       e aos dados de Marriage os dados do usuário
+       '''
+       budget_data = validated_data.pop('budget')
+       budget_data['user'] = current_user
+       validated_data['user'] = current_user
+
+       # Cria marriage, cria budget e retorna Marriage, como a função pede
+       budget_data['marriage'] = Marriage.objects.create(**validated_data)
+       BudgetSerializer().create(validated_data=budget_data)
+       return budget_data['marriage']
```

Tenha especial atenção com a função create que fizemos “na mão” para o MarriageSerializer. Os demais serializers conseguem, com os acréscimos que fizemos, capturar user da requisição e associá-lo à entidade sendo criada. Como em Marriage fizemos a criação na mão, precisamos também manualmente recuperar os dados de usuário e acrescentá-los aos dados usados para criar as entidades.

```bash
# budget/views.py



from rest_framework import viewsets
from .models import Vendor, Marriage, Budget
+ from rest_framework.authentication import BasicAuthentication
from .serializers import (AdminVendorSerializer,
                          VendorSerializer,
                          MarriageSerializer,
                          BudgetSerializer)
+ from .permissions import IsOwnerOrAdmin


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer
+   authentication_classes = [BasicAuthentication]

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer



class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
+   authentication_classes = [BasicAuthentication]
+   permission_classes = [IsOwnerOrAdmin]
+
+
+   def get_queryset(self):
+       """
+       Quem for admin vê todos os casamentos.
+       Caso contrário, a pessoa só vê os próprios casamentos.
+       """
+       if self.request.user.is_superuser:
+           return Marriage.objects.all()
+       else:
+           return Marriage.objects.filter(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
+   authentication_classes = [BasicAuthentication]
+   permission_classes = [IsOwnerOrAdmin]
+
+
+   def get_queryset(self):
+       if self.request.user.is_superuser:
+           return Budget.objects.all()
+       else:
+           return Budget.objects.filter(user=self.request.user)
```

Perceba que adicionamos as variáveis authentication_classes e permission_classes no código acima. Essas variáveis definem a autenticação e permissão necessárias para utilização das views em questão. Essa é uma alternativa da configuração padrão usando no settings.py para, por exemplo, definir diferentes tipos de permissão e autenticação em sua aplicação.

Agora, quando um usuário autenticado criar um Marriage ou Budget, a API definirá automaticamente o campo user como seus dados. Além disso, quando qualquer requisição tentar acessar um Marriage ou Budget, a API verificará se ela tem as credenciais da parte proprietária da entidade ou se é admin para permitir ou negar o acesso. Além disso, sobrescrevemos ali a função get_queryset do MarriageViewset. Essa função é responsável por buscar todas as entidades do modelo quando se recebe uma requisição GET /marriages. Aqui, falamos que quem for admin vê todos os eventos - quem não for só vê os dos quais é dono ou dona.

Para efetivar essas mudanças, nós acrescentamos user, um campo obrigatório, às tabelas Marriage e Budget. Normalmente, para fazer uma migração para aplicá-los ao banco, precisaríamos permitir que esse campo tenha valor nulo ou atribuir um user default a todas as entidades já existentes no banco. Para não ter esse trabalho, aproveitando que ainda estamos desenvolvendo, vamos aprender a resetar o banco de dados da aplicação. Rode os seguintes comandos, alterando-os para colocar os nomes das suas aplicações e o ID do seu container:

```bash
docker ps # Para descobrir o ID do seu container com o banco de dados
docker stop <ID do seu container do banco> # Parar o container
docker remove <ID do seu container do banco> # Deletar o container
docker build -t seu-projeto-db .
docker run -d -p 3306:3306 --name=seu-projeto-mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=seu-projeto_database marryme-db # Recriar o container
python3 manage.py migrate seu-app zero # Desfazer todas as migrations do app budget
rm seu-app/migrations/000* # Deletar a migration
python3 manage.py makemigrations # Recriar as migrations - agora com o campo user
python3 manage.py migrate # Efetuar as migrações para criar o banco
python3 manage.py createsuperuser # Recrie seu superuser
```

De olho na dica 👀: tome nota dessa sequência de comandos. Resetar o banco pode te ajudar muito durante o desenvolvimento de uma aplicação num processo seletivo.

Agora abra o painel de admin e confira que tudo está no lugar.

Vamos testar? Primeiramente, vá até o dashboard de admin e crie alguns User. Agora crie alguns vendors. Em seguida, através do Thunder Client, faça um POST /marriages/ com os metadados do modelo - e criando, ao mesmo tempo, o respectivo orçamento:

```bash
{
    "codename": "Casamento do Século",
    "date": "2023-12-31",
    "budget": {
        "vendors": [3, 4]
    }
}
```

Na aba Auth, da requisição, coloque as credenciais de algum User. Sua resposta será:

```bash
{
  "id": 3,
  "codename": "Casamento do Século",
  "date": "2023-12-31",
  "budget": {
    "id": 1,
    "vendors": [
      3,
      4
    ],
    "user": 2
  },
  "user": 2
}
```

Agora, quando esse usuário tentar acessar o casamento criado o resultado será a informação do casamento:

```bash
{
    "id": 1,
    "user": 1,
    "codename": "Meu Casamento",
    "date": "2023-12-31"
}
```

Se o usuário tentar acessar o casamento de outro usuário o resultado será um erro de permissão:

```bash
{
    "detail": "You do not have permission to perform this action."
}
```

Por outro lado, o admin terá acesso a todos os casamentos e orçamentos. Com estes passos, você adicionou a lógica de autenticação onde um usuário só pode acessar os Marriages e Budgets que ele criou, e o admin tem acesso a tudo. Outros usuários não-autenticados ou sem permissões de administração receberão mensagens de erro.
</details>
</br>

<details>
<summary><strong>  </strong></summary>

```bash
```

```bash
```

```bash
```


</details>
</br>


