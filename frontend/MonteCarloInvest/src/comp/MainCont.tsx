
import InputBar from './InpurBar'
import GraphContainer from "./GraphContainer"
import StatBox from './statBox'
import {useState} from 'react';
import "./MainCont.scss"

interface Stats {

        Average_Final?: number | null,
        Max_Final?: number | null,
        Median_Final?: number| null,
        Median_Gain?: number| null,
        Min_Final?: number| null,
        STD_Final?: number| null
}

interface DataPoints{

        Final_Bals?: number[] | null,
        Real_Final_Bals?: number[] | null,
        Bals?: number[][] | null,
        Real_Bals?: number[][] | null

}

function MainCont(){

    const [loading, setLoading] =  useState<boolean>(false);
    const [stats, setStats] = useState<Stats | null>(null);
    const [dataPoints, setData]  = useState<DataPoints | null>(null);
    const [isError, setError] = useState <boolean>(false);

    const sendData = async (principle: number, monthly:number, duration:number, simCount:number) => {

        //Start loading
        setLoading(true)
        setData(null)

        duration = Math.floor(duration)
        simCount = Math.floor(simCount)


        const response = await fetch("https://tylerkelly1.pythonanywhere.com/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ principle, monthly, duration, simCount})
            });

            const data = await response.json();

            if(data.Error == true){
                setError(true)
            }
            else{
                setError(false)
            }

            setData(data.DataPoints)
            setStats(data.Stats)
            setLoading(false)


    };

    const handleSubmit = (principle: number, monhtly: number, duration:number, simCount:number) => {
        sendData(principle, monhtly, duration, simCount)
    }

    function displayError(error:boolean){
        if(error){
            return <>
            An input atleast 1 sim size and 1 duration
            </>
        }
    }

    function loadingScreen(loading:boolean) {

        if (loading){
 
        return (
            <div style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.7)", // dark overlay
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "white",
            fontSize: "2rem",
            fontWeight: "bold",
            zIndex: 9999 // makes sure it’s on top
            }}>
            Loading...
            </div>
        );

        }
    }


    return (<>

    <div className='main-container'>

    <div className='input-bar'>
        <InputBar sendToAPI={handleSubmit}/>
    </div>

    <div className='graph-container'>
        <GraphContainer Bals={dataPoints?.Bals}/>
    </div>

    <div className='stat-box'>
        <StatBox stats={stats}/>
    </div>

    {displayError(isError)}
    {loadingScreen(loading)}
    

    </div>

    </>)

}

export default MainCont