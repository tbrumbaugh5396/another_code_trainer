import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CLUE_LIST = ["Two Pointers", "Monotonic Stack", "Sliding Window", "Binary Search", "DFS", "BFS"];

function App() {
    const [problems, setProblems] = useState([]);
    const [currentIdx, setCurrentIdx] = useState(0);
    const [selectedClues, setSelectedClues] = useState([]);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);

    // Fetch the 61 problems from our FastAPI backend
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/problems')
            .then(res => {
                setProblems(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Connection Error:", err);
                setLoading(false);
            });
    }, []);

    const currentProblem = problems[currentIdx];

    const toggleClue = (clue) => {
        setSelectedClues(prev =>
            prev.includes(clue) ? prev.filter(c => c !== clue) : [...prev, clue]
        );
    };

    const handleVerify = async () => {
        // Here we send our reasoning to the backend logic
        try {
            const res = await axios.post('http://127.0.0.1:8000/validate', {
                problem_id: currentProblem.id,
                user_clues: selectedClues
            });
            setResult(res.data);
        } catch (e) {
            setResult({ success: false, feedback: "Validation server unreachable." });
        }
    };

    if (loading) return <div style={styles.loader}>INITIALIZING_SYSTEM_TRAINER...</div>;
    if (!problems.length) return <div style={styles.loader}>DATABASE_EMPTY: Run scraper.py</div>;

    return (
        <div style={styles.container}>
            {/* Sidebar Navigation */}
            <div style={styles.sidebar}>
                <h3 style={{ color: '#888' }}>PROB_MANIFEST</h3>
                {problems.map((p, idx) => (
                    <div
                        key={p.id}
                        onClick={() => { setCurrentIdx(idx); setResult(null); setSelectedClues([]); }}
                        style={{
                            ...styles.sideItem,
                            background: currentIdx === idx ? '#333' : 'transparent',
                            color: currentIdx === idx ? '#00ff00' : '#ccc'
                        }}
                    >
                        {idx + 1}. {p.title.substring(0, 20)}...
                    </div>
                ))}
            </div>

            {/* Main Trainer Area */}
            <div style={styles.main}>
                <div style={styles.header}>
                    <h1>{currentProblem.title}</h1>
                    <div style={styles.badgeRow}>
                        <span style={styles.badge}>TIME: {currentProblem.complexity_time || 'O(N)'}</span>
                        <span style={styles.badge}>SPACE: {currentProblem.complexity_space || 'O(1)'}</span>
                    </div>
                </div>

                <div style={styles.card}>
                    <h3>PROBLEM_DESCRIPTION</h3>
                    <div style={styles.description}>
                        {currentProblem.description}
                    </div>
                </div>

                <div style={styles.logicSection}>
                    <h3>IDENTIFY_MECHANICS</h3>
                    <p style={{ color: '#666' }}>Select the invariants required to solve this optimally:</p>
                    <div style={styles.clueGrid}>
                        {CLUE_LIST.map(clue => (
                            <button
                                key={clue}
                                onClick={() => toggleClue(clue)}
                                style={{
                                    ...styles.clueBtn,
                                    backgroundColor: selectedClues.includes(clue) ? '#00ff00' : '#1a1a1a',
                                    color: selectedClues.includes(clue) ? '#000' : '#fff'
                                }}
                            >
                                {clue}
                            </button>
                        ))}
                    </div>

                    <button onClick={handleVerify} style={styles.verifyBtn}>
                        VALIDATE_REASONING
                    </button>
                </div>

                {result && (
                    <div style={{
                        ...styles.resultCard,
                        borderColor: result.success ? '#00ff00' : '#ff4444'
                    }}>
                        <h4>{result.success ? ">>> VALIDATION_PASSED" : ">>> LOGIC_INCOMPLETE"}</h4>
                        <p>{result.feedback}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

const styles = {
    container: { display: 'flex', height: '100vh', backgroundColor: '#0a0a0a', color: '#fff', fontFamily: 'monospace' },
    sidebar: { width: '250px', borderRight: '1px solid #333', padding: '1rem', overflowY: 'auto' },
    sideItem: { padding: '8px', cursor: 'pointer', fontSize: '0.8rem', borderBottom: '1px solid #222' },
    main: { flex: 1, padding: '2rem', overflowY: 'auto' },
    header: { borderBottom: '2px solid #00ff00', paddingBottom: '1rem', marginBottom: '2rem' },
    badgeRow: { display: 'flex', gap: '10px', marginTop: '10px' },
    badge: { background: '#222', padding: '4px 10px', borderRadius: '4px', fontSize: '0.7rem', border: '1px solid #444' },
    card: { background: '#111', padding: '1.5rem', border: '1px solid #333', borderRadius: '8px' },
    description: { lineHeight: '1.6', fontSize: '0.95rem', whiteSpace: 'pre-wrap', color: '#ccc' },
    logicSection: { marginTop: '2rem' },
    clueGrid: { display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '1.5rem' },
    clueBtn: { padding: '10px 15px', border: '1px solid #444', cursor: 'pointer', borderRadius: '4px', transition: '0.2s' },
    verifyBtn: { width: '100%', padding: '15px', background: '#00ff00', color: '#000', border: 'none', fontWeight: 'bold', cursor: 'pointer' },
    resultCard: { marginTop: '1.5rem', padding: '1rem', borderLeft: '4px solid', background: '#1a1a1a' },
    loader: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: '#00ff00', background: '#000' }
};

export default App;