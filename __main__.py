from core.engine import Engine

if __name__ == "__main__":
    hdl = """
        /* dasd asd asd asdasd asd 
            dsadasdasd
        */
        // dasd sad asd asd asd asdsa
        
        // dasda sdasd asd as dsadadsad
        CHIP abcd {
            IN a[15], b[2], c;
            OUT c[-1, a[10;
        }
    """

    engine = Engine(hdl)
    engine.parse()
    print(engine.chip_name)

    print(engine.input_pins)
    print(engine.output_pins)

