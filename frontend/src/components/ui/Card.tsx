import React from 'react';
import type { CardProps } from '../../types';

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  padding = 'md',
  border = true,
  shadow = 'md',
}) => {
  const paddingClasses = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  };

  const shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  };

  const cardClasses = `
    bg-dark-800 rounded-lg transition-all duration-200
    ${border ? 'border border-dark-700' : ''}
    ${shadowClasses[shadow]}
    ${paddingClasses[padding]}
    ${className}
  `;

  return (
    <div className={cardClasses}>
      {children}
    </div>
  );
};

export default Card;