
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

### UML Diagram
```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string username
        +string hashed_password
        +string full_name
        +string phone_number
        +string user_type
        +bool is_active
        +register()
        +login()
        +updateProfile()
        +deactivate()
    }

    class CleaningService {
        +int id
        +string name
        +string description
        +decimal price
        +int duration
        +bool is_active
        +int provider_id
        +createService()
        +updateService()
        +disableService()
    }

    class Appointment {
        +int id
        +int customer_id
        +int service_id
        +int provider_id
        +datetime appointment_date
        +string status
        +string notes
        +datetime created_at
        +datetime updated_at
        +createAppointment()
        +cancel()
        +updateStatus()
        +addNotes()
    }

    User "1" <-- "0..*" CleaningService : provides
    User "1" <-- "0..*" Appointment : books
    CleaningService "1" <-- "0..*" Appointment : includes
    User "1" <-- "0..*" Appointment : serves


```

### Prototype

#### Index
![Index Design](images/indexDesign.png)

#### Login
![Login Page](images/Login.png)

#### Register
![Register Page](images/Register.png)

#### View Bookings
![View Bookings](images/ViewAssignedBooking.png)