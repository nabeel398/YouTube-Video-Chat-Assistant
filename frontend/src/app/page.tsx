'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';

const VideoChatApp = dynamic(() => import('@/components/VideoChatApp'), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-gray-600">Loading YouTube Chat Assistant...</p>
      </div>
    </div>
  ),
});

export default function Home() {
  return <VideoChatApp />;
}