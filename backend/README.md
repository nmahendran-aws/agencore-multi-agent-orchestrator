# Orchestrator Agent Backend

NestJS backend application that provides WebSocket API to interact with the AWS Bedrock AgentCore orchestrator agent.

## Features

- **WebSocket Communication**: Real-time bidirectional communication using Socket.io
- **Streaming Responses**: Stream agent responses to the frontend as they arrive
- **AWS Integration**: Connects to BedrockAgentRuntime and retrieves agent ARN from SSM Parameter Store
- **CORS Enabled**: Configured to work with frontend on localhost:3000

## Prerequisites

- Node.js 18+ and npm
- AWS credentials configured (via AWS CLI or environment variables)
- Orchestrator agent ARN stored in AWS Parameter Store (default: `/agents/mahen_orchestrator_agent_arn`)

## Installation

```bash
npm install
```

## Configuration

Copy `.env.example` to `.env` and configure if needed:

```bash
cp .env.example .env
```

### Environment Variables

- `SSM_PARAMETER_NAME`: Parameter Store location for agent ARN (default: `/agents/mahen_orchestrator_agent_arn`)
- `AWS_REGION`: AWS region (optional, defaults to AWS CLI config)
- `FRONTEND_URL`: Frontend URL for CORS (default: `http://localhost:3000`)
- `PORT`: Server port (default: `3001`)

The application will use AWS credentials from your AWS CLI configuration by default. If you need to specify credentials explicitly, add them to `.env`.

## Running the Application

### Development Mode

```bash
npm run start:dev
```

The server will start on http://localhost:3001

### Production Mode

```bash
npm run build
npm run start:prod
```

## API

### WebSocket Events

**Client → Server:**
- `message`: Send a user message to the orchestrator agent
  ```javascript
  socket.emit('message', { message: 'Your question here' });
  ```

**Server → Client:**
- `response`: Streaming response chunks from the agent
  ```javascript
  socket.on('response', (chunk) => {
    console.log(chunk);
  });
  ```
- `response-complete`: Signal that the response is complete
  ```javascript
  socket.on('response-complete', () => {
    console.log('Response complete');
  });
  ```
- `error`: Error messages
  ```javascript
  socket.on('error', (error) => {
    console.error(error);
  });
  ```

## Project Structure

```
src/
├── orchestrator/
│   ├── orchestrator.gateway.ts   # WebSocket gateway
│   ├── orchestrator.service.ts   # AWS integration service
│   └── orchestrator.module.ts    # Module definition
├── app.module.ts                 # Root module
└── main.ts                       # Application entry point
```
