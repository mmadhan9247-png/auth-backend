# Flask Authentication API Testing Guide

## Start the Server
```bash
cd backend
python run.py
```

## API Endpoints

### 1. Check Server Status
```bash
curl http://localhost:5000/
```

### 2. Register a New User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 4. Get Current User (Requires Token)
```bash
# Replace YOUR_TOKEN_HERE with the access token from login response
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Protected Dashboard (Requires Token)
```bash
curl -X GET http://localhost:5000/api/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 6. Protected Profile (Requires Token)
```bash
curl -X GET http://localhost:5000/api/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 7. Admin Panel (Admin Only)
```bash
# First register/login as admin user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'

# Then access admin panel
curl -X GET http://localhost:5000/api/admin \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

### 8. Test Invalid Token
```bash
curl -X GET http://localhost:5000/api/dashboard \
  -H "Authorization: Bearer invalid_token"
```

### 9. Test Without Token
```bash
curl -X GET http://localhost:5000/api/dashboard
```

## Expected Responses

### Registration Success (201)
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-...",
    "is_active": true
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Login Success (200)
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-...",
    "is_active": true
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Protected Route Success (200)
```json
{
  "message": "Welcome to your dashboard, testuser!",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-...",
    "is_active": true
  },
  "data": {
    "total_users": 1,
    "active_users": 1
  }
}
```

### Error Responses

#### Missing Token (401)
```json
{
  "msg": "Missing Authorization Header"
}
```

#### Invalid Token (422)
```json
{
  "msg": "Invalid token"
}
```

#### Invalid Credentials (401)
```json
{
  "error": "Invalid username or password"
}
```

## Automated Testing

Run the automated test script:
```bash
cd backend
python test_api.py
```

This will test all endpoints automatically and show you the results.

## Testing with Postman

1. Import the following collection into Postman:
   - Base URL: `http://localhost:5000`
   - Create requests for each endpoint listed above
   - Set headers: `Content-Type: application/json`
   - For protected routes, add `Authorization: Bearer {{token}}`
   - Use environment variables for tokens

## Common Issues

1. **Server not running**: Make sure `python run.py` is running and shows no errors
2. **Port already in use**: Change port in `run.py` or kill existing process
3. **Database errors**: Delete `app.db` file to reset database
4. **Import errors**: Make sure you're in the virtual environment: `.venv\Scripts\Activate.ps1`
