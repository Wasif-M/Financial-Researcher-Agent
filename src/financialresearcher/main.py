#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financialresearcher.crew import Financialresearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """Run the Crew"""
    inputs={
        "company":"VisionX"
    }
    results=Financialresearcher().crew().kickoff(inputs=inputs)
    print(results.raw)


if __name__ =="__main__":
    run()