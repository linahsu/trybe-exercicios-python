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

## Testando o banco de dados

Com o banco configurado, podemos escrever testes para nossa aplicação! Por exemplo, para checar se as tabelas do banco de dados estão funcionais. Isso pode ser feito através de operações como inserções e remoções de registros.

<details>
<summary><strong> Checando os dados iniciais do banco </strong></summary>

O objetivo da última fixture que criamos, é adicionar alguns dados no banco. Dito isso, podemos escrever testes para verificar que foram inseridos corretamente. Na fixture foram criados os seguintes objetos:

* User: <"testuser">
* Person: <"Antoine Fuqua">, <"Denzel Washington"> e <"Chloë Grace Moretz">
* Genre: <"Suspense">
* Movie: <"O Protetor">
* MovieTheater: <"Cine 1">
* MovieRoom: <"Sala 1">
* MovieSeat: <"A1">, <"A2">, <"A3">, <"A4"> e <"A5">

Para começar, crie o arquivo test_db.py dentro do diretório movies/tests e escreva os seguintes testes:

```bash
# tests/test_db.py
from django.contrib.auth.models import User
from movies.models import Person, Genre, Movie, MovieTheater


def test_user_table_is_healthy():
    number_of_users = len(User.objects.all())
    assert number_of_users == 1

    User.objects.create(username="felps", password="terceS")
    number_of_users = len(User.objects.all())
    assert number_of_users == 2

    user = User.objects.get(id=1)
    user.delete()
    number_of_users = len(User.objects.all())
    assert number_of_users == 1


def test_people_table_is_healthy():
    amount_of_people = len(Person.objects.all())
    assert amount_of_people == 3

    Person.objects.create(name="Kimberly Peirce")
    amount_of_people = len(Person.objects.all())
    assert amount_of_people == 4

    person = Person.objects.get(id=4)
    person.delete()
    amount_of_people = len(Person.objects.all())
    assert amount_of_people == 3


def test_genre_table_is_healthy():
    number_of_genres = len(Genre.objects.all())
    assert number_of_genres == 1

    Genre.objects.create(name="Ação")
    number_of_genres = len(Genre.objects.all())
    assert number_of_genres == 2

    genre = Genre.objects.get(id=1)
    genre.delete()
    number_of_genres = len(Genre.objects.all())
    assert number_of_genres == 1


def test_movies_table_is_healthy():
    number_of_movies = len(Movie.objects.all())
    assert number_of_movies == 1

    Movie.objects.create(
        title="Carrie", direction=Person.objects.create(name="Kimberly Peirce")
    )
    number_of_movies = len(Movie.objects.all())
    assert number_of_movies == 2

    movie = Movie.objects.get(id=1)
    movie.delete()
    number_of_movies = len(Movie.objects.all())
    assert number_of_movies == 1


def test_movie_theaters_table_is_healthy():
    number_of_movie_theaters = len(MovieTheater.objects.all())
    assert number_of_movie_theaters == 1

    MovieTheater.objects.create(name="Cine 2")
    number_of_movie_theaters = len(MovieTheater.objects.all())
    assert number_of_movie_theaters == 2

    movie_theater = MovieTheater.objects.get(id=1)
    movie_theater.delete()
    number_of_movie_theaters = len(MovieTheater.objects.all())
    assert number_of_movie_theaters == 1
```

Execute os testes que você implementou para vê-los em funcionamento.

```bash
python3 -m pytest
```

Nos testes acima escolhemos algumas das tabelas da aplicação e fazemos três verificações: se a quantidade inicial de registros é a esperada, se um novo registro foi inserido corretamente e se um registro foi removido corretamente.

Não se preocupe, os testes para as demais tabelas serão feitos por você nos exercícios! 🤓

Perceba que ainda não estamos testando o funcionamento da aplicação em si, esse será nosso próximo passo! 🚀

</details>
</br>

## Testando templates

Na aplicação temos três rotas que renderizam templates. São elas: /, <int:theater_id>/rooms e <int:theater_id>/room/<int:room_id>/seats. Cada uma das rotas, naturalmente, está vinculada a uma função da view: index, theater_details e room_details, respectivamente. Testaremos a seguir as duas primeiras e deixaremos a última para a sua prática!

Para melhor organizar nossos testes, vamos criar dois arquivos de testes, um para cada uma das páginas que vamos testar. Crie os arquivos test_index.py e test_theater_details.py dentro do diretório tests.

<details>
<summary><strong> Testando o status code da resposta </strong></summary>

Os primeiros testes que escreveremos para os templates serão para verificar o status code da resposta da requisição. Para as três rotas que testaremos, quando a requisição for bem sucedida, o status code da resposta será 200 OK. Além disso, para a página theater_details, quando um id inexistente é passado na rota, o status code da resposta será 404 NOT FOUND.

Usaremos a fixture client para simular o acesso às rotas, observe:

```bash
# tests/test_index.py
def test_if_response_is_200(client):
    response = client.get("/")
    assert response.status_code == 200
```

```bash
# tests/test_theater_details.py
def test_if_response_is_200(client):
    response = client.get("/1/rooms")
    assert response.status_code == 200


def test_if_response_is_404_when_movie_theater_does_not_exists(client):
    response = client.get("/2/rooms")
    assert response.status_code == 404
```

</details>
</br>

<details>
<summary><strong> Testando o template renderizado </strong></summary>

Para rotas que renderizam templates, podemos escrever um teste para validar a chamada do template correto. Felizmente, o plugin pytest-django possui um método que faz exatamente isso, assertTemplateUsed do módulo pytest_django.asserts.

Observe os novos testes abaixo:

```bash
# tests/test_index.py
+ from pytest_django.asserts import assertTemplateUsed

# ...

+ def test_correct_template_is_rendered(client):
+    response = client.get("/")
+    assertTemplateUsed(response, "index.html")
```

```bash
# tests/test_theater_details.py
+ from pytest_django.asserts import assertTemplateUsed


+ def test_if_correct_template_is_rendered(client):
+     response = client.get("/1/rooms")
+     assertTemplateUsed(response, "theater_details.html")
```

</details>
</br>

<details>
<summary><strong> Testando o conteúdo do template </strong></summary>

Podemos também escrever testes que checam o conteúdo do template renderizado.

Se você inspecionou a aplicação, a executou e também adicionou novos registros no banco, deve ter percebido que na página inicial, index.html, aparecem os dados dos cinemas cadastrados. De maneira similar, as páginas theater_details.html e room_details.html mostram respectivamente os dados das salas do cinema e dos assentos de uma sala de cinema.

Para escrever esses testes usaremos outro método do plugin pytest-django, o assertContains. Esse método checa se um elemento está contido na resposta da requisição. Veja como ficam os testes:

```bash
# tests/test_index.py
- from pytest_django.asserts import assertTemplateUsed
+ from pytest_django.asserts import assertTemplateUsed, assertContains
+ from movies.models import MovieTheater


# ...


+ def test_if_template_contains_created_theater(client):
+     cine_1 = MovieTheater.objects.get(id=1)
+     response = client.get("/")
+     assertContains(response, cine_1)
```

```bash
# tests/test_theater_details.py
- from pytest_django.asserts import assertTemplateUsed
+ from pytest_django.asserts import assertTemplateUsed, assertContains
+ from movies.models import MovieRoom


# ...


+ def test_if_template_contains_created_room(client):
+     room_1 = MovieRoom.objects.get(id=1)
+     response = client.get("/1/rooms")
+     assertContains(response, room_1)
```

Execute o comando para rodar os testes para ver seus testes em ação. 😎

```bash
python3 -m pytest
```

</details>
</br>

## Testando a autenticação

Dentro do arquivo movies/views.py podemos ver que as classes implementadas estão definidas com a permissão IsAuthenticatedOrReadOnly. Esse tipo de permissão permite que pessoas usuárias visualizem dados mesmo sem autenticação. Entretanto, não permite que insiram, modifiquem ou deletem dados do banco sem estarem autenticadas. Ou seja, sem autenticação os dados com essa permissão são somente leitura (ReadOnly)

A autenticação que está sendo usada é a TokenAuthentication. Escreveremos dois tipos de teste para validar a autenticação: validar o funcionamento da rota de obtenção do token e validar a inserção de dados no banco com e sem autenticação.

Para começarmos, crie um arquivo test_auth.py dentro da pasta tests.

<details>
<summary><strong> Testando o retorno do token </strong></summary>

Para testar a obtenção do token vamos fazer requisições à rota com dados válidos e inválidos de usuários. Novamente, vamos usar a fixture client para fazer as requisições, observe:

```bash
# tests/test_auth.py

def test_get_authentication_token_using_wrong_credentials(client):
    response = client.post("/api/generate-token", {"username": "admin", "password": "wrong"})
    assert response.status_code == 400


def test_get_authentication_token(client):
    response = client.post("/api/generate-token", {"username": "testuser", "password": "12345"})
    assert response.status_code == 200
    assert "token" in response.json()
```

elembrando 🧠: testuser foi criado na fixture que insere dados no banco.

Os testes acima verificam que com dados inválidos a rota retorna o status code 400 BAD REQUEST e que com dados válidos retorna 200 OK. Além disso, quando a requisição é bem sucedida, checamos também se há o campo token no corpo da requisição.

</details>
</br>

<details>
<summary><strong> Testando a inserção de dados no banco </strong></summary>

Agora, escreveremos uma validação para o status code de uma requisição que não possui o token de autenticação. Depois validaremos a inserção de um elemento no banco. Para implementar esses testes usaremos o token recebido da requisição e também o método credentials da fixture client para inserir o token no cabeçalho da requisição.

Observe como ficam os testes:

```bash
# tests/test_auth.py

# ...

+ def test_post_new_theater_without_token(client):
+     response = client.post("/api/movie-theaters/", {"name": "Cine 2"})
+     assert response.status_code == 401
+ 
+ 
+ def test_post_new_theater_using_generated_token(client):
+     response = client.post("/api/generate-token", {"username": "testuser", "password": "12345"})
+     client.credentials(HTTP_AUTHORIZATION="Token " + response.json()["token"])
+     response = client.post("/api/movie-theaters/", {"name": "Cine 2"})
+     assert response.status_code == 201
+     assert response.json()["name"] == "Cine 2"
```

O status code 401 UNAUTHORIZED representa uma resposta de requisição que não foi autorizada, enquanto o 201 CREATED representa uma requisição bem sucedida de criação de um novo elemento no banco. Execute o comando de teste para ver os testes que você implementou passando. 🎉

```bash
python3 -m pytest
```

Sucesso! Agora podemos partir para os testes dos C.R.U.D.s implementados!
</details>
</br>

## Testando um C.R.U.D.

Para finalizarmos os testes que estamos escrevendo para a aplicação vamos agora testar dois dos C.R.U.D.s que foram implementados.

Na aplicação foram feitos seis rotas que implementam um C.R.U.D.. Faremos os testes de duas delas e as outras quatro servirão para você praticar.

Crie dois arquivos dentro da pasta tests: test_theater_endpoint.py e test_people_endpoint.py.

<details>
<summary><strong> Testando a operação Read </strong></summary>

Os testes de leitura serão os mais simples dentre todos os outros. Isso porque não é necessária autenticação para essa operação.

Escreveremos dois testes para cada um dos arquivos, um para resgatar todos os registros do banco e outro resgatando um registro específico. Observe a implementação abaixo:

```bash
# tests/test_theater_endpoint.py
def test_get_all_movie_theaters(client):
    response = client.get("/api/movie-theaters/")
    number_of_movie_theaters = len(response.json())
    assert response.status_code == 200
    assert number_of_movie_theaters == 1

def test_get_one_movie_theater(client):
    response = client.get("/api/movie-theaters/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Cine 1"
```

```bash
# tests/test_people_endpoint.py
def test_get_all_people(client):
    response = client.get("/api/people/")
    amount_of_people = len(response.json())
    assert response.status_code == 200
    assert amount_of_people == 3

def test_get_one_person(client):
    response = client.get("/api/people/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Antoine Fuqua"
```

Note que no primeiro teste de cada arquivo checamos pela quantidade de registros retornados no corpo da requisição. Já no segundo, a requisição é feita direto para a rota do objeto em si, note que o 1 representa o id do objeto, e depois validamos um atributo específico daquele registro.

</details>
</br>

<details>
<summary><strong> Testando a operação Create </strong></summary>

Para os testes de criação de registros, faremos verificações de algumas das requisições com autenticação para checar se a criação ocorre com sucesso e outras sem autenticação para verificar o impedimento da criação. Apesar de parece redundante com os testes em test_auth.py, aqui ignoraremos a lógica de produção dos tokens. Queremos saber se as rotas estão ou não protegidas. Adicione a implementação abaixo nos arquivos de teste:

```bash
# tests/test_theater_endpoint.py
+ from django.contrib.auth.models import User


# ...


+ def test_unauthorized_post(client):
+     response = client.post("/api/movie-theaters/", {"name": "Cine 2"})
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_post(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.post("/api/movie-theaters/", {"name": "Cine 2"})
+     assert response.status_code == 201
+     assert response.json()["name"] == "Cine 2"
```

```bash
# tests/test_people_endpoint.py
+ from django.contrib.auth.models import User


# ...


+ def test_unauthorized_post(client):
+     response = client.post("/api/people/", {"name": "Jack Black"})
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_post(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.post("/api/people/", {"name": "Jack Black"})
+     assert response.status_code == 201
+     assert response.json()["name"] == "Jack Black"
```

Perceba que, ao invés de solicitar o token através da rota de autenticação, estamos usando o método .force_authenticate() do client para forçar a autenticar o usuário. Isso é feito para simplificar o teste dado que não queremos testar a obtenção do token em si.

</details>
</br>

<details>
<summary><strong> Testando a operação Update </strong></summary>

Para testar o método de atualização de registro, será necessário fazer uma requisição direto na rota do objeto em si. Seguiremos a mesma idea dos testes para o Create dado que o método Update também requer autenticação. Adicione a implementação abaixo nos arquivos de teste:

```bash
# tests/test_theater_endpoint.py

# ...


+ def test_unauthorized_put(client):
+     response = client.put("/api/movie-theaters/1/", {"name": "Cinema 1"})
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_put(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.put("/api/movie-theaters/1/", {"name": "Cinema 1"})
+     assert response.status_code == 200
+     assert response.json()["name"] == "Cinema 1"
```

```bash
# tests/test_people_endpoint.py

# ...


+ def test_unauthorized_put(client):
+     response = client.put("/api/people/1/", {"name": "Antonio Banderas"})
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_put(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.put("/api/people/1/", {"name": "Antonio Banderas"})
+     assert response.status_code == 200
+     assert response.json()["name"] == "Antonio Banderas"
```

Bem parecido com os testes de criação, não é mesmo? Note que mudamos apenas o método usado por client e os dados recebidos por esse método.

</details>
</br>

<details>
<summary><strong> Testando a operação Delete </strong></summary>

Agora a última das operações do C.R.U.D., o Delete. Para testar essa operação, também faremos a requisição direto na rota do objeto. Além disso, como a operação Delete também requer autenticação, seguiremos a mesma ideia dos testes anteriores. Adicione a implementação abaixo nos arquivos de teste:

```bash
# tests/test_theater_endpoint.py

# ...


+ def test_unauthorized_delete(client):
+     response = client.delete("/api/movie-theaters/1/")
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_delete(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.delete("/api/movie-theaters/1/")
+     assert response.status_code == 204
```

```bash
# tests/test_people_endpoint.py

# ...


+ def test_unauthorized_delete(client):
+     response = client.delete("/api/people/1/")
+     assert response.status_code == 401
+ 
+ 
+ def test_authorized_delete(client):
+     user = User.objects.get(id=1)
+     client.force_authenticate(user)
+     response = client.delete("/api/people/1/")
+     assert response.status_code == 204
```

Com esses testes implementados, cobrimos todas as operações do C.R.U.D. e boa parte da aplicação.

Execute o comando de testes e veja agora 32 testes sendo aprovados! 🎉

</details>
</br>

# Deployment no Railway

<details>
<summary><strong> Usando o gunicorn com o Django </strong></summary>

### O que é o gunicorn

O gunicorn é um servidor HTTP WSGI para Python. Ele é um servidor de produção, ou seja, ele é destinado a ser usado quando precisamos fazer o deploy de uma aplicação Python. O papel dele será bem semelhante ao realizado pelo comando runserver do Django, mas trazendo vantagens como melhor desempenho e mais segurança.

### Como usar o gunicorn com o Django

Para usar o gunicorn com o Django, precisamos fazer algumas alterações no nosso projeto. A primeira delas é instalar o gunicorn no nosso ambiente virtual:

```bash
pip install gunicorn
```

Relembrando 🧠: Se quiser usar o gunicorn em um projeto que já possui um arquivo de dependências como requirements.txt, adicione-o lá.

Com isso, você já pode utilizar o gunicorn para rodar sua aplicação localmente! 🚀

Basta executar o comando:

```bash
gunicorn seu_projeto_django.wsgi
```

Quando rodamos esse comando, o gunicorn irá buscar o objeto chamado application dentro do arquivo wsgi.py da pasta do seu projeto Django. Esse objeto é o responsável por receber as requisições HTTP e retornar as respostas, também usado por baixo dos panos pelo runserver do Django e é registrado na variável WSGI_APPLICATION do settings.py.

De olho na dica 👀: O gunicorn também pode ser utilizado com outros frameworks como o Flask e o FastAPI.

</details>
</br>

<details>
<summary><strong> Usando o Docker com o Django </strong></summary>

O servidor gunicorn será uma peça fundamental para o deploy da nossa aplicação Django no Railway. Mas antes de começarmos as configurações no Railway, precisamos preparar uma imagem Docker que será usada como base para o deploy.

Esse passo nos ajudará a garantir comportamentos consistentes entre os ambientes de desenvolvimento e produção, e facilitará muito o processo de deploy no Railway.

### Ponto de partida

Para os procedimentos que faremos, vamos usar como base a aplicação cinetrybe.

Esse repositório contém uma aplicação Django que gerencia salas de cinema utilizando conceitos que já vimos no curso até aqui. Nele já temos um Dockerfile para uma instância do banco de dados MySQL e as principais dependências definidas no requirements.txt (como o gunicorn e mysqlclient).

Como vamos focar no deploy, não vamos nos aprofundar no código da aplicação.

### Dockerfile para o Django

A primeira alteração que vamos fazer é criar um Dockerfile para a nossa aplicação Django. Esse Dockerfile será responsável por criar uma imagem Docker que será usada como base para o deploy no Railway.

Como já temos um Dockerfile para o Mysql, vamos renomeá-lo para criar um novo arquivo chamado Dockerfile na raiz do projeto e adicionar o conteúdo a seguir:

```bash
mv Dockerfile Dockerfile.mysql
touch Dockerfile
touch .dockerignore
```

Arquivo Dockerfile

```bash
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt install -y python3-dev netcat-openbsd default-libmysqlclient-dev build-essential pkg-config \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["gunicorn", "cinetrybe.wsgi", "--bind", "0.0.0.0:8000"]
```

Arquivo .dockerignore

```bash
.env

.git
.cache

.venv

*.egg-info

setup.cfg
__pycache__
.coverage
.pytest_cache
```

De olho na dica 👀: Existem diversas formas de configurar um ambiente com Docker para aplicação Django. Se você encontrar outras formas de fazê-la, não se preocupe! O importante é que você entenda os conceitos e consiga aplicá-los no seu projeto.

Alguns comentários importantes sobre essa configuração sugerida para o Dockerfile:

* Estamos usando a imagem python:3.10-slim como base, então a versão do Python será a 3.10. Imagens slim não são tão enxutas quanto as alpine, mas com ela podemos garantir que o mysqlclient será instalado sem muita complexidade;
* Estamos definindo a variável de ambiente PYTHONUNBUFFERED como 1. Essa variável é importante para garantir que as saídas do Python sejam exibidas imediatamente no terminal, sem que seja feito cache das saídas. Assim poderemos ver mensagens de debug no terminal em tempo real;
* Estamos instalando as dependências do sistema operacional necessárias para instalar o mysqlclient (a dependência do Django para conexão com o banco MySQL), mas elas podem variar de acordo com a imagem base que você escolher;
* Estamos utilizando o parâmetro --bind do gunicorn para definir o endereço e porta que o servidor irá escutar. Nesse caso, estamos definindo que o gunicorn irá escutar na porta 8000 de todas as interfaces de rede (0.0.0.0). Essa configuração será essencial para nossa aplicação ser acessível no Railway.
* Com o .dockerignore, estamos evitando que alguns arquivos desnecessários sejam enviados ao container. Isso é importante para evitar que o container fique muito pesado e também para não expor dados sensíveis. Você pode adicionar outros arquivos que não deseja enviar ao container, como arquivos de testes, arquivos de configuração do editor de texto, etc.

Para testar se a nossa imagem está funcionando, vamos construí-la e executá-la localmente:

```bash
docker build -t cinetrybe .
docker run -it --rm -p 8000:8000 cinetrybe
```

### Conectando ao banco de dados

Nesse momento, se você tentar acessar a aplicação no navegador, você verá um erro de conexão com o banco de dados. Isso acontece porque o gunicorn está tentando se conectar ao banco de dados, mas não consegue encontrar o servidor.

Para isso, precisaremos de um docker-compose para subir o banco de dados e a aplicação Django ao mesmo tempo. Vamos criar um arquivo docker-compose.yml na raiz do projeto:

```bash
touch docker-compose.yml
```

Arquivo docker-compose.yml

```bash
version: "3.8"

services:
  db_service:
    build:
      context: .
      dockerfile: Dockerfile.mysql
    volumes:
      - ./database:/docker-entrypoint-initdb.d/:ro
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - db_service
```

Além disso, precisamos fazer um pequeno ajuste no settings.py da nossa aplicação Django para que a variável DATABASES faça a conexão com o serviço mysql_db definido no docker-compose.yml:

Arquivo settings.py

```bash

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'cinetrybe_database',
       'USER': 'root',
       'PASSWORD': 'password',
-       'HOST': '127.0.0.1',
+       'HOST': 'db_service',
       'PORT': '3306',
    }
}
```

Maravilha! 🎉 Agora podemos rodar nossa aplicação com o docker-compose:

```bash
docker-compose up --build
```

Ao acessar http://localhost:8000/ temos… um novo erro! 😅

Esse erro ocorre porque, através do docker-compose.yml, subimos uma nova instância do banco de dados, e por isso precisamos criar as tabelas novamente com python3 manage.py migrate dentro dela. Além disso, vamos precisar do comando collectstatic e eventualmente do makemigrations. Vejamos como fazer isso!

### Configurando o entrypoint

Como precisamos rodar alguns comandos antes de iniciar o gunicorn, como o das migrations, vamos criar um entrypoint para nossa aplicação. O entrypoint é um script que será executado no CMD do Dockerfile.

Para isso, vamos criar um arquivo entrypoint.sh na raiz do projeto:

```bash
touch entrypoint.sh
```

Arquivo entrypoint.sh

```bash
#!/bin/sh

# Essa parte é importante para garantir que o banco de dados já esteja no ar
# antes de rodar as migrações

while ! nc -z db_service 3306 ; do
    echo "> > > Esperando o banco de dados MySQL ficar disponível..."
    sleep 3
done

echo "> > > Banco de dados MySQL disponível!"


python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn cinetrybe.wsgi --bind 0.0.0.0:8000
```

E vamos ajustar o Dockerfile para que ele execute esse script:

Arquivo Dockerfile

```bash
...

-CMD ["gunicorn", "cinetrybe.wsgi", "--bind", "0.0.0.0:8000"]
+CMD ["sh", "entrypoint.sh"]
```

Agora, vamos construir e rodar nossa aplicação novamente:

```bash
docker-compose up --build
```

Agora sim! 🎉 Se acessar a rota /admin, verá a tela de login

Ah, e como ainda não existe um super-user cadastrado no banco de dados local, podemos criar um com o comando:

```bash
docker-compose run --rm web python manage.py createsuperuser
```

Temos nossa aplicação rodando com o gunicorn e o banco de dados MySQL em serviços no Docker localmente. Mas ainda temos alguns ajustes para fazer antes de fazer o deploy no Railway. 👀
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
