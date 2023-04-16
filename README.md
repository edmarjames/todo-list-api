# Table of contents
+ [Introduction](#todo-list-api)
+ [Routes](#routes)
+ [Upcoming new features](#upcoming-new-features)
+ [Installation](#installation)
+ [Roadmap](#roadmap)
+ [Project status](#project-status)
+ [Languages and tools](#language-and-tools)

## <a name="#todo-list-api"></a>To-do list API

I created this API to apply what I have learned on creating REST API using Django Rest Framework. This API includes 3 high level functionalities which is Users management, tasks management and notes management. On the routes section we will talk about the detailed sub functionalities of each high level functionalities.

## Routes

1. [Register](https://todo-list-notes-api.onrender.com/users/register) 
    - This **POST** route allows a user to register to the to-do list api. The request body is in JSON format and requires the following.

        ```
        {
		    "username": "johndoe",
		    "first_name": "John",
		    "last_name": "Doe",
		    "email": "johndoe@mail.com",
		    "password": "johndoe1",
            "password2": "johndoe1"
		}    
        ```

    - **Validation**
        - The API will not allow user's to register using an email that is already taken or already existing in the database.
        - All fields are required.
        - Checks if email is valid.
        - Removes leading and trailing whitespace, comma and period.
        - Checks if password and password2 matches.

2. [Login](https://todo-list-notes-api.onrender.com/users/login)
    - This **POST** route allows the user to login to the to-do list api. Upon successful login, the API will provide the generated token, is_superuser field and new_token_created field on the response. The request body is in JSON format and requires the following.

    	```
    	{
		    "username": "johndoe",
		    "password": "johndoe1"
		}
    	```

    - **Validation**
    	- The API can determine if the username or password is incorrect and will throw an error message as a response.

3. [Create task](https://todo-list-notes-api.onrender.com/task/)
    - This **POST** route allows authenticated users to create a new task. The request body is in JSON format and requires the following. Take note that the format of the deadline should be **yyyy-MM-dd**

        ```
        {
            "title": "Wash the dishes",
            "description": "Finish it within 20 minutes",
            "deadline": "2023-04-16"
        }
        ```

    - **Validation**
        - Checks if the title is already existing in the database.
        - Checks if the deadline set is in the past.

4. [Get all task](https://todo-list-notes-api.onrender.com/task/)
    - This **GET** route allows the authenticated user to fetch the details of all of his/her created tasks. The response is JSON format.

5. [Get single task](https://todo-list-notes-api.onrender.com/task/4b22c7e8-d12a-4f41-b37a-8ba845d3c5db)
    - This **GET** route allows authenticated users to fetch the details of a certain task. The URL requires as taskId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/task/taskId`**

    - **Validation**
        - Checks if the taskId is existing.

6. [Update task](https://todo-list-notes-api.onrender.com/task/71937fd7-5b55-4e5e-8181-f199fca632e5/)
    - This **PATCH** route allows the authenticated user to update the details of a specific task. The URL requires a taskId parameter. Please see route below. 

        **`https://todo-list-notes-api.onrender.com/task/taskId/`**

        The request body is in JSON format and requires the following.

        ```
        {
		    "title": "Wash the dishes",
            "description": "Finish it within 20 minutes".
            "deadline": "2023-04-16",
            "status": "completed"
		}
        ```

    - The authenticated user may also opted to put only the detail that is needed to be updated either it is the title, description, deadline or status.

    - **Validations**
        - Checks if the taskId is existing.
        - Deadline should not be in the past.

7. [Delete task](https://todo-list-notes-api.onrender.com/task/73613832-7735-4ed1-a05b-1d26f3531747/)
    - This **DELETE** route allows authenticated users to delete a single task. The URL requires a taskId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/task/taskId/`**

    - **Validation**
        - Checks if the taskId is existing.

8. [Archive task](https://todo-list-notes-api.onrender.com/tasks/archive/0e772e85-ac72-4c51-824a-8779c352cb22)
    - This **PATCH** route allows the authenticated users to archive a specific task. The URL requires a taskId parameter. Please see route below. 

        **`https://todo-list-notes-api.onrender.com/tasks/archive/taskId`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
        - Checks if the taskId is existing.

9. [Activate task](https://todo-list-notes-api.onrender.com/tasks/activate/4b22c7e8-d12a-4f41-b37a-8ba845d3c5da)
    - This **PATCH** route allows the authenticated users to activate a specific task. The URL requires a taskId parameter. Please see route below. 

        **`https://todo-list-notes-api.onrender.com/tasks/activate/taskId`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
        - Checks if the taskId is existing.

10. [Create note](https://todo-list-notes-api.onrender.com/note/)
	- This **POST** route allows authenticated users to create a new note. The request body is in JSON format and requires the following.

        ```
        {
            "title": "How to migrate migrations on django?",
            "Content": "Run this command on your terminal python manage.py makemigrations"
        }
        ```

    - **Validation**
        - Checks if the title is already existing in the database.

11. [Get all notes](https://todo-list-notes-api.onrender.com/note/)
    - This **GET** route allows the authenticated user to fetch the details of all of his/her created notes. The response is JSON format.

12. [Get single note](https://todo-list-notes-api.onrender.com/note/95f4e47e-ae0b-43f9-a04c-e40cd34b8862)
    - This **GET** route allows authenticated users to fetch the details of a certain note. The URL requires as noteId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/note/noteId`**

    - **Validation**
        - Checks if the noteId is existing.

13. [Update note](https://todo-list-notes-api.onrender.com/note/e4ae8224-50bf-4239-bb01-992995e239c7/)
    - This **PATCH** route allows the authenticated user to update the details of a specific note. The URL requires a noteId parameter. Please see route below. 

        **`https://todo-list-notes-api.onrender.com/note/noteId/`**

        The request body is in JSON format and requires the following.

        ```
        {
		    "title": "How to migrate database migrations on django?",
            "content": "Run this command on your terminal python manage.py makemigrations"
		}
        ```

    - The authenticated user may also opted to put only the detail that is needed to be updated either it is the title or content.

    - **Validations**
        - Checks if the noteId is existing.

14. [View order history](https://capstone-2-bautista.onrender.com/users/myOrders)
    - This **GET** route allows authenticated users to view their order history. It requires a bearer token of the user. The response is in a JavaScript object format.

    - **Validation**
        - This route is only permitted to non-admin users. The API will provide an error message if an admin tries to access this route.

15. [Get all products](https://capstone-2-bautista.onrender.com/products/)
	- This **GET** route allows **admin** users to fetch all product details regardless if it is active or not. This requires an admin access token and the response is in a JavaScript object format.

	- **Validation**
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

16. [Add product](https://capstone-2-bautista.onrender.com/products/add)
    - This **POST** route allows **admin** users to add a new product to the database. This requires an admin access token and the request body is in JSON format and requires the following.
        - name
        - description
        - source
        - price

    - The source here, refers to the image url.

    - If the admin wants to add multiple products at the same time. He/she wrap your request body with square brackets. Please refer to the snippet below.

        ```
	    [
		    {
		        "name": "Item A",
		        "description": "Item A description",
		        "source": "https://i.ibb.co/TPx5GDS/product-image-placeholder.jpg",
		        "price": "100"
		    },
		    {
		        "name": "Item B",
		        "description": "Item B description",
		        "source": "https://i.ibb.co/TPx5GDS/product-image-placeholder.jpg",
		        "price": "200"
		    }
		]
        ```

    - **Validations**
        - The API will show an error message as a response, if the provided product name is already existing in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

17. [Update product](https://capstone-2-bautista.onrender.com/products/639ed7800cf6a4468acba0d2)
    - This **PUT** route allows **admin** users to update the details of a specific product. This requires an admin access token and the URL requires a productId parameter. Please see route below. 

        **`https://capstone-2-bautista.onrender.com/products/:productId`**

        The request body is in JSON format and requires the following.

        ```
	    {
	    	"name": Item A,
	    	"description" "Item A description",
	    	"source": "https://i.ibb.co/TPx5GDS/product-image-placeholder.jpg",
	    	"price": 200
		}
        ```

    - The admin may also opted to put only the detail that is needed to be updated either it is the name, description, source or price.

    - **Validations**
        - The API will show an error message as a response, if the provided productId does not exists in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

18. [Archive product](https://capstone-2-bautista.onrender.com/products/639ed7800cf6a4468acba0d2/archive)
    - This **PUT** route allows **admin** users to archive a specific product. This requires an admin access token and the URL requires a productId parameter. Please see route below. 

        **`https://capstone-2-bautista.onrender.com/products/:productId/archive`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
        - The API will show an error message as a response if the provided productId does not exists in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

19. [Activate product](https://capstone-2-bautista.onrender.com/products/639ed7800cf6a4468acba0d2/activate)
    - This **PUT** route allows **admin** users to activate a specific product. This requires an admin access token and the URL requires a productId parameter. Please see route below.

        **`https://capstone-2-bautista.onrender.com/products/:productId/activate`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
        - The API will show an error message as a response if the provided productId does not exists in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

20. [Get all orders](https://capstone-2-bautista.onrender.com/users/allOrders)
    - This **GET** route allows **admin** users to fetch all the orders of all users registered on the API. This requires an admin access token. The response is in a JavaScript object format.

    - **Validation**
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

21. [Get all users](https://capstone-2-bautista.onrender.com/users/allUsers)
    - This **GET** route allows **admin** users to fetch the details of all users registered on the API.
    This requires an admin access token. The response is in a JavaScript object format.

    - **Validation**
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

22. [Set user as admin](https://capstone-2-bautista.onrender.com/users/639ed3720cf6a4468acb9b29/setAsAdmin)
    - This **PUT** route allows **admin** users to pick a user from the list of all users and set him/her as an admin. This requires an admin access token. The URL requires a userId parameter. Please see route below.

        **`https://capstone-2-bautista.onrender.com/users/:userId/setAsAdmin`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
    	- The API will provide an error message as a response, if the provided userId does not exist in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

23. [Set as normal user](https://capstone-2-bautista.onrender.com/users/639ed3720cf6a4468acb9b29/setAsNormalUser)
    - This **PUT** route allows **admin** users to pick a user from the list of all users and revoke admin privilages from him/her. This requires an admin access token. The URL requires a userId parameter. Please see route below.

        **`https://capstone-2-bautista.onrender.com/users/:userId/setAsNormalUser`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
    	- The API will provide an error message as a response, if the provided userId does not exist in the database.
        - This route is only permitted to admin users. The API will provide an error message if a non-admin user tries to access this route.

## <a name="#upcoming-new-features"></a>Upcoming New Features

Since my project does not have features yet that are present on popular E-commerce sites nowadays. I am continously developing new features that will transform my app into a real and publishable one.

Here is an overview of the upcoming features

+ Add shipping address on checkout
+ Payment options
+ Order status
+ Order tracking
+ Order cancellation
+ Product review

## Installation

If you want to checkout the code and install it on your local machine you may clone my repo by simply running this command.

### `git clone git@gitlab.com:batch-211-bautista/capstone-2-bautista.git`

Then install the packages by simply running.

### `npm install`

Then simply run this command to start it on your localhost.

### `nodemon index.js`

Please feel free to use your favorite API Testing tool but I recommend using Postman.

## Roadmap

For the future releases, I'm planning to follow the list of my upcoming new features listed above and I will also update this README file once I got new ideas along the way.

## <a name="#project-status"></a>Project Status

As of now, I'm taking a break on development since I am also going to be busy on Job hunting. But please feel free to check the code and let me know if you find any bugs or potential new features.

## <a name="#language-and-tools"></a>Languages and tools used

<p align="center">
    ![logo-mongodb-with-name](/uploads/f860dec26db0a69ef9a12488812057c8/logo-mongodb-with-name.png)
    ![logo-expressjs-with-name](/uploads/ee4325e407dec9709d189b97ce4cc69c/logo-expressjs-with-name.png)
    ![logo-nodejs-with-name](/uploads/0603502f0b4cded65579c5d773ae3fec/logo-nodejs-with-name.png)
    ![logo-git-with-name](/uploads/048bca6c9875b9bc7a4a35acabb6ec35/logo-git-with-name.png)
    ![logo-postman-with-name](/uploads/44a043b21779f3075455ec8867d3d92b/logo-postman-with-name.png)
    ![logo-sublime-text-3-with-name](/uploads/a41216bc7af655f6d540456e61b216c7/logo-sublime-text-3-with-name.png)
</p>