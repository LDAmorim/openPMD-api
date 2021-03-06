#!/usr/bin/env python
"""
This file is part of the openPMD-api.

Copyright 2019 openPMD contributors
Authors: Axel Huebl
License: LGPLv3+
"""
from openpmd_api import Series, Access_Type, Dataset, Mesh_Record_Component, \
    Unit_Dimension
import numpy as np


SCALAR = Mesh_Record_Component.SCALAR


if __name__ == "__main__":
    # open file for writing
    f = Series(
        "../samples/7_particle_write_serial_py.h5",
        Access_Type.create
    )

    # all required openPMD attributes will be set to reasonable default values
    # (all ones, all zeros, empty strings,...)
    # manually setting them enforces the openPMD standard
    f.set_meshes_path("fields")
    f.set_particles_path("particles")

    # new iteration
    cur_it = f.iterations[0]

    # particles
    electrons = cur_it.particles["electrons"]
    electrons.set_attribute(
        "Electrons... the necessary evil for ion acceleration! ",
        "Just kidding.")

    # let's set a weird user-defined record this time
    electrons["displacement"].set_unit_dimension({Unit_Dimension.M: 1})
    electrons["displacement"][SCALAR].set_unit_SI(1.e-6)
    dset = Dataset(np.dtype("float64"), extent=[2])
    electrons["displacement"][SCALAR].reset_dataset(dset)
    electrons["displacement"][SCALAR].make_constant(42.43)
    # don't like it anymore? remove it with:
    # del electrons["displacement"]

    electrons["weighting"][SCALAR].set_unit_SI(1.e-5)

    particlePos_x = np.random.rand(234).astype(np.float32)
    particlePos_y = np.random.rand(234).astype(np.float32)
    d = Dataset(particlePos_x.dtype, extent=particlePos_x.shape)
    electrons["position"]["x"].reset_dataset(d)
    electrons["position"]["y"].reset_dataset(d)

    particleOff_x = np.arange(234, dtype=np.uint)
    particleOff_y = np.arange(234, dtype=np.uint)
    d = Dataset(particleOff_x.dtype, particleOff_x.shape)
    electrons["positionOffset"]["x"].reset_dataset(d)
    electrons["positionOffset"]["y"].reset_dataset(d)

    electrons["position"]["x"].store_chunk(particlePos_x)
    electrons["position"]["y"].store_chunk(particlePos_y)
    electrons["positionOffset"]["x"].store_chunk(particleOff_x)
    electrons["positionOffset"]["y"].store_chunk(particleOff_y)

    # at any point in time you may decide to dump already created output to
    # disk note that this will make some operations impossible (e.g. renaming
    # files)
    f.flush()

    # now the file is closed
    del f
