import React, { useState } from 'react';
import { Card } from '../ui';
import ProcessingStageComponent from './ProcessingStage';
import type { TransparencyState } from '../../types';

interface TransparencyPanelProps {
  transparencyState: TransparencyState;
  className?: string;
}

const TransparencyPanel: React.FC<TransparencyPanelProps> = ({
  transparencyState,
  className = '',
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!transparencyState.isActive) {
    return null;
  }

  const completedStages = transparencyState.stages.filter(stage => stage.status === 'completed');
  const progressPercentage = Math.round((completedStages.length / transparencyState.stages.length) * 100);

  return (
    <Card className={`${className}`} padding="none">
      {/* Header */}
      <div className="p-4 border-b border-dark-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-primary-blue rounded-full animate-pulse"></div>
              <h3 className="text-lg font-light text-dark-100">
                🤖 Processing Your Request
              </h3>
            </div>
            {transparencyState.progress > 0 && (
              <span className="text-sm text-dark-400 bg-dark-700 px-2 py-1 rounded">
                {progressPercentage}%
              </span>
            )}
          </div>
          
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
            aria-label={isExpanded ? 'Collapse' : 'Expand'}
          >
            <svg
              className={`w-5 h-5 text-dark-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mt-3">
          <div className="w-full bg-dark-600 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-primary-blue to-primary-purple h-2 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${transparencyState.progress * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Stages List */}
      {isExpanded && (
        <div className="p-4">
          <div className="space-y-2">
            {transparencyState.stages.map((stage) => (
              <ProcessingStageComponent
                key={stage.id}
                stage={stage}
                isActive={transparencyState.currentStage?.id === stage.id}
              />
            ))}
          </div>

          {/* Footer */}
          <div className="mt-4 pt-4 border-t border-dark-700">
            <div className="flex items-center justify-between text-sm text-dark-400">
              <span>
                {completedStages.length} of {transparencyState.stages.length} steps completed
              </span>
              <span>
                Real-time processing insights
              </span>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
};

export default TransparencyPanel;