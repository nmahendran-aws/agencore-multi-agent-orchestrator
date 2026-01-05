import {
    WebSocketGateway,
    WebSocketServer,
    SubscribeMessage,
    MessageBody,
    ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';
import { OrchestratorService } from './orchestrator.service';

@WebSocketGateway({
    cors: {
        origin: '*', // In production, specify your frontend URL
    },
})
export class OrchestratorGateway {
    @WebSocketServer()
    server: Server;

    private readonly logger = new Logger(OrchestratorGateway.name);

    constructor(private readonly orchestratorService: OrchestratorService) { }

    @SubscribeMessage('message')
    async handleMessage(
        @MessageBody() data: { message: string },
        @ConnectedSocket() client: Socket,
    ): Promise<void> {
        this.logger.log(`Received message from client: ${data.message}`);

        try {
            // Stream the response back to the client
            for await (const chunk of this.orchestratorService.invokeAgentStreaming(
                data.message,
            )) {
                // Emit each chunk as it arrives
                client.emit('response', chunk);
            }

            // Signal completion
            client.emit('response-complete');
        } catch (error) {
            this.logger.error('Error processing message:', error);
            client.emit('error', { message: error.message });
        }
    }

    handleConnection(client: Socket) {
        this.logger.log(`Client connected: ${client.id}`);
    }

    handleDisconnect(client: Socket) {
        this.logger.log(`Client disconnected: ${client.id}`);
    }
}
