# ESUSU API

## Routes Documentation

### User Registration (Sign up)

This endpoint allows a user register on the Esusu platform

Method | URL
------ | ---
POST | auth/signup/

#### Request Object

Type | description
---- |  -----------
**UserSignup** object | Object containing user signup form values.

#### Response Object

Name | Type | description
---- | ---- |  -----------
user | **BaseUser** object | Object containing information describing a user.

### Setup an Esusu group ( referred to as society in the platform)

This endpoint allows a user to setup savings group preferences to create a co-operative on the platform and become a group (society) admin

Method | URL
------ | ---
POST | society/

#### Request Object

Type | description
---- |  -----------
**SocietyRegistration** object | Object containing society creation form values.

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

#### Response Object

Name | Type | description
---- | ---- |  -----------
societies | array | List object containing **Society** objects


### Get members of my Esusu society and the amount of money they have saved

This endpoint allows a society admin, to be able to see a list of all members in their society and how much they have saved.

Method | URL
------ | ---
GET | society/contributions/

#### Response Object

Name | Type | description
---- | ---- |  -----------
users | array | List object containing **SocietyContribution** objects


### Invite a user to my Esusu society.

This endpoint allows a society admin to be able to send out a society invitation and add a user to the society via a unique ID.

Method | URL
------ | ---
PUT | invite/society/{id}/

#### Response Object

Name | Type | description
---- | ---- |  -----------
**InviteConfirmation** | object | Invite confirmation message


## Object Definitions

### UserSignup
Name | Type | description 
---- | ---- | -----------
email | string | The email address of the user
first_name | string | The first name of the user
last_name | string | The last name of the user.
password | string | The password of the user. 
confirm_password | string | The password of the user.

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
email | int | The email address of the user.
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
