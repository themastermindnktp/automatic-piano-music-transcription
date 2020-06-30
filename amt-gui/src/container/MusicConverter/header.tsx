import React from 'react';
import './header.scss';

const HeaderPage = ({children, buttonUpload}: any) => {
    return (
        <div>
            <div className="svg-container">
                <svg viewBox="0 0 800 400" className="svg">
                    <path id="curve" fill="#50c6d8" d="M 800 300 Q 400 350 0 300 L 0 0 L 800 0 L 800 300 Z">
                    </path>
                </svg>
            </div>

            <header>
                <h1> Automatic Music Transcription </h1>
                <h3> Please choose a music file </h3>
                {buttonUpload}
            </header>

            <main>
                {children}
            </main>

            <footer>
                <p> Powered by group </p>
                <small>🕷 Wish you luck, <a href="http://armantaherian.com">Arman</a>.</small>
            </footer>
            <div className={'backdrop'}/>
        </div>
    )
}

export default HeaderPage;