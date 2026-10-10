# AI Context: Photo Share

## Purpose and scope

Build a beginner-friendly local photo-sharing web app. Registered users can upload one image with a caption and view a shared feed. Do not add search, follows, profiles, direct messages, hashtags, stories, password resets, or public feed access.

## Stack and storage

- Python, Flask, Peewee, and SQLite.
- Use a local SQLite database (for example, `photo_share.db`).
- Save uploaded image files directly in the project-root `uploads/` directory: `./uploads/`.
- Store only each generated image filename in the database; never store the file itself in SQLite.
- Do not commit the database or uploaded files to Git.

## Agreed product decisions

- Registration requires `username`, `email`, and `password`.
- Both username and email are unique.
- Login uses username and password.
- Passwords must be stored only as Werkzeug password hashes.
- After successful registration, log the new user in and redirect to the feed.
- Captions are required short text, maximum 500 characters.
- Accept only `.jpg`, `.jpeg`, and `.png` images, up to 5 MB.
- Generate a safe, unique filename; do not trust or reuse the uploaded filename.

## Data model

- `User`: `id`, unique `username`, unique `email`, hashed `password`.
- `Post`: `id`, unique `image` filename, `caption`, required `user` foreign key, `created_at`.
- `Like`: `id`, required `user` and `post` foreign keys, unique `(user, post)` pair. Create this table now, but do not add like UI/route until the essential app works.
- Enable SQLite foreign keys. Deleting a post must cascade-delete its likes.

## Routes and screens

| Endpoint | URL | Methods | Access | Result |
| --- | --- | --- | --- | --- |
| `login` | `/` | GET, POST | Public | Login screen; logged-in users go to feed. |
| `register` | `/register` | GET, POST | Public | Register, create session, go to feed. |
| `logout` | `/logout` | GET | Logged in | Clear session, go to login. |
| `post_list` | `/posts` | GET | Logged in | Shared feed, newest first. |
| `create_post` | `/posts/new` | GET, POST | Logged in | Upload one image and caption. |
| `post_detail` | `/posts/<int:post_id>` | GET | Logged in | One post or 404. |
| uploads | `/uploads/<filename>` | GET | Logged in | Serve a saved image safely. |

Protected routes redirect unauthenticated users to `login`. The shared layout is `templates/base.html`; all pages extend it. Templates are `login.html`, `register.html`, `posts/list.html`, `posts/new.html`, and `posts/detail.html`.

## Essential behavior

- Feed shows every post, newest first: image, caption, username, and posted time.
- Clicking an image opens its detail page.
- Upload validation errors stay on the upload page; successful POSTs redirect to the feed.
- Login failures say only “Invalid username or password.”
- Registration failures clearly identify duplicate username or email.
- Use the Flask session to store the current user id.

## Later only

Likes, comments, editing captions, and deleting posts are later work. Do not implement them before registration, login, upload, feed, and detail pages work.
