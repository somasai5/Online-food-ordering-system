
## Online Food Delivery System
Python + Streamlit + Data Structures Project

This project is an Online Food Ordering System implemented using Python, Streamlit for the GUI, and custom Data Structures such as Queue, Stack, Linked List, and File Handling to manage orders.

It replicates real-world restaurant workflows:

Customers browse menu & place orders

Orders go into a Queue (FIFO)

Admin processes orders → move to Stack (LIFO)

Admin can undo last delivery

Admin can add menu items & update item availability status

Order bill is auto generated

## Features
Feature	Description
Customer Order	Browse menu, choose quantity, generate bill
Order Queue	FIFO queue for pending orders
Delivered History Stack	LIFO stack for delivered orders
Undo Delivery	Move last delivered order back to queue
Admin Authentication	Using credentials stored in admin.txt
Edit Menu	Admin can add new food items & toggle availability
File Storage	Uses menu.txt and orders.txt
Streamlit GUI	User-friendly interface
##  Technologies Used

Python

Streamlit

OOP concepts (Classes, Methods)

Queue (Linked List implementation)

Stack (List implementation)

File Handling (menu.txt, admin.txt, orders.txt)

 Project Structure
Online_food_delivery_system/
│
├── main.py               <-- Streamlit application
├── menu.txt              <-- Menu database
├── admin.txt             <-- Admin credentials
└── orders.txt            <-- Saved order history (auto generated)

## menu.txt Format
101,Veg Burger,Burgers,130.00,1
102,Chicken Burger,Burgers,150.00,1
103,Cheese Burger,Burgers,140.00,1
201,Margherita Pizza,Pizza,250.00,1
202,Pepperoni Pizza,Pizza,350.00,1
203,Veggie Pizza,Pizza,300.00,1
301,French Fries,Sides,80.00,1
302,Onion Rings,Sides,90.00,1
401,Coke,Beverages,60.00,0

## admin.txt
Balaji
12345

## How to Run
Install dependencies
pip install streamlit pandas

Run application
streamlit run main.py

Application starts at:
http://localhost:8501

 Working Flow
##  Customer

Browse menu

Add items to cart by quantity

View bill

Order pushed to order queue

## Admin

Login

View Menu

Add New Item

Update Availability (Available / Not Available)

Process Next Order → moves to Delivered stack

Undo Delivery → moves back to Queue

View Pending / Delivered orders



## Data Structure Usage
DS	Usage
Queue (Linked List)	Pending Customer Orders
Stack	Delivered Order History
File Handling	Menu, Admin & Order Storage
Classes & OOP	System modularity





## Future Enhancements

Deploy online on Streamlit Cloud

Add login signup for customers

PDF bill download

Food images & card UI (Swiggy style)

Database integration (SQLite / MySQL)
