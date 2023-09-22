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
  after this command the changes will apply to database BUT KEEP IN MIND IF YOU ARE CHANGING THE TABLE NAME it will not just simply do the change it will drop the table and create a new table so in our case the user will not change to name users. migration will drop the user table and create a new table with name users so the new users table will be empty, without any committed data in it. IF you have a database with so many data it is not a great idea to change the table name. Now we have to seed that file again. IT's easy in our case becasue it was only two column(id, username) and 6 row (users in seed.py) to do it again repeat the commands above
  python3 seeds.py
  and our new table called users is there with users again.

- Migration 2: Add email column

  - Add a new column called "email" to the "user" table.
    add this to schema(models.py)
    email = Column(String(55))
    add this to repr
    - f"email={self.email}, " \
      then
      alembic revision --autogenerate -m 'added email column'
      alembic upgrade head

- Migration 3: Add a unique constraint(kisitlamna) on the username

  - You might run into an error here (feel free to save for last or skip). Take a look at this StackOverflow post for a hint:
    - https://stackoverflow.com/questions/30378233/sqlite-lack-of-alter-support-alembic-migration-failing-because-of-this-solutio
  - **Add a unique constraint on the "username" column in the "user" table so that two users cannot have the same username.**
  - Unique Constraint Docs: https://docs.sqlalchemy.org/en/14/core/constraints.html#unique-constraint

                Solution: in models.py
                username = Column(String, unique=True)
                alembic revision --autogenerate -m 'added unique username constraint'
                alembic upgrade head
                and we gor an error bc of using sqlite
                "    raise NotImplementedError

        NotImplementedError: No support for ALTER of constraints in SQLite dialect. Please refer to the batch mode feature which allows for SQLite migrations using a copy-and-move strategy."
        there is a work around them, to do that in the readme check the stackoverflow post above which says do couple things to fix

        1. go to migration > env.py
        2. find this part all the way towards to end:
           with connectable.connect() as connection:
           context.configure(
           connection=connection, target_metadata=target_metadata
           )
        3. add 'render_as_batch=True' to the very end of 'connection=connection, target_metadata=target_metadata' like so;
           with connectable.connect() as connection:
           context.configure(
           connection=connection, target_metadata=target_metadata, render_as_batch=True
           )
        4. alembic upgrade head again it's gonna give the same error
        5. we need to revert back here, revert back 1 that's gonna undo the email,
           alembic downgrade -1
           no longer have an email then we run alembic downgrade -1 again we'll go back to singular user tablename (we can even go back to the very beginning with alembic downgrade base command which took Tom to create user table step the first migration that is done)
           I code along with him so I did go back to the begonning
           we deleted all other migrations file except the create table one we go back becasue we downgrade and canceled other migrations
           We go back to create user table migration so we don't even have a table now called user in our DB
           with this new configuration we should be able to generate a new migration with this unique constraint and it should work now
        6. regenerate new migration
           alembic revision --autogenerate -m 'add email and unique username'
           FAILED
           we got rid pff the last migration version file too
           no versions left
           we generate again
           alembic revision --autogenerate -m 'add email and unique username'
           DONE we have a new versions file with new migration which will create our new table with alembic upgrade head command
           it created new table with email and unique username

        Not: he said it is better to start over with the new configuration

        7. Let's test out if the constraint work
           seed.py add one of the username twice and try to populate our table with those info and lets see what happens run python3 seeds.py to populate db
           we got an error and its not population our db
           UNIQUE constraint failed: user.username
           unique username constraints work

        8. let's change back to those usernames to unique again and populate our db (make table)
           python3 seeds.py
           our db/table ia populated with username and email

    .

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
