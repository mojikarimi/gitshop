
# Git Shop Project


This project is a store site that uses a variety of back-end technologies, including the admin panel and the site.





## Panel included:
  
**Blog Panel :** This section includes items such as post editing, adding posts, adding and editing categories, etc. 


**Main Panel :** This section includes the main items of the site, such as the name of the site, the name of the panel, icons, sliders and different sections of the footer, etc.

**Shop Panel :** This section is related to shop sections such as adding products, editing products, orders and...

**User Panel :** This section is related to users and their management, for example adding access and...

## Site included:

**Blog :** This section is about displaying posts, searching for posts, etc.

**Main :** This section is related to the main sections of the site, such as questions and answers and the main page, etc.

**Profile :** This section is related to the user's profile, such as addresses, personal information, orders, etc.

**Shop :** This section is related to products and their search, shopping cart, etc

**User :** This section is related to the user and his activities such as login and registration.
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



## Number of Pages
Tickets Image
![Tickets Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/tickets.png)


Ticket Chat Image
![Ticket Chat Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/ticketschat.png)

Edit Product Image
![Edit Product Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/panelEditProduct.png)

Product List Image
![TProduct List Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/productlist.png)

Cart List Image
![Cart List Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/CartList.png)

Details List Image
![Details List Imagee](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/detailscart.png)

User Add Permissions and Group Image
![User Add Permissions and Group Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/userperms.png)

Single Product Image
![Single Product Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/singleproductpage.png)

Single Product Image
![Single Product Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/singleproductpage.png)

Blog Page Image
![Blog Page Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/blogpage.png)

Add Menu and Sort Image 
![Add Menu and Sort Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/addMenu%20andSortMenu.png)

Panel Main Image
![Panel Main Image](https://github.com/mojikarimi/gitshop_project_django/blob/master/Media/ImageForGit/PanelMainPage.png)

# Site implementation steps
### Creating a virtual environment

To run the first project, you must create a virtual environment to install the required packages

```python
pip install -m venv venv
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
 # ecample@2gmail.com

EMAIL_HOST_PASSWORD = email_host_password
 # *******

```
### Project implementation

```python
python manage.py runserver
```