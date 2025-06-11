
## Database Structure

The cleaning service platform uses SQLite with SQLAlchemy ORM. The database consists of three main entities:

1. **User** - Stores both customer and service provider information
2. **CleaningService** - Contains the service details offered by providers
3. **Appointment** - Manages the scheduling between customers and providers

### ER Diagram

```mermaid
erDiagram
    User ||--o{ CleaningService : "provides"
    User ||--o{ Appointment : "books as customer"
    User ||--o{ Appointment : "fulfills as provider"
    CleaningService ||--o{ Appointment : "included in"
    
    User {
        int id PK
        string email
        string username
        string hashed_password
        string full_name
        string phone_number
        enum user_type
        bool is_active
    }
    
    CleaningService {
        int id PK
        string name
        text description
        float price
        int duration
        bool is_active
        int provider_id FK
    }
    
    Appointment {
        int id PK
        int customer_id FK
        int service_id FK
        int provider_id FK
        datetime appointment_date
        enum status
        string notes
        datetime created_at
        datetime updated_at
    }
```


### Prototype

#### Index
![Index Design](design/images/indexDesign.png)

#### Login
![Login Page](design/images/Login.png)

#### Register
![Register Page](design/images/Register.png)

#### View Bookings
![View Bookings](design/images/ViewAssignedBooking.png)