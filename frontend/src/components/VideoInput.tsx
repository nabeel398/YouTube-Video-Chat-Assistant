'use client';

import { useState } from 'react';
import { Loader } from 'lucide-react';

interface VideoInputProps {
  onSubmit: (url: string) => Promise<void>;
  isProcessing: boolean;
  isVideoProcessed: boolean;
}

export default function VideoInput({ onSubmit, isProcessing, isVideoProcessed }: VideoInputProps) {
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');

  const extractVideoId = (url: string) => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\/\?\#]+)/,
      /youtube\.com\/v\/([^&\/\?\#]+)/
    ];
    
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  };

  const isValidYouTubeUrl = (url: string) => {
    return extractVideoId(url) !== null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!videoUrl.trim()) {
      setError('Please enter a YouTube URL');
      return;
    }

    if (!isValidYouTubeUrl(videoUrl)) {
      setError('Please enter a valid YouTube URL');
      return;
    }

    try {
      await onSubmit(videoUrl.trim());
    } catch (err: any) {
      setError(err.detail || 'Failed to process video. Please try again.');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Process YouTube Video</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="videoUrl" className="block text-sm font-medium text-gray-700 mb-2">
            YouTube Video URL
          </label>
          <input
            type="url"
            id="videoUrl"
            value={videoUrl}
            onChange={(e) => {
              setVideoUrl(e.target.value);
              setError('');
            }}
            placeholder="https://www.youtube.com/watch?v=..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            disabled={isProcessing || isVideoProcessed}
          />
        </div>

        {error && (
          <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg border border-red-200">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!videoUrl.trim() || !isValidYouTubeUrl(videoUrl) || isProcessing || isVideoProcessed}
          className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
        >
          {isProcessing ? (
            <>
              <Loader className="w-4 h-4 animate-spin" />
              <span>Processing Video...</span>
            </>
          ) : isVideoProcessed ? (
            <>
              <span>✓ Video Processed</span>
            </>
          ) : (
            <span>Process Video</span>
          )}
        </button>
      </form>

      <div className="mt-6 text-sm text-gray-600">
        <h3 className="font-medium mb-2">Supported URL formats:</h3>
        <ul className="list-disc list-inside space-y-1">
          <li>youtube.com/watch?v=VIDEO_ID</li>
          <li>youtu.be/VIDEO_ID</li>
          <li>youtube.com/embed/VIDEO_ID</li>
        </ul>
      </div>
    </div>
  );
}