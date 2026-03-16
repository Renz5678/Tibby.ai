import React, { useState } from 'react';
import { ChatProvider } from './context/ChatContext';
import Sidebar from './components/Sidebar/Sidebar';
import Header from './components/Header/Header';
import ChatBox from './components/ChatBox/ChatBox';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ChatProvider>
      <div className="app">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="main-content">
          <Header onMenuClick={toggleSidebar} />
          <ChatBox />
        </main>
      </div>
    </ChatProvider>
  );
}

export default App;
