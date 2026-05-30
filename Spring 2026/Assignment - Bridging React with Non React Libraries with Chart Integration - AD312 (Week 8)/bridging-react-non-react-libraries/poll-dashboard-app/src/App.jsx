import { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function App() {
  const [votes, setVotes] = useState({
    React: 0,
    Vue: 0,
    Angular: 0
  });

  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current) {
      chartRef.current = new Chart(canvasRef.current, {
        type: 'bar',
        data: {
          labels: ['React', 'Vue', 'Angular'],
          datasets: [{
            label: 'Votes',
            data: [votes.React, votes.Vue, votes.Angular]
          }]
        }
      });
    } else {
      chartRef.current.data.datasets[0].data = [
        votes.React,
        votes.Vue,
        votes.Angular
      ];
      chartRef.current.update();
    }

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null;
      }
    };
  }, [votes]);
  
  return (
    <div>
      <h1>Poll Dashboard</h1>
      <button onClick={() => setVotes({...votes, React: votes.React + 1})}>React</button>
      <button onClick={() => setVotes({...votes, Vue: votes.Vue + 1})}>Vue</button>
      <button onClick={() => setVotes({...votes, Angular: votes.Angular + 1})}>Angular</button>
      <canvas ref={canvasRef}></canvas>
    </div>
  );
}

// TEST CASES

// Normal Cases
// Case 1: Click 'React' once ==> React gets 1 vote
// Case 2: Click 'Vue' twice ==> Vue gets 2 votes
// Case 3: Click 'Angular' three times ==> Angular gets 3 votes

// Edge Cases
// Case 1: Refresh the page ==> The status will return to the original 0 values
// Case 2: Click 'Angular' quickly for 10 times ==> Angular updates votes to 10 without crashing
// Case 3: Click 'Votes' icon ==> The votes disappear from the bar chart