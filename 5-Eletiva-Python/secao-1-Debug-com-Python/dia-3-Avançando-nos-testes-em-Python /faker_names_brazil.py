from faker import Faker


faker = Faker(locale="pt_BR")

# Anota aí 📝: A seed (semente) é um valor que serve como base para a geração
# de números aleatórios. Se a mesma seed for usada, teremos sempre a mesma
# sequência de resultados. Por padrão, o Faker usa o timestamp atual do
# sistema e por isso cada execução resulta em valores diferentes.
Faker.seed(0)  # repare que usamos a classe 'Faker', e não a instância 'faker'
# De olho na dica 👀: o valor 0 é arbitrário, ou seja, você pode usar qualquer
# valor que quiser! A biblioteca Faker aceita valores dos tipos int, float,
# str, bytes e bytearray.

print(faker.name())
print(faker.phone_number())
print(faker.cpf())
