import React, { useRef, useEffect } from 'react';
import { useChat } from '../../context/ChatContext';
import Message from '../Message/Message';
import TypingIndicator from '../TypingIndicator/TypingIndicator';
import styles from './ChatBox.module.css';

export default function ChatBox() {
    const { messages, isLoading, inputValue, setInputValue, sendMessage } = useChat();
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    // Auto-focus input on mount
    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim() && !isLoading) {
            sendMessage(inputValue);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className={styles.container}>
            {/* Messages Area */}
            <div className={styles.messagesWrapper}>
                {messages.length === 0 ? (
                    <div className={styles.welcome}>
                        <div className={styles.welcomeContent}>
                            <h1 className={styles.welcomeTitle}>
                                👋 Hello, Gentinian!
                            </h1>
                            <p className={styles.welcomeText}>
                                I'm Tibby, your friendly GTDLNHS chatbot. How can I help you today?
                            </p>
                            <p className={styles.welcomeHint}>
                                💡 Check the sidebar for quick questions!
                            </p>
                        </div>
                    </div>
                ) : (
                    <div className={styles.messages}>
                        {messages.map((message) => (
                            <Message key={message.id} message={message} />
                        ))}
                        {isLoading && <TypingIndicator />}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* Input Form */}
            <form className={styles.inputForm} onSubmit={handleSubmit}>
                <input
                    ref={inputRef}
                    type="text"
                    className={styles.input}
                    placeholder="Type your message..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isLoading}
                    maxLength={500}
                />
                <button
                    type="submit"
                    className={styles.sendButton}
                    disabled={!inputValue.trim() || isLoading}
                    aria-label="Send message"
                >
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </form>
        </div>
    );
}
