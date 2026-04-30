<<<<<<< HEAD
# Dynamic QR Code System

A full-stack application for creating dynamic QR codes with short URLs.

## Features

- Create short URLs with QR codes
- Edit target URLs after creation
- Soft delete QR codes
- Optional expiration timestamps
- URL validation and normalization
- Malicious URL blocking

## Backend (FastAPI)

### Setup

1. Navigate to backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn app.main:app --reload`

### API Endpoints

- `POST /qr` - Create QR code
- `GET /qr/{token}` - Redirect to original URL
- `GET /qr/{token}/image` - Get QR code image
- `PUT /qr/{token}` - Update QR code
- `DELETE /qr/{token}` - Delete QR code
- `GET /qr` - List QR codes

## Frontend (React + TypeScript)

### Setup

1. Navigate to frontend directory
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

## Usage

1. Start the backend server
2. Start the frontend server
3. Open the frontend in browser
4. Create QR codes, edit them, or delete as needed
=======
# QRcode
>>>>>>> 9581dedc568fb9433eb1568b00498bd0539bd6b0
