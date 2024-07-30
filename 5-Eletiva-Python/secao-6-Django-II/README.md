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

# Token Authentication

<details>
<summary><strong> Permitindo a quem usa obter Tokens </strong></summary>

A autenticação básica é excelente por ser bem simples de implementar - você coloca as credenciais no cabeçalho da requisição e pronto! Além disso, ela carrega a vantagem de não exigir nenhum armazenamento ou gerenciamento de dados por parte do servidor - ele só precisa saber autenticar uma pessoa de acordo com suas credenciais. Mas há desvantagens também: as credenciais são enviadas no cabeçalho de toda requisição - uma interceptação de dados pode comprometê-las.

A autenticação por token requer um pouco mais de gerenciamento por parte do servidor - o gerenciamento das tokens - mas é mais segura - as credenciais só são enviadas para se obter uma token, e esta pode ser revogada com facilidade. 

### Segurança

#### Autenticação por Token
Oferece melhor segurança, pois os tokens podem ter prazos curtos e ser revogados facilmente. Os tokens também podem ser emitidos com permissões específicas.

#### Autenticação Básica
Menos seguro, pois as credenciais (nome de usuário/senha) são enviadas com cada requisição e podem ser interceptadas. As credenciais também são armazenadas no servidor, representando um risco potencial caso o servidor seja comprometido.

### Ausência de Estado

#### Autenticação por Token
Stateless, não requer armazenamento de sessão no servidor, o que reduz a carga no servidor.

#### Autenticação Básica
Stateless, não requer armazenamento de sessão no servidor, o que reduz a carga no servidor.

### Complexidade de Implementação

#### Autenticação por Token
Mais complexo de implementar em comparação com a Autenticação Básica, pois requer a geração e manipulação de tokens no lado do servidor, além de lidar com a expiração e revogação de tokens.

#### Autenticação Básica
Mais fácil de implementar, pois envolve apenas a verificação das credenciais em cada requisição. Nenhuma geração ou manipulação de token é necessária.

No Django REST Framework, fazer autenticação por Token é ainda melhor pois dá quase a mesma quantidade de trabalho que fazer autenticação básica. Vamos ver como isso funciona? Primeiro, você precisará acrescentar um app novo à suas configurações e alterar a configuração padrão de autenticação:

```bash
# marryme/settings.py

# ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'budget',
    'rest_framework',
+   'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
-       'rest_framework.authentication.BasicAuthentication',
+       'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# ...
```

Agora, vamos primeiro criar uma rota para que uma pessoa possa enviar, via requisição, suas credenciais para obter uma token:

```bash
# marryme/urls.py


from django.contrib import admin
from django.urls import path, include
+ from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
+    path('login/', obtain_auth_token, name='login'),
    path('', include('budget.urls')),
]
```

E pronto! O Django REST Framework nos dá toda essa lógica já pronta. Para testar, rode as migrations para termos a lógica de tokens no banco e faça uma requisição à sua nova rota:

```bash
// POST /login/

{
  "username": "AlgumUser",
  "password":  "SenhaDesteUser"
}
```

Você obterá sua token.

</details>
</br>

<details>
<summary><strong> Autenticando com Tokens </strong></summary>

Para permitir que as Tokens sejam usadas como autenticação, vá em suas views e faça a alteração abaixo:

```bash
# budget/views.py


from rest_framework import viewsets
from .models import Vendor, Marriage, Budget
- from rest_framework.authentication import BasicAuthentication
+ from rest_framework.authentication import TokenAuthentication
from .serializers import (AdminVendorSerializer,
                          VendorSerializer,
                          MarriageSerializer,
                          BudgetSerializer)
from .permissions import IsOwnerOrAdmin


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer
-   authentication_classes = [BasicAuthentication]
+   authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer


class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
-   authentication_classes = [BasicAuthentication]
+   authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

def get_queryset(self):
    if self.request.user.is_superuser:
        return Marriage.objects.all()
    else:
        return Marriage.objects.filter(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
-   authentication_classes = [BasicAuthentication]
+   authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

def get_queryset(self):
    if self.request.user.is_superuser:
        return Budget.objects.all()
    else:
        return Budget.objects.filter(user=self.request.user)
```

E é isso, sim, só isso, que muda! Substituímos a classe de autenticação de BasicAuthentication para TokenAuthentication.

Agora faça uma requisição para obter o casamento de uma pessoa usuária sem autenticar e veja que você não tem acesso aos dados. Agora acrescente ao cabeçalho da requisição a chave Authorization com o valor Token SuaTokenAqui, e veja como funciona! Experimente alterar entre tokens de diferentes users e veja como cada pessoa só acessa o próprio dado!
</details>
</br>

# SimpleJWT

<details>
<summary><strong> Instalar, rotear, configurar e pronto! </strong></summary>

Todas as técnicas que foram ensinadas até agora podem ser usadas no Django, contudo, você precisará implementar toda a lógica dessas autenticações por sua conta. As autenticações BasicAuthentication e TokenAuthentication que usamos são implementadas no Django REST Framework. A Simple JWT não: ela vem de um plugin do Django REST Framework. Entretanto, ela é poderosa e implementável em pouquíssimos passos.

### Segurança

#### Autenticação por Token
Oferece melhor segurança, pois os tokens podem ter prazos curtos e ser revogados facilmente. Os tokens também podem ser emitidos com permissões específicas.

#### Autenticação Básica
Menos seguro, pois as credenciais (nome de usuário/senha) são enviadas com cada requisição e podem ser interceptadas. As credenciais também são armazenadas no servidor, representando um risco potencial caso o servidor seja comprometido.

#### Simple JWT
Oferece segurança avançada, geração automática de tokens JWT e suporte a tokens de atualização. Os tokens podem ter tempo de vida configurável e podem ser revogados. Possui integração simples com o Django REST Framework.

### Ausência de Estado

#### Autenticação por Token
Stateless, não requer armazenamento de sessão no servidor, o que reduz a carga no servidor.

#### Autenticação Básica
Stateless, não requer armazenamento de sessão no servidor, o que reduz a carga no servidor.

#### Simple JWT
Stateless, não requer armazenamento de sessão no servidor, o que reduz a carga no servidor.

### Complexidade de Implementação

#### Autenticação por Token
Mais complexo de implementar em comparação com a Autenticação Básica, pois requer a geração e manipulação de tokens no lado do servidor, além de lidar com a expiração e revogação de tokens.

#### Autenticação Básica
Mais fácil de implementar, pois envolve apenas a verificação das credenciais em cada requisição. Nenhuma geração ou manipulação de token é necessária.

#### Simple JWT
Mais complexo que a Autenticação Básica, mas oferece biblioteca completa para lidar com a geração, manipulação e renovação de tokens JWT. Requer configurações adicionais, mas proporciona mais recursos e flexibilidade.

Para trocar nossa TokenAuthentication por SimpleJWT, siga os passos adiante. Primeiro, instale o módulo abaixo:

```bash
pip install djangorestframework-simplejwt
```
A seguir, ajuste as configurações, substituindo a autenticação padrão de TokenAuthentication por JWTAuthentication

```bash
# marryme/settings.py

INSTALLED_APPS = [
    # ...
    'rest_framework',
-   'rest_framework.authtoken',
+   'rest_framework_simplejwt',
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
-       'rest_framework.authentication.TokenAuthentication',
+       'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Outras configurações do DRF ...
}
```

A seguir, ajuste as suas rotas:

```bash
# marryme/urls.py


from django.urls import path, include
- from rest_framework.authtoken.views import obtain_auth_token
+ from rest_framework_simplejwt.views import (TokenObtainPairView,
+                                             TokenRefreshView,
+                                             TokenVerifyView)

urlpatterns = [
    path('admin/', admin.site.urls),
-   path('login/', obtain_auth_token, name='login'),
+   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
+   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
+   path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('budget.urls')),
]
```

Como definimos a autenticação JWT como padrão no arquivo settings.py podemos remover a variável authentication_classes nas views. Isso fará com que o simple JWT seja o padrão para toda aplicação. Caso você não defina uma configuração padrão de autenticação e permissão, você precisará indicar com authentication_classes e permission_classes quais serão essas configurações, caso contrário, não haverá autenticação e todas as pessoas terão as permissões.

```bash
from rest_framework import viewsets
from .models import Vendor, Marriage, Budget
- from rest_framework.authentication import TokenAuthentication
from .serializers import (AdminVendorSerializer,
                          VendorSerializer,
                          MarriageSerializer,
                          BudgetSerializer)
from .permissions import IsOwnerOrAdmin


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer
-   authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer




class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
-   authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

def get_queryset(self):
    if self.request.user.is_superuser:
        return Marriage.objects.all()
    else:
        return Marriage.objects.filter(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
-   authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

def get_queryset(self):
    if self.request.user.is_superuser:
        return Budget.objects.all()
    else:
        return Budget.objects.filter(user=self.request.user)
```

E tudo já deve funcionar! Faça, primeiro, uma requisição com as credenciais para /token/:

```bash
// POST /token/

{
  "username": "SeuUser",
  "password": "SuaSenha"
}

```

Você receberá duas tokens: uma na chave access e outra na chave refresh. Para testar, copie a da chave access para o cabeçalho da requisição com a chave Authorization e o valor Bearer SeuToken. Faça os testes de acesso a rotas protegidas para ver que tudo continua funcionando! Para além disso, o endpoint token/verify/ que criamos recebe no corpo da requisição a chave token com uma de suas tokens e retorna 200 OK se elas forem válidas, e 401 UNAUTHORIZED caso contrário. No endpoint /token/refresh/, você envia sua token da chave refresh e recebe uma nova token access, podendo gerar novas tokens sem precisar usar suas credenciais mais do que uma vez!

</details>
</br>

Qual autenticação devo usar?!
Lembre-se: não existe bala de prata. Não existe tecnologia infalível ou melhor em 100% dos contextos. Dito isso, uma regra geral boa de se adotar é: se usar o Django REST Framework, use Simple JWT - é a opção mais completa, mais segura e, em função do que o framework fornece, a mais fácil de implementar. Caso use somente o Django comum, use TokenAuthentication. Caso precise somente de algo realmente simples o BasicAuthentication quebra um galho.

# Testando com pytest

Apesar do Django possuir um sistema de testes nativos, a ferramenta de teste mais utilizada pelas pessoas desenvolvedoras Django é o pytest. Além disso, vale lembrar que já utilizamos o pytest em outras ocasiões ao longo do conteúdo e por isso, já temos uma certa familiaridade com ele.

Além do pytest também usaremos o pytest-django que é um plugin que fornece um conjunto de ferramentas úteis para testar aplicações e projetos Django. Como nenhum dos dois pacotes são nativos do python, precisaremos instalá-los. Execute os comandos abaixo:

```bash
python3 -m pip install pytest
python3 -m pip install pytest-django
```

<details>
<summary><strong> Configurando o pytest </strong></summary>

Como a ferramenta de testes escolhida não é a nativa do Django, será necessário fazer uma breve configuração para seu uso.

Crie na raiz do projeto um arquivo com nome pyproject.toml. Esse arquivo é usado para configurar ferramentas que serão utilizadas em seu projeto, pytest, black, flake8, etc.

```bash
# -- pyproject.toml --

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "cinetrybe.settings"
python_files = ["tests/test_*.py", "tests/*_test.py"]
```

O arquivo acima define o módulo onde se encontram as configurações do projeto, ou seja, cinetrybe.settings indica que o arquivo settings.py se encontra dentro do projeto cinetrybe. Além disso, definimos que os arquivos a serem testados se encontrarão dentro do diretório tests e seus nomes deverão começar com test_ ou terminar com _test.py.

Feito isso, você já deve ser capaz de executar o comando para rodar os testes:

```bash
python3 -m pytest
```

</details>
</br>

<details>
<summary><strong> Fixtures para os testes </strong></summary>

Uma fixture é um conjunto predefinido de dados, configurações ou estados que são usados como base para realizar testes de software de forma consistente e controlada. Uma fixture garante que os testes sejam executados em condições conhecidas e reprodutíveis, permitindo que os resultados sejam avaliados de maneira confiável.

Agora que configuramos o pytest, chegou a hora de preparar as ferramentas auxiliares. Primeiramente, vamos criar o diretório tests na raiz do projeto.

De olho na dica 👀: toda vez que uma nova aplicação é iniciada - django-admin startapp <nome> - automaticamente é gerado um arquivo tests.py no diretório criado. Entretanto, se a quantidade de testes a criar não for pequena, a boa prática é dividi-los em mais arquivos.

Dentro da pasta tests, vamos criar um arquivo chamado conftest.py. Esse arquivo é responsável por conter fixtures que serão utilizados nos testes.

</details>
</br>

<details>
<summary><strong> Implementando o conftest.py </strong></summary>

O Django possui uma classe chamada Client que pode ser usada para testes. Essa classe age como um navegador fictício permitindo que você teste suas views e interaja com a aplicação que você desenvolveu. Ao usar essa classe é simulado um ambiente de teste, com um banco de dados para ele que você pode preencher à vontade, sem atrapalhar o banco de dados real da aplicação.

Já o DRF implementa uma classe chamada APIClient que herda da classe Client do Django. Como na aplicação usamos o DRF, seguiremos usando a classe APIClient dado que ela apenas estende o comportamento da classe Client.
</details>
</br>

<details>
<summary><strong> APIClient </strong></summary>

No arquivo conftest.py, vamos importar a classe APIClient do módulo restframework.test para escrever as fixtures:

```bash
# tests/conftest.py
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()
```

Essa fixture já poderá ser usada nos testes para simular as requisições HTTP (GET, POST, PUT, DELETE). O próximo passo agora é configurar o banco de dados de teste para que possa ser usado durante os testes e também para já ter alguns dados para testar.

</details>
</br>

<details>
<summary><strong> Banco de dados </strong></summary>

A configuração padrão do banco de dados de teste não permite que ele seja acessado. Sendo assim, precisaremos escrever uma fixture para permitir seu uso. Como todas as views da aplicação usam o banco de dados, aplicaremos essa fixture automaticamente na execução dos testes através do parâmetro autouse.

A liberação do acesso de uma função de teste ao banco de dados é feita através da fixture db, implementada pelo plugin pytest-django. Entretanto, implementaremos uma nova fixture que acessará a fixture db e será aplicada a todos os testes.

A implementação dessa fixture fica assim:

```bash
# tests/conftest.py

# ...


+ @pytest.fixture(autouse=True)
+ def enable_db_access_for_all_tests(db):
+     pass

```

No código acima, a fixture enable_db_access_for_all_tests acessa a fixture db e é aplicada automaticamente aos testes graças ao parâmetro autouse. Note que não foi necessário implementar nada dentro da função, porque desejávamos apenas aplicar a fixture db aos testes.

O próximo passo é popular o banco com alguns dados para que possamos usá-los nos testes. Criaremos então uma terceira fixture terá a responsabilidade de preparar os dados do banco para os testes. Observe a implementação:

```bash
# tests/conftest.py
# ...
+ from django.contrib.auth.models import User
+ from movies.models import (MovieTheater,
+                           MovieRoom,
+                           Genre,
+                           Movie,
+                           Person,
+                           MovieSeat)


# ...


+ @pytest.fixture(scope="session", autouse=True)
+ def django_db_setup(django_db_setup, django_db_blocker):
+     with django_db_blocker.unblock():
+         User.objects.create_user(username="testuser", password="12345")
+ 
+         movie_theater = MovieTheater.objects.create(name="Cine 1")
+         genre = Genre.objects.create(name="Suspense")
+         direction = Person.objects.create(name="Antoine Fuqua")
+         actor = Person.objects.create(name="Denzel Washington")
+         actress = Person.objects.create(name="Chloë Grace Moretz")
+         movie = Movie.objects.create(
+             title="O Protetor",
+             direction=direction,
+         )
+         movie.genre.add(genre)
+         movie.actors.add(actor)
+         movie.actors.add(actress)
+ 
+         room = MovieRoom.objects.create(
+             name="Sala 1", theater=movie_theater, movie=movie
+         )
+ 
+         MovieSeat.objects.create(name="A1", room=room)
+         MovieSeat.objects.create(name="A2", room=room)
+         MovieSeat.objects.create(name="A3", room=room)
+         MovieSeat.objects.create(name="A4", room=room, is_occupied=True)
+         MovieSeat.objects.create(name="A5", room=room, is_occupied=True)

```

No código acima definimos nossa fixture django_db_setup, que acessa a fixture django_db_setup implementada pelo pytest-django. A django-db-setup é responsável por criar o banco de dados de teste e django_db_blocker para controlar as permissões do banco. Observe que with django_db_blocker.unblock(): abre um contexto onde o banco está acessível, permitindo a inserção dos dados.

Perceba que novamente usamos o parâmetro autouse para aplicar automaticamente essa fixture e definimos o escopo como session para que os dados sejam inseridos apenas uma vez e não a cada teste.

Com as fixtures implementadas podemos iniciar a construção dos testes.
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
