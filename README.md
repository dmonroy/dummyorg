# Sample Project: REST api for organization management


1. Install requirements

```
pip install -r requirements.txt
```

2. Create a database

```
psql -U postgres -h localhost org -c 'CREATE DATABASE org'
```

3. Initialize the database

```
psql -U postgres -h localhost org -f org.sql
```

4. Start the service

```
python org.py
```

5. Play with the service

Service runs on port 8000 by default.

- Organizations endpoint: http://localhost:8000/api/v1/organizations
- API docs: http://localhost:8000/api/doc