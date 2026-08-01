from core.engine.parse_engine import ParseEngine

if __name__ == "__main__":
    hdl = """
    CHIP Mux4Way16 {
        IN
         a;
        OUT
         b;
        
        PARTS:
        Mux16(a     =a, b=b, sel=sel[0], out=aMuxb);
    }
    """

    engine = ParseEngine(hdl)
    engine.parse()

    print(engine.chip_name)
    print(engine.input_pins)
    print(engine.output_pins)
    print(engine.chip_connections)

