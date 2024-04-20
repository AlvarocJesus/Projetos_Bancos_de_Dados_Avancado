-- username: alvimcoelhojesus
-- password: Wz5wyAvFghP6DCPs
-- mongodb+srv://alvimcoelhojesus:<password>@projeto2documentstore.bv2jjzy.mongodb.net/

-- 1. Listar todos os cursos oferecidos por um determinado departamento
db.departamento.findAll({}, { columnName: cursos })

-- 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre

