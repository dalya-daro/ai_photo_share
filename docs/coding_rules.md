# Coding Rules: Photo Share

## General

- Keep Python, templates, names, and comments simple and beginner-friendly.
- Implement only the requested essential feature set. Do not add libraries or extra product features without a clear need.
- Prefer small, readable functions and explicit validation over clever abstractions.

## Flask and access control

- Use `url_for()` for internal URLs; do not hard-code application URLs in templates.
- Store only `user.id` in `session`; fetch the current user from the database when needed.
- Every protected view, including uploaded-image serving, must check authentication and redirect to `url_for('login')` when absent.
- Redirect already authenticated visitors from Login and Register to `post_list`.
- After successful POST actions, use Post/Redirect/Get. Render the same form only for validation errors.
- Use flash messages or clear inline errors. Login failure must not reveal whether the username or password was incorrect.

## Passwords and user input

- Hash passwords with Werkzeug helpers; never store, log, or display raw passwords.
- Trim username and email input. Store email in lowercase before checking uniqueness.
- Validate required registration fields and report duplicate username/email clearly.
- Require a non-empty caption of at most 500 characters.

## Upload handling

- Save images only under the project-root `uploads/` directory (`./uploads/`).
- Allow only case-insensitive `.jpg`, `.jpeg`, and `.png` extensions.
- Enforce the 5 MB maximum before saving the file.
- Use `secure_filename()` as needed, but save under a generated unique filename (for example a UUID plus a validated extension).
- Never use the original filename as the stored filename or as a filesystem path.
- Store the generated filename, not a path, in `Post.image`.
- Serve uploads only from the configured `uploads/` directory and never accept arbitrary filesystem paths.

## Database

- Use Peewee models backed by one SQLite database.
- `User.username`, `User.email`, and `Post.image` are unique.
- `Post.user` is required. `Like` has a unique `(user, post)` pair.
- Enable SQLite foreign keys; `Like.post` cascades when a post is deleted.
- Set `Post.created_at` with a callable default such as `datetime.datetime.now`, not `now()` at model definition time.
- Load posts newest first by `created_at`.

## Templates and scope

- All pages extend `templates/base.html`.
- Show logged-out navigation: Login and Register. Show logged-in navigation: Post List, New post, Logout, and username text.
- Build only login, registration, post list, create post, and post detail before optional features.
- Enforce ownership on any future edit/delete action in the view, not only by hiding buttons.

## Repository hygiene

- Do not commit `*.db`, secrets, or uploaded images. Keep `uploads/` out of Git except an optional placeholder file.
- Do not delete user data or files unless the relevant feature explicitly requires it.
