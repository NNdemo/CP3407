
## Database Structure

The cleaning service platform uses SQLite with SQLAlchemy ORM. The database consists of three main entities:

1. **User** - Stores both customer and service provider information
2. **CleaningService** - Contains the service details offered by providers
3. **Appointment** - Manages the scheduling between customers and providers

### ER Diagram
![ER Diagram](images/database_ERD.png)


### UML Diagram
![UML Diagram](images/database_UML.jpg)

### Prototype

#### Index
![Index Design](images/indexDesign.png)

#### Login
![Login Page](images/Login.png)

#### Register
![Register Page](images/Register.png)

#### View Bookings
![View Bookings](images/ViewAssignedBooking.png)