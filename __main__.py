from pathlib import Path

from test.tester import TestParser

if __name__ == "__main__":
    # cli()
    TestParser().parse("""
        a,b; out
        0,0; 0
        0,1; 1
        1,0; 1
        1,1; 0
    """)