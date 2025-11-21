'use client';

import { useState } from 'react';
import VideoInput from './VideoInput';
import ChatBox from './ChatBox';
import { api } from '@/lib/api';

export default function VideoChatApp() {
  const [sessionId, setSessionId] = useState<string>('');
  const [isVideoProcessed, setIsVideoProcessed] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleVideoSubmit = async (url: string) => {
    setIsProcessing(true);
    try {
      const newSessionId = `session_${Date.now()}`;
      await api.processVideo(url, newSessionId);
      
      setSessionId(newSessionId);
      setIsVideoProcessed(true);
    } catch (error) {
      console.error('Error processing video:', error);
      throw error;
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            YouTube Video Chat Assistant
          </h1>
          <p className="text-gray-600">
            Process any YouTube video and chat with its content using AI
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Video Input Sidebar */}
          <div className="lg:col-span-1">
            <VideoInput 
              onSubmit={handleVideoSubmit}
              isProcessing={isProcessing}
              isVideoProcessed={isVideoProcessed}
            />
            
            {isVideoProcessed && (
              <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-700 font-medium">✓ Video Processed Successfully</p>
                <p className="text-green-600 text-sm mt-1">Session: {sessionId}</p>
                <p className="text-green-600 text-sm">You can now chat with the video content!</p>
              </div>
            )}
          </div>

          {/* Chat Area */}
          <div className="lg:col-span-2">
            <div className="h-[600px]">
              {isVideoProcessed ? (
                <ChatBox sessionId={sessionId} />
              ) : (
                <div className="bg-white rounded-lg shadow-lg h-full flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <p className="text-lg mb-2">Process a YouTube video to start chatting</p>
                    <p className="text-sm">Enter a YouTube URL in the left panel to begin</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}