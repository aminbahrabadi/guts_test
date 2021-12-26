# Theater Seating Algorithm / API
## Live demo
You can test live demo here: [Theater Seating Algorithm / API](https://guts.ir)
## How to run
1. Clone the project
2. Open terminal and create a virtual environment:
<br />```virtualenv venv```
3. Activate virtual environment:
<br />```source venv/bin/activate```
4. Install packages:
<br />```pip install -r requirements.txt```
5. Migrate and create database:
<br />```python manage.py migrate```
6. Run server:
<br />```python manage.py runserver```
7. You can run tests:
<br />```python manage.py test```
8. Open the browser and browse this URL:
<br />```127.0.0.1:8000```
## Quickstart
1. Create a section
2. Create seats in the section
3. Create customers
4. Seat customers
### OR
Click on ```Quickstart``` button on the navbar to create a section with 3 rows and 8 seats in every row.
## Reseting
You can delete all Sections and all Customers by browsing to reset section. The reset section can be found in the navbar items.
## Api
### Sections Retrieve (GET request):
<br />URL: ```/api/retrieve-sections/```
### Seats Retrieve (POST request):
<br />URL: ```/api/retrieve-seats/```
<br />Data load sample: ```{
   "section_id":1
}```
### Ticket wallet api (POST request):
<br />URL: ```/api/retrieve-single-seat/```
<br />Data load sample: ```{
   "customer_name":"Amin"
}```
### Seat customers api (POST request):
<br />URL: ```/api/bulk-seating/```
<br />Data load sample: ```{
   "section_id":1,
   "customer_list":[
      [
         "A",
         "aisle",
         "3"
      ],
      [
         "B",
         "",
         "3"
      ]
   ]
}```
