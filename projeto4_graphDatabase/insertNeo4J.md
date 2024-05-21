# Formatacao dados para Neo4J

## Delete dos dados

```cypher
MATCH (n:classroom) DELETE n;
MATCH (n:department) DELETE n;
MATCH p=()-[:PREREQ]->() DELETE p;
MATCH (n:course) DELETE n;
MATCH (n:instructor) DELETE n;
MATCH (n:section) DELETE n;
MATCH (n:student) DELETE n;
MATCH p=()-[:TEACHES]->() DELETE p;
MATCH p=()-[:ADVISOR]->() DELETE p;
```

## Inserts Tabelas

### Instructor -> OK

(:instructor { id: , name: , dept_name: , salary: })

```cypher
create
(:instructor { id: '10101', name: 'Srinivasan', dept_name: 'Comp. Sci.', salary: '65000'}),
(:instructor { id: '12121', name: 'Wu', dept_name: 'Finance', salary: '90000'}),
(:instructor { id: '15151', name: 'Mozart', dept_name: 'Music', salary: '40000'}),
(:instructor { id: '22222', name: 'Einstein', dept_name: 'Physics', salary: '95000'}),
(:instructor { id: '32343', name: 'El Said', dept_name: 'History', salary: '60000'}),
(:instructor { id: '33456', name: 'Gold', dept_name: 'Physics', salary: '87000'}),
(:instructor { id: '45565', name: 'Katz', dept_name: 'Comp. Sci.', salary: '75000'}),
(:instructor { id: '58583', name: 'Califieri', dept_name: 'History', salary: '62000'}),
(:instructor { id: '76543', name: 'Singh', dept_name: 'Finance', salary: '80000'}),
(:instructor { id: '76766', name: 'Crick', dept_name: 'Biology', salary: '72000'}),
(:instructor { id: '83821', name: 'Brandt', dept_name: 'Comp. Sci.', salary: '92000'}),
(:instructor { id: '98345', name: 'Kim', dept_name: 'Elec. Eng.', salary: '80000'}),
```

### Student -> OK

(:student {id: , name: , tot_cred: })

```cypher
create
(:student {id: '00128', name: 'Zhang', dept_name: 'Comp. Sci.', tot_cred: '102'}),
(:student {id: '12345', name: 'Shankar', dept_name: 'Comp. Sci.', tot_cred: '32'}),
(:student {id: '19991', name: 'Brandt', dept_name: 'History', tot_cred: '80'}),
(:student {id: '23121', name: 'Chavez', dept_name: 'Finance', tot_cred: '110'}),
(:student {id: '44553', name: 'Peltier', dept_name: 'Physics', tot_cred: '56'}),
(:student {id: '45678', name: 'Levy', dept_name: 'Physics', tot_cred: '46'}),
(:student {id: '54321', name: 'Williams', dept_name: 'Comp. Sci.', tot_cred: '54'}),
(:student {id: '55739', name: 'Sanchez', dept_name: 'Music', tot_cred: '38'}),
(:student {id: '70557', name: 'Snow', dept_name: 'Physics', tot_cred: '0'}),
(:student {id: '76543', name: 'Brown', dept_name: 'Comp. Sci.', tot_cred: '58'}),
(:student {id: '76653', name: 'Aoi', dept_name: 'Elec. Eng.', tot_cred: '60'}),
(:student {id: '98765', name: 'Bourikas', dept_name: 'Elec. Eng.', tot_cred: '98'}),
(:student {id: '98988', name: 'Tanaka', dept_name: 'Biology', tot_cred: '120'}),
```

### Course -> OK

(:course { course_id: , credits: , dept_name: , title: })

```cypher
create
(:course { course_id: 'BIO-101', title: 'Intro. to Biology', dept_name: 'Biology', credits: '4'}),
(:course { course_id: 'BIO-301', title: 'Genetics', dept_name: 'Biology', credits: '4'}),
(:course { course_id: 'BIO-399', title: 'Computational Biology', dept_name: 'Biology',credits: '3'}),
(:course { course_id: 'CS-101', title: 'Intro. to Computer Science', dept_name: 'Comp. Sci.', credits: '4'}),
(:course { course_id: 'CS-190', title: 'Game Design', dept_name: 'Comp. Sci.', credits: '4'}),
(:course { course_id: 'CS-315', title: 'Robotics', dept_name: 'Comp. Sci.', credits: '3'}),
(:course { course_id: 'CS-319', title: 'Image Processing', dept_name: 'Comp. Sci.', credits: '3'}),
(:course { course_id: 'CS-347', title: 'Database System Concepts', dept_name: 'Comp. Sci.', credits: '3'}),
(:course { course_id: 'EE-181', title: 'Intro. to Digital Systems', dept_name: 'Elec. Eng.', credits: '3'}),
(:course { course_id: 'FIN-201', title: 'Investment Banking', dept_name: 'Finance', credits: '3'}),
(:course { course_id: 'HIS-351', title: 'World History', dept_name: 'History', credits: '3'}),
(:course { course_id: 'MU-199', title: 'Music Video Production', dept_name: 'Music', credits: '3'}),
(:course { course_id: 'PHY-101', title: 'Physical Principles', dept_name: 'Physics', credits: '4'}),
```

### Classroom -> OK

(:classroom { building: , room_number: , capacity: })

```cypher
create
(:classroom { building: 'Packard', room_number: '101', capacity: '500'}),
(:classroom { building: 'Painter', room_number: '514', capacity: '10'}),
(:classroom { building: 'Taylor', room_number: '3128', capacity: '70'}),
(:classroom { building: 'Watson', room_number: '100', capacity: '30'}),
(:classroom { building: 'Watson', room_number: '120', capacity: '50'}),
```

### Department -> OK

(:department { dept_name: , budget: , building: })

```cypher
create
(:department { dept_name: 'Biology', building: 'Watson', budget: '90000'}),
(:department { dept_name: 'Comp. Sci.', building: 'Taylor', budget: '100000'}),
(:department { dept_name: 'Elec. Eng.', building: 'Taylor', budget: '85000'}),
(:department { dept_name: 'Finance', building: 'Painter', budget: '120000'}),
(:department { dept_name: 'History', building: 'Painter', budget: '50000'}),
(:department { dept_name: 'Music', building: 'Packard', budget: '80000'}),
(:department { dept_name: 'Physics', building: 'Watson', budget: '70000'}),
```

### Time_Slot -> OK

(:time_slot { day: , start_ht: , start_min: , time_slot_id: , end_hr: , end_min: })

```cypher
create
(:time_slot { time_slot_id: 'A', day: 'M', start_ht: '8', start_min: '0', end_hr: '8', end_min: '50' }),
(:time_slot { time_slot_id: 'A', day: 'W', start_ht: '8', start_min: '0', end_hr: '8', end_min: '50' }),
(:time_slot { time_slot_id: 'A', day: 'F', start_ht: '8', start_min: '0', end_hr: '8', end_min: '50' }),
(:time_slot { time_slot_id: 'B', day: 'M', start_ht: '9', start_min: '0', end_hr: '9', end_min: '50' }),
(:time_slot { time_slot_id: 'B', day: 'W', start_ht: '9', start_min: '0', end_hr: '9', end_min: '50' }),
(:time_slot { time_slot_id: 'B', day: 'F', start_ht: '9', start_min: '0', end_hr: '9', end_min: '50' }),
(:time_slot { time_slot_id: 'C', day: 'M', start_ht: '11', start_min: '0', end_hr: '11', end_min: '50' }),
(:time_slot { time_slot_id: 'C', day: 'W', start_ht: '11', start_min: '0', end_hr: '11', end_min: '50' }),
(:time_slot { time_slot_id: 'C', day: 'F', start_ht: '11', start_min: '0', end_hr: '11', end_min: '50' }),
(:time_slot { time_slot_id: 'D', day: 'M', start_ht: '13', start_min: '0', end_hr: '13', end_min: '50' }),
(:time_slot { time_slot_id: 'D', day: 'W', start_ht: '13', start_min: '0', end_hr: '13', end_min: '50' }),
(:time_slot { time_slot_id: 'D', day: 'F', start_ht: '13', start_min: '0', end_hr: '13', end_min: '50' }),
(:time_slot { time_slot_id: 'E', day: 'T', start_ht: '10', start_min: '30', end_hr: '11', end_min: '45' }),
(:time_slot { time_slot_id: 'E', day: 'R', start_ht: '10', start_min: '30', end_hr: '11', end_min: '45' }),
(:time_slot { time_slot_id: 'F', day: 'T', start_ht: '14', start_min: '30', end_hr: '15', end_min: '45' }),
(:time_slot { time_slot_id: 'F', day: 'R', start_ht: '14', start_min: '30', end_hr: '15', end_min: '45' }),
(:time_slot { time_slot_id: 'G', day: 'M', start_ht: '16', start_min: '0', end_hr: '16', end_min: '50' }),
(:time_slot { time_slot_id: 'G', day: 'W', start_ht: '16', start_min: '0', end_hr: '16', end_min: '50' }),
(:time_slot { time_slot_id: 'G', day: 'F', start_ht: '16', start_min: '0', end_hr: '16', end_min: '50' }),
(:time_slot { time_slot_id: 'H', day: 'W', start_ht: '10', start_min: '0', end_hr: '12', end_min: '30' }),
```

### Section -> Ok

```cypher
create
(:section { course_id: 'BIO-101', sec_id: 1, semester: 'Summer', year: 2017, building: 'Painter', room_number: 514, time_slot_id: 'B' }),
(:section { course_id: 'BIO-301', sec_id: 1, semester: 'Summer', year: 2018, building: 'Painter', room_number: 514, time_slot_id: 'A' }),
(:section { course_id: 'CS-101', sec_id: 1, semester: 'Fall', year: 2017, building: 'Packard', room_number: 101, time_slot_id: 'H' }),
(:section { course_id: 'CS-101', sec_id: 1, semester: 'Spring', year: 2018, building: 'Packard', room_number: 101, time_slot_id: 'F' }),
(:section { course_id: 'CS-190', sec_id: 1, semester: 'Spring', year: 2017, building: 'Taylor', room_number: 3128, time_slot_id: 'E' }),
(:section { course_id: 'CS-190', sec_id: 2, semester: 'Spring', year: 2017, building: 'Taylor', room_number: 3128, time_slot_id: 'A' }),
(:section { course_id: 'CS-315', sec_id: 1, semester: 'Spring', year: 2018, building: 'Watson', room_number: 120, time_slot_id: 'D' }),
(:section { course_id: 'CS-319', sec_id: 1, semester: 'Spring', year: 2018, building: 'Watson', room_number: 100, time_slot_id: 'B' }),
(:section { course_id: 'CS-319', sec_id: 2, semester: 'Spring', year: 2018, building: 'Taylor', room_number: 3128, time_slot_id: 'C' }),
(:section { course_id: 'CS-347', sec_id: 1, semester: 'Fall', year: 2017, building: 'Taylor', room_number: 3128, time_slot_id: 'A' }),
(:section { course_id: 'EE-181', sec_id: 1, semester: 'Spring', year: 2017, building: 'Taylor', room_number: 3128, time_slot_id: 'C' }),
(:section { course_id: 'FIN-201', sec_id: 1, semester: 'Spring', year: 2018, building: 'Packard', room_number: 101, time_slot_id: 'B' }),
(:section { course_id: 'HIS-351', sec_id: 1, semester: 'Spring', year: 2018, building: 'Painter', room_number: 514, time_slot_id: 'C' }),
(:section { course_id: 'MU-199', sec_id: 1, semester: 'Spring', year: 2018, building: 'Packard', room_number: 101, time_slot_id: 'D' }),
(:section { course_id: 'PHY-101', sec_id: 1, semester: 'Fall', year: 2017, building: 'Watson', room_number: 100, time_slot_id: 'A' }),
```

## Create Relações

### Exemplo

```cypher
match (i:instructor {id: "Meu id"}),(s:student {id: "Meu id"})
create
(i)-[:ADVISOR]->(s)
```

### Advisor -> Ok

```cypher
match (s:student { id: '00128' }), (i:instructor { id: '45565' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '12345' }), (i:instructor { id: '10101' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '23121' }), (i:instructor { id: '76543' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '44553' }), (i:instructor { id: '22222' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '45678' }), (i:instructor { id: '22222' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '76543' }), (i:instructor { id: '45565' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '76653' }), (i:instructor { id: '98345' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '98765' }), (i:instructor { id: '98345' }) create (i)-[:ADVISOR]->(s);
match (s:student { id: '98988' }), (i:instructor { id: '76766' }) create (i)-[:ADVISOR]->(s);
```

### Prereq -> Ok

```cypher
match (c:course { course_id: 'BIO-301' }), (c2:course { course_id: 'BIO-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'BIO-399' }), (c2:course { course_id: 'BIO-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'CS-190' }), (c2:course { course_id: 'CS-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'CS-315' }), (c2:course { course_id: 'CS-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'CS-319' }), (c2:course { course_id: 'CS-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'CS-347' }), (c2:course { course_id: 'CS-101' }) create (c)-[:PREREQ]->(c2);
match (c:course { course_id: 'EE-181' }), (c2:course { course_id: 'PHY-101' }) create (c)-[:PREREQ]->(c2);
```

### Teaches

```cypher

```

### Takes -> Ok

```cypher
match (s:student { id: '00128' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '00128' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-347' })
create (s)-[:TAKES { grade: 'A-'}]->(s2);

match (s:student { id: '12345' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'C'}]->(s2);

match (s:student { id: '12345' }), (s2:section { sec_id: 2, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '12345' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-315' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '12345' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-347' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '19991' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'HIS-351' })
create (s)-[:TAKES { grade: 'B'}]->(s2);

match (s:student { id: '23121' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'FIN-201' })
create (s)-[:TAKES { grade: 'C+'}]->(s2);

match (s:student { id: '44553' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'PHY-101' })
create (s)-[:TAKES { grade: 'B-'}]->(s2);

match (s:student { id: '45678' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'F'}]->(s2);

match (s:student { id: '45678' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'B+'}]->(s2);

match (s:student { id: '45678' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (s)-[:TAKES { grade: 'B'}]->(s2);

match (s:student { id: '54321' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'A-'}]->(s2);

match (s:student { id: '54321' }), (s2:section { sec_id: 2, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (s)-[:TAKES { grade: 'B+'}]->(s2);

match (s:student { id: '55739' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'MU-199' })
create (s)-[:TAKES { grade: 'A-'}]->(s2);

match (s:student { id: '76543' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '76543' }), (s2:section { sec_id: 2, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '76653' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2017 , course_id: 'EE-181' })
create (s)-[:TAKES { grade: 'C'}]->(s2);

match (s:student { id: '98765' }), (s2:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (s)-[:TAKES { grade: 'C-'}]->(s2);

match (s:student { id: '98765' }), (s2:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-315' })
create (s)-[:TAKES { grade: 'B'}]->(s2);

match (s:student { id: '98988' }), (s2:section { sec_id: 1, semester: 'Summer', year: 2017 , course_id: 'BIO-101' })
create (s)-[:TAKES { grade: 'A'}]->(s2);

match (s:student { id: '98988' }), (s2:section { sec_id: 1, semester: 'Summer', year: 2018 , course_id: 'BIO-301' })
create (s)-[:TAKES { grade: 'A'}]->(s2);
```

### Classroom - Section -> Ok

```cypher
match (c:classroom { building: 'Painter', room_number: '514' }), (s:section { sec_id: 1, semester: 'Summer', year: 2017 , course_id: 'BIO-101' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Painter', room_number: '514' }), (s:section { sec_id: 1, semester: 'Summer', year: 2018 , course_id: 'BIO-301' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Packard', room_number: '101' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Packard', room_number: '101' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-101' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Taylor', room_number: '3128' }), (s:section { sec_id: 1, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Taylor', room_number: '3128' }), (s:section { sec_id: 2, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Watson', room_number: '120' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-315' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Watson', room_number: '100' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Taylor', room_number: '3128' }), (s:section { sec_id: 2, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Taylor', room_number: '3128' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-347' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Taylor', room_number: '3128' }), (s:section { sec_id: 1, semester: 'Spring', year: 2017 , course_id: 'EE-181' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Packard', room_number: '101' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'FIN-201' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Painter', room_number: '514' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'HIS-351' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Packard', room_number: '101' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'MU-199' })
create (c)-[:CLASSSECTION]->(s);

match (c:classroom { building: 'Watson', room_number: '100' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'PHY-101' })
create (c)-[:CLASSSECTION]->(s);
```

### Course - Section -> Ok

```cypher
match (c:course { course_id: 'BIO-101' }), (s:section { sec_id: 1, semester: 'Summer', year: 2017 , course_id: 'BIO-101' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'BIO-301' }), (s:section { sec_id: 1, semester: 'Summer', year: 2018 , course_id: 'BIO-301' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-101' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-101' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-101' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-101' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-190' }), (s:section { sec_id: 1, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-190' }), (s:section { sec_id: 2, semester: 'Spring', year: 2017 , course_id: 'CS-190' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-315' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-315' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-319' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-319' }), (s:section { sec_id: 2, semester: 'Spring', year: 2018 , course_id: 'CS-319' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'CS-347' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'CS-347' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'EE-181' }), (s:section { sec_id: 1, semester: 'Spring', year: 2017 , course_id: 'EE-181' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'FIN-201' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'FIN-201' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'HIS-351' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'HIS-351' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'MU-199' }), (s:section { sec_id: 1, semester: 'Spring', year: 2018 , course_id: 'MU-199' })
create (c)-[:COURSESECTION]->(s);

match (c:course { course_id: 'PHY-101' }), (s:section { sec_id: 1, semester: 'Fall', year: 2017 , course_id: 'PHY-101' })
create (c)-[:COURSESECTION]->(s);
```
