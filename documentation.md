# Esusu API

## API Documentation
All endpoints except those for user signup and login require an authorization ```access_key``` sent in the ```Authorization``` header along with the request. The token can be obtained after user login by copying the contents of the access_key field in the login response object.
The expected header value is ```Bearer <access_key>```

### User Registration (Sign up)

This endpoint allows a user register on the Esusu platform

Method | URL
------ | ---
POST | auth/signup/

#### Request Object

Type | description
---- |  -----------
**UserSignup** object | Object containing user signup form values.

#### Response Status Code: 201, 403
#### Response Object

Name | Type | description
---- | ---- |  -----------
user | **BaseUser** object | Object containing information describing a user.

### User Login

This endpoint allows a user log into the Esusu platform

Method | URL
------ | ---
POST | auth/login/

#### Request Object

Type | description
---- |  -----------
**Login** object | Object containing user signup form values.

#### Response Status Code: 201, 403, 404
#### Response Object

Name | Type | description
---- | ---- |  -----------
token | **Token** | Object containing jwt access and refresh tokens.

### Setup an Esusu group ( referred to as society in the platform)

This endpoint allows a user to setup savings group preferences to create a co-operative on the platform and become a group (society) admin

Method | URL
------ | ---
POST | society/

#### Request Object

Type | description
---- |  -----------
**SocietyRegistration** object | Object containing society creation form values.

#### Response Status Code: 201
#### Response Object

Name | Type | description
---- | ---- |  -----------
society | **Society** | Json object constaining the basic details of a society.


### Search for public societies to join

This endpoint allows a user to be able to search public societies that can be joined on the platform.

Method | URL
------ | ---
GET | society/search/

#### Request Parameter

ParameterType| Name | Type | description
-------- | ---- | ---- |  -----------
URL Parameter | name | string | The name of the Esusu society

#### Response Status Codes: 200
#### Response Object

Name | Type | description
---- | ---- |  -----------
societies | array | List object containing **Society** objects


### Get members of my Esusu society and the amount of money they have saved

This endpoint allows a society admin, to be able to see a list of all members in their society and how much they have saved.

Method | URL
------ | ---
GET | society/contributions/

#### Response Status Codes: 200, 404, 403
#### Response Object

Name | Type | description
---- | ---- |  -----------
users | array | List object containing **SocietyContribution** objects


### Invite a user to my Esusu society.

This endpoint allows a society admin to be able to send out a society invitation and add a user to the society via a unique ID.

Method | URL
------ | ---
PUT | invite/society/{id}/

#### Response Status Code: 202, 403, 404
#### Response Object

Name | Type | description
---- | ---- |  -----------
**InviteConfirmation** | object | Invite confirmation message


### Create a new Tenure.

This endpoint allows a society admin to create a new Tenure.

Method | URL
------ | ---
POST | tenure/

#### Request Object

Type | description
---- |  -----------
**NewTenure** | Object containing the date a Tenure should start.

#### Response Status Code: 201, 403
#### Response Object

Name | Type | description
---- | ---- |  -----------
**NewTenure** | object | Tenure creation object message


### Get the details of a Tenure and the collection schedule of the society members

This endpoint allows a society admin, to be able to see the tenure start and end dates as well as the collection schedule of all the members in the society.

Method | URL
------ | ---
GET | tenure/{id}/

#### Response Status Codes: 200, 403, 404
#### Response Object

Name | Type | description
---- | ---- |  -----------
tenure | **Tenure** | Object containing the tenure information.


## Object Definitions

### UserSignup
Name | Type | description 
---- | ---- | -----------
email | string | The email address of the user.
first_name | string | The first name of the user
last_name | string | The last name of the user.
password | string | The password of the user. 
confirm_password | string | The password of the user.

### Login
Name | Type | description 
---- | ---- | -----------
email | string | The email address of the user.
password | string | The password of the user. 

### Token
Name | Type | description 
---- | ---- | -----------
refresh_key | string | JWT token to get a new access key without forcing the user to login.
access_key | string | JWT token that provides authentication and authorization information for a user.

### BaseUser
Name | Type | description
---- | ---- |  -----------
id | string | The id of the user.
email | int | The email address of the user.
first_name | double | The first name of the user.
last_name | string | The last name of the user.
is_superuser | boolean | Indicates if the user us a super user.
is_society_admin | boolean | Indicates if a user is a society (group) admin.
is_active | boolean | Indicates if this user is an active user.
date_joined | string | The ISO 8601 datetime the user joined the platform.


#### UserContribution
Name | Type | description
---- | ---- |  -----------
id | string | The id of the user.
email | int | The email address of the user..
first_name | double | The first name of the user.
last_name | string | The last name of the user.
is_superuser | boolean | Indicates if the user us a super user.
is_society_admin | boolean | Indicates if a user is a society (group) admin.
is_active | boolean | Indicates if this user is an active user.
date_joined | string | The ISO 8601 datetime the user joined the platform.
contributions_this_month | int | The amount a user has contributed since the last collection period.
all_time_contribution | string | The amount of money that the user has contributed throughout his/her membership in the society.


### SocietyRegistration
Name | Type | description
---- | ---- | -----------
description | int | The id of the movie the comment belongs to
maximum_capacity | integer | The maximum number of users that can belong to this society.
periodic_amount | Integer | The amount in Naira that each member is meant to contribute each period.
is_searchable | boolean | Indicates if a society should show up in public searches.

### Society
Name | Type | description
---- | ---- | -----------
id | string | The id of the society.
description | int | The id of the movie the comment belongs to
maximum_capacity | integer | The maximum number of users that can belong to this society.
periodic_amount | Integer | The amount in Naira that each member is meant to contribute each period.
is_searchable | boolean | Indicates if a society should show up in public searches.
date_created | string | The ISO 8601 datetime the society was created.


#### SocietyAccount
Name | Type | description
---- | ---- |  -----------
id | string | The id of the user.
balance | int | The account balance of the society.
date_created | string | The ISO 8601 datetime the account was created.


#### SocietyContribution
Name | Type | description
---- | ---- | -----------
id | string | The id of the society.
description | int | The id of the movie the comment belongs to
maximum_capacity | integer | The maximum number of users that can belong to this society.
periodic_amount | Integer | The amount in Naira that each member is meant to contribute each period.
is_searchable | boolean | Indicates if a society should show up in public searches.
users | array | List of **UserContribution** objects.
account | **SocietyAccount** | The account information of the society.

#### InviteConfirmation
Name | Type | description
---- | ---- | -----------
message | string | Invitation description.


#### NewTenure
Name | Type | description
---- | ---- | -----------
start_date | string | The date the Tenure should start.


#### Tenure
Name | Type | description
---- | ---- | -----------
id | string | The tenure id
start_date | string | The tenure start date
tentative_end_date | string | The tenure's tentative end date (See the Tenure model documentation for more.)
maximum_end_date | string | The last day this tenure could reach (See the Tenure model documentation for more.)
collection_schedules | **CollectionSchedule**[] | A list of collection schedules for each user.

#### CollectionSchedule
Name | Type | description
---- | ---- | -----------
id | string | The collection schedule id
user | **BaseUser** | The collecting user.
collection_date | string | The collection date if the user.
