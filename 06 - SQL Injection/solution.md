# LAB 06 - SQL Injection

**N.B.** Remember to add the row `10.9.0.5  www.seed-server.com` to the */etc/hosts* file on the machine to reach the seed-server website.

## 3.1 - Task 1
Use `mysql -u root -pdees` to login inside mysql service of container mysql (10.9.0.6):
1. Execute `SHOW databases` to show available databases;
2. Select a database with `USE datatabase_name`;
3. Show available tables of selected DB with `SHOW tables`;
4. Show content of table with `SELECT * FROM table_name`.

```sql
SHOW databases;
USE sqllab_users;
SHOW tables;
SELECT * FROM credential;
```

## 3.2 - Task 2


### Task 2.1
Write `admin'#` inside the **Username** field. This will skip the password field and check only based on the provided username, commentin everything that comes after (in the SQL code).

The login will then be successful and will show us the employees data.

### Task 2.2
We will now trying to do the same but from a terminal.

We know we need to excape some characters:
- '(single quote) --> %27;
- " "(space) --> %20;
- #(hashtag) --> %23;

So we can now build our url which will be something like: 
```bash
curl 'www.seed-server.com/unsafe_home.php?username=admin%27%23'
```

### Task 2.3
Here we try to execute multiple queries separating them by using a semicolon (`;`).
So we put in the username field on the login page the below command:
```sql
admin'; UPDATE credential SET Salary=25000 WHERE Name = "Alice"#
```

However the PHP code has an implicit countermeasure that will cause this to fail; by using the `mysqli::query()` method we are asking the server to execute only **ONE** query, but we are giving **TWO**, so the server will return an error.

## 3.3 - Task 3

### Task 3.1
To achieve this we first log as alice with `alice` and `seedalice` or by exploiting SQL injection.
Then we want to put on the first field of the edit page, which in this case is the *Nickname* field the following text:
```sql
',salary=25000 where name="Alice"#
```

In this way, we are updating our salary.

### Task 3.2
As simple as to follow the preceding task, we modify it by writing:
```sql
',salary=1 where name="Boby"#
```

thus changing the condition to edit `Boby` profile.

### Task 3.3
As the last part of this task here, we first test the login of Boby with `Boby` and `seedboby`.
After checking that it works, we can then work from Alice perspective:
- we log in as Alice;
- looking at the code in *unsafe_edit_backend.php* we can see that `Phone Number` is placed after `password` when building the update query; we can take advantage of this flaw.
- we then put into the edit form, `' where name="boby"#` into the Phone Number field and the new password into the password field. Et voilà!

Now we are able to login into Boby profile with the new password.

**N.B.:** to be sure of inserting the password correctly inside the password field, we can change the type of the field from password to text from the devtools section of the page.

## Task 4
Testing the defense section before editing backend files we can notice that is vulnerable to SQL Injection as it shows us Admin data by only putting `admin';#` on the username field.

We can make it super secure!.

We rewrite this section:
```php
// do the query
// do the query
$result = $conn->query("SELECT id, name, eid, salary, ssn
                        FROM credential
                        WHERE name= '$input_uname' and Password= '$hashed_pwd'");
if ($result->num_rows > 0) {
  // only take the first row 
  $firstrow = $result->fetch_assoc();
  $id     = $firstrow["id"];
  $name   = $firstrow["name"];
  $eid    = $firstrow["eid"];
  $salary = $firstrow["salary"];
  $ssn    = $firstrow["ssn"];
}
```

to this:
```php
// Prepare the SQL statement to prevent SQL injection
$stmt = $conn->prepare("SELECT id, name, eid, salary, ssn
                        FROM credential
                        WHERE name= ? and Password= ?");
// Bind the parameters: two strings (ss)
$stmt->bind_param("ss", $input_uname, $hashed_pwd);
// Execute the statement
$stmt->execute(); 
// Get the result
// Bind the results from the query to PHP variables
$stmt->bind_result($id, $name, $eid, $salary, $ssn);
$stmt->fetch();
```