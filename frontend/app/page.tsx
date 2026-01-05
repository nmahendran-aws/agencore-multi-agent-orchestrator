'use client';

import { useEffect, useState, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const socketRef = useRef<Socket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messageIdCounter = useRef(0);

  // Generate unique message ID
  const generateMessageId = () => {
    messageIdCounter.current += 1;
    return `${Date.now()}-${messageIdCounter.current}`;
  };

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentResponse]);

  useEffect(() => {
    // Connect to WebSocket
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3001';
    const socket = io(backendUrl, {
      // Prevent automatic reconnection attempts that could cause duplicates
      reconnection: true,
      reconnectionAttempts: 3,
      reconnectionDelay: 1000,
    });

    // Connection handlers
    const handleConnect = () => {
      console.log('Connected to backend');
      setIsConnected(true);
    };

    const handleDisconnect = () => {
      console.log('Disconnected from backend');
      setIsConnected(false);
    };

    // Response handler
    const handleResponse = (chunk: string) => {
      setCurrentResponse((prev) => prev + chunk);
    };

    // Response complete handler
    const handleResponseComplete = () => {
      setCurrentResponse((prev) => {
        if (prev) {
          setMessages((msgs) => [
            ...msgs,
            {
              id: generateMessageId(),
              role: 'assistant',
              content: prev,
            },
          ]);
        }
        return '';
      });
      setIsLoading(false);
    };

    // Error handler
    const handleError = (error: { message: string }) => {
      console.error('Socket error:', error);
      setMessages((msgs) => [
        ...msgs,
        {
          id: generateMessageId(),
          role: 'assistant',
          content: `Error: ${error.message}`,
        },
      ]);
      setIsLoading(false);
      setCurrentResponse('');
    };

    // Register event listeners
    socket.on('connect', handleConnect);
    socket.on('disconnect', handleDisconnect);
    socket.on('response', handleResponse);
    socket.on('response-complete', handleResponseComplete);
    socket.on('error', handleError);

    socketRef.current = socket;

    // Cleanup function - properly remove all listeners
    return () => {
      socket.off('connect', handleConnect);
      socket.off('disconnect', handleDisconnect);
      socket.off('response', handleResponse);
      socket.off('response-complete', handleResponseComplete);
      socket.off('error', handleError);
      socket.disconnect();
    };
  }, []);

  const handleSend = () => {
    if (!inputValue.trim() || !socketRef.current || !isConnected || isLoading) {
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: generateMessageId(),
      role: 'user',
      content: inputValue,
    };
    setMessages((msgs) => [...msgs, userMessage]);

    // Send to backend
    socketRef.current.emit('message', { message: inputValue });

    // Clear input and set loading
    setInputValue('');
    setIsLoading(true);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl h-[90vh] flex flex-col">
        {/* Header */}
        <div className="glass-card p-6 mb-4">
          <h1 className="text-3xl font-bold gradient-text mb-2">
            Orchestrator Agent Chat
          </h1>
          <p className="text-gray-400 text-sm">
            Connected: {isConnected ? (
              <span className="text-green-400">●</span>
            ) : (
              <span className="text-red-400">●</span>
            )}
          </p>
        </div>

        {/* Chat Container */}
        <div className="glass-card flex-1 flex flex-col overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && !currentResponse && (
              <div className="text-center text-gray-400 mt-20">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-xl mb-2">Start a conversation</p>
                <p className="text-sm">
                  Ask me anything! I can help with technical and HR questions.
                </p>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`message-bubble ${message.role === 'user' ? 'message-user' : 'message-assistant'}`}
                >
                  {message.content}
                </div>
              </div>
            ))}

            {/* Current streaming response */}
            {currentResponse && (
              <div className="flex justify-start">
                <div className="message-bubble message-assistant">
                  {currentResponse}
                  <span className="inline-block w-2 h-4 ml-1 bg-white pulse-animation" />
                </div>
              </div>
            )}

            {/* Loading indicator */}
            {isLoading && !currentResponse && (
              <div className="flex justify-start">
                <div className="message-bubble message-assistant">
                  <div className="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-6 border-t border-gray-800">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                disabled={!isConnected || isLoading}
                className="input-primary flex-1"
              />
              <button
                onClick={handleSend}
                disabled={!isConnected || isLoading || !inputValue.trim()}
                className="btn-primary"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
