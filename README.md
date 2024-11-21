# Table of contents
+ [Introduction](#todo-list-api)
+ [Routes](#routes)
+ [Upcoming new features](#upcoming-new-features)
+ [Installation](#installation)
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

14. [Delete note](https://todo-list-notes-api.onrender.com/note/95f4e47e-ae0b-43f9-a04c-e40cd34b8862/)
    - This **DELETE** route allows authenticated users to delete a single note. The URL requires a taskId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/note/noteId/`**

    - **Validation**
        - Checks if the noteId is existing.

15. [Get all users tasks](https://todo-list-notes-api.onrender.com/all_tasks)
	- This **GET** route allows **admin** users to fetch all tasks details of all users. This requires the user to be a superuser and the response is JSON format.

16. [Get all users notes](https://todo-list-notes-api.onrender.com/all_notes)
    - This **GET** route allows **admin** users to fetch all notes details of all users. This requires the user to be a superuser and the response is JSON format.

17. [Get all users](https://todo-list-notes-api.onrender.com/all_users)
    - This **GET** route allows **admin** users to fetch details of all users. This requires the user to be a superuser and the response is JSON format.

18. [Set user as admin](https://todo-list-notes-api.onrender.com/set_as_admin/2)
    - This **PATCH** route allows **admin** users to pick a user from the list of all users and set him/her as an admin. This requires the user to be a superuser. The URL requires a userId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/set_as_admin/userId`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
    	- Checks if the userId is existing.

19. [Set as normal user](https://todo-list-notes-api.onrender.com/set_as_normal_user/2)
    - This **PATCH** route allows **admin** users to pick a user from the list of all users and revoke admin privilages from him/her. This requires the user to be a superuser. The URL requires a userId parameter. Please see route below.

        **`https://todo-list-notes-api.onrender.com/set_as_normal_user/userId`**

    - The API will provide a message as a response, once operation is successful.

    - **Validations**
    	- Checks if the userId is existing.

## <a name="#upcoming-new-features"></a>Upcoming New Features

What I have in mind is to make the task and notes draggable and make the deleting of each to be a drag and drop action.

Here is an overview of the upcoming features

+ Drag and drop sorting
+ Drag and drop deleting

## Installation

If you want to checkout the code and install it on your local machine you may clone my repo by simply running this command.

### `git clone https://github.com/edmarjames/todo-list-api.git`

Then run the index.html using live server.

Please feel free to use your favorite API Testing tool but I recommend using Postman.

## <a name="#project-status"></a>Project Status

As of now, I'm taking a break on development since I am also going to be busy on my day job. But please feel free to check the code and let me know if you find any bugs or potential new features.

## <a name="#language-and-tools"></a>Languages and tools used

<p align="left" style="display: flex; justify-content: space-around;">
    <img src="https://i.ibb.co/VWnyF7X/drf.png" alt="drf" width="50" height="50" />
    <img src="https://i.ibb.co/M2yZBc7/django.png" alt="django" width="50" height="50" />
    <img src="https://i.ibb.co/JQ2XBm1/python.png" alt="django" width="50" height="50" />
    <img src="https://i.ibb.co/PZZLq7J/vscode-removebg-preview.png" alt="vscode" width="50" height="50" />
    <img src="https://i.ibb.co/n6Ddy51/logo-postman.png" alt="postman" width="55" height="55" />
</p>
