from faker import Faker

faker = Faker(locale="es_AR")

print(faker.last_name())
print(faker.email())
print(faker.password())
print(faker.url())
print(faker.license_plate())
