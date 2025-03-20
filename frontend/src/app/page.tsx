/**
 * src/app/page.tsx
 * Main page component for the Claude chat application
 * Includes context providers and the AppLayout component
 */

import { ChatProvider } from '../context/ChatContext';
import { FileProvider } from '../context/FileContext';
import AppLayout from '../components/AppLayout';

export default function Home() {
  return (
    <ChatProvider>
      <FileProvider>
        <div className="min-h-screen max-h-screen overflow-hidden">
          <AppLayout />
        </div>
      </FileProvider>
    </ChatProvider>
  );
}
