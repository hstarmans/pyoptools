# standard imports

# third-party imports

# local imports
from pyoptools.raytrace import shape
from pyoptools.raytrace import surface
from pyoptools.raytrace import component
from pyoptools.raytrace.mat_lib import material


def test_component_surflist():
    S0 = surface.Spherical(shape=shape.Circular(radius=50), curvature=1.0 / 200.0)
    S1 = surface.Spherical(shape=shape.Circular(radius=50), curvature=1.0 / 200.0)
    S2 = surface.Cylinder(radius=50, length=10)
    L1 = component.Component(
        surflist=[
            (S0, (0, 0, -5), (0, 0, 0)),
            (S1, (0, 0, 5), (0, 0, 0)),
            (S2, (0, 0, 6.5), (0, 0, 0)),
        ],
        material=material.schott["BK7"],
    )
    print(type(L1.surflist))
    for surf in L1.surflist:
        assert len(surf) == 3, "Wrong surface length"


def test_cylindrical_lens():
    import pytest
    from pyoptools.raytrace.comp_lib import CylindricalLens
    from pyoptools.raytrace.ray import Ray

    # Plano-convex cylindrical lens
    lens = CylindricalLens(size=(20, 20), thickness=10, curvature_s1=1.0/50.0, curvature_s2=0.0, material=1.5)
    surfs = lens.surflist
    assert len(surfs) == 6, f"Expected 6 surfaces (S1..S6), got {len(surfs)}"
    for key in ["S1", "S2", "S3", "S4", "S5", "S6"]:
        assert key in surfs, f"Missing surface {key}"

    # Ray hitting through front surface S1
    r_front = Ray(origin=(0, 0, -20), direction=(0, 0, 1))
    res_front = lens.propagate(r_front, 1.0)
    assert len(res_front) > 0

    # Ray hitting lateral surface S5
    r_side = Ray(origin=(-20, 0, 0.5), direction=(1, 0, 0))
    res_side = lens.propagate(r_side, 1.0)
    assert len(res_side) > 0

    # Check non-physical curvature error
    with pytest.raises(ValueError):
        CylindricalLens(size=(50, 20), thickness=10, curvature_s1=1.0/20.0)
