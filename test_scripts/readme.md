# MyClean Application Test Script Collection

## 📁 Directory Structure

This directory contains a comprehensive test suite for the MyClean application, covering backend API testing, frontend UI testing, and various utility tools.

## 🚀 Quick Start

### 1. Verify Setup (Recommended to run first)
```bash
C:\Python312\python.exe verify_setup.py
```

### 2. Install Test Dependencies
```bash
C:\Python312\python.exe install_test_dependencies.py
```

### 3. Run Recommended Tests
```bash
# Backend API Test (Recommended to run first)
C:\Python312\python.exe test_backend_only.py

# Simplified Comprehensive Test
C:\Python312\python.exe test_myclean_simple.py
```

## 📋 Test Script Documentation

### 🔧 Core Test Scripts

#### `test_backend_only.py` ⭐ **Recommended**
- **Function**: Dedicated backend API functionality testing
- **Features**: Most stable and comprehensive backend testing
- **Test Coverage**:
  - Health check (`/api/health`)
  - User registration (`/api/auth/register`)
  - User login (`/api/auth/login`)
  - Service management (`/api/services`)
  - Order management (`/api/orders`)
- **Requirements**: Only backend service needs to be running
- **Expected Result**: 🎉 All backend API tests pass!

#### `test_myclean_simple.py`
- **Function**: Simplified comprehensive testing
- **Features**: Quick verification of core functionality
- **Test Coverage**: Backend API + Frontend health check
- **Requirements**: Backend service must be running, frontend optional
- **Use Case**: Quick application status verification

#### `test_frontend_ui.py`
- **Function**: Frontend user interface automation testing
- **Features**: Uses Selenium WebDriver for UI testing
- **Test Coverage**:
  - Page navigation testing
  - User registration forms
  - User login forms
  - Service page browsing
- **Requirements**: Frontend service + Chrome browser required
- **Dependencies**: selenium, webdriver-manager

#### `test_myclean_app.py`
- **Function**: Complete frontend and backend testing
- **Features**: Most comprehensive test coverage
- **Test Coverage**: Includes all functional module tests
- **Requirements**: Both frontend and backend services must be running
- **Use Case**: Complete regression testing

#### `run_all_tests.py`
- **Function**: Comprehensive test suite manager
- **Features**: Automatically runs multiple test scripts and generates reports
- **Capabilities**:
  - Automatic service status detection
  - Batch test execution
  - Detailed test report generation
  - Save test results to files

### 🛠️ Utility Tool Scripts

#### `install_test_dependencies.py`
- **Function**: Automatically installs required Python dependencies for testing
- **Packages**: requests, selenium, webdriver-manager
- **When to Use**: Before running tests for the first time

#### `debug_backend.py`
- **Function**: Backend API debugging tool
- **Features**: Quick diagnosis of backend issues
- **Test Items**:
  - Health check
  - Service list retrieval
  - User registration testing
- **Use Case**: Quick diagnosis when backend issues occur

#### `fix_database.py`
- **Function**: Database repair and rebuild tool
- **Features**: Resolves database-related issues
- **Capabilities**:
  - Delete old database
  - Create new database structure
  - Insert initial test data
- **When to Use**: When database is corrupted or has structural issues

#### `check_database.py`
- **Function**: Database status checking tool
- **Features**: Non-destructive checking
- **Check Items**:
  - Database connection status
  - Table structure integrity
  - Data record statistics
- **Use Case**: Verify database status

#### `start_backend.py`
- **Function**: Backend service startup helper script
- **Features**: Simplifies backend startup process
- **Capability**: Automatically switches to backend directory and starts service

#### `verify_setup.py`
- **Function**: Verify test environment setup
- **Features**: Checks if all files are properly configured
- **Check Items**:
  - Test script integrity
  - Documentation file existence
  - Backend file accessibility
- **When to Use**: After initial setup or when encountering path issues

### 📄 Configuration Files

#### `test_requirements.txt`
- **Function**: Test dependency package list
- **Contents**:
  ```
  requests>=2.31.0
  selenium>=4.15.0
  webdriver-manager>=4.0.0
  ```

## 📚 Documentation Files

### `README_Test_Instructions.md`
- Detailed test usage documentation
- Complete installation and usage guide
- Troubleshooting guide

### `Test_Results_Report.md`
- Complete test execution report
- Test result statistics and analysis
- Problem resolution records

### `Quick_Test_Guide.md`
- Quick start guide
- One-click test commands
- Frequently asked questions

## 🎯 Test Coverage Features

### ✅ Fully Tested Features
- **User Management**
  - Customer registration and login
  - Service provider registration and login
  - Password hashing and verification

- **Service Management**
  - Service list retrieval (6 service types)
  - Service categorization (Flowers, Cleaning, Gifts)
  - Service duration options (10 configurations)
  - Price calculation and multiplier handling

- **Order Management**
  - Order creation and validation
  - Order number generation
  - Price calculation
  - Time handling
  - Order status management

- **Database Operations**
  - CRUD operation verification
  - Data integrity checking
  - Relational query testing

### ⏳ Features Requiring Frontend Service
- User interface interaction testing
- Form submission validation
- Page navigation testing
- Role switching functionality

## 🔧 Environment Requirements

### Required Software
- **Python 3.12** - For running test scripts
- **Chrome Browser** - For frontend UI testing (optional)

### Service Requirements
- **Backend Service**: http://localhost:8000 (required)
- **Frontend Service**: http://localhost:5173 (required for UI testing)

### Python Dependencies
- requests >= 2.31.0
- selenium >= 4.15.0 (for UI testing)
- webdriver-manager >= 4.0.0 (for UI testing)

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Backend Connection Failed
```bash
# Check backend service status
C:\Python312\python.exe debug_backend.py

# If database issues, repair database
C:\Python312\python.exe fix_database.py
```

#### 2. Database Error (500 Internal Server Error)
```bash
# Rebuild database
C:\Python312\python.exe fix_database.py

# Check database status
C:\Python312\python.exe check_database.py
```

#### 3. Missing Dependencies
```bash
# Reinstall dependencies
C:\Python312\python.exe install_test_dependencies.py
```

#### 4. Chrome Browser Issues
- Ensure Chrome browser is installed
- Check if ChromeDriver is properly installed
- Can enable headless mode in test scripts

## 📊 Test Execution Records

### Latest Test Results ✅
```
[15:26:30] SUCCESS: 🎉 All backend API tests passed!
✅ Test completed: Backend API functionality normal!

Test Statistics:
- Total test items: 5 main functional modules
- Passed tests: 5/5 (100%)
- Failed tests: 0/5 (0%)
```

### Test Data Examples
- **Users**: 2 preset users + dynamically generated test users
- **Services**: 6 service types (Fresh Flowers $21.0, Dried Flowers $25.0, etc.)
- **Orders**: Dynamically generated test orders
- **Database**: 5 main tables with complete relational structure

## 🎉 Usage Recommendations

### Daily Development Testing
1. **Quick Verification**: `test_backend_only.py`
2. **Issue Diagnosis**: `debug_backend.py`
3. **Database Issues**: `fix_database.py`

### Complete Regression Testing
1. **Start Services**: Backend + Frontend
2. **Run Tests**: `run_all_tests.py`
3. **View Reports**: Check generated test reports

### First-Time Usage
1. **Verify Setup**: `verify_setup.py`
2. **Install Dependencies**: `install_test_dependencies.py`
3. **Fix Database**: `fix_database.py`
4. **Run Tests**: `test_backend_only.py`

## 📞 Technical Support

If you encounter issues:
1. Check `Quick_Test_Guide.md` for quick solutions
2. Check `README_Test_Instructions.md` for detailed instructions
3. Check `Test_Results_Report.md` for known issues and solutions

---

**Last Updated**: 2025-07-30
**Test Status**: ✅ Backend functionality fully operational
**Maintenance Status**: 🔄 Under continuous maintenance