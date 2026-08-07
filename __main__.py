from core.engine.parse_engine import ParseEngine, DefaultParseEngine

if __name__ == "__main__":
    hdl = """
    // This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/1/And.hdl
**
 * And gate:
 * if (a and b) out = 1, else out = 0 
 */
CHIP And {
    IN a, b;
    OUT out;
    
    PARTS:
    Nand(a=a, b=b, out=aNandb);
    Not(in=aNandb, out=out);
}
    """

    engine = DefaultParseEngine()
    engine.parse(hdl)

    print(engine.chip_name)
    print(engine.input_pins)
    print(engine.output_pins)
    print(engine.chip_parts)
