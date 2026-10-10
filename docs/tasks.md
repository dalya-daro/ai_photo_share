# Implementation Tasks: Photo Share

Complete tasks in this order. Do not start later tasks until the current task works.

## 1. Project setup

- [ ] Create the Flask app, templates directory, static assets if needed, project-root `uploads/` directory, and SQLite connection.
- [ ] Configure a secret key and a 5 MB request/upload limit.
- [ ] Add `.gitignore` entries for the database and uploaded images while retaining an empty `uploads/` placeholder if needed.
- [ ] Confirm the app can render a simple page locally.

## 2. Database models

- [ ] Add `User`, `Post`, and `Like` Peewee models.
- [ ] Enforce unique username, email, image filename, and the `(user, post)` like pair.
- [ ] Add required foreign keys and cascade deletion from `Post` to `Like`.
- [ ] Enable SQLite foreign keys and create the tables.

## 3. Shared layout and authentication

- [ ] Create `base.html` with flash messages and navigation appropriate to login state.
- [ ] Implement `/register`: username, email, password; hash password; auto-login on success.
- [ ] Implement `/`: username/password login; redirect authenticated visitors to `/posts`.
- [ ] Implement `/logout`: clear the session and redirect to `/`.
- [ ] Add a reusable login-required check for protected routes.

## 4. Upload a post

- [ ] Create `/posts/new` and `posts/new.html` with multipart form fields `photo` and `caption`.
- [ ] Require a file and a non-empty caption of 500 characters or fewer.
- [ ] Reject files over 5 MB and extensions other than `.jpg`, `.jpeg`, `.png`.
- [ ] Generate a unique safe filename, save it in `./uploads/`, then create the `Post` row.
- [ ] On success, redirect to `/posts`; on validation failure, stay on the form with a clear error.

## 5. Feed and detail

- [ ] Implement `/uploads/<filename>` with login protection and safe serving from `./uploads/`.
- [ ] Implement `/posts`, loading posts with their users and ordering newest first.
- [ ] Add an empty-feed message and a New post link.
- [ ] Implement `/posts/<int:post_id>`; show the post or return 404.
- [ ] Make feed images link to their detail page.

## 6. Verify essential flows

- [ ] Register a user and confirm automatic login.
- [ ] Confirm duplicate username and email are rejected.
- [ ] Confirm login/logout and protected-route redirects.
- [ ] Upload valid JPG, JPEG, and PNG files; verify invalid, missing, and oversized files are rejected.
- [ ] Confirm newest-first feed, detail page, and image access only while logged in.

## 7. Optional later work

- [ ] Add like/unlike using the existing `Like` table.
- [ ] Add comments only when requested.
- [ ] Add owner-only caption edits and post deletion; remove the saved image when deleting a post if practical.
