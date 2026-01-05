import { Module } from '@nestjs/common';
import { OrchestratorGateway } from './orchestrator.gateway';
import { OrchestratorService } from './orchestrator.service';

@Module({
    providers: [OrchestratorGateway, OrchestratorService],
})
export class OrchestratorModule { }
