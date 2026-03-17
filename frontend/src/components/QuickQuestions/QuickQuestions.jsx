import React from 'react';
import { useChat } from '../../context/ChatContext';
import styles from './QuickQuestions.module.css';

const quickQuestions = [
    { label: '📝 How to enroll?', message: 'How do I enroll?' },
    { label: '📍 Where is the school?', message: 'Where is the school located?' },
    { label: '🎓 What strands are offered?', message: 'What strands are offered in Senior High School?' },
    { label: '🎯 What clubs are available?', message: 'What clubs and organizations are available?' },
    { label: '📞 Contact information', message: 'Contact information?' },
];

export default function QuickQuestions({ onClose }) {
    const { sendMessage } = useChat();

    const handleQuestionClick = (msg) => {
        sendMessage(msg);
        if (onClose) onClose();
    };

    return (
        <div className={styles.container}>
            <div className={styles.chips}>
                {quickQuestions.map((q, idx) => (
                    <button
                        key={idx}
                        className={styles.chip}
                        onClick={() => handleQuestionClick(q.message)}
                    >
                        {q.label}
                    </button>
                ))}
            </div>
        </div>
    );
}
