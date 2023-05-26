<img title="LapZone header" alt="LapZone header image" width="100%" src="./lapzone/static/images/site_header.webp">

# 1. Introduction

Internet shop "LapZone".

## 1.1 Purpose

Write an internet shop to practice working with the Django framework. Make the market a place for selling laptops and accessories for them.
Everyone can visit the site, visit the "About" and "FAQs" pages, search products, go to their detail pages, etc.
Only registered users can have a personal account on the site, have a wish list, look at their orders, etc.

## 1.2 Scope

-   Write site markup;
-   Use Bootstrap 5 for some custom styles;
-   Write a Django site using Python;
-   Work out the structure of the database;
-   Deploy the site to hosting.

## 1.3 Overview

-   General pages
    -   Home page (with all product categories, new products, brands, etc)
    -   Product detail page
    -   Cart page
    -   Order page
    -   About page
    -   FAQs page
    -   Feedback page
    -   Page to unsubscribe from mailing
-   Auth pages
    -   Login page
    -   Logout page
    -   Register page
    -   Email confirmation page
    -   Password change page
    -   Password reset page
-   User pages
    -   Profile page
    -   Wish list page
    -   Page with orders
    -   Profile edit page
-   Admin page

# 2. Functional requirements

The system consists of the following main functional blocks:

-   Registration, authentication and authorization;
-   Guest functionality;
-   User functionality;
-   Admin functionality.

## 2.1. User types

The system provides for three types of people:

-   Guest (a person who can visit general pages and make orders);
-   User (a registered person who can have personal account and wish list);
-   Admin (a person who has permission to access the admin panel).

> When a guest makes an order and fills in the personal information fields for it, he automatically becomes a user.

## 2.2. Registration

> Use Django extension "django-allauth" for auth functionality

Registration should consist of username and password.

The registration form should include fields such as:

1. Username (required field);
2. Password (required field);
3. Password again (required field, which should be equal to the first password field).

> Add registration through social networks such as Google (Facebook).

## 2.3. User authentication

User authentication should be by username and password.

## 2.4. Admin authentication

Admin authentication should be by username and password.

## 2.5. Guest functionality

Guest can:

-   Visit the "Home", "About", "FAQs" pages;
-   Visit the product detail page;
-   Leave product reviews;
-   Fill out a cart;
-   Make an order;
-   Visit the "Feedback" page and send a feedback email.

Guest cannot:

-   Have a wish list
-   Have a personal profile

### 2.5.1. Leaving reviews for a product

Everybody can see the special form for leaving reviews under each product detail. Review will consist of a name, email, body and the date and time they were created.

## 2.6. User functionality

After authentication, the user gets access to such functional blocks as:

-   Having a wish list;
-   Having a order list;
-   Having a personal profile;
-   Editing a personal profile.

### 2.6.1. Wish list

The user has access to a "wish" button next to each product. This "like" button should be on the product card for all products and on every product detail page.

### 2.6.2. Having a personal profile

General information about the user should be printed:

-   Email,
-   Username,
-   Count of user:
    -   Wishes,
    -   Orders.

And a profile should consist of the following pages:

-   User wishes,
-   User orders.

> On these pages, users can see and delete information.

### 2.6.3. Editing personal profile

The user can edit personal information:

-   Email,
-   Username,
-   Password.

## 2.7. Admin functionality

Django admin functionality.

> Add all models for admin to show them on admin pages.

# 3. Development requirements

-   Technology stack;
-   Apps;
-   Testing;
-   Apps database table structure;
-   General file structure.

## 3.1. Technology stack

To implement the site, the following stack of technologies is proposed:

-   Backend:
    -   Python programming language;
    -   Django framework with the following extensions:
        -   django-allauth;
        -   django-ckeditor;
        -   django-recaptcha3.
    -   PostgreSQL / MySQL database (Django ORM);
-   Frontend:
    -   HTML & CSS;
    -   JavaScript;
    -   Bootstrap 5.

## 3.2. Apps

-   Shop (for working with displaying product lists, product details, brands, etc.);
-   Customer (for working with user profiles and pages that are connected with them);
-   Cart (for working with a user's or guest's cart through sessions);
-   Order (for working with user orders and payments);
-   Mailing (for working with mailing).

## 3.3. Testing

The main test cases are:

-   Models testing
-   Views testing
-   Forms testing

> Write tests just after adding new content (models, views and forms)

### 3.3.1 Models testing

Test model fields and methods (if there are any). Check all field parameters such as max_length, verbose_name, required, blank, etc.

### 3.3.2 Views testing

Test all conditions of views. Check valid and invalid URLs, data, parameters, etc. Test all HTTP methods that view can answer.

### 3.3.3 Forms testing

Test form fields and validation methods (if there are any). Check all field parameters. Test validation with valid and invalid data.

## 3.4. Apps database table structure

Apps that need database tables (models):

-   Shop
-   Order
-   Mailing

### 3.4.1. Shop

<img title="Shop DB" alt="Shop app db table structure image" width="100%" src="./md_images/apps_db/shop.jpg">

### 3.4.2. Order

<img title="Order DB" alt="Order app db table structure image" width="100%" src="./md_images/apps_db/order.jpg">

### 3.4.3. Mailing

<img title="Mailing DB" alt="Mailing app db table structure image" width="100%" src="./md_images/apps_db/mailing.jpg">

## 3.5. General file structure

<pre>
LapZone
│
│   .gitattributes
│   .gitignore
│   README.md
│   Tech spec.md
│   
├───lapzone
│   │   .env
│   │   file_env_example.txt
│   │   manage.py
│   │   
│   ├───cart
│   │   │   apps.py
│   │   │   cart.py
│   │   │   context_processors.py
│   │   │   services.py
│   │   │   urls.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───migrations
│   │   │       __init__.py
│   │   │       
│   │   ├───templates
│   │   │   └───cart
│   │   │       │   detail.html
│   │   │       │   _base.html
│   │   │       │   
│   │   │       └───utils
│   │   │               _product_table.html
│   │   │               
│   │   └───tests
│   │           test_cart.py
│   │           test_views.py
│   │           __init__.py
│   │           
│   ├───customer
│   │   │   apps.py
│   │   │   forms.py
│   │   │   urls.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───templates
│   │   │   └───customer
│   │   │       │   detail.html
│   │   │       │   wish_list.html
│   │   │       │   
│   │   │       └───utils
│   │   │               _link_list_group.html
│   │   │               
│   │   └───tests
│   │           test_forms.py
│   │           test_views.py
│   │           __init__.py
│   │           
│   ├───general
│   │   │   admin_mixins.py
│   │   │   error_views.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───tests
│   │   │       test_error_views.py
│   │   │       __init__.py
│   │   │       
│   │   └───test_mixins
│   │           for_models.py
│   │           for_views.py
│   │           __init__.py
│   │           
│   ├───lapzone
│   │       asgi.py
│   │       settings.py
│   │       urls.py
│   │       wsgi.py
│   │       __init__.py
│   │       
│   ├───mailing
│   │   │   admin.py
│   │   │   apps.py
│   │   │   context_processors.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   services.py
│   │   │   urls.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───migrations
│   │   │       0001_initial.py
│   │   │       __init__.py
│   │   │       
│   │   ├───templates
│   │   │   └───mailing
│   │   │           confirm_delete.html
│   │   │           email.html
│   │   │           
│   │   └───tests
│   │           test_forms.py
│   │           test_models.py
│   │           test_views.py
│   │           __init__.py
│   │           
│   ├───media
│   │   ├───carousel_images
│   │   │       ASUS_ROG_Strix_G15_banner.webp
│   │   │       Asus_ROG_Zephyrus_M16_banner.webp
│   │   │       Site_header.webp
│   │   │       
│   │   ├───products
│   │   │       asus-rog-strix-g15-g513ic.webp
│   │   │       asus-rog-zephyrus-m16.webp
│   │   │       asus-tuf-gaming-f15.webp
│   │   │       bag-for-laptop-asus-rog-bp4701-17.jpg
│   │   │       corsair-k70-rgb-mk2-cherry-mx-red-usb-black.jpg
│   │   │       dell-g15-5520.webp
│   │   │       lenovo-legion-5-15ach6h_EgkN0aa.webp
│   │   │       logitech-g502-special-edition.jpg
│   │   │       steelseries-aerox-3-wireless-onyx.webp
│   │   │       
│   │   └───product_shots
│   │           asus-rog-strix-g15-g513ic-shot-1.webp
│   │           asus-rog-zephyrus-m16-shot-1.jpg
│   │           asus-rog-zephyrus-m16-shot-2.jpg
│   │           asus-rog-zephyrus-m16-shot-3.jpg
│   │           asus-rog-zephyrus-m16-shot-4.jpg
│   │           asus-rog-zephyrus-m16-shot-5.webp
│   │           
│   ├───order
│   │   │   admin.py
│   │   │   apps.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   services.py
│   │   │   urls.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───migrations
│   │   │       0001_initial.py
│   │   │       0002_orderitem_total_price.py
│   │   │       __init__.py
│   │   │       
│   │   ├───templates
│   │   │   └───order
│   │   │           email.html
│   │   │           order_checkout.html
│   │   │           order_detail.html
│   │   │           order_list.html
│   │   │           _base.html
│   │   │           
│   │   └───tests
│   │           test_forms.py
│   │           test_models.py
│   │           test_views.py
│   │           __init__.py
│   │           
│   ├───shop
│   │   │   admin.py
│   │   │   apps.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   services.py
│   │   │   urls.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │   
│   │   ├───migrations
│   │   │       0001_initial.py
│   │   │       0002_alter_review_parent.py
│   │   │       0003_alter_like_created_alter_like_product_and_more.py
│   │   │       0004_carouselimage_alter_brand_slug_alter_category_slug_and_more.py
│   │   │       0005_carouselimage_product.py
│   │   │       __init__.py
│   │   │       
│   │   ├───templates
│   │   │   └───shop
│   │   │       │   home.html
│   │   │       │   product_detail.html
│   │   │       │   product_list.html
│   │   │       │   _base.html
│   │   │       │   
│   │   │       └───utils
│   │   │               _product_card.html
│   │   │               
│   │   └───tests
│   │           test_forms.py
│   │           test_models.py
│   │           test_views.py
│   │           __init__.py
│   │           
│   ├───static
│   │   ├───css
│   │   │   │   general.css
│   │   │   │   
│   │   │   └───shop
│   │   │           product_detail.css
│   │   │           
│   │   ├───images
│   │   │       favicon.ico
│   │   │       logo.ico
│   │   │       site_header.webp
│   │   │       
│   │   └───js
│   │       │   go_to_top_btn.js
│   │       │   loading_form_btn.js
│   │       │   remove_btn.js
│   │       │   resize_pagination.js
│   │       │   toggle_theme.js
│   │       │   
│   │       ├───cart
│   │       │       cart_btn.js
│   │       │       quantity_field.js
│   │       │       remove_btn.js
│   │       │       
│   │       ├───order
│   │       │       is_create_profile_switcher.js
│   │       │       
│   │       └───shop
│   │               like_btn.js
│   │               product_list.js
│   │               
│   └───templates
│       │   _base.html
│       │   _base_email.html
│       │   
│       ├───account
│       │   │   account_inactive.html
│       │   │   base.html
│       │   │   email.html
│       │   │   email_confirm.html
│       │   │   login.html
│       │   │   password_change.html
│       │   │   password_reset.html
│       │   │   password_reset_done.html
│       │   │   password_reset_from_key.html
│       │   │   password_reset_from_key_done.html
│       │   │   password_set.html
│       │   │   signup.html
│       │   │   signup_closed.html
│       │   │   verification_sent.html
│       │   │   verified_email_required.html
│       │   │   
│       │   ├───email
│       │   │       account_already_exists_message.html
│       │   │       email_confirmation_message.html
│       │   │       email_confirmation_signup_message.html
│       │   │       password_reset_key_message.html
│       │   │       unknown_account_message.html
│       │   │       
│       │   ├───messages
│       │   │       cannot_delete_primary_email.txt
│       │   │       email_confirmation_sent.txt
│       │   │       email_confirmed.txt
│       │   │       email_deleted.txt
│       │   │       logged_in.txt
│       │   │       logged_out.txt
│       │   │       password_changed.txt
│       │   │       password_set.txt
│       │   │       primary_email_set.txt
│       │   │       unverified_primary_email.txt
│       │   │       
│       │   └───snippets
│       │           already_logged_in.html
│       │           
│       ├───pages
│       │       about.html
│       │       error.html
│       │       FAQs.html
│       │       feedback.html
│       │       
│       ├───socialaccount
│       │   │   authentication_error.html
│       │   │   base.html
│       │   │   connections.html
│       │   │   login_cancelled.html
│       │   │   signup.html
│       │   │   
│       │   ├───messages
│       │   │       account_connected.txt
│       │   │       account_connected_other.txt
│       │   │       account_connected_updated.txt
│       │   │       account_disconnected.txt
│       │   │       
│       │   └───snippets
│       │           login_extra.html
│       │           provider_list.html
│       │           
│       └───utils
│               _alert.html
│               _pagination_nav.html
│               
├───md_images
│   │   demo.jpg
│   │   
│   └───apps_db
│           mailing.jpg
│           order.jpg
│           shop.jpg
│           
└───requirements
        base.txt
        development.txt
        production.txt
</pre>

# 4. Non-functional requirements

-   Localization and languages
-   Design requirements
    -   General site structure
    -   Layout requirements
-   Graphic content
-   Website domain, hosting
-   Browser support
-   Requirements for the development of the site from the standpoint of search engine promotion
    -   General
    -   Text
    -   Images
    -   Meta tags

## 4.1. Localization and languages

The site must be implemented in English.

## 4.2. Design requirements

Minimalist design with clear content. Site layout must be implemented on the Bootstrap 5 layout framework because Bootstrap supports the latest, stable releases of all major browsers and platforms.

### 4.2.1 General site structure

-   Header
-   Main
-   Footer

The site header should have a light/dark mode switcher. The footer of the site should have a logo and links to the author's social networks.

### 4.2.2 Layout requirements

-   Should be displayed correctly, both on computers and on mobile devices;
-   Should be cross-browser.

## 4.3 Graphic content

-   Favicon image (website icon for the browser);
-   Application logo image;
-   Icon set on [ionicons](https://ionic.io/ionicons).

## 4.4 Website domain, hosting

Use Render hosting (which will give us a domain) to deploy the site because it has web services support and provides a PostgreSQL database.

> Use PythonAnywhere as a fallback

## 4.5 Browser support

The site should open and function correctly in the current versions of the main popular browsers: Chrome, Firefox, Safari, etc.

## 4.6 Requirements for the development of the site from the standpoint of search engine promotion

### 4.6.1 General

The site must meet the requirements of the Google search engine for ease of viewing on mobile devices. The requirements are displayed at https://developers.google.com/speed/docs/insights/mobile.

### 4.6.2 Text

-   It is necessary to place the text in the form of text (not pictures). It is desirable that the text be available immediately and not open on click, hover, etc. The text should not be hidden by JavaScripts;
-   The text on the site should be easy to read, formatted, and not contain spelling errors;
-   All site pages must contain unique text;
-   The text of the page should contain 1 heading with the H1 tag, which should include key words and phrases. There can be 2 headings with the H2 tag in the text, and they should also include keywords and phrases. You can't put all the text on the page in the title tag;
-   Headings should at least partially match the navigation.

### 4.6.3 Images

-   An alt-attribute must be registered for all pictures. You can't put more than 7 words in an alt attribute. As for images, they must be unique;
-   Only popular image extensions (JPEG and PNG) should be used.

### 4.6.4 Meta tags

-   It should be possible to edit meta tags and add text;
-   The \<title> tag must match the content of the page and include the main search queries, must include no more than 64 words;
-   The \<description> meta tag should be a brief and precise description of the content of the page and should not be the same as the \<title> tag.
