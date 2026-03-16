import React from 'react';
import QuickQuestions from '../QuickQuestions/QuickQuestions';
import styles from './Sidebar.module.css';

export default function Sidebar({ isOpen, onClose }) {
    return (
        <>
            {isOpen && <div className={styles.overlay} onClick={onClose} />}
            <aside className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
                <div className={styles.header}>
                    <div className={styles.logo}>
                        <span className={styles.logoIcon}>🏫</span>
                        <h2>GTDLNHS</h2>
                    </div>
                </div>

                <div className={styles.content}>
                    <section className={styles.section}>
                        <h3>About</h3>
                        <p>
                            General Tiburcio de Leon National High School - Your partner in quality education.
                        </p>
                    </section>

                    <section className={styles.section}>
                        <h3>Contact</h3>
                        <div className={styles.contactItem}>
                            <span>📞</span>
                            <a href="tel:0967-023-7047">0967-023-7047</a>
                        </div>
                        <div className={styles.contactItem}>
                            <span>📧</span>
                            <a href="mailto:gtdlnhs2007@gmail.com">gtdlnhs2007@gmail.com</a>
                        </div>
                    </section>

                    <section className={styles.section}>
                        <h3>Location</h3>
                        <p className={styles.address}>
                            Corner Mercado St., General T. de Leon, Valenzuela City, Metro Manila
                        </p>
                    </section>

                    <section className={styles.section}>
                        <h3>Social Media</h3>
                        <div className={styles.social}>
                            <a
                                href="https://www.facebook.com/share/1BMPoam8K2/?mibextid=wwXIfr"
                                target="_blank"
                                rel="noopener noreferrer"
                                className={styles.socialLink}
                            >
                                <span>📱</span> Facebook
                            </a>
                        </div>
                    </section>

                    {/* Quick Questions in Sidebar */}
                    <section className={styles.section}>
                        <h3>Quick Questions</h3>
                        <QuickQuestions onClose={onClose} />
                    </section>
                </div>

                <div className={styles.footer}>
                    <p>Made with 💙 for Gentinians</p>
                </div>
            </aside>
        </>
    );
}
