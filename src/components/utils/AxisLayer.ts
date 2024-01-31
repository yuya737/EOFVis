import { PathLayer } from "deck.gl/typed";
import type { LayersList } from "deck.gl/typed";

export class AxisLayer{
    readonly xmin: number;
    readonly xmax: number;
    readonly ymin: number;
    readonly ymax: number;
    readonly gridWidth: number;

    constructor(xmin: number, xmax: number, ymin: number, ymax: number, gridWidth: number){
        this.xmin = xmin;
        this.xmax = xmax;
        this.ymin = ymin;
        this.ymax = ymax;
        this.gridWidth = gridWidth;
    }

    getLayers() : LayersList {
        // X-Y axis layer
        let axisLayer = new PathLayer({
            id: 'axis-layer',
            data: [[[this.xmin, 0], [this.xmax, 0]], [[0, this.ymin], [0, this.ymax]]],
            getPath: d => d,
            getColor: [155, 155, 155],
            getWidth: 4,
            pickable: false,
            widthUnits: 'pixels'
        })
        let ret: LayersList = [axisLayer]

        const generateNumbers = (max, min, interval) =>
            Array.from({ length: Math.floor((max - min) / interval) + 1 }, (_, index) => max - index * interval);
        
        generateNumbers(this.xmax, this.xmin, this.gridWidth).forEach((x, index) => {
            ret.push(new PathLayer({
                id: `grid-x-layer-${index}`,
                data: [[[x, this.ymin], [x, this.ymax]]],
                getPath: d => d,
                getColor: [100, 100, 100],
                getWidth: 1,
                pickable: false,
                widthUnits: 'pixels'
            }))
        })

        generateNumbers(this.ymax, this.ymin, this.gridWidth).forEach((y, index) => {
            ret.push(new PathLayer({
                id: `grid-y-layer-${index}`,
                data: [[[this.xmin, y], [this.xmax, y]]],
                getPath: d => d,
                getColor: [100, 100, 100],
                getWidth: 1,
                pickable: false,
                widthUnits: 'pixels'
            }))
        })
        return ret
    }
}