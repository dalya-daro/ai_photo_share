# Routing design: Photo Share

This document maps **Flask URLs** to views, HTTP methods, and templates. Screens and transitions are in [screens.md](screens.md).

Use one shared layout: `templates/base.html`.

Suggested view functions live in `app.py` (or a `views` module). Endpoint names below are what you pass to `url_for(...)`.

---

## Route list

| Endpoint (`url_for`) | URL | HTTP methods | Login? | Template | View function |
| --- | --- | --- | --- | --- | --- |
| `login` | `/` | GET, POST | No | `login.html` | `login()` |
| `register` | `/register` | GET, POST | No | `register.html` | `register()` |
| `logout` | `/logout` | GET | Yes | none (redirect) | `logout()` |
| `post_list` | `/posts` | GET | Yes | `posts/list.html` | `post_list()` |
| `create_post` | `/posts/new` | GET, POST | Yes | `posts/new.html` | `create_post()` |
| `post_detail` | `/posts/<int:post_id>` | GET | Yes | `posts/detail.html` | `post_detail(post_id)` |

**Public routes:** `login`, `register`  
**Protected routes:** `logout`, `post_list`, `create_post`, `post_detail`  
If a protected route is opened without a session, `redirect(url_for("login"))`.

Uploaded image files are **not** HTML routes in the table above. Serve them with Flask, for example `/uploads/<filename>` → `send_from_directory` (GET, login required). Template: none.

---

## Each route

### `GET /` and `POST /` — Login

| Item | Value |
| --- | --- |
| Endpoint | `login` |
| Login required? | No |
| Template | `login.html` |

- **GET:** show the login form. If the user is already logged in, `redirect(url_for("post_list"))`.
- **POST:** read `username` and `password`. If they match, save the user id in `session`, then `redirect(url_for("post_list"))`. If they do not match, render `login.html` again (same URL, error message).

---

### `GET /register` and `POST /register` — User Registration

| Item | Value |
| --- | --- |
| Endpoint | `register` |
| Login required? | No |
| Template | `register.html` |

- **GET:** show the sign-up form. If already logged in, `redirect(url_for("post_list"))`.
- **POST:** create the user (hashed password). On success, log them in (`session`) and `redirect(url_for("post_list"))`. On failure, render `register.html` again.

---

### `GET /logout` — Logout

| Item | Value |
| --- | --- |
| Endpoint | `logout` |
| Login required? | Yes (if not logged in, still send them to Login) |
| Template | none |

- Clear the session (`session.clear()`).
- `redirect(url_for("login"))`.

GET is enough for a beginner app (a header link). No page is rendered.

---

### `GET /posts` — Post List (Top)

| Item | Value |
| --- | --- |
| Endpoint | `post_list` |
| Login required? | Yes |
| Template | `posts/list.html` |

- Load posts, **newest first**, with each post’s username.
- Render the list. The **New post** button should be `url_for("create_post")`.
- Each photo (or post title) links to `url_for("post_detail", post_id=post.id)`.

---

### `GET /posts/new` and `POST /posts/new` — Create Post

| Item | Value |
| --- | --- |
| Endpoint | `create_post` |
| Login required? | Yes |
| Template | `posts/new.html` |

- **GET:** show the upload form.
- **POST:** read the file and caption. Save the file, save the `Post` row. Then `redirect(url_for("post_list"))` (Post/Redirect/Get, so refresh does not upload twice).
- On validation error (not jpg/png, over 5 MB, missing file): render `posts/new.html` again with an error. Do not redirect.

HTML form must use `method="post"` and `enctype="multipart/form-data"`.

---

### `GET /posts/<int:post_id>` — Post Details

| Item | Value |
| --- | --- |
| Endpoint | `post_detail` |
| Login required? | Yes |
| Template | `posts/detail.html` |

- Load one post by `post_id`. If missing, abort 404.
- Render photo, caption, username, time.
- **Back to list** is `url_for("post_list")`.

Use `<int:post_id>` so Flask only accepts numbers (not `/posts/new` as an id). Define **`/posts/new` before** this route if both are in the same file, or keep the `int` converter so `new` cannot match.

---

## Redirects (Flask)

These are the transitions from [screens.md](screens.md), written as redirects.

| From | When | To |
| --- | --- | --- |
| `login` POST | Password is correct | `post_list` |
| `register` POST | New user saved | `post_list` (session set) |
| `logout` GET | Session cleared | `login` |
| `create_post` POST | Post saved | `post_list` |
| any protected view | No session | `login` |
| `login` or `register` GET | Already logged in | `post_list` |

---

## Templates to create

```
templates/
  base.html
  login.html
  register.html
  posts/
    list.html
    new.html
    detail.html
```

---

## Later routes (only if time permits)

Keep using the same pages when possible. Add POST handlers; avoid extra URLs unless needed.

| Endpoint | URL | Methods | Purpose |
| --- | --- | --- | --- |
| `like_post` | `/posts/<int:post_id>/like` | POST | Like (or unlike) then redirect back |
| `add_comment` | `/posts/<int:post_id>/comments` | POST | Save comment, redirect to `post_detail` |
| `edit_post` | `/posts/<int:post_id>/edit` | GET, POST | Only if inline edit on the list is too hard |
| `delete_post` | `/posts/<int:post_id>/delete` | POST | Owner only; then redirect to `post_list` |

Do not implement these until the six routes in the main table work.
