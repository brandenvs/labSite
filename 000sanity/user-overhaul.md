# User Overhaul

> 18 OCT '24
>
> Biggest change being AJAX requests

## Webpages

1. User Login
   1. Form
    (email, password)
2. User SignUp
   1. Form
    (email, password, confirm_password)
3. User Account
   1. Can add data
    (first_name, last_name, phone number, profile picture)
   2. Messages
   3. Settings
    (logout, delete account, contact support)

## User Roles

### Permissions Index

| Group    | Access                            |
| -------- | --------------------------------- |
| Admin    | 🗝️ All applications, is superuser. |
| Standard | 🗝️ Access to their applications.   |

### User Function

- To store applications which were created on the website.
  - How are you going to do this?
    - I think I can use GitHub Actions and pull from a code repository / Build from a docker file even.
