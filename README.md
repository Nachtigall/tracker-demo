# Tracker demo project

## Hey there!

In this repo, you can find my approach to solve tech task. 

### What I have done:

0. docker
* packed all project into Docker. You can run it via `docker-compose up --build tracker` and access via `http://localhost:8001/`

1. general:
* put project requirements in Pipfile via pipenv. With old-style requirements.txt it's quite hard to manage all dependencies. Better solutions for that to have something like Pipenv, Poetry, etc.
* added automatic migration into docker-compose.

2. dev experience:
* added `black` and `isort` libraries to keep sorting and code always in the same style.

3. app logic:
* you can find three apps inside - `project`, `sheet` and `user`

4. endpoints:
* POST `/user/auth/` - used to get auth token (valid for 1 day) which can be used to authenticate future requests. Demo users (username|pass) - `admin|admin`, `test_1|admin`, `test_2|admin`. 
* GET `/user/details/` - get all user details (projects, sheets, etc).

* GET `/project/` - get all projects.
* POST `/project/` - create a project instance.
* GET `/project/{id}/` - get a project instance.
* PATCH `/project/{id}/`- update a project instance (only for project owners).
* DELETE `/project/{id}/`- delete a project instance (only for project owners).

* GET `/sheet/` - get sheet for all users in the same projects.
* POST `/sheet/` - create a sheet instance. User can create sheets only in projects he is involved.
* GET `/sheet/{id}/` - get a sheet instance (if sheet id is from another projects - access if forbidden).
* PATCH `/sheet/{id}/`- update a sheet instance (only own sheet can be edited).
* DELETE `/sheet/{id}/`- delete a sheet instance (only own sheet can be deleted). 

All this information is also available in swagger. Index page redirects to `http://localhost:8001/swagger/` with nice UI.

5. tests:
* added test for `project`, `sheet` and `user`. Not much, of course, but at least basic approach.

In any case, there is a lot of stuff that can be discussed and done differently and I'm more than happy to have a call face to face.
