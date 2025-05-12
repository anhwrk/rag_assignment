import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { measurementSchema } from '../validations/schemas';

export const ChatInput = ({ onSubmit, isLoading, isError }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(measurementSchema),
    defaultValues: {
      message: ''
    }
  });

  const onSubmitValid = (data) => {
    onSubmit(data.message);
    reset();
  };

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit(onSubmitValid)} className="input-form">
        <div className="input-wrapper">
          <input
            {...register('message')}
            type="text"
            placeholder="Enter your measurements and fit issues..."
            disabled={isLoading || isError}
            className={errors.message ? 'error' : ''}
          />
        </div>
        <button 
          type="submit" 
          disabled={isLoading || isError}
          className={isLoading ? 'loading' : ''}
        >
          {isLoading ? 'Getting Recommendation...' : 'Get Recommendation'}
        </button>
      </form>
      
      {errors.message && (
        <span className="error-message">
          {errors.message.message}
        </span>
      )}
    </div>
  );
};