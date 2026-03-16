import React from 'react';
import { useChat } from '../../context/ChatContext';
import styles from './Header.module.css';

export default function Header({ onMenuClick }) {
    const { clearChat, messages } = useChat();

    const handleClearChat = () => {
        if (messages.length > 0 && window.confirm('Clear all messages?')) {
            clearChat();
        }
    };

    return (
        <header className={styles.header}>
            <button className={styles.menuButton} onClick={onMenuClick} aria-label="Toggle sidebar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>

            <div className={styles.branding}>
                <div className={styles.logo}>
                    <img src="/tibby-icon.png" alt="Tibby" className={styles.logoImg} />
                </div>
                <div className={styles.info}>
                    <h1 className={styles.title}>Tibby</h1>
                    <p className={styles.subtitle}>GTDLNHS Chatbot Assistant</p>
                </div>
            </div>

            {messages.length > 0 && (
                <button className={styles.clearButton} onClick={handleClearChat} aria-label="Clear chat">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            )}
        </header>
    );
}
