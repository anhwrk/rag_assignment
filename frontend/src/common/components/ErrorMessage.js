import React from 'react';
import '../styles/index.css';

export const ErrorMessage = ({ error }) => {
  const getErrorMessage = () => {
    if (!error) return 'An unexpected error occurred';
    
    if (typeof error === 'string') return error;
    
    if (error.message) return error.message;
    
    return 'Unable to get recommendation. Please try again.';
  };

  return (
    <div className="error-message">
      <div className="error-content">
        <div className="error-icon">⚠️</div>
        <div className="error-text">{getErrorMessage()}</div>
      </div>
    </div>
  );
};
