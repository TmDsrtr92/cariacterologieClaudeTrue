import React from 'react';
import { ChatContainer } from '../components/chat';

const Home: React.FC = () => {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex-shrink-0 mb-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-light text-dark-50 mb-2">
            Q&A Assistant
          </h1>
          <p className="text-dark-300 font-light">
            Ask any question and get intelligent responses with full transparency into the processing steps.
          </p>
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 min-h-0">
        <ChatContainer />
      </div>
    </div>
  );
};

export default Home;