import React from 'react';
import { useTypingEffect } from '../../hooks/useTypingEffect';
import styles from './Message.module.css';

export default function Message({ message }) {
    const { text, sender, timestamp, cached, isError } = message;

    // Always call hook unconditionally (Rules of Hooks)
    const typedText = useTypingEffect(text, 18);

    // Only use the typing effect output for bot messages
    const displayText = (sender === 'bot' && !isError) ? typedText : text;

    const formatTime = (date) => {
        return new Date(date).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className={`${styles.message} ${styles[sender]}`}>
            <div className={styles.bubble}>
                <p className={styles.text}>{displayText}</p>
                <div className={styles.meta}>
                    <span className={styles.time}>{formatTime(timestamp)}</span>
                    {cached && <span className={styles.cachedBadge}>💾 cached</span>}
                </div>
            </div>
        </div>
    );
}
