import React from 'react';
import type { ProcessingStage } from '../../types';

interface ProcessingStageProps {
  stage: ProcessingStage;
  isActive?: boolean;
}

const ProcessingStageComponent: React.FC<ProcessingStageProps> = ({ 
  stage, 
  isActive = false 
}) => {
  const getStatusIcon = () => {
    switch (stage.status) {
      case 'completed':
        return (
          <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        );
      case 'in_progress':
        return (
          <div className="w-6 h-6 bg-primary-blue rounded-full flex items-center justify-center">
            <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
          </div>
        );
      case 'error':
        return (
          <div className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        );
      default: // pending
        return (
          <div className="w-6 h-6 bg-dark-600 border-2 border-dark-500 rounded-full"></div>
        );
    }
  };

  const getStatusColor = () => {
    switch (stage.status) {
      case 'completed':
        return 'text-green-400';
      case 'in_progress':
        return 'text-primary-blue';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-dark-400';
    }
  };

  return (
    <div className={`
      flex items-start gap-3 p-3 rounded-lg transition-all duration-200
      ${isActive ? 'bg-dark-750 border border-dark-600' : 'hover:bg-dark-800'}
    `}>
      {/* Status Icon */}
      <div className="flex-shrink-0 mt-1">
        {getStatusIcon()}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          {stage.icon && (
            <span className="text-lg" role="img" aria-label={stage.name}>
              {stage.icon}
            </span>
          )}
          <h4 className={`font-light ${getStatusColor()}`}>
            {stage.name}
          </h4>
          {stage.timestamp && (
            <span className="text-xs text-dark-500">
              {new Intl.DateTimeFormat('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
              }).format(stage.timestamp)}
            </span>
          )}
        </div>
        
        <p className="text-sm text-dark-300 font-light leading-relaxed">
          {stage.description}
        </p>

        {/* Progress indicator for in-progress stages */}
        {stage.status === 'in_progress' && (
          <div className="mt-2">
            <div className="w-full bg-dark-600 rounded-full h-1">
              <div className="bg-primary-blue h-1 rounded-full animate-pulse w-1/3"></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessingStageComponent;