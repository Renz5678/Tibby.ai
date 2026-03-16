import React from 'react';
import { useChat } from '../../context/ChatContext';
import styles from './QuickQuestions.module.css';

const quickQuestions = [
    {
        category: '📝 Enrollment',
        icon: '📝',
        questions: [
            'How to enroll?',
            'What are the requirements?',
            'Is there an entrance exam?',
            'Do you accept transferees?',
        ],
    },
    {
        category: '🏫 School Info',
        icon: '🏫',
        questions: [
            'Where is the school?',
            'What facilities are there?',
            'School hours?',
            'When does school year start?',
        ],
    },
    {
        category: '🎓 Programs',
        icon: '🎓',
        questions: [
            'What grade levels?',
            'What strands are offered?',
            'Is there a SPED program?',
            'Is there work immersion?',
        ],
    },
    {
        category: '📚 Student Life',
        icon: '📚',
        questions: [
            'What clubs are available?',
            'Uniform policy?',
            'Can I leave school early?',
            'What if I am absent?',
        ],
    },
    {
        category: '📞 Contact & Updates',
        icon: '📞',
        questions: [
            'How to contact the school?',
            'How can parents stay updated?',
            'Is there online learning?',
            'How to run for SSG?',
        ],
    },
];

export default function QuickQuestions({ onClose }) {
    const { sendMessage } = useChat();

    const handleQuestionClick = (question) => {
        sendMessage(question);
        // Close sidebar on mobile after selecting a question
        if (onClose) onClose();
    };

    return (
        <div className={styles.container}>
            <div className={styles.categories}>
                {quickQuestions.map((category, idx) => (
                    <div key={idx} className={styles.category}>
                        <h4 className={styles.categoryTitle}>
                            <span className={styles.icon}>{category.icon}</span>
                            {category.category}
                        </h4>
                        <div className={styles.questions}>
                            {category.questions.map((question, qIdx) => (
                                <button
                                    key={qIdx}
                                    className={styles.chip}
                                    onClick={() => handleQuestionClick(question)}
                                    data-icon={category.icon}
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
