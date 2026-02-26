import React, { useState } from 'react';

const Trainer = ({ problem }) => {
    const [identifiedClues, setIdentifiedClues] = useState([]);
    const [complexityGuess, setComplexityGuess] = useState("");

    const checkAnalysis = () => {
        // Logic to compare identifiedClues against the hidden 'correct_clues' in DB
        if (identifiedClues.includes("unweighted") && identifiedClues.includes("shortest_path")) {
            alert("Correct Analysis! This points to BFS.");
        }
    };

    return (
        <div className="trainer-box">
            <div className="description-scroll">{problem.description}</div>

            <div className="mechanics-grid">
                <h4>Identify Structural Invariants:</h4>
                <label><input type="checkbox" onChange={() => setIdentifiedClues([...identifiedClues, "unweighted"])} /> Unweighted Graph</label>
                <label><input type="checkbox" onChange={() => setIdentifiedClues([...identifiedClues, "overlapping"])} /> Overlapping Subproblems</label>
            </div>

            <div className="complexity-selector">
                <h4>Predicted Time Complexity:</h4>
                <select value={complexityGuess} onChange={(e) => setComplexityGuess(e.target.value)}>
                    <option value="O(1)">O(1)</option>
                    <option value="O(log n)">O(log n)</option>
                    <option value="O(n)">O(n)</option>
                    <option value="O(n log n)">O(n log n)</option>
                </select>
            </div>

            <button onClick={checkAnalysis}>Validate Mechanics</button>
        </div>
    );
};