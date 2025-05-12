import React from "react";
import { useBraFitting } from "./hooks/useBraFitting";
import { useScrollToBottom } from "./hooks/useScrollToBottom";
import { ChatInput } from "./components/ChatInput";
import { ChatMessage } from "./components/ChatMessage";
import { LoadingIndicator } from "../../common/components/LoadingIndicator";
import { ErrorMessage } from "../../common/components/ErrorMessage";
import './styles/index.css'

const ChatInterface = () => {
  const { 
    messages, 
    isLoading, 
    error, 
    handleSubmit, 
  } = useBraFitting();
  
  const bottomRef = useScrollToBottom(messages);

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            isUser={msg.isUser}
            text={msg.text}
            recommendation={msg.recommendation}
          />
        ))}
        
        {isLoading && <LoadingIndicator />}
        
        {error && ( <ErrorMessage error={error} /> )}
        
        <div ref={bottomRef} />
      </div>

      <ChatInput 
        onSubmit={handleSubmit}
        isLoading={isLoading}
        placeholder="Enter your measurements and fit issues..."
      />
    </div>
  );
};

export default ChatInterface;
