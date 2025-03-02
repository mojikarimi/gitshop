![GitShop Wall](https://github.com/mojikarimi/gitshop/tree/master/Media/Wallpaper/image1.png)
# Git Shop


This project simulates the implementation of an online store using Django and uses it to sell a variety of products such as digital, clothing, etc.




## Components:
  
**Account APP :** This app is used for things like user registration and login.

**Blog APP :** This app includes sections related to blogging and content production.

**Main APP :** This app includes the main sections of the site, including the main site items such as the site title, adding a slider and site footer, etc.

**Profile APP :** This app includes items related to the user panel such as orders, views, likes, etc.

**Shop APP :** This app includes shopping-related items such as the user's shopping cart, products, etc.

**Panel APP :** This app includes paths related to the panel section.

## App details:

**Account APP** (Click [here](https://github.com/mojikarimi/gitshop/tree/master/Media/ImagesApp/Account) to view images.):  
* Panel:
  1. Users List
  2. Users Permissions
  3. Users Groups
* Front:
  1. Login
  2. Register
  3. Verify Email
  4. Change Password
  5. Logout

**Blog App** (Click [here](https://github.com/mojikarimi/gitshop/tree/master/Media/ImagesApp/Blog) to view images.): 
* Panel:
  1. Add Post
  2. Delete Post
  3. Update Post
  4. Posts Lists
  5. Tags Post
  6. Dynamic Category
  7. Add Comments
  8. View Comments & Edit Status
* Front:
  1. Posts Search
  2. View Posts
  3. Add Comments
  4. Like System

**Main App** (Click [here](https://github.com/mojikarimi/gitshop/tree/master/Media/ImagesApp/Main) to view images.): 
* Panel:
  1. Ticketing System
  2. Add Slider
  3. Main Details (Title Site, Tile Panel etc.)
  4. Dynamic Menu
  5. App Chat
  6. Add FAQ
  7. FAQ Category
* Front:
  1. FAQ
  2. Main Page
  3. Chat App

**Profile APP** (Click [here](https://github.com/mojikarimi/gitshop/tree/master/Media/ImagesApp/Profile) to view images.):
* Front:
  1. Profile Dashboard
  2. User History
  3. User Comments
  4. User Information
  5. User Address
  6. User Tickets
  7. User Orders
  8. User's Favorites

**Shop APP** (Click [here](https://github.com/mojikarimi/gitshop/tree/master/Media/ImagesApp/Shop) to view images.):
* Panel:
  1. Add Product
  2. Update Product
  3. Delete Product
  4. List Product
  5. Comments Lists
  6. Detail Comment
  7. View Carts
  8. View Orders
  9. dynamic Group
  10. Dynamic Category
  11. Dynamic Sub Category
* Front:
  1. Product Page
  2. Star Rating
  3. Add Favorite Product
  4. View Products
  5. Products Search
  6. Search Filters
  7. Add Comments
  8. User Shopping Cart
  9. Payment steps



## Items made in the project
- Chat Real Time
- Using FileSystemStorage
- Captcha
- Building a ticketing system
- Use canvasjs to display views
- Using Ajax
- Using toast and notification system
- Using ORM Django and Regex to implement site search
- Making products with desired features
- Building a like and dislike system
- Using multiple databases
- Construction of SSO system
- Create a personalized user
- Create a custom tag template
- Creating a dynamic menu
- Creating a dynamic menu



# Site implementation steps
### Creating a virtual environment

To run the first project, you must create a virtual environment to install the required packages

```python
python -m venv venv
```
### Installing packages
The next step is to install all the packages that are in the requirements file

```python
pip install -r requirements.txt
```
### Set Setting.py File
In this step, we have to set a series of items in the settings file

- **Creating a secret key**

In the Python shell, type the following commands and copy the security key


```python
django.core.management.utils.get_random_secret_key()

print(get_random_secret_key())
```

- **Set up the database**

Instead the database section, put **your related items** or if you want to use a database, place the following command instead of **DATABASE**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gitshop.sqlite3',
    }
}
```

- **Getting captcha keys**
Get the captcha codes from the Google site

Link = https://developers.google.com/recaptcha

Replace them after getting the key.

```python
RECAPTCHA_PUBLIC_KEY = recaptcha_public_key

RECAPTCHA_PRIVATE_KEY = recaptcha_private_key

```
- **Email setup**
Set an email to send email verification code

```python

EMAIL_HOST_USER = email_host_user
 # example@example.com

EMAIL_HOST_PASSWORD = email_host_password
 # *******

```
### Project implementation

```python
python manage.py runserver
```