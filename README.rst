simtools ![travis-ci](https://travis-ci.org/ZachGlassman/simtools.svg?branch=master)
--------

simtools provides a tool for simulation pipelines in Python.  Its built to be fairly general and can also perform data analysis.

The package is based on the concept of a Simulation which pipelines different calculations.  These calculations may rely on the previous calculation or be independent.  Some automatic parallelization is performed when possible.

simtools provides easy tooling for computing simulations over a variety of input parameters, organizing out in hdf5 files for further analysis and storage, and a framework for reusable calculation components.

Although originally meant for simulation it can also be used for data analysis.