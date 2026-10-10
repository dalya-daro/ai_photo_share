# Requirements: Photo Share

A beginner-friendly Instagram-style photo sharing app built with **Flask** and **Peewee**.

---

## App Overview

Photo Share is a small web app where logged-in users post **one photo and a short caption**, then see everyone’s posts in **one shared feed**.

- Users must **log in** to view the feed and to post.
- There is **no search** and **no follow** in this version.
- The first version should stay small: get registration, login, upload, and the post list working well before adding extras.

---

## Target users

People who share **travel photos** and **everyday photos** with friends.

They are not professional photographers. They want a simple place to:

1. Make an account
2. Upload a photo with a short caption
3. Scroll a list of posts from everyone in the app

---

## Essential features

Build these first, in this order. Each item is a small piece of work.

### 1. Project setup

- Create a Flask app that can show a simple page in the browser.
- Connect **Peewee** and a local database (SQLite is enough).
- Add a templates folder and a basic layout (header, page title, links).

### 2. User registration

- Show a sign-up form: **username** and **password** only.
- Save a new user in the database.
- Do not save the password as plain text (hash it).
- If the username is already taken, show a clear error.
- After a successful sign-up, send the user to the login page (or log them in).

### 3. Login and logout

- Show a login form: username and password.
- If the details are wrong, show a clear error. Do not say which field was wrong in a complicated way; “Invalid username or password” is enough.
- After login, remember who the user is (Flask session).
- Show a logout action that clears the session.
- Pages that need a logged-in user (feed, upload) must redirect to login if the user is not logged in.

### 4. Photo upload (create a post)

- Show an upload form only to logged-in users.
- The form has:
  - one photo file
  - one short caption
- Save the image file on disk (for example in an `uploads` folder).
- Save a post in the database: who posted it, caption, file name, created time.
- One post = **one photo + one caption**.
- Allowed files: **jpg** and **png** only.
- Reject files larger than **5 MB**, with a simple error message.

### 5. Post list (shared feed)

- Logged-in users see **everyone’s posts** in one list.
- Each item shows: photo, caption, username, and when it was posted.
- Newest posts first.
- Guests (not logged in) cannot see the feed.

### 6. Home / navigation

- Logged-out users see links to **Register** and **Login**.
- Logged-in users see links to **Feed**, **Upload**, and **Logout**, and can see their username.

---

## Features to add if time permits

Do these only after the essential features work. Still keep them small. Skip search and follow.

### 7. Like a post

- A logged-in user can like a post.
- A user can like a post only **once**.
- Show a like count on the post.
- The same button can unlike (optional, only if it stays simple).

### 8. Comment on a post

- A logged-in user can add a short comment on a post.
- Show comments under the post (or on a simple post page).
- Show who wrote each comment.

### 9. Edit caption and delete own post

- Only the **owner** can edit the caption of their post.
- Only the **owner** can delete their post.
- When a post is deleted, also remove its image file if that is easy to do.

---

## Non-functional requirements

These are quality rules, not extra screens.

| Topic | Rule |
| --- | --- |
| Stack | Flask + Peewee + SQLite |
| Language | Keep code and comments simple enough for a beginner |
| Access | Login required to view posts and to post |
| Accounts | Username + password (no email in this version) |
| Photos | jpg / png only, max about 5 MB, one photo per post |
| Captions | Short text (a few hundred characters is enough) |
| Data | Posts belong to a user; deleting a user later is out of scope |
| Hosting | Run locally on the developer’s computer for now |
| Privacy | This is a small shared feed among registered users, not a public website for strangers |

---

## Things to be aware of during implementation

- **One step at a time.** Finish registration and login before building upload. Finish upload before polishing the feed.
- **Protect pages.** Any page that shows posts or accepts an upload must check that the user is logged in.
- **Never store raw passwords.** Use a password hash (for example Werkzeug’s password helpers).
- **Keep uploads safe.** Do not trust the original file name. Save a new name. Only allow `.jpg`, `.jpeg`, and `.png`.
- **Do not put uploaded photos inside Git.** Ignore the uploads folder (except maybe an empty placeholder).
- **Database models stay small.** Start with `User` and `Post`. Add `Like` and `Comment` tables only when you build those features.
- **Owner-only actions.** Edit and delete must check “this post belongs to the current user.” Do not rely on hiding the button only.
- **Simple UI is enough.** A list of photos and forms is fine. Do not copy all of Instagram’s layout.
- **Out of scope for this version:** search, follow, profile pages, direct messages, hashtags, stories, email reset, and visiting the feed without logging in.
