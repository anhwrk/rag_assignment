import React from 'react';
import '../styles/index.css';

export const ChatMessage = ({ text, isUser, recommendation }) => {
  if (isUser) {
    return <div className="message user">{text}</div>;
  }

  if (!recommendation) {
    return;
  }

  return (
    <div className="message bot">
      <div className="recommendation">
        <h4>Recommended Size: {recommendation.recommendation}</h4>
        
        {recommendation.reasoning && (
          <p className="reasoning">{recommendation.reasoning}</p>
        )}
        
        {recommendation.fit_tips && (
          <p className="fit-tips">
            <strong>Fit Tips:</strong> {recommendation.fit_tips}
          </p>
        )}
        
        {recommendation.identified_issues?.length > 0 && (
          <div className="issues">
            <h5>Identified Issues:</h5>
            <ul>
              {recommendation.identified_issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}
        
        {recommendation.confidence && (
          <div className="confidence">
            Confidence: {(recommendation.confidence * 100).toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  );
};