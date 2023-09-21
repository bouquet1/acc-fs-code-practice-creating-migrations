# acc-fs-code-practice-creating-migrations

## Instructions

Fork and clone this repository then `cd` into it.

In the terminal, run:

- `pipenv install && pipenv shell`
- `alembic upgrade head`
- `python3 seeds.py`

This will generate a `data.db` file (which we will update using migrations) and populate it with a few users that are instantiated in the `seeds.py` file.

## Alembic Commands Cheat Sheet

[Notion Link](https://furry-shrimp-4f0.notion.site/Alembic-Commands-Cheat-Sheet-1561ad0f713d43bfbb3f559a3e29ec03?pvs=25)

## Migration Deliverables

- Migration 1: Change user table to users
  First, go to our schema for those changes. models.py change tablename.
  use alembic to detect these changes and auto generate migration. so in terminal command
  alembic revision --autogenerate -m 'description of change'
  apply the changes to our DB
  alembic upgrade head
  after this command the changes will apply to database BUT KEEP IN MIND IF YOU ARE CHANGING THE TABLE NAME it will not just simply do the change it will drop the table and create a new table so in our case the user will not change to name users. migration will drop the user table and create a new table with name users so the new users table will be empty, without any committed data in it. IF you have a database with so many data it is not a great idea to change the table name. Now we have to seed that file again. IT's easy in our case becasue it was only two column(id, username) and 6 row (users in seed.py)

- Migration 2: Add email column
  - Add a new column called "email" to the "user" table.
- Migration 3: Add a unique constraint on the username
  - You might run into an error here (feel free to save for last or skip). Take a look at this StackOverflow post for a hint:
    - https://stackoverflow.com/questions/30378233/sqlite-lack-of-alter-support-alembic-migration-failing-because-of-this-solutio
  - Add a unique constraint on the "username" column in the "user" table so that two users cannot have the same username.
  - Unique Constraint Docs: https://docs.sqlalchemy.org/en/14/core/constraints.html#unique-constraint
- Migration 4: Add created_at and updated_at timestamps
  - Add "created_at" and "updated_at" timestamp columns to the "user" table to track creation and update times.
  - `func` - https://docs.sqlalchemy.org/en/14/core/functions.html#selected-known-functions
  - `server_default` - https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#fetching-server-generated-defaults
  - `onupdate` - https://docs.sqlalchemy.org/en/14/core/constraints.html#on-update-and-on-delete
  - Updated `__**repr__**` method:

```python
    def __repr__(self):
        return f"\n<User "\
            + f"id={self.id}," \
            + f"username={self.username}," \
            + f"email={self.email}," \
            + f"created_at={self.create_at}," \
            + f"updated_at={self.updated_at}," \
            + f" >"
```

- Migration 5: Add phone number column
  - Add a new column called "phone_number" to the "user" table to store user contact phone numbers.
- Migration 6: Add a new table, "Pet", that is based on the following:
  ![Pet Entity](https://raw.githubusercontent.com/codetombomb/acc-fs-code-practice-creating-migrations/main/images/pet-entity.png)
