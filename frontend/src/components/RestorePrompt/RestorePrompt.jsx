import React from 'react';
import { useChat } from '../../context/ChatContext';
import styles from './RestorePrompt.module.css';

export default function RestorePrompt() {
    const { showRestorePrompt, handleRestoreYes, handleRestoreNo } = useChat();

    if (!showRestorePrompt) return null;

    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <img
                    src="/tibby-icon.png"
                    alt="Tibby"
                    className={styles.avatar}
                />
                <h2 className={styles.title}>Previous Conversation Found</h2>
                <p className={styles.description}>
                    Would you like to continue where you left off?
                </p>
                <div className={styles.actions}>
                    <button className={styles.btnYes} onClick={handleRestoreYes}>
                        Yes, restore it
                    </button>
                    <button className={styles.btnNo} onClick={handleRestoreNo}>
                        No, start fresh
                    </button>
                </div>
            </div>
        </div>
    );
}
