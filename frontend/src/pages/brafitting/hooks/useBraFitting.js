import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { braFittingService } from '../services';

export const useBraFitting = () => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  
  const mutation = useMutation({
    mutationFn: braFittingService.getRecommendation,
    onMutate: (text) => {
      setError(null); 
      setMessages(prev => [...prev, { text, isUser: true }]);
    },
    onSuccess: (response) => {
      if (!response.recommendation) {
        throw new Error('Invalid response from server');
      }
      
      setMessages(prev => [...prev, {
        text: `Recommended Size: ${response.recommendation}`,
        isUser: false,
        recommendation: response
      }]);
    },
    onError: (error) => {
      console.log({error})
      const errorMessage = error.response?.data?.message 
        || error.message 
        || 'Sorry, there was an error getting your recommendation. Please try again.';
      
      setError(errorMessage);
      setMessages(prev => [...prev, {
        text: errorMessage,
        isUser: false,
        isError: true
      }]);
    }
  });

  const clearError = () => {
    setError(null);
  };

  const handleSubmit = async (text) => {
    if (!text?.trim()) {
      setError('Please enter your measurements and fit issues');
      return;
    }
    
    try {
      await mutation.mutate(text);
    } catch (err) {
      setError(err.message);
    }
  };

  return {
    messages,
    isLoading: mutation.isPending,
    error,
    clearError,
    handleSubmit
  };
};