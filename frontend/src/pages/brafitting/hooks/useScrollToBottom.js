import { useEffect, useRef } from 'react';

export const useScrollToBottom = (dependency) => {
  const bottomRef = useRef(null);
  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [dependency]);
  
  return bottomRef;
}; 