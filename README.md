# Book Recommendation System

A Django-based web application that allows users to search for books, submit recommendations, like and comment on recommendations, and view all recommendations. The application integrates with the Google Books API to retrieve book data.

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Environment Variables](#environment-variables)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Authentication](#1-authentication)
  - [Books](#2-books)
  - [Recommendations](#3-recommendations)
  - [Likes](#4-likes)
  - [Comments](#5-comments)
  - [Frontend Views](#6-frontend-views)

## Features

- **User Authentication**: Register, login, and logout functionalities.
- **Google Books Integration**: Search and retrieve book details via Google Books API.
- **Recommendations**: Submit, update, and view book recommendations.
- **Likes**: Like or unlike book recommendations.
- **Comments**: Comment on book recommendations.
- **Filtering and Ordering**: Filter and order recommendations by ratings and publication date.

## Setup Instructions

### Environment Variables

Create a `.env` file in the root directory of your project and add the following variables:


Replace `your_secret_key` with your Django secret key and `your_google_books_api_key` with your Google Books API key.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/book-recommendation-system.git
    cd book-recommendation-system
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Collect static files**:

    ```bash
    python manage.py collectstatic
    ```

### Running the Application

1. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

2. **Access the application**:
   - Open your browser and navigate to `http://127.0.0.1:8000/`.

## API Endpoints

### 1. **Authentication**

- **Register**: `/api/register/` (POST)
  - Register a new user.

  **Request Body**:
  ```json
  {
      "username": "your_username",
      "password1": "your_password",
      "password2": "your_password"
  }
- **Login**: `/api/login/` (POST)
  - Log in an existing user.

  **Request Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }

### 2. **Search Books**

- **Endpoint**: `/api/search/` (GET)

  This endpoint allows you to search for books using the Google Books API. It returns a list of books that match the search query.

  **Query Parameters**:
  - `q`: The search query string (e.g., book title, author, etc.).

  **Example**:
 
**Response**:
A JSON array of book objects with the following fields:
```json
[    { "google_books_id": "book_id",
       "title": "Book Title",
       "author": "Author Name",
       "description": "Book Description",
       "cover_image": "URL to cover image",
       "ratings": 4.5,
       "publishedDate": "YYYY-MM-DD"    },    ...]
```

### 3. **Submit Recommendation**

- **Endpoint**: `/api/submit_recommendation/` (POST)

  This endpoint allows a logged-in user to submit a recommendation for a book. If the book has already been recommended, the existing recommendation will be updated to include the new user.
  
  **Request Headers:**

  ```http
  Content-Type: application/json
  X-CSRFToken: <csrf_token>
  ```
  **Request Body**:
  ```json
  {
      "book_id": "google_books_id"
  }
  ```

### 4. **List All Recommendations**

- **Endpoint**: `/api/recommendations/`(GET)

  This endpoint retrieves a list of all book recommendations made by users.

  **Response**:

  A JSON array of recommendation objects with the following structure:

  ```json
  [
      {
          "id": 1,
          "user": ["username1", "username2"],
          "book": {
              "author": "Author Name",
              "title": "Book Title",
              "description": "Book Description",
              "book_id": 1,
              "cover_image": "URL to cover image",
              "ratings": 4.5,
              "publishedDate": "YYYY-MM-DD"
          },
          "likes": 5,
          "comments": [
              {
                  "name": "commenter_username",
                  "comment": "Nice book!"
              }
          ],
          "is_liked_by_user": true,
          "created_at": "2024-08-09T10:00:00Z"
      },
      ...
  ]
 

### 5. **View My Recommendations**

- **Endpoint**: `/api/recommendations/my_recommendations/` (GET)

  This endpoint allows a logged-in user to retrieve a list of book recommendations they have submitted.

  **Request Headers:**

  ```http
  Content-Type: application/json
  X-CSRFToken: <csrf_token>
  ```

  **Response**:

  A JSON array of recommendation objects submitted by the logged-in user. Each recommendation object has the following structure:

  ```json
  [
      {
          "id": 1,
          "user": ["username"],
          "book": {
              "author": "Author Name",
              "title": "Book Title",
              "description": "Book Description",
              "book_id": 1,
              "cover_image": "URL to cover image",
              "ratings": 4.5,
              "publishedDate": "YYYY-MM-DD"
          },
          "likes": 5,
          "comments": [
              {
                  "name": "commenter_username",
                  "comment": "Nice book!"
              }
          ],
          "is_liked_by_user": true,
          "created_at": "2024-08-09T10:00:00Z"
      },
      ...
  ]

### 6. **Like/Unlike a Book**

- **Endpoint**: `/api/likes/` (POST)

  This endpoint allows a logged-in user to like or unlike a book recommendation.

  ```http
  Content-Type: application/json
  X-CSRFToken: <csrf_token>
  ```

  **Request Body**:

  ```json
  {
      "bookId": 1
  }

### 5. **Submit Comment**

- **Endpoint**: `/api/comments/` (POST)

  This endpoint allows a logged-in user to submit a comment on a book recommendation.
 
  ```http
  Content-Type: application/json
  X-CSRFToken: <csrf_token>
  ```

  **Request Body**:

  ```json
  {
      "bookId": 1,
      "comment": "This is a fantastic book!"
  }

### 6. **Frontend Views**

The frontend views of the application provide a user interface for interacting with the book recommendations system. Below is a description of the available views.

#### **Home**

- **Endpoint**: `/api/index/` (GET)

  This view displays the home page of the application. It typically includes navigation links to other parts of the application and any relevant introductory information.

  **Example**:
  Visiting `/api/index/` will render the home page where users can navigate to other features of the application.

#### **Recommendations View**

- **Endpoint**: `/api/recommendationsList/` (GET)

  This view displays a list of all book recommendations. Users can see all the recommendations, including details about the book, likes, comments, and other relevant information.

  **Example**:
  Visiting `/api/recommendationsList/` will render a page listing all recommendations with options to like and comment.

#### **Submit Recommendation View**

- **Endpoint**: `/api/submit_recommendation/` (POST)

  This view provides a form for submitting a new book recommendation. Users can submit a recommendation for a book that is not already in the system.

  **Form Fields**:
  - `book_id`: The Google Books ID of the book to be recommended.

  **Example**:
  A form at `/api/submit_recommendation/` allows users to enter a book ID and submit a recommendation.

---

This section describes the available frontend views of the application, including their endpoints and functionality.
