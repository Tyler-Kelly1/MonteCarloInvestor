
import "./GraphContainer.scss"
import { ResponsiveLine } from '@nivo/line';


interface DataPoints{

        Final_Bals?: number[] | null,
        Real_Final_Bals?: number[] | null,
        Bals?: number[][] | null,
        Real_Bals?: number[][] | null

}

function GraphContainer({Bals} : DataPoints){

    const data = Bals?.map((line, lineIndex) => ({
        id: `Simulation ${lineIndex + 1}`,
        data: line.map((y, x) => ({ x, y }))
        }));

    console.log(data)




    function graphRender(data : any | null){

        if(data == null){
            return (<>Nothing to see here folks</>)
        }

        return (
            <>
            
            <ResponsiveLine
    data={data}
    margin={{ top: 50, right: 120, bottom: 60, left: 80 }}
    xScale={{ type: 'linear', min: 'auto', max: 'auto' }} // dynamic scaling
    yScale={{
        type: 'linear',
        min: 'auto',
        max: 'auto',
        stacked: false
    }}
    curve="monotoneX"
    axisTop={null}
    axisRight={null}
    axisBottom={{
        tickSize: 5,
        tickPadding: 10,
        tickRotation: 0,
        legend: 'Year',
        legendOffset: 40,
        legendPosition: 'middle'
    }}
    axisLeft={{
        tickSize: 5,
        tickPadding: 10,
        tickRotation: 0,
        legend: 'Balance ($)',
        legendOffset: -60,
        legendPosition: 'middle',
        format: (value) => `$${value.toLocaleString()}`
    }}
    colors={{ scheme: 'set1' }}
    pointSize={6}
    pointColor={{ theme: 'background' }}
    pointBorderWidth={2}
    pointBorderColor={{ from: 'serieColor' }}
    pointLabelYOffset={-12}
    legends={[
        {
            anchor: 'bottom-right',
            direction: 'column',
            translateX: 100,
            itemWidth: 80,
            itemHeight: 20,
            symbolSize: 12,
            symbolShape: 'circle',
            itemOpacity: 0.75,
            effects: [
                {
                    on: 'hover',
                    style: {
                        itemBackground: 'rgba(0, 0, 0, .03)',
                        itemOpacity: 1
                    }
                }
            ]
        }
    ]}
/>

       
            
            </>
        )


    }


    return (<>

        {graphRender(data)}

    </>)
}

export default GraphContainer