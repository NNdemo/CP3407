# Iteration 2 Test Report

## User Stories Implementation Status

| # | User Story | Priority | Effort Estimate | Status | Test Result |
|---|------------|----------|-----------------|--------|-------------|
| 1 | Customer Account Registration | 10 | 1.4 days | ✅ Implemented | ✅ Running Correctly |
| 2 | Customer Account Login | 10 | 2 days | ✅ Implemented | ✅ Running Correctly |
| 3 | Browse Cleaning Services | 10 | 5 days | ✅ Implemented | ✅ Running Correctly |
| 4 | Book a Cleaning Service | 10 | 5 days | ✅ Implemented |✅ Running Correctly|
| 5 | View Assigned Bookings | 30 | 2.5 days |  ✅ Implemented |✅ Running Correctly|
| 6 | Provider Account Registration | 10 | 5 days | ✅ Implemented |✅ Running Correctly|
| 7 | Provider Login | 10 | 5 days | ✅ Implemented |✅ Running Correctly|
| 8 | Manage Provider Availability| 10 | 5 days | ✅ Implemented |✅ Running Correctly|

## Test Summary

Iteration 2 user stories all have been implemented successfully and they are operational. The application has a complete set of functionality of:

- **User Authentication**: Registration and login systems for customers and providers
- **Service Discovery**: Browse and view available cleaning services
- **Booking System**: Complete booking workflow for cleaning services
- **Order Management**: View and track assigned bookings
- **Provider Order Check**: provider can access the pending order to confirm whether to accept it.

## Test Coverage

- ✅ Frontend UI components
- ✅ Backend API endpoints
- ✅ Database operations
- ✅ User authentication flow
- ✅ Service booking workflow
- ✅ Order management system

## Issues Encountered and Resolved

- All functions are operating normally and no problems have been found for the time being
- Some functions, such as providers updating order information and accepting orders, have bugs when users create orders. Users' operations on the front end cannot connect the updated information to the back end and write it to the database
- During iteration 2, we modified the front-end code and the back-end interface. Now, the functions with bugs can operate normally

## Notes

- Each of the user stories is completed with their priority levels and effort estimations
- The customers have an end-to-end application experience with the app.
- The service management is also provided on the provider side
- The database schema can carry out all the required operations
- Individual API endpoints are secured adequately and in a manner that they are functional
