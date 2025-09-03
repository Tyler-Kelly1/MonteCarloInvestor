
import "./statBox.scss"
import {useState} from 'react';

interface Stats {

        Average_Final?: number | null,
        Max_Final?: number | null,
        Median_Final?: number| null,
        Median_Gain?: number| null,
        Min_Final?: number| null,
        STD_Final?: number| null
}

interface Props{
    stats?: Stats | null
} 

function StatBox( {stats} : Props) {

    const [result, setResult] = useState<any>(null); 
    const [loading, setLoading] =  useState<boolean>(false);

    // Helper function that checks for null value
    // If it is null display 'N/A'
    const displayValue = (val: any) => val ?? "N/A";



    return(


        <>
        <div className="statBox">
        <p>Average Final Balance: ${displayValue(stats?.Average_Final)}</p>
        <p>Median Final Balance: ${displayValue(stats?.Median_Final)}</p>
        <p>Max Final Balance: ${displayValue(stats?.Max_Final)}</p>
        <p>Min Final Balance: ${displayValue(stats?.Min_Final)}</p>
        <p>STD Final Balance: ${displayValue(stats?.STD_Final)}</p>




        </div>
        
        </>
    )

}


export default StatBox