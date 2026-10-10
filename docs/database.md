# Database design: Photo Share

This document describes the **SQLite** database for Photo Share, to be used with **Peewee**. Related docs: [requirements.md](requirements.md), [screens.md](screens.md), [routes.md](routes.md).

**What is stored in the database vs on disk**

- The database stores **text and numbers**: who the user is, captions, file names, likes.
- The actual **photo file** is saved in an `uploads/` folder. A post row only remembers the **file name**.

**How a person logs in**

- Register saves **username**, **email**, and **password**.
- Login uses **username** and **password**.
- Posts show **username** (the display name).

---

## List of tables

| Table (SQLite) | Peewee model | Build now? | Short purpose |
| --- | --- | --- | --- |
| `user` | `User` | Yes | One row = one account that can log in. |
| `post` | `Post` | Yes | One row = one photo + caption in the feed. |
| `like` | `Like` | Yes (table now; like button can wait) | One row = this user liked this post. |
| *(none)* | `Comment` | No | Add only if comments are built later. |

---

## Relationships (why tables connect)

```
User  1 --------<  Post     one user can create many posts
User  1 --------<  Like     one user can like many posts
Post  1 --------<  Like     one post can receive many likes
```

- **User → Post** is **one-to-many**. That is why `post` has a foreign key `user_id`.
- **User ↔ Post** for likes is **many-to-many**. We do not put “liked by” as a list inside `post`. We use a third table, `like`.

If a **post is deleted**, all **like** rows for that post are deleted too.

---

## Table: `user`

### Role (why this table is necessary)

The app requires registration and login. Flask must look up a person, check their password, and remember them in the session (`user.id`).

Without `user`:

- nobody could sign up or log in
- we would not know **who** created a post
- we could not show a username on the feed

### Columns

| Column name | Peewee type | SQL data type | Primary key | Foreign key | Unique | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | `AutoField` | `INTEGER` | **Yes** | | (PK) | Internal id. Saved in the Flask session after login. |
| `username` | `CharField` | `VARCHAR(80)` | | | **Yes** | Login name and name shown on posts. |
| `email` | `CharField` | `VARCHAR(255)` | | | **Yes** | Stored at registration. Not used to log in in this version. |
| `password` | `CharField` | `VARCHAR(255)` | | | | **Hashed** password only (Werkzeug). Never store the real password. |

In SQLite, Peewee will create this table as `user` (model name `User`).

### Constraints

- **Primary key:** `id`
- **Unique:** `username` (so “username already taken” works)
- **Unique:** `email` (so the same email is not used twice)

### Candidate indexes

- Unique index on `username` — every login looks up this column (`unique=True` already creates it).
- Unique index on `email` — same.

### Notes for this table

- Do **not** add a second “name” column. `username` is the name on posts.
- `password` must be long enough for a hash (`max_length=255`).

---

## Table: `post`

### Role (why this table is necessary)

The main screens are Create Post, Post List, and Post Details. Each published photo is one row.

Without `post`:

- there would be nothing to show in the feed
- `/posts/<id>` would have no record to load
- the caption and “who posted / when” would have nowhere to live

The **picture file** is not inside this table. Only the **file name** is stored (for example `a1b2c3.jpg`). Flask later serves `/uploads/a1b2c3.jpg`.

### Columns

| Column name | Peewee type | SQL data type | Primary key | Foreign key | Unique | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | `AutoField` | `INTEGER` | **Yes** | | (PK) | Used in the URL `/posts/<id>`. |
| `image` | `CharField` | `VARCHAR(255)` | | | **Yes** (recommended) | Saved file name on disk, not the user’s original file name. |
| `caption` | `CharField` or `TextField` | short text | | | | A few hundred characters. |
| `user` | `ForeignKeyField(User)` | `INTEGER` column `user_id` | | **Yes → `user.id`** | | Who posted this. One user, many posts. |
| `created_at` | `DateTimeField` | `DATETIME` | | | | When it was posted. Feed is newest first. |

### Constraints

- **Primary key:** `id`
- **Foreign key:** `user_id` → `user.id` (required; a post always has a poster)
- **Unique:** `image` so two posts do not share the same file name

### Candidate indexes

- `created_at` — Post List always sorts newest first.
- `user_id` — Peewee/SQLite usually index foreign keys; useful later for “posts by this user”.
- Unique on `image`.

### Notes for this table

- Do not store a `like_count` column. Count rows in `like` instead so the number cannot go stale.
- When deleting a post, also delete the file in `uploads/` if that is easy.

---

## Table: `like`

### Role (why this table is necessary)

A like is not only a number on the screen. The app must remember **who** liked **which post**:

- the same person may like a post **only once**
- later we can unlike by deleting that one row
- the like count is “how many rows exist for this post”

Without `like`, we could add +1 to a number, but we could not stop double-likes or know if the current user already liked it.

The like **button** can wait. Creating this table now is still useful so we do not redesign later.

### Columns

| Column name | Peewee type | SQL data type | Primary key | Foreign key | Unique | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | `AutoField` | `INTEGER` | **Yes** | | (PK) | Simple row id. |
| `user` | `ForeignKeyField(User)` | `INTEGER` `user_id` | | **Yes → `user.id`** | part of pair | Who liked. |
| `post` | `ForeignKeyField(Post)` | `INTEGER` `post_id` | | **Yes → `post.id`** | part of pair | Which post. |

No `created_at` on likes for now.

### Constraints

- **Primary key:** `id`
- **Foreign keys:** `user_id` → `user.id`, `post_id` → `post.id`
- **Unique together:** `(user_id, post_id)` — one like per user per post
- **On delete of a post:** `CASCADE` — like rows for that post are removed

### Candidate indexes

- Unique index on `(user_id, post_id)` — enforces the rule and speeds up “did this user already like this post?”
- `post_id` — counting likes for one post (often helped by the composite unique index)

### Notes for this table

- Deleting a **user** is out of scope. You may still set `on_delete='CASCADE'` on `like.user` so leftover likes do not remain if that changes later.

---

## Table we are not creating yet: comments

Comments are “if time permits.” When you add them, a `comment` table would need:

- `id` (PK)
- `user` (FK → `user.id`) — who wrote it
- `post` (FK → `post.id`) — which post
- `body` — the text
- `created_at`
- `on_delete='CASCADE'` on `post` so comments disappear with the post

Do not build this until likes (or the essential screens) work.

---

## Implementation considerations for Peewee

1. **SQLite file.** Use one file, for example `photo_share.db`. Give every model the same database (`Meta.database` or a small `BaseModel`).

2. **Create tables.** After models exist: `database.create_tables([User, Post, Like])`. Changing columns later is awkward in SQLite, so keep these three tables stable.

3. **`ForeignKeyField` vs `user_id`.** In Python you write `post.user` (a `User`). SQLite stores `user_id`. Both `Post.user == current_user` and `Post.user_id == current_user.id` work.

4. **Backref (optional).** `ForeignKeyField(User, backref='posts')` lets you use `user.posts`. Helpful, not required.

5. **CASCADE and SQLite.** On `Like.post` use `ForeignKeyField(Post, backref='likes', on_delete='CASCADE')`. SQLite ignores foreign keys unless you turn them on when the app starts:

   `PRAGMA foreign_keys = ON;`

   Peewee does not always do this for you.

6. **Unique like pair.** In the `Like` model `Meta`:

   `indexes = ((('user', 'post'), True),)`

   `True` means unique. If a second like is inserted, SQLite raises an integrity error. Check `exists()` first, or catch that error.

7. **`DateTimeField` default.** Use `default=datetime.datetime.now` **with no parentheses**. If you write `now()`, every post gets the time from when Python loaded the class, not the time of each insert.

8. **Password length.** Werkzeug hashes are long. Use `CharField(max_length=255)`, not a short field.

9. **Email and username.** Set `unique=True` on both `CharField`s. Compare usernames in a consistent way (for example strip spaces). Storing email in lowercase avoids duplicates like `A@x.com` and `a@x.com`.

10. **Do not commit secrets or uploads.** Gitignore `*.db` and the `uploads/` folder.

11. **Build order.** You can create all three tables immediately, but write Flask code in this order: `User` (register/login) → `Post` (upload/list/detail) → `Like` (button).

---

## How tables map to routes

| Route | Tables used |
| --- | --- |
| `POST /register` | Insert `user` |
| `POST /` (login) | Read `user` by `username` |
| `POST /posts/new` | Insert `post` (file saved on disk) |
| `GET /posts` | Read `post` joined to `user`, order by `created_at` descending |
| `GET /posts/<id>` | Read one `post` joined to `user` |
| Like (later) | Insert or delete `like`; `COUNT` rows per post |
