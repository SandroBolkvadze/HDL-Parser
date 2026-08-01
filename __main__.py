from core.parse_engine import ParseEngine

if __name__ == "__main__":
    hdl = """
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/1/Mux4Way16.hdl
/**
 * 4-way 16-bit multiplexor:
 * out = a if sel = 00
 *       b if sel = 01
 *       c if sel = 10
 *       d if sel = 11
 */
CHIP Mux4Way16 {
    IN a[16], b[16], c[16], d[16], sel[2];
    OUT out[16];
    
    PARTS:
    Mux16(a=a, b=b, sel=sel[0], out=aMuxb);
    Mux16(a=c, b=d, sel=sel[0], out=cMuxd);
    
    Mux16(a=aMuxb, b=cMuxd, sel=sel[1], out=out);
}
    """

    engine = ParseEngine(hdl)
    engine.parse()
    print(engine.chip_name)

    print(engine.input_pins)
    print(engine.output_pins)
    print(engine.chip_parts)

