import React from 'react';
import type { TextareaProps } from '../../types';

const Textarea: React.FC<TextareaProps> = ({
  label,
  placeholder,
  value,
  onChange,
  error,
  disabled = false,
  rows = 4,
  className = '',
}) => {
  const textareaClasses = `
    w-full px-3 py-2 bg-dark-800 border rounded-lg text-dark-100 font-light
    placeholder-dark-400 transition-colors duration-200 resize-vertical
    focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent
    disabled:opacity-50 disabled:cursor-not-allowed custom-scrollbar
    ${error ? 'border-red-500 focus:ring-red-500' : 'border-dark-600 hover:border-dark-500'}
    ${className}
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-light text-dark-200 mb-1">
          {label}
        </label>
      )}
      <textarea
        className={textareaClasses}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        disabled={disabled}
        rows={rows}
      />
      {error && (
        <p className="mt-1 text-sm text-red-400 font-light">{error}</p>
      )}
    </div>
  );
};

export default Textarea;