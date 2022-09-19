# **JBT Employment DEMO**

## ********Drone Pizza delivery system********

### **Introduction**
This system was built to provide a demonstration of work skills for Chris Lee. 

### **Installation**
1. [Install Python](https://www.python.org/)
2. [Install Django](https://www.djangoproject.com/download/)
3. Clone repository

### **System Provisioning**

1. Go to main project directory in terminal. 
2. Run `python manage.py runserver`. This will create the blank database tables.
3. Run `python manage.py createsuperuser`. Follow prompts to create user credentials to access the Django Admin.
4. Open browser and navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) 
5. Run `manage.py import_deliveries`. This will import the deliveries.

### **How to Use the system**
The system has not been tested to run. No unit test were written. 

1. http://127.0.0.1:8000/get_next_destination/<int:drone_token>/ is the only end point. Token is currently only an integer
for drone identification. An implementation of security protocols will need to be added.
   
2. csv import can be found at drone_destination/management/commands/import_deliveries

### Original Instructions
Here is the challenge:
 
Create a backend service to calculate routes for a small pizza chain that recently purchased one drone to deliver their pizzas. Drone range is 25 miles and must come back to the store for a new battery before it runs out of energy.
The drone will reach out to your backend service to receive its next destination in GPS coordinates. The drone will only request the next destination once it is ready to leave the pizza store, or once it has reached a previously commanded destination and made a delivery.
You may use any programming language you prefer. Your code should be syntactically correct, but it is not required to be functional.
 
Assumptions:
-              Assume the only requirement to come back to the Pizza store is to get new batteries (Infinite Pizza storage capacity).
-              Assume the drone has a constant and stable internet connection.
-              You cannot send direct commands to the drone, but you may assume that another service exists which will provide you with any information you may need about the drone (example: remaining range, current location, etc).
Expected functionality:
1.            Given a CSV file with order time and delivery address, calculate the optimal path (you are free to define what “optimal path” means to you).
2.            Provide a HTTP GET endpoint that will send the drone its next destination in GPS coordinates upon request. Remember, the drone will only reach out to your backend service to get the next destination once it has completed its previous destination or when it’s ready to leave the pizza store.
3.            The drone will reach out to your backend service with a set username and password to authenticate itself. Your backend service must authenticate the drone and provide it with a token that it can use to authorize all subsequent requests to your REST API. This token must be validated before providing the drone any data. The token must expire 1 hour after being issued and the drone must request to refresh the token or obtain a new one.
You are welcome to implement any additional functionality you think is important for this scenario.

### Updated Instructions
Hi Chris,
 
Glad to see you in our next stage, and always a good idea to ask questions if things are unclear. I will be cautious, 
and answer your direct questions where it makes sense, and let you decide in areas that we would like to see your 
idea(s). Answers interjected in blue below.

* Am I expected to queue up the records, and give the drone the next closest address if it can make it to 
the next destination and be able to reach home? 
```diff
The drone will only request the next destination:
- once it is ready to leave the pizza store
- once it has reached a previously commanded destination and made a delivery.
The drone will not queue,  it will only ask service at the scenarios above. Do the best service prep you can in order to service the drones requests.
Remember to make sure the drone can always make it home for re-charge.
```
* Are pizza delivery priorities based on order time or destination? It’s a slippery slope if destination is 
chosen. 
```diff
Latitude for you to enforce your pizza company policies. I think the best business case is to 
make it as cost effective and efficient as possible.
```
* Assumptions:
    * Will I assume that the range is static, and we don’t need to account for weather for the range?
  
```diff
Do not worry about weather. Let’s assume sunny skies and no wind interference.
```

*   CSV questions:
What does this csv file look like in regards to number of records? Am I to assume building a manage.py command and set a 
    cron job to run that command, to look for new records?

```diff
Example: # of records should handle dynamic list.
order_time        address
8/11/2022 12:15   6868 Capri Ave, Ventura CA
8/11/2022 13:15   311 E Daily Dr, Camarillo CA
8/11/2022 14:15   3900 Bluefin Cir, Oxnard CA
..
Adding or subtracting can be a talking points in your code, but we understand limited time on first POC.
```
 

I’m unsure why we would be calculating optimum path during the csv import process. I would expect to do this based on 
the HTTP get process from the drone. This seems more scalable, based on the possibility of multiple drones and where 
each drone is currently located at a particular time and battery capacity (based on the assumption that everyone gets 
the same pizza from the unlimited pizza storage capacity). Can you please clarify the why in calculating the optimal 
path during the import process?
```diff
This is a matter of design on if you pre-calculate or real time calculate. You are at liberty to determine based on 
complexity, or value.
```

As far as the authentication portion.  My thoughts are that each drone would be provisioned within a secured siloed 
network from the manufacturer, and given an initial token to start with.  I’m unsure why a drone would be using a 
username and a password (that seems more like something that the pizza company’s provisioning process would use). 
Once the pizza company has logged in and taken delivery of the drone, that’s where I see a refresh token is given to 
the drone.  I’m happy to accept your response for this as “Just do what the instructions say”
```diff
Please, you won’t hear that response 😊
Your point is valid, Rewording the requirement as follow.
3. The drone will reach out to your backend service with secure credentials.
  
I hope this information helps. Please let me know if I misinterpreted or did not address your concerns.
Important: make sure the test has a level of interest/fun for you !! and don’t go deep into a rabbit hole. It’s ok to pass or stub if needed with your time budget.
 
Best Regards,
-john
```

