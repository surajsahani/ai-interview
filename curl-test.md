# API test command

This document provides example commands for using the curl test API interface.

## User Management API

### create user

```bash
# Create new user
curl -X POST http://localhost:8000/api/v1/user \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "john_doe",
    "password": "secure_password123",
    "email": "john.doe@example.com",
    "staff_id": "EMP001",
    "role": 1
  }'

# Expected successful response::
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "user_name": "john_doe",
#     "staff_id": "EMP001",
#     "email": "john.doe@example.com",
#     "status": 0,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }

# Error response (email already registered):
# {
#   "code": "409",
#   "message": "Email already registered",
#   "data": null
# }
```

### 获取用户详情

```bash
# Get user details
curl -X GET http://localhost:8000/api/v1/user/d772d20f-fce9-4340-9c6b-b34dabfc3fe6  

# Expected successful response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "d772d20f-fce9-4340-9c6b-b34dabfc3fe6",
#     "user_name": "john_doe",
#     "staff_id": "EMP001",
#     "email": "john.doe@example.com",
#     "status": 0,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }

# Error Response (Not Found):
# {
#   "code": "404",
#   "message": "User not found",
#   "data": null
# }
```

### Get user list

```bash
# Get user list (pagination)
curl -X GET "http://localhost:8000/api/v1/user?skip=0&limit=10"

# Expected successful response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "user_id": "550e8400-e29b-41d4-a716-446655440000",
#       "user_name": "john_doe",
#       "staff_id": "EMP001",
#       "email": "john.doe@example.com",
#       "status": 0,
#       "role": 1,
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... 更多用户
#   ]
# }
```

### 更新用户

```bash
# Update user
curl -X PUT http://localhost:8000/api/v1/user/d772d20f-fce9-4340-9c6b-b34dabfc3fe6 \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "john_smith",
    "email": "john.smith@example.com",
    "status": 1
  }'

# Expected successful response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "user_name": "john_smith",
#     "staff_id": "EMP001",
#     "email": "john.smith@example.com",
#     "status": 1,
#     "role": 1,
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### Delete user

```bash
# Delete user
curl -X DELETE http://localhost:8000/api/v1/user/550e8400-e29b-41d4-a716-446655440000

# Expected successful response::
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

## Job Management API

### Create a job

```bash
# Create new position
curl -X POST http://localhost:8000/api/v1/job \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Front-end development engineer",
    "job_description": "Responsible for the front-end development of the companys products, using the React technology stack to implement user interfaces and interactive functions",
    "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
    "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"]
  }'

# Expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "Front-end development engineer",
#     "job_description": "Responsible for the front-end development of the company's products, using the React technology stack to implement user interfaces and interactive functions",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#     "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### Get job details

```bash
# Get job details
curl -X GET http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000

# Expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "Front-end development engineer",
#     "job_description": "Responsible for the front-end development of the company's products, using the React technology stack to implement user interfaces and interactive functions",",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#     "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### Get job listings

```bash
# Get job list (paginated)
curl -X GET "http://localhost:8000/api/v1/job?skip=0&limit=10"

# Expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "job_id": "550e8400-e29b-41d4-a716-446655440000",
#       "job_title": "Front-end Development Engineer",
#       "job_description": "Responsible for the front-end development of the company's products, using the React technology stack to implement user interfaces and interactive functions",,
#       "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#       "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"],
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... More jobs
#   ]
# }
```

### Update job

```bash
# Update job information
curl -X PUT http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior front-end development engineer",
    "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Redux", "Next.js"]
  }'

# Expected response::
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "job_id": "550e8400-e29b-41d4-a716-446655440000",
#     "job_title": "Senior front-end development engineer",
#     "job_description": "Responsible for the front-end development of the company's products, using the React technology stack to implement user interfaces and interactive functions",
#     "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Redux", "Next.js"],
#     "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"],
#     "create_date": "2024-03-20T10:00:00.000Z"
#   }
# }
```

### Delete job

```bash
# Delete job
curl -X DELETE http://localhost:8000/api/v1/job/550e8400-e29b-41d4-a716-446655440000

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### Search jobs

```bash
# Search jobs
curl -X GET "http://localhost:8000/api/v1/job/search/前端?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "job_id": "550e8400-e29b-41d4-a716-446655440000",
#       "job_title": "Front-end development engineer",
#       "job_description": "Responsible for the front-end development of the company's products, using the React technology stack to implement user interfaces and interactive functions",
#       "technical_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
#       "soft_skills": ["Teamwork", "Communication skills", "Problem solving skills"],
#       "create_date": "2024-03-20T10:00:00.000Z"
#     },
#     // ... More matching jobs
#   ]
# }
```

## Test Management API

### Create test

```bash
# Create test
curl -X POST http://localhost:8000/api/v1/test \
  -H "Content-Type: application/json" \
  -d '{
    "type": "coding",
    "language": "English",
    "difficulty": "medium",
    "job_id": "job001",
    "user_id": "user001",
    "examination_points": ["React", "JavaScript", "前端性能优化"],
    "test_time": 90
  }'

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "coding",
#     "language": "English",
#     "difficulty": "medium",
#     "status": "open",
#     "job_id": "job001",
#     "job_title": "Front-end development engineer",
#     "user_id": "user001",
#     "user_name": "Zhang San",
#     "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#     "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#     "test_time": 90,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": null
#   }
# }
```

### Get test details

```bash
# Get test details
curl -X GET http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "coding",
#     "language": "English",
#     "difficulty": "medium",
#     "status": "open",
#     "job_id": "job001",
#     "job_title": "Front-end development engineer",
#     "user_id": "user001",
#     "user_name": "Zhang San",
#     "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#     "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#     "test_time": 90,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": null
#   }
# }
```

### Get test list

```bash
# Get a list of tests (paginated)
curl -X GET "http://localhost:8000/api/v1/test?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "Front-end development engineer",
#       "user_id": "user001",
#       "user_name": "Zhang San",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... More tests
#   ]
# }
```

### update test

```bash
# update test
curl -X PUT http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "interview",
    "language": "Chinese",
    "difficulty": "hard",
    "status": "in_progress",
    "job_id": "job002",
    "user_id": "user002",
    "question_ids": ["q001", "q002", "q003", "q004"],
    "examination_points": ["React", "JavaScript", "Front-end performance optimization", "Component design"],
    "test_time": 120
  }'

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "test_id": "550e8400-e29b-41d4-a716-446655440000",
#     "activate_code": "1234567890",
#     "type": "interview",
#     "language": "Chinese",
#     "difficulty": "hard",
#     "status": "in_progress",
#     "job_id": "job002",
#     "job_title": "Backend development engineer",
#     "user_id": "user002",
#     "user_name": "John Doe",
#     "question_ids": ["q001", "q002", "q003", "q004"],
#     "examination_points": ["React", "JavaScript", "Front-end performance optimization", "Component design"],
#     "test_time": 120,
#     "create_date": "2024-03-20T10:00:00.000Z",
#     "start_date": "2024-03-20T10:00:00.000Z",
#     "expire_date": "2024-03-27T10:00:00.000Z",
#     "update_date": "2024-03-20T11:00:00.000Z"
#   }
# }
```

### Delete test

```bash
# Delete test
curl -X DELETE http://localhost:8000/api/v1/test/550e8400-e29b-41d4-a716-446655440000

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### Get test by user ID

```bash
# Get test by user ID
curl -X GET "http://localhost:8000/api/v1/test/user/user001?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "Front-end development engineer",
#       "user_id": "user001",
#       "user_name": "Zhang San",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", ""Front-end performance optimization"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... More tests by this user
#   ]
# }
```

### Get test by job ID

```bash
# Get test by job ID
curl -X GET "http://localhost:8000/api/v1/test/job/job001?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "前端开发工程师",
#       "user_id": "user001",
#       "user_name": "张三",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... More tests for this position
#   ]
# }
```

### Get tests based on status

```bash
# Get tests based on status
curl -X GET "http://localhost:8000/api/v1/test/status/open?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "Front-end development engineer",
#       "user_id": "user001",
#       "user_name": "Zhang San",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... More open tests
#   ]
# }
```

### Get tests based on type

```bash
# Get tests based on type
curl -X GET "http://localhost:8000/api/v1/test/type/coding?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "test_id": "550e8400-e29b-41d4-a716-446655440000",
#       "activate_code": "1234567890",
#       "type": "coding",
#       "language": "English",
#       "difficulty": "medium",
#       "status": "open",
#       "job_id": "job001",
#       "job_title": "Front-end development engineer",
#       "user_id": "user001",
#       "user_name": "Zhang San",
#       "question_ids": ["q001", "q002", "q003", "q004", "q005", "q006", "q007", "q008", "q009", "q010"],
#       "examination_points": ["React", "JavaScript", "Front-end performance optimization"],
#       "test_time": 90,
#       "create_date": "2024-03-20T10:00:00.000Z",
#       "start_date": "2024-03-20T10:00:00.000Z",
#       "expire_date": "2024-03-27T10:00:00.000Z",
#       "update_date": null
#     },
#     // ... More Programmatic Testing
#   ]
# }
```

## Error code description

- `400`: Validation error
- `404`: Resource not found
- `409`: Resource conflict (e.g. the mailbox is already registered)
- `422`: Invalid request format
- `500`: Server internal error 

## Issue Management API

### create question

```bash
# Create new question
curl -X POST http://localhost:8000/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is React’s Virtual DOM?",
    "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out which parts of the real DOM need to be updated, and finally updates only the parts that need to be updated, thereby improving performance.",
    "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
    "job_title": "Front-end Development Engineer",
    "language": "Chinese",
    "difficulty": "medium",
    "type": "short_answer"
  }'

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "What is React’s Virtual DOM?",
#     "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#     "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
#     "job_title": "Front-end development engineer",
#     "language": "Chinese",
#     "difficulty": "medium",
#     "type": "short_answer"
#   }
# }
```

### 获取问题详情

```bash
# Get problem details
curl -X GET http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "What is React’s Virtual DOM?",
#     "answer": Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#     "examination_points": ["React", "虚拟DOM", "Performance optimization"],
#     "job_title": "Front-end development engineer",
#     "language": "Chinese",
#     "difficulty": "medium",
#     "type": "short_answer"
#   }
# }
```

### 获取问题列表

```bash
# Get a list of questions (paginated)
curl -X GET "http://localhost:8000/api/v1/question?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "What is React’s Virtual DOM?",
#       "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#       "examination_points": ["React", "Virtual DOM", "Performance optimization"],
#       "job_title": "Front-end development engineer",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... More questions
#   ]
# }
```

### Update question

```bash
# Update question
curl -X PUT http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "question": "A detailed explanation of Reacts virtual DOM and its advantages",
    "difficulty": "hard",
    "examination_points": ["React", "Virtual DOM", "Performance optimization", "rendering mechanism"]
  }'

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "question_id": "550e8400-e29b-41d4-a716-446655440000",
#     "question": "A detailed explanation of React's virtual DOM and its advantages",
#     "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#     "examination_points": ["React", "Virtual DOM", "Performance optimization", "rendering mechanism"],
#     "job_title": "Front-end Development Engineer",
#     "language": "Chinese",
#     "difficulty": "hard",
#     "type": "short_answer"
#   }
# }
```

### delete question

```bash
# delete question
curl -X DELETE http://localhost:8000/api/v1/question/550e8400-e29b-41d4-a716-446655440000

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": {
#     "deleted": true
#   }
# }
```

### Search questions

```bash
# Search questions
curl -X GET "http://localhost:8000/api/v1/question/search/React?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "What is React’s Virtual DOM?",
#       "answer": Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#       "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
#       "job_title": "Front-end development engineer",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... More matching questions
#   ]
# }
```

### Get questions based on position

```bash
# Get questions based on position
curl -X GET "http://localhost:8000/api/v1/question/job/前端开发工程师?skip=0&limit=10"

# expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "What is React’s Virtual DOM?",
#       "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance.,"
#       "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
#       "job_title": "Front-end development engineer",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... More questions about this position
#   ]
# }
```

### Get questions based on difficulty

```bash
# Get questions based on difficulty
curl -X GET "http://localhost:8000/api/v1/question/difficulty/medium?skip=0&limit=10"

# Expected response::
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "What is React's Virtual DOM?",,
#       "answer": Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out the parts of the real DOM that need to be updated, and finally only updates the parts that need to be updated, thereby improving performance. ",
#       "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
#       "job_title": "Front-end development engineer",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... More medium difficulty questions
#   ]
# }
```

### Get questions by topic type

```bash
# Get questions by topic type
curl -X GET "http://localhost:8000/api/v1/question/type/short_answer?skip=0&limit=10"

# Expected response:
# {
#   "code": "0",
#   "message": "success",
#   "data": [
#     {
#       "question_id": "550e8400-e29b-41d4-a716-446655440000",
#       "question": "What is React's Virtual DOM?",
#       "answer": "Virtual DOM is a core concept of React. It is a lightweight copy of the real DOM. When the state of a component changes, React first updates it in the virtual DOM, then uses a diffing algorithm to find out which parts of the real DOM need to be updated, and finally updates only the parts that need to be updated, thereby improving performance.",,
#       "examination_points": ["React", "Virtual DOM", "Performance Optimization"],
#       "job_title": "Front-end development engineer",
#       "language": "Chinese",
#       "difficulty": "medium",
#       "type": "short_answer"
#     },
#     // ... More short answer questions
#   ]
# }
```

## Chat API

### Start chatting, called when the interview starts for the first time

```bash
curl -X POST http://localhost:8000/api/v1/chat/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "user123",
    "test_id": "test456",
    "job_title": "React Web Developer",
    "examination_points": "React, JavaScript, TypeScript, React Router, React State Management, Redux, React Hooks, React Context API, React Performance Optimization",
    "test_time": 3,
    "language": "English",
    "difficulty": "easy"
  }'
```

### Submit the questions answered by the user and return new messages from the interviewer

```bash
curl -X POST http://localhost:8000/api/v1/chat/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "user123",
    "test_id": "test456",
    "question_id": "question789",
    "user_answer": "React's virtual DOM is an in-memory data structure that represents the ideal state of the UI. When the application state changes, React first updates it in the virtual DOM, then compares the differences between the new and old virtual DOMs through the diffing algorithm, and finally applies only the differences to the actual DOM, thereby improving performance."
  }' 