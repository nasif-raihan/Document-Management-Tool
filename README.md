# Document Management Tool

## Overview
This Django project is a document management tool designed to facilitate efficient organization, storage, and sharing of documents. It follows the principles of Domain-Driven Development (DDD), adheres to the SOLID principles, and prioritizes application-focused development over framework-specific implementations.

## Features
- User signup and login
- Create, read, update, and delete (CRUD) operations for documents
- Share documents with others
- Manage access to documents

## APIs
1. **User Signup and Login**
    - `/registration`: Register a new user
      - **Request Payload:**
        ```json
        {
            "username": "First Document",
            "email": "test@mail.com",
            "password1": "password",
            "password2": "password"
        }
        ```
    - `/login`: Log in an existing user
      - **Request Payload:**
        ```json
        {
            "username": "First Document",
            "password": "password"
        }
        ```

2. **Document CRUD Operations**
   - ### Get Document Details
        - **Request URL:** `/documents`
        - **Request Method:** `GET`
        - **Request Payload:**
          ```json
          {
              "documentTitle": "First Document",
              "documentOwnerUsername": "test_user"
          }
          ```
        - **Response:**
          ```json
          {
              "documentTitle": "First Document",
              "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
              "documentOwnerUsername": "test_user",
              "sharedUserUsernames": ["user1", "user2"]
          }
          ```
   - ### Create Document Details
       - **Request URL:** `/documents`
       - **Request Method:** `POST`
       - **Request Payload:**
         ```json
         {
             "title": "First Document",
             "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
             "owner": {
                 "username": "test_user",
                 "password": "password"
             },
             "sharedWith": ["user1", "user2"]
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "First Document",
             "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
             "documentOwnerUsername": "test_user",
             "sharedUserUsernames": ["user1", "user2"]
         }
         ```
   - ### Update Document Details
       - **Request URL:** `/documents`
       - **Request Method:** `PUT`
       - **Request Payload:**
         ```json
         {
             "title": "Updated Document Title",
             "content": "Updated content here",
             "owner": {
                 "username": "test_user",
                 "password": "password"
             },
             "sharedWith": ["user1", "user2"]
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "Updated Document Title",
             "content": "Updated content here",
             "documentOwnerUsername": "test_user",
             "sharedUserUsernames": ["user1", "user2"]
         }
         ```
   - ### Delete Document Details
       - **Request URL:** `/documents`
       - **Request Method:** `DELETE`
       - **Request Payload:**
         ```json
         {
             "documentTitle": "Document to be deleted",
             "documentOwnerUsername": "test_user"
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "First Document",
             "message": "Document deleted successfully"
         }
         ```

3. **User Access Detail**
   - ### Get User Access Details
       - **Request URL:** `/share-details/`
       - **Request Method:** `GET`
       - **Request Payload:**
         ```json
         {
             "documentTitle": "Document to be retrieved",
             "sharedUserUsername": "user1"
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "Document to be retrieved",
             "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
             "documentOwnerUsername": "test_user",
             "sharedUserUsernames": ["user1", "user2"],
             "permissionType": "Read Only"
         }
         ```
   - ### Create User Access Details
       - **Request URL:** `/share-details/`
       - **Request Method:** `POST`
       - **Request Payload:**
         ```json
         {
             "documentTitle": "Document to be shared",
             "documentOwnerUsername": "test_user",
             "permissionType": "Read Only",
             "sharedUserUsernames": ["user1", "user2"]
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "Document to be shared",
             "documentOwnerUsername": "test_user",
             "permissionType": "Read Only",
             "sharedUserUsernames": ["user1", "user2"],
             "message": "Document shared successfully"
         }
         ```
   - ### Update User Access Details
       - **Request URL:** `/share-details/`
       - **Request Method:** `PUT`
       - **Request Payload:**
         ```json
         {
             "documentTitle": "Document to be updated",
             "documentOwnerUsername": "test_user",
             "permissionType": "Edit",
             "sharedUserUsernames": ["user3", "user4"]
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "Document to be updated",
             "documentOwnerUsername": "test_user",
             "permissionType": "Edit",
             "sharedUserUsernames": ["user3", "user4"],
             "message": "Document access updated successfully"
         }
         ```

   - ### Delete User Access Details
       - **Request URL:** `/share-details/`
       - **Request Method:** `DELETE`
       - **Request Payload:**
         ```json
         {
             "documentTitle": "Document to be unshared",
             "sharedUserUsername": "user1"
         }
         ```
       - **Response:**
         ```json
         {
             "documentTitle": "Document to be unshared",
             "message": "Document access removed successfully"
         }
         ```

## Installation
1. Clone the repository: `git clone https://github.com/nasif-raihan/Document-Management-Tool.git`
2. Install dependencies: `poetry install`
3. Run migrations: `make migrate`

## Usage
1. Start the server: `make runserver`
2. Access the API endpoints using a REST client like Postman or through frontend applications.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
