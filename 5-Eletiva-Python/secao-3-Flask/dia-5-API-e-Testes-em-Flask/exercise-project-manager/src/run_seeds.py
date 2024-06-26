from models.projectModel import ProjectModel


projects = [
    {
        "idProject": 1,
        "name": "Aplicação Web para Gerenciamento de Tarefas",
        "task": "Design de Interface do Usuário",
        "status": "Concluído",
        "completionPercentage": 100,
        "descriptionTask": "Criar o design visual do sistema, incluindo a definição de layouts, cores e elementos gráficos.",
        "deadline": "15/07/2023",
        "responsible": "Pedro Santos"
    },
    {
        "idProject": 1,
        "name": "Aplicação Web para Gerenciamento de Tarefas",
        "task": "Desenvolvimento do Backend",
        "status": "Em progresso",
        "completionPercentage": 20,
        "descriptionTask": "Implementar a lógica de negócio e a infraestrutura necessária para suportar as funcionalidades da aplicação.",
        "deadline": "30/08/2023",
        "responsible": "João Oliveira"
    },
    {
        "idProject": 1,
        "name": "Aplicação Web para Gerenciamento de Tarefas",
        "task": "Desenvolvimento do Frontend",
        "status": "Em progresso",
        "completionPercentage": 10,
        "descriptionTask": " Implementar as telas e a interação do usuário com o site, seguindo o design de interface",
        "deadline": "30/09/2023",
        "responsible": "Maria Costa"
    },
    {
        "idProject": 1,
        "name": "Aplicação Web para Gerenciamento de Tarefas",
        "task": "Testes de performance",
        "status": "Não iniciado",
        "completionPercentage": 0,
        "descriptionTask": "Realizar testes de funcionalidade, usabilidade e desempenho do aplicativo, e identificar eventuais bugs.",
        "deadline": "31/10/2023",
        "responsible": "Ana Silva"
    },
    {
        "idProject": 1,
        "name": "Aplicação Web para Gerenciamento de Tarefas",
        "task": "Deploy",
        "status": "Não iniciado",
        "completionPercentage": 0,
        "descriptionTask": "Preparar o ambiente de produção, realizar o lançamento do site.",
        "deadline": "30/11/2023",
        "responsible": "Luísa Mendes"
    },
    {
        "idProject": 2,
        "name": "Aplicativo móvel para rastreamento de exercícios físicos",
        "task": "Design de Interface do Usuário",
        "status": "Concluído",
        "completionPercentage": 100,
        "descriptionTask": "Criar o design visual do sistema, incluindo a definição de layouts, cores e elementos gráficos.",
        "deadline": "30/06/2023",
        "responsible": "Sofia Martins"
    },
    {
        "idProject": 2,
        "name": "Aplicativo móvel para rastreamento de exercícios físicos",
        "task": "Desenvolvimento do Backend",
        "status": "Concluído",
        "completionPercentage": 100,
        "descriptionTask": "Implementar a lógica de negócio e a infraestrutura necessária para suportar as funcionalidades da aplicação.",
        "deadline": "30/07/2023",
        "responsible": "Marta Rodrigues"
    },
    {
        "idProject": 2,
        "name": "Aplicativo móvel para rastreamento de exercícios físicos",
        "task": "Desenvolvimento do Frontend",
        "status": "Concluído",
        "completionPercentage": 100,
        "descriptionTask": " Implementar as telas e a interação do usuário com o site, seguindo o design de interface",
        "deadline": "30/08/2023",
        "responsible": "André Ferreira"
    },
    {
        "idProject": 2,
        "name": "Aplicativo móvel para rastreamento de exercícios físicos",
        "task": "Testes de performance",
        "status": "Em progresso",
        "completionPercentage": 80,
        "descriptionTask": "Realizar testes de funcionalidade, usabilidade e desempenho do aplicativo, e identificar eventuais bugs.",
        "deadline": "31/09/2023",
        "responsible": "Miguel Carvalho"
    },
    {
        "idProject": 2,
        "name": "Aplicativo móvel para rastreamento de exercícios físicos",
        "task": "Deploy",
        "status": "Não iniciado",
        "completionPercentage": 0,
        "descriptionTask": "Preparar o ambiente de produção, realizar o lançamento do site.",
        "deadline": "30/10/2023",
        "responsible": "Inês Sousa"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Análise de viabilidade técnica e financeira",
        "status": "Atrasado",
        "completionPercentage": 70,
        "descriptionTask": "Avaliar a infraestrutura tecnológica necessária, considerando aspectos como capacidade de processamento, armazenamento e custos associados.",
        "deadline": "25/06/2023",
        "responsible": "Laura Costa"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Design de Interface do Usuário",
        "status": "Em progresso",
        "completionPercentage": 40,
        "descriptionTask": "Criar o design visual do sistema, incluindo a definição de layouts, cores e elementos gráficos.",
        "deadline": "10/07/2023",
        "responsible": "Sofia Martins"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Desenvolvimento do Backend",
        "status": "Em progresso",
        "completionPercentage": 15,
        "descriptionTask": "Implementar a lógica de negócio e a infraestrutura necessária para suportar as funcionalidades da aplicação.",
        "deadline": "30/08/2023",
        "responsible": "Marta Rodrigues"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Desenvolvimento do Frontend",
        "status": "Em progresso",
        "completionPercentage": 5,
        "descriptionTask": " Implementar as telas e a interação do usuário com o site, seguindo o design de interface",
        "deadline": "30/09/2023",
        "responsible": "André Ferreira"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Testes de performance",
        "status": "Não iniciado",
        "completionPercentage": 0,
        "descriptionTask": "Realizar testes de funcionalidade, usabilidade e desempenho do aplicativo, e identificar eventuais bugs.",
        "deadline": "30/10/2023",
        "responsible": "Thiago Cardoso"
    },
    {
        "idProject": 3,
        "name": "Sistema de gestão de vendas online",
        "task": "Deploy",
        "status": "Não iniciado",
        "completionPercentage": 0,
        "descriptionTask": "Preparar o ambiente de produção, realizar o lançamento do site.",
        "deadline": "30/11/2023",
        "responsible": "Beatriz Gomes"
    }
]

for project in projects:
  ProjectModel(project).save()