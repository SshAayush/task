# Django Web Application - User Management

## Features

- User Registration and Authentication: Users can register for accounts and authenticate themselves to access the home page.
- User Profile Management: Logged-in users can edit their profiles, change their passwords, and delete their accounts.
- Admin User Management(Super Admin): Admin users can view, edit, and delete other users accounts.
- Staff User Management(Staff): Staff users can view and edit other users accounts.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- PostgreSQL

### Installation

1. Clone the repository: `git clone https://github.com/SshAayush/task`
2. Navigate to the project directory: `cd task`
3. Install the environment(conda)
4. Configure database settings by updating the DATABASES section in .env file with your PostgreSQL connection details.
5. Apply migrations to set up the database: `python manage.py makemigrations`
   `python manage.py migrate`
6. Create a superuser for the admin dashboard : `python manage.py createsuperuser` (Which will be your SuperAdmin)
7. Run the development server: `python manage.py runserver`
8. To create a staff user through the admin dashboard, navigate to `127.0.0.1:8000/admin`. Use the admin credentials to log in, then set the desired user's status to staff

## Setting up Environment

You can use the requirements.txt file to recreate the environment or install the packages in another environment. To create a new environment with the packages listed in requirements.txt, you can use:

**Use the requirements.txt File**

```
conda create --name new_environment_name --file requirements.txt
`
```

**To install packages from the conda-forge channel, you can use:**

```
conda config --add channels conda-forge

```

**To install the packages in an existing environment, you can use:**

```
conda install --file requirements.txt

```

**or**

```
pip install -r requirements.txt
```

## Usage

After setting up the project, you can access the website by navigating to `http://127.0.0.1:8000/` in your web browser.

- **User Registration**: Navigate to `/signup/` to register a new user.
- **Edit Profile**:Navigate to `/profile/` to edit user profile.
- **Change Password and Delete Account**: Navigate to `/security/` to change password and delete account.
- **Manage User**: Navigate to `/viewuser/` where admins and staff members can view and edit details of other users. Admin also have the ability to delete user accounts.
- **Logout**: Navigate to `/logout/` to terminate the session.
