import React, { useState, useRef, useEffect } from 'react';
import type { SelectProps } from '../../types';

const Select: React.FC<SelectProps> = ({
  label,
  placeholder = 'Select an option...',
  value,
  onChange,
  options,
  error,
  disabled = false,
  className = '',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const selectRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (isOpen) {
      setHighlightedIndex(-1);
    }
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (disabled) return;

    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen && highlightedIndex >= 0) {
          const selectedOption = options[highlightedIndex];
          if (!selectedOption.disabled) {
            onChange?.(selectedOption.value);
            setIsOpen(false);
          }
        } else {
          setIsOpen(!isOpen);
        }
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setHighlightedIndex(prev => 
            prev < options.length - 1 ? prev + 1 : 0
          );
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (isOpen) {
          setHighlightedIndex(prev => 
            prev > 0 ? prev - 1 : options.length - 1
          );
        }
        break;
      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  const selectedOption = options.find(option => option.value === value);

  const selectClasses = `
    relative w-full px-3 py-2 bg-dark-800 border rounded-lg text-dark-100 font-light
    cursor-pointer transition-colors duration-200 flex items-center justify-between
    focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent
    disabled:opacity-50 disabled:cursor-not-allowed
    ${error ? 'border-red-500 focus:ring-red-500' : 'border-dark-600 hover:border-dark-500'}
    ${className}
  `;

  return (
    <div className="w-full" ref={selectRef}>
      {label && (
        <label className="block text-sm font-light text-dark-200 mb-1">
          {label}
        </label>
      )}
      <div
        className={selectClasses}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        tabIndex={0}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span className={selectedOption ? 'text-dark-100' : 'text-dark-400'}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>

      {isOpen && (
        <div className="absolute z-50 w-full mt-1 bg-dark-800 border border-dark-600 rounded-lg shadow-lg max-h-60 overflow-auto custom-scrollbar">
          {options.map((option, index) => (
            <div
              key={option.value}
              className={`
                px-3 py-2 cursor-pointer transition-colors duration-150 font-light
                ${highlightedIndex === index ? 'bg-dark-700' : 'hover:bg-dark-700'}
                ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}
                ${option.value === value ? 'bg-primary-purple text-white' : 'text-dark-100'}
              `}
              onClick={() => {
                if (!option.disabled) {
                  onChange?.(option.value);
                  setIsOpen(false);
                }
              }}
              onMouseEnter={() => setHighlightedIndex(index)}
              role="option"
              aria-selected={option.value === value}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}

      {error && (
        <p className="mt-1 text-sm text-red-400 font-light">{error}</p>
      )}
    </div>
  );
};

export default Select;