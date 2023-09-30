# Initial Singularity - Your K-Pop Inspired E-commerce Platform
Welcome to Initial Singularity – more than just a shop, it's a creation born out of pure fandom and dedication. For fans, by a fan, every product is lovingly crafted at home by the owner. Drawing inspiration from the captivating world of K-Pop (Korean Pop Music), Initial Singularity aims to bridge the gap caused by the expensive prices of official merchandise, making it affordable for every K-Pop enthusiast out there.

At Initial Singularity, I understand the magic of being a fan, and I want to enhance that experience by offering affordable and high-quality products that celebrate the K-Pop culture. Join me on this journey as we create a community of passionate fans who wear their love for K-Pop with pride!

[View deployed site here] ()
![Responsive Mockup]()

## Table of Contents
- [About](#about)
- [UX](#ux)
  - [Ideal Client](#ideal-client)
  - [Client Stories](#client-stories)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Features Left to Implement](#features-left-to-implement)
- [Testing](./Testing.md)
- [Database](#Database-Schema)
- [Deployment](#deployment)

## About

The goals of this website are:
* Showcase and Sell Products: 
      The primary goal of the website is to serve as an online platform to showcase and sell the handcrafted products inspired by K-Pop. 

* Provide Product Information: 
      Each product have a detailed descriptions, high-quality images to give potential buyers a clear understanding 
      of what they're purchasing. This information helps build trust and encourages users to make informed decisions.

* Implement Secure Payment Processing:
      As the website handles financial transactions, ensuring a secure payment gateway is of utmost importance. It builds trust and reassures 
      customers that their personal and financial information is protected.


# UX
## Ideal client
### Initial Singularity caters to the following ideal visitor:
 
* K-Pop Enthusiasts: The website is specifically designed for individuals who are passionate about K-Pop and have a deep interest in the Korean pop music culture. These fans are likely to be familiar with various K-Pop artists, groups, and trends.

* Affordable Merchandise Seekers: The website caters to fans who appreciate high-quality, handcrafted products inspired by K-Pop but may find official merchandise to be too expensive. These visitors are looking for affordable alternatives without compromising on the fandom experience.

* Frequent Online Shoppers: The ideal visitor is likely to be comfortable with online shopping and enjoys browsing and purchasing products from e-commerce platforms. They are tech-savvy and expect a smooth, user-friendly online shopping experience.

* International Audience: As K-Pop has a global following, the website should appeal to fans from various countries and cultures who share a common interest in Korean pop music.

* Value-Conscious Buyers: The ideal visitor appreciates the value of handcrafted products and seeks to support independent creators while obtaining products that fit their budget.

Overall, the ideal visitor for the Initial Singularity website is a dedicated K-Pop enthusiast who is looking for an affordable and community-driven shopping experience, accompanied by unique and high-quality products inspired by their favorite music genre.

### Client stories

1. As a K-Pop fan, I want to explore a wide range of handcrafted products inspired by my favorite K-Pop artists, so I can find unique and affordable merchandise to express my fandom with pride.

2. As a new visitor to the website, I want a user-friendly interface that allows me to easily navigate through different collections, so I can quickly find and purchase the products that resonate with my fandom.

3. As an international fan, I want to have a seamless shopping experience with various shipping options and transparent international shipping costs, so I can confidently order products from anywhere in the world.

4. As a customer, I want to feel confident about the security of my personal and financial information during the checkout process, knowing that the website uses secure payment processing to protect my data.



## Features 
### Existing Features

1. **User Registration and Authentication**: Users can create accounts, log in, and log out.

2. **Product Listings**: Display a catalog of products, each with detailed descriptions, images, and prices.

3. **Product Search and Filters**: Allow users to search for products by keywords and apply filters to narrow down their choices.

4. **Shopping Cart**: Users can add products to their cart, view the contents, and proceed to checkout.

5. **Checkout Process**: A step-by-step process for users to enter shipping details, select payment methods, and complete their orders.

6. **Payment Integration**: Integration with a secure payment gateway to process payments.

7. **Order History**: Users can view their order history, including order number and details.

8. **Responsive Design**: Ensuring the website is usable and looks good on various devices (desktop, tablet, mobile).

9.  **Security Measures**: Implementation of security best practices to protect user data and payment information.

10. **Navigation Menu and Layout**: A structured layout with a navigation menu for easy access to different sections of the website.

## Features Left to Implement

1. **International Shipping Prices**: Display transparent international shipping costs.

2. **Product Reviews**: Allow customers to leave reviews and ratings for products.

3. **Customer Support Section**: Add a customer support section with additional resources and FAQs.

4. **Community Blog**: Add a blog to build a community and share K-Pop-related content.

# Database Schema

The database for our application is structured as follows:

## Tables

### 1. Users

   - **Description**: The Users table stores information about registered users of our application.
   - **Columns**:
        - `user_id` (Primary Key): Unique identifier for each user.
        - `username`: User's username (unique).
        - `email`: User's email address (unique).
        - `password_hash`: Hashed password for authentication.
        - `created_at`: Timestamp of user registration.

### 2. Products

   - **Description**: The Products table contains information about the products available in our catalog.
   - **Columns**:
        - `product_id` (Primary Key): Unique identifier for each product.
        - `name`: Product name.
        - `description`: Product description.
        - `price`: Product price.
        - `category`: Product category.
        - `image_url`: URL to the product image.

### 3. Orders

   - **Description**: The Orders table records details of user orders.
   - **Columns**:
        - `order_id` (Primary Key): Unique identifier for each order.
        - `user_id` (Foreign Key): References the user who placed the order.
        - `order_date`: Date and time of the order.
        - `total_amount`: Total order amount.
        - `payment_method`: Payment method used for the order.

### 4. OrderItems

   - **Description**: The OrderItems table stores individual items within an order.
   - **Columns**:
        - `order_item_id` (Primary Key): Unique identifier for each order item.
        - `order_id` (Foreign Key): References the order to which the item belongs.
        - `product_id` (Foreign Key): References the product in the order.
        - `quantity`: Quantity of the product in the order.
        - `subtotal`: Subtotal cost of the item within the order.

## Relationships

   - The Users table is related to the Orders table through the user_id foreign key.
   - The Products table is related to the OrderItems table through the product_id foreign key.
   - The Orders table is related to the OrderItems table through the order_id foreign key.

## Constraints

   - Usernames and email addresses in the Users table are unique to ensure no duplicate user accounts.
   - Foreign key constraints ensure data integrity by linking related records in different tables.
   - Proper indexing is used for efficient data retrieval.

# Deployment

## Heroku Deployment

This application can be easily deployed to Heroku using the following steps:

Create a Heroku Account: If you don't have one already, sign up for a free Heroku account.

Install Heroku CLI: Install the Heroku CLI on your local machine to interact with Heroku from the command line.

Fork this Repository: Fork this repository to your GitHub account by clicking the "Fork" button at the top-right corner of this page.

Create a New Heroku App: Log in to your Heroku account and create a new app from the Heroku dashboard. Choose a unique name for your app.

Connect GitHub Repository: In the "Deploy" tab of your Heroku app dashboard, under the "Deployment method" section, select "GitHub" as the deployment method. Connect your forked repository by searching for its name.

Configure Environment Variables: In the "Settings" tab of your Heroku app dashboard, click on the "Reveal Config Vars" button. Add any necessary environment variables used in your application.

Deploy the App: In the "Deploy" tab, manually deploy your app by clicking the "Deploy Branch" button under the "Manual deploy" section. This will deploy the latest version of your app from the main branch.

View Your App: Once the deployment is successful, click on the "Open App" button in the top-right corner of the Heroku dashboard to view your deployed app.

