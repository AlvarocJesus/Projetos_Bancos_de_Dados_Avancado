# Projeto 2 - MongoDB

## Acessos ao mongodb atlas

username: alvimcoelhojesus
password: Wz5wyAvFghP6DCPs
mongodb+srv://alvimcoelhojesus:<password>@projeto2documentstore.bv2jjzy.mongodb.net/

## 1. Listar todos os cursos oferecidos por um determinado departamento

mongo.db.departamentos.find({ columnName: cursos })
departamnetos: { cursos: [ { ObjectId: 1, } ] }

cursos: { ObjectId: 1 }

## 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre

semestre: {
cursos: [
{
disciplinas: [
{
ObjectId: 1,
}
]
}
]
}

cursos: {
ObjectId: 1,
}

disciplinas: {
ObjectId: 1
}

## 3. Encontrar todos os estudantes que estão matriculados em um curso específico

cursos: {
objectId: 1,
nome_curso: "Engenharia de Software",
alunos: [
{
ObjectId: 1,
}
]
}

alunos: {
ObjectId: 1
}

## 4. Listar a média de salários de todos os professores em um determinado departamento

departamentos: {
professores: [
{
ObjectId: 1
}
]
}

professores: {
ObjectId: 1,
salario: 1000
}

## 5. Recuperar o número total de créditos obtidos por um estudante específico

estudantes: [
{
ObjectId: 1,
creditos: 100
}
]

## 6. Encontrar todas as disciplinas ministradas por um professor em um semestre específico

semestre: {
professor: [
disciplinas: [
{
ObjectId: 1
}
]
}

professores: {}

disciplinas: {}

cursos: {}

## 7. Listar todos os estudantes que têm um determinado professor como orientador

professores: {
alunos: [
{
ObjectId: 1
}
]
}

alunos: {
ObjectId: 1
}

## 8. Recuperar todas as salas de aula sem um curso associado

salas: {
cursos: [
{
ObjectId: 1
}
]
}

cursos: {
ObjectId: 1
}

## 9. Encontrar todos os pré-requisitos de um curso específico

cursos: {
pre_requisitos: [
{
ObjectId: 1
}
]
}

pre_requisitos: {
ObjectId: 1
}

## 10. Recuperar a quantidade de alunos orientados por cada professor

professores: {
alunos: [
{
ObjectId: 1
}
]
}

alunos: {
ObjectId: 1
}
