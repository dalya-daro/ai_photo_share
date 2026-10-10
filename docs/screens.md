# Screen design: Photo Share

This document describes the **pages a user sees**. Flask routes that match these pages are in [routes.md](routes.md).

There is **no welcome page**. The home URL `/` is the **Login** screen.

Shared layout for every page: `templates/base.html`  
(header with app name, nav links, flash messages, and `{% block content %}`.)

---

## Screen list

| # | Screen | Template | URL | Login required? |
| --- | --- | --- | --- | --- |
| 1 | Login | `login.html` | `/` | No |
| 2 | User Registration | `register.html` | `/register` | No |
| 3 | Post List (Top) | `posts/list.html` | `/posts` | Yes |
| 4 | Create Post | `posts/new.html` | `/posts/new` | Yes |
| 5 | Post Details | `posts/detail.html` | `/posts/<id>` | Yes |

Logout is **not a screen**. It is a link/action that sends the user back to Login. See [routes.md](routes.md).

---

## Header (on every screen)

Use `base.html` so every page has the same header.

**Not logged in**

- App name (links to Login `/`)
- Login
- Register

**Logged in**

- App name (links to Post List `/posts`)
- Post List
- New post
- Logout
- Current username (text only, not a profile page)

---

## 1. Login

| Item | Value |
| --- | --- |
| Purpose | Let an existing user sign in. This is the first page of the app. |
| Login required? | No |
| URL | `/` |
| Template | `templates/login.html` (extends `base.html`) |
| Main content | Form: username, password, submit button “Log in”. Link: “Create an account” → Register. |

**If already logged in:** do not show this form. Send the user to Post List.

**On success:** go to Post List.  
**On failure:** stay on Login and show “Invalid username or password”.

---

## 2. User Registration

| Item | Value |
| --- | --- |
| Purpose | Create a new account (username + password only). |
| Login required? | No |
| URL | `/register` |
| Template | `templates/register.html` (extends `base.html`) |
| Main content | Form: username, password, submit button “Sign up”. Link: “Already have an account?” → Login. |

**If already logged in:** send the user to Post List.

**On success:** log the user in automatically, then go to Post List.  
**On failure:** stay on Register (for example “That username is already taken”).

---

## 3. Post List (Top)

| Item | Value |
| --- | --- |
| Purpose | Show everyone’s posts in one feed (newest first). This is the main screen after login. |
| Login required? | Yes |
| URL | `/posts` |
| Template | `templates/posts/list.html` (extends `base.html`) |
| Main content | A **New post** button → Create Post. A list of posts. If there are no posts, show a short empty message and the same button. |

**Each post in the list shows**

- Photo (click → Post Details)
- Caption
- Username
- Date/time posted

Do **not** put the upload form on this page. Create Post is its own screen.

**If not logged in:** send the user to Login.

---

## 4. Create Post

| Item | Value |
| --- | --- |
| Purpose | Let a logged-in user add one photo and a short caption. |
| Login required? | Yes |
| URL | `/posts/new` |
| Template | `templates/posts/new.html` (extends `base.html`) |
| Main content | Form (`enctype="multipart/form-data"`): file input (photo), text field (caption), submit “Post”. Link: “Cancel” → Post List. |

Remind the user on the page: jpg or png, max about 5 MB, one photo.

**On success:** go to Post List.  
**On failure:** stay on Create Post and show a simple error (wrong file type, file too big, missing photo).

**If not logged in:** send the user to Login.

---

## 5. Post Details

| Item | Value |
| --- | --- |
| Purpose | Show one post larger, with its caption and who posted it. |
| Login required? | Yes |
| URL | `/posts/<id>` (example: `/posts/3`) |
| Template | `templates/posts/detail.html` (extends `base.html`) |
| Main content | Large photo, caption, username, date/time, **Back to list** → Post List. |

If the post id does not exist: show a simple “Post not found” message (or Flask 404).

**If not logged in:** send the user to Login.

Likes, comments, edit caption, and delete are **not** on this screen in the first version. See “Later screens” below.

---

## Screen transitions

```
Login  --(success)-------------->  Post List
Register --(success, auto login)->  Post List

Post List --(New post)----------->  Create Post
Create Post --(success)---------->  Post List
Create Post --(Cancel)----------->  Post List

Post List --(click photo)-------->  Post Details
Post Details --(Back to list)---->  Post List

Any protected page (not logged in) --> Login
Logout -------------------------------> Login
```

---

## Later (only if time permits)

Do not build extra templates until the five screens above work.

| Extra | Where it would appear | Login required? |
| --- | --- | --- |
| Like / unlike | Button + count on Post List and/or Post Details | Yes |
| Comments | List + form on Post Details | Yes |
| Edit caption / delete | Buttons on **my** posts in the Post List (and maybe Post Details) | Yes (must be the owner) |

No new top-level screens are required for those extras unless edit becomes too cramped on the list.
