
import './InputBar.scss'
import {useState} from 'react';

interface Props {
    sendToAPI: (principle:number, monhtly:number, duration:number, simCount: number) => any;
}

function InputBar({ sendToAPI } : Props) {

    const [principle, setPrinciple] = useState<number>(50);
    const [monthly, setMonthly] = useState<number>(10);
    const [duration, setDuration] = useState<number>(5);
    const [simCount, setCount] = useState<number>(3);

    const handleSubmit = () => {
        sendToAPI(principle, monthly, duration, simCount)
    };


  return (
    <>

    <div className='frame'>

        <label>
            Starting Balance ($): 
            <input
            type="number"
            value={principle}
            onChange={(e) => setPrinciple(Number(e.target.value) <= 0 ? 1 : Number(e.target.value))}
            onFocus={(e) => e.target.value = ""} // clears box on click
            onBlur={(e) => {
                if (!e.target.value || Number(e.target.value) <= 0) {
                setPrinciple(1); // reset to 1 if empty or invalid
                e.target.value = "1"; // update input box display
                }
            }}
            min={1} // prevents negative numbers with arrows
            />
        </label>

        <label>
            Monthly Investment ($): 
            <input
            type="number"
            value={monthly}
            onChange={(e) => setMonthly(Number(e.target.value) < 0 ? 0 : Number(e.target.value))}
            onFocus={(e) => e.target.value = ""} // clears box on click
            onBlur={(e) => {
                if (!e.target.value || Number(e.target.value) <= 0) {
                setMonthly(0); // reset to 1 if empty or invalid
                e.target.value = "0"; // update input box display
                }
            }}
            min={0} // prevents negative numbers with arrows
            />
        </label>

         <label>
            Duration (Years): 
            <input
            type="number"
            step="1"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value) <= 0 ? 1 : Number(e.target.value))}
            onFocus={(e) => e.target.value = ""} // clears box on click
            onBlur={(e) => {
                if (!e.target.value || Number(e.target.value) <= 0) {
                setDuration(1); // reset to 1 if empty or invalid
                e.target.value = "1"; // update input box display
                }
            }}
            min={1} // prevents negative numbers with arrows
            />
        </label>

            <label>
                Simulation Count: 
                <input
                type="number"
                step="1"
                value={simCount}
                onChange={(e) => setCount((Number(e.target.value)) <= 0 ? 1 : Number(e.target.value))}
                onFocus={(e) => e.target.value = ""} // clears box on click
                onBlur={(e) => {
                    if (!e.target.value || Number(e.target.value) <= 0) {
                    setCount(1); // reset to 1 if empty or invalid
                    e.target.value = "1"; // update input box display
                    }
                }}
                min={1} // prevents negative numbers with arrows
                />
            </label>

        <button onClick={() => handleSubmit()}>Submit</button>

    </div>
    </>
  )
}

export default InputBar