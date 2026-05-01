<<<<<<< HEAD
# QR Code Generator

A full-stack application for creating QR Code with short URLs.

## GIF
<img width="800" height="750" alt="ezgif-82fdf17dab057f1a" src="https://github.com/user-attachments/assets/bd3f03af-f9f5-4c96-9aee-4d809348622b" />

## Image
<img width="992" height="951" alt="QR_CODE_jpg" src="https://github.com/user-attachments/assets/e393783b-f839-4003-99d0-5bd38da0406a" />

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
