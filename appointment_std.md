# 🗺️ Technical Roadmap: Multi-Step Customer Booking Flow (Wizard Booking Flow)

### 📌 Overall Architecture

- **Frontend Strategy:** Step-by-step state storage in the browser's `sessionStorage` to create a fast, page-refresh-free multi-step form (Wizard).
    
      
    
- **Backend Architecture:** Each step in this process features completely isolated dedicated **Views**, **Actions**, and **Services** to ensure input/output logic remains separated per step.
    
      
    

## 🎯 Step-by-Step Stages & Sample Request/Response Data

### 🟢 Step 1: Mobile Number Entry & Authentication (OTP)

In this step, the mobile number is received, a verification code is sent, and after confirmation, the user is authenticated.

  

- **Sample Request Payload:**
    
      
    

JSON

```
{
  "phone_number": "09123456789",
  "otp_code": "5842"
}
```

- **Sample Response Payload:**
    
      
    

JSON

```
{
  "status": "success",
  "message": "Code verified successfully",
  "is_authenticated": true
}
```

- **Browser Cache Storage (`sessionStorage`):**
    
      
    

JSON

```
{
  "phone_number": "09123456789"
}
```

### 🟢 Step 2: Barber and Service Selection (Dynamic Filtering)

In this step, the list of barbers along with specific services offered by each barber is retrieved, and data is saved after user selection.

  

- **Sample Request:**
    
    Request to fetch barber and service data (no special parameters required).
    
      
    
- **Sample Response Payload:**
    
      
    

JSON

```
[
  {
    "barber_id": 1,
    "barber_name": "Ali Rasouli",
    "services": [
      {
        "service_id": 10,
        "name": "Haircut & Beard Trim",
        "price": 250000,
        "duration_minutes": 45
      },
      {
        "service_id": 12,
        "name": "Groom Package",
        "price": 1200000,
        "duration_minutes": 120
      }
    ]
  },
  {
    "barber_id": 2,
    "barber_name": "Reza Moradi",
    "services": [
      {
        "service_id": 10,
        "name": "Haircut",
        "price": 200000,
        "duration_minutes": 40
      }
    ]
  }
]
```

- **Browser Cache Storage (`sessionStorage`):**
    
      
    

JSON

```
{
  "phone_number": "09123456789",
  "barber_id": 1,
  "service_id": 10
}
```

### 🟢 Step 3: Date & Available Time Slots Selection

Based on the selected barber and service, working days and available slots are retrieved, and the user selects their desired time.

  

- **Sample Request Query:**
    
      
    

JSON

```
{
  "barber_id": 1,
  "service_id": 10
}
```

- **Sample Response Payload:**
    
      
    

JSON

```
{
  "available_slots": {
    "2026-09-10": ["10:00", "10:45", "11:30", "16:00", "16:45"],
    "2026-09-11": ["11:00", "11:45", "17:00", "17:45"]
  }
}
```

- **Browser Cache Storage (`sessionStorage`):**
    
      
    

JSON

```
{
  "phone_number": "09123456789",
  "barber_id": 1,
  "service_id": 10,
  "booking_date": "2026-09-10",
  "start_time": "16:00"
}
```

### 🟢 Step 4: Information Preview & Final Booking Submit (Review & Final Submit)

All collected information from the browser cache is displayed to the user, and upon clicking the final submit button, the entire structure is sent to the server for storage.

  

- **Sample Final Request Payload (from Browser Cache):**
    
      
    

JSON

```
{
  "phone_number": "09123456789",
  "barber_id": 1,
  "service_id": 10,
  "booking_date": "2026-09-10",
  "start_time": "16:00"
}
```

- **Sample Response Payload:**
    
      
    

JSON

```
{
  "status": "success",
  "message": "Your appointment has been successfully booked.",
  "appointment_id": 1048,
  "details": {
    "barber_name": "Ali Rasouli",
    "service_name": "Haircut & Beard Trim",
    "date": "2026-09-10",
    "start_time": "16:00",
    "end_time": "16:45",
    "final_price": 250000
  }
}
```

- **Action after Successful Response:** Clear `sessionStorage` and redirect the user to the "Booking Confirmation" page.