# Orchestrator Agent Frontend

Next.js frontend application that provides a modern chat interface to interact with the orchestrator agent via WebSocket.

## Features

- **Real-time Chat**: WebSocket-based communication using Socket.io
- **Streaming Responses**: Display agent responses as they stream in real-time
- **Premium UI**: Modern dark theme with glassmorphism effects and smooth animations
- **Conversation History**: Maintains message history during the session
- **Connection Status**: Visual indicator for WebSocket connection state

## Prerequisites

- Node.js 18+ and npm
- Backend server running on port 3001 (or configured URL)

## Installation

```bash
npm install
```

## Configuration

Create a `.env.local` file with the backend URL (optional - defaults to http://localhost:3001):

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:3001
```

See `env.example.txt` for reference.

## Running the Application

### Development Mode

```bash
npm run dev
```

The app will start on http://localhost:3000

### Production Mode

```bash
npm run build
npm run start
```

## Usage

1. Ensure the backend server is running
2. Open http://localhost:3000 in your browser
3. Wait for the connection indicator to show green
4. Type your message and press Enter or click Send
5. Watch as responses stream in real-time from the orchestrator agent

## Features

### Chat Interface
- **User Messages**: Displayed on the right with gradient background
- **Assistant Messages**: Displayed on the left with glass morphism effect
- **Streaming**: Responses appear character by character as they arrive
- **Loading States**: Visual indicators while waiting for responses

### Keyboard Shortcuts
- **Enter**: Send message
- **Shift + Enter**: New line in message

## Project Structure

```
app/
├── globals.css          # Global styles with glassmorphism theme
├── layout.tsx           # Root layout with metadata
└── page.tsx             # Main chat interface component
```

## Styling

The application uses:
- **Tailwind CSS**: Utility-first CSS framework
- **Custom CSS**: Glassmorphism effects, gradients, animations
- **Inter Font**: Modern typography from Google Fonts

## WebSocket Events

The frontend listens for:
- `connect`: Connection established
- `disconnect`: Connection lost
- `response`: Streaming response chunks
- `response-complete`: Response finished
- `error`: Error messages
