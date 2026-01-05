import { Injectable, Logger } from '@nestjs/common';
import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';
import {
    BedrockAgentCoreClient,
    InvokeAgentRuntimeCommand,
} from '@aws-sdk/client-bedrock-agentcore';

@Injectable()
export class OrchestratorService {
    private readonly logger = new Logger(OrchestratorService.name);
    private ssmClient: SSMClient;
    private agentCoreClient: BedrockAgentCoreClient;
    private agentRuntimeArn: string | null = null;

    constructor() {
        // Initialize AWS clients - will use default credentials from environment
        this.ssmClient = new SSMClient({});
        this.agentCoreClient = new BedrockAgentCoreClient({});
    }

    /**
     * Retrieve orchestrator agent runtime ARN from Parameter Store
     */
    private async getAgentRuntimeArn(): Promise<string> {
        if (this.agentRuntimeArn) {
            return this.agentRuntimeArn;
        }

        try {
            // Get parameter name from environment or use default
            const parameterName = process.env.SSM_PARAMETER_NAME || '/agents/mahen_orchestrator_agent_arn';

            this.logger.log(`Retrieving agent ARN from Parameter Store: ${parameterName}`);

            const command = new GetParameterCommand({
                Name: parameterName,
            });

            const response = await this.ssmClient.send(command);

            if (response.Parameter?.Value) {
                this.agentRuntimeArn = response.Parameter.Value;
                this.logger.log(`Retrieved agent runtime ARN: ${this.agentRuntimeArn}`);
                return this.agentRuntimeArn;
            }
        } catch (error) {
            this.logger.error(
                `Failed to retrieve agent ARN from Parameter Store`,
                error,
            );
            throw new Error(
                'Could not retrieve orchestrator agent ARN from Parameter Store',
            );
        }

        throw new Error('Failed to get agent runtime ARN');
    }

    /**
     * Invoke the orchestrator agent with streaming support
     * This async generator yields chunks of text as they arrive
     */
    async *invokeAgentStreaming(userQuery: string): AsyncGenerator<string> {
        try {
            const agentRuntimeArn = await this.getAgentRuntimeArn();

            this.logger.log(
                `Invoking agentcore runtime with query: ${userQuery}`,
            );

            const payload = JSON.stringify({ prompt: userQuery });

            const command = new InvokeAgentRuntimeCommand({
                agentRuntimeArn,
                qualifier: 'DEFAULT',
                payload: payload,
            });

            const response = await this.agentCoreClient.send(command);

            // Process the streaming response
            if (response.response) {
                this.logger.log('Processing streaming response...');

                const stream = response.response;

                // Convert the stream to a buffer and process
                const chunks: Uint8Array[] = [];

                // Use the transformToByteArray helper from SDK
                const bytes = await stream.transformToByteArray();
                const fullText = new TextDecoder().decode(bytes);

                // Check if it's event-stream format
                const contentType = response.contentType || '';
                if (contentType.includes('text/event-stream')) {
                    // Parse event-stream format line by line
                    const lines = fullText.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            let content = line.substring(6).trim();
                            // Remove surrounding quotes if present
                            if (content.startsWith('"') && content.endsWith('"')) {
                                content = content.slice(1, -1);
                            }
                            // Unescape newlines
                            content = content.replace(/\\n/g, '\n');
                            if (content) {
                                yield content;
                            }
                        }
                    }
                } else {
                    // Try to parse as JSON, otherwise return as text
                    try {
                        const data = JSON.parse(fullText);
                        yield data.response || fullText;
                    } catch {
                        yield fullText;
                    }
                }
            } else {
                this.logger.warn('No response received from agent');
                yield 'Error: No response from agent';
            }
        } catch (error) {
            this.logger.error('Error invoking agent:', error);
            yield `Error: ${error.message}`;
        }
    }
}
